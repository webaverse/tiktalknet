import sys
import torch
import torchaudio
import speechbrain as sb
from speechbrain.utils.distributed import run_on_main
from hyperpyyaml import load_hyperpyyaml
from src.speaker_clustering_and_id.voxceleb_prepare import prepare_voxceleb
from tqdm.contrib import tqdm

class SpeakerClusteringAndIdModel():
    def __init__(self, speaker, paramsFilePath):
        self.speaker = speaker
        self.paramsFile, self.runOpts, self.overrides = sb.core.parse_arguments([paramsFilePath])
        self.params = self.parseParamsFile()
        self.enrolDataLoader, self.paramstestDataLoader = self.dataioPrep(self.params)
        self.enrolDict = self.computeEmbeddingLoop(self.enrolDataLoader)
        self.testDict = self.computeEmbeddingLoop(self.testDataLoader)


    def parseParamsFile(self):
        with open(self.paramsFile) as fin:
            params = load_hyperpyyaml(fin, self.overrides)
        return params

    def dataioPrep(self, params):
        dataFolder = params["data_folder"]
        enrolData = sb.dataio.dataset.DynamicItemDataset.from_csv(
            csv_path=params["enrol_data"], replacements={"data_root": dataFolder},
        )
        enrolData = enrolData.filtered_sorted(sort_key="duration")
        testData = sb.dataio.dataset.DynamicItemDataset.from_csv(
            csv_path=params["test_data"], replacements={"data_root": dataFolder},
        )
        testData = testData.filtered_sorted(sort_key="duration")
        datasets = [enrolData, testData]
        @sb.utils.data_pipeline.takes("wav", "start", "stop")
        @sb.utils.data_pipeline.provides("sig")
        def audio_pipeline(wav, start, stop):
            start = int(start)
            stop = int(stop)
            num_frames = stop - start
            sig, fs = torchaudio.load(
                wav, num_frames=num_frames, frame_offset=start
            )
            sig = sig.transpose(0, 1).squeeze(1)
            return sig
        sb.dataio.dataset.add_dynamic_item(datasets, audio_pipeline)
        sb.dataio.dataset.set_output_keys(datasets, ["id", "sig"])
        enrolDataLoader = sb.dataio.dataloader.make_dataloader(
            enrolData, **params["enrol_dataloader_opts"]
        )
        testDataLoader = sb.dataio.dataloader.make_dataloader(
            testData, **params["test_dataloader_opts"]
        )
        return enrolDataLoader, testDataLoader

    def compute_embedding(self, wavs, wav_lens):
        with torch.no_grad():
            feats = self.params["compute_features"](wavs)
            feats = self.params["mean_var_norm"](feats, wav_lens)
            embeddings = self.params["embedding_model"](feats, wav_lens)
            embeddings = self.params["mean_var_norm_emb"](
                embeddings, torch.ones(embeddings.shape[0]).to(embeddings.device)
            )
        return embeddings.squeeze(1)


    def computeEmbeddingLoop(self, dataLoader):
        embedding_dict = {}
        with torch.no_grad():
            for batch in tqdm(dataLoader, dynamic_ncols=True):
                batch = batch.to(self.params["device"])
                seg_ids = batch.id
                wavs, lens = batch.sig
                found = False
                for seg_id in seg_ids:
                    if seg_id not in embedding_dict:
                        found = True
                if not found:
                    continue
                wavs, lens = wavs.to(self.params["device"]), lens.to(self.params["device"])
                emb = self.computeEmbedding(wavs, lens).unsqueeze(1)
                for i, seg_id in enumerate(seg_ids):
                    embedding_dict[seg_id] = emb[i].detach().clone()
        return embedding_dict

    def getEmbeddingForSpeaker(self):
        embeddings = {} 
        embeddingsForSpk = {}
        for key in self.enrolDict.keys():
            spk_id = key.split('/')[0]
            if spk_id in embeddings:
                embeddings[spk_id].append(self.enrolDict[key])
            else:
                embeddings[spk_id] = []
                embeddings[spk_id].append(self.enrolDict[key])
        for key in embeddings.keys():
            embeddingsForSpk[key] = sum(embeddings[key]) / len(embeddings[key])
        return embeddingsForSpk    

    def run(self):
        sb.core.create_experiment_directory(
            experiment_directory=self.params["output_folder"],
            hyperparams_to_save=self.paramsFile,
            overrides=self.overrides,
        )

        veriFilePath = 'src/speaker_clustering_and_id/veri_test.txt'

        prepare_voxceleb(
            data_folder=self.params["data_folder"],
            save_folder=self.params["save_folder"],
            verification_pairs_file=veriFilePath,
            splits=["test"],
            split_ratio=[90, 10],
            seg_dur=300,
            source=self.params["voxceleb_source"]
            if "voxceleb_source" in self.params
            else None,
        )

        run_on_main(self.params["pretrainer"].collect_files)
        self.params["pretrainer"].load_collected(self.params["device"])
        self.params["embedding_model"].eval()
        self.params["embedding_model"].to(self.params["device"])

        enrolDictSpk = self.getEmbeddingForSpeaker()
        print(enrolDictSpk)
