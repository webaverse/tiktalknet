from nemo.collections.tts.models import TalkNetSpectModel
from nemo.collections.tts.models import TalkNetPitchModel
from nemo.collections.tts.models import TalkNetDursModel
from core.talknet_singer import TalkNetSingerModel
from core import extract, vocoder, reconstruct
from core.download import download_from_drive
from scipy.io import wavfile
import tensorflow as tf
import numpy as np
import traceback
import ffmpeg
import torch
import json
import time
import uuid
import io
import os


DEVICE = "cuda:0"
RUN_PATH = os.path.dirname(os.path.realpath(__file__))
extract_dur = extract.ExtractDuration(RUN_PATH, DEVICE)

playback_hide = {
    "display": "none",
}
tnmodels, tnmodel, tnpath, tndurs, tnpitch = {}, None, None, None, None
voc, last_voc, sr_voc, rec_voc = None, None, None, None


def get_silent_wav():
    f = open("assets/silent.wav", "rb")
    buffer = io.BytesIO(f.read())
    return buffer

def generate_audio(
    model,
    custom_model,
    transcript,
    pitch_options,
    pitch_factor,
    wav_name,
    f0s,
    f0s_wo_silence,
):
    global tnmodels, tnpath, tndurs, tnpitch, voc, last_voc, sr_voc, rec_voc

    if model is None:
        return [None, "No character selected", playback_hide, None]
    if transcript is None or transcript.strip() == "":
        return [
            None,
            "No transcript entered",
            playback_hide,
            None,
        ]
    load_error, talknet_path, vocoder_path = download_from_drive(
        model.split("|")[0], custom_model, RUN_PATH
    )
    if load_error is not None:
        return [
            None,
            load_error,
            playback_hide,
            None,
        ]

    try:
        with torch.no_grad():
            tnmodel = tnmodels.get(talknet_path)
            if tnmodel is None:
                # if tnpath != talknet_path:
                    singer_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetSinger.nemo"
                    )
                    if os.path.exists(singer_path):
                        tnmodel = TalkNetSingerModel.restore_from(singer_path)
                    else:
                        tnmodel = TalkNetSpectModel.restore_from(talknet_path)
                    durs_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetDurs.nemo"
                    )
                    pitch_path = os.path.join(
                        os.path.dirname(talknet_path), "TalkNetPitch.nemo"
                    )
                    if os.path.exists(durs_path):
                        tndurs = TalkNetDursModel.restore_from(durs_path)
                        tnmodel.add_module("_durs_model", tndurs)
                        tnpitch = TalkNetPitchModel.restore_from(pitch_path)
                        tnmodel.add_module("_pitch_model", tnpitch)
                    else:
                        tndurs = None
                        tnpitch = None
                    tnmodel.eval()
                    tnpath = talknet_path
                    tnmodels[talknet_path] = tnmodel

            # Generate spectrogram
            try:
                token_list, tokens, arpa = extract_dur.get_tokens(transcript)
                if tndurs is None or tnpitch is None:
                    return [
                        None,
                        "Model doesn't support pitch prediction",
                        playback_hide,
                        None,
                    ]
                spect = tnmodel.generate_spectrogram(tokens=tokens)
                # Vocoding
                if last_voc != vocoder_path:
                    voc = vocoder.HiFiGAN(vocoder_path, "config_v1", DEVICE)
                    last_voc = vocoder_path
                audio, audio_torch = voc.vocode(spect)

                # Reconstruction
                if "srec" in pitch_options:
                    new_spect = reconstruct_inst.reconstruct(spect)
                    if rec_voc is None:
                        rec_voc = vocoder.HiFiGAN(
                            os.path.join(RUN_PATH, "models", "hifirec"), "config_v1", DEVICE
                        )
                    audio, audio_torch = rec_voc.vocode(new_spect)

                # Super-resolution
                if sr_voc is None:
                    sr_voc = vocoder.HiFiGAN(
                        os.path.join(RUN_PATH, "models", "hifisr"), "config_32k", DEVICE
                    )
                sr_mix, new_rate = sr_voc.superres(audio, 22050)

                # Create buffer
                buffer = io.BytesIO()
                wavfile.write(buffer, new_rate, sr_mix.astype(np.int16))
                return buffer
            except IndexError:
                return getSilentWav()
    except Exception:
        return str(traceback.format_exc())


# if __name__ == "__main__":
#     s = "test"
#     voice = "1kpEjZ3YqMN3chKSXODOqayEm581rxj4r"
#     r = generate_audio(voice + "|default", None, s, [], 0, None, None, None)
