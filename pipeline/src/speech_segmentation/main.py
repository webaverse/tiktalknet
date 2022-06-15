import subprocess


class SpeechSegmentationModel():
    def __init__(self):
        None

    def run(self, audioFile, outputPath):
        command = "ina_speech_segmenter.py -d smn -g false -i " + audioFile.filePath + " -o " + outputPath
        p = subprocess.Popen(command, shell=True)
        p.wait()
        output, errors = p.communicate()
        print(p.returncode, errors, output)

    def spliceAudioFile(self):
        None