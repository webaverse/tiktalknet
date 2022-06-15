import os
import glob
import wave
import contextlib
from src.audio_scraping.main import AudioScraper
from src.synthetic_detection.main import SyntheticDetectionModel
from src.source_separation.main import SourceSeparationModel
from src.speech_segmentation.main import SpeechSegmentationModel
from src.speaker_diarization.main import SpeakerDiarizationModel
from src.speaker_clustering_and_id.main import SpeakerClusteringAndIdModel
from src.speech_recognition_and_transcription.main import SpeechRecognitionAndTranscriptionModel
from src.domain_and_topic_detection.main import DomainAndTopicDetectionModel


INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"


def linuxifyPath(path):
    return path.replace("\\", "/")


class AudioFile():
    def __init__(self, filePath):
        self.name = filePath[filePath.rindex("/") + 1:filePath.rindex(".") - 1]
        self.fileType = filePath[filePath.rindex(".") + 1:]
        self.filePath = filePath
        self.numFrames, self.frameRate, self.duration = self.getFileInfo()

    def getFileInfo(self):
        with contextlib.closing(wave.open(self.filePath, 'r')) as f:
            numFrames = f.getnframes()
            frameRate = f.getframerate()
            duration = numFrames / float(frameRate)
        return [numFrames, frameRate, duration]

    def pretty(self):
        print(
            "\t\t\t>Type:       \t" + self.fileType + "\n" +
            "\t\t\t>File Path:   \t" + self.filePath + "\n" +
            "\t\t\t># Frames:   \t" + str(self.numFrames) + "\n" +
            "\t\t\t>Frame Rate: \t" + str(self.frameRate) + "\n" +
            "\t\t\t>Duration:   \t" + str(self.duration) + "\n"
        )
        

class Speaker():
    def __init__(self, inputPath):
        self.name = inputPath[inputPath.rindex("/") + 1:]
        self.inputPath = inputPath
        self.outputPath = OUTPUT_FOLDER + "/" + self.name
        AudioScraper(self)
        self.audioFiles = self.getInputAudioFiles()
        self.cleanUpAudioFiles()
        self.setupOutputFile()

    def setupOutputFile(self):
        if not os.path.isdir(self.outputPath):
            os.mkdir(self.outputPath) 

    def getInputAudioFiles(self):
        audioFiles = []
        for audioFilePath in glob.glob(self.inputPath + "/*.wav"):
            audioFiles.append(AudioFile(linuxifyPath(audioFilePath)))
        return audioFiles

    def cleanUpAudioFiles(self):
        audioFileIndex = 0
        for audioFilePath in glob.glob(self.inputPath + "/*.wav"):
            newFileName = self.inputPath + "/" + self.name + "-" + str(audioFileIndex) + ".wav"
            os.rename(audioFilePath, newFileName)
            audioFileIndex += 1

    def pretty(self):
        print(
            "\t\t>Name:                \t" + self.name + "\n" +
            "\t\t>Input Path:          \t" + self.inputPath + "\n" +
            "\t\t># Input Audio Files: \t" + str(len(self.audioFiles)) + "\n"
        )


class Pipeline():
    def __init__(self, inputFolder):
        self.speakers = self.getSpeakers(inputFolder + "/*")
        self.pretty()

    def getSpeakers(self, inputFolder):
        speakers = []
        for speakerPath in glob.glob(inputFolder):
            speakers.append(Speaker(linuxifyPath(speakerPath)))
        return speakers

    def runSyntheticDetection(self):
        for speaker in self.speakers:
            model = SyntheticDetectionModel(speaker)
            model.run()

    def runSourceSeparation(self):
        model = SourceSeparationModel()
        for speaker in self.speakers:
            for audioFile in speaker.audioFiles:
                model.run(audioFile, OUTPUT_FOLDER + "/" + speaker.name)

    def runSpeechSegmentation(self):
        model = SpeechSegmentationModel()
        for speaker in self.speakers:
            for audioFile in speaker.audioFiles:
                model.run(audioFile, OUTPUT_FOLDER + "/" + speaker.name)

    def runSpeakerDiarization(self):
        for speaker in self.speakers:
            model = SpeakerDiarizationModel(speaker)
            model.run()

    def runSpeakerClusteringAndId(self):
        for speaker in self.speakers:
            model = SpeakerClusteringAndIdModel(speaker, "src/speaker_clustering_and_id/hparams/verification_ecapa_test1.yaml")
            model.run()

    def runSpeechRecognitionAndTranscription(self):
        for speaker in self.speakers:
            model = SpeechRecognitionAndTranscriptionModel(speaker)
            model.run()

    def runDomainAndTopicDetection(self):
        for speaker in self.speakers:
            model = DomainAndTopicDetectionModel(speaker)
            model.run()
        
    def pretty(self):
        speakerIndex = 0 
        audioFileIndex = 0
        for speaker in self.speakers:
            print("\t>Speaker (" + str(speakerIndex) + ")")
            speaker.pretty()
            speakerIndex += 1

            for audioFile in speaker.audioFiles:
                print("\t\t>Audio File (" + str(audioFileIndex) + ")")
                audioFile.pretty()
                audioFileIndex += 1
            audioFileIndex = 0


if __name__ == '__main__':

    print("Initializing pipeline...")
    pipeline = Pipeline(INPUT_FOLDER)

    #print("Running synthetic speech detection model...")
    #syntheticDetectionOutput = pipeline.runSyntheticDetection()

    #print("Running source separation model...")
    #sourceSeparationOutput = pipeline.runSourceSeparation()

    print("Running speech segmentation model...")
    speechDetectionOutput = pipeline.runSpeechSegmentation()

    print("Running speaker diarization model...")
    speakerDiarizationOutput = pipeline.runSpeakerDiarization()

    print("Running speaker clustering + identification model...")
    speakerClusteringAndIdOutput = pipeline.runSpeakerClusteringAndId()

    print("Running speech recognition + transcription model...")
    speechRecognitionAndTranscriptionOutput = pipeline.runSpeechRecognitionAndTranscription()

    print("Running domain / topic detection model...")
    domainAndTopicDetectionResult = pipeline.runDomainAndTopicDetection()

    print("Pipeline complete.")