import os
import subprocess


class SpeakerDiarizationModel():
    def __init__(self, speaker):
        self.speaker = speaker
        self.energyVadDir = speaker.outputPath + "/energy_VAD"
        self.vadDir = self.energyVadDir + "/labs"
        self.xvecDir = self.energyVadDir + "/xvectors"
        self.fileList = self.generateFileList()
        self.setupOutputFolders()

    def generateFileList(self):
        return self.speaker.outputPath + "/file_list.txt"

    def setupOutputFolders(self):
        for outputFolder in [self.energyVadDir, self.vadDir, self.xvecDir]:
            if not os.path.isdir(outputFolder):
                os.mkdir(outputFolder) 

    def generateTaskFile(self):
        None

    def xvectors(self):
        command = \
            "src/speaker_diarization/VBx/extract.sh " + \
            "ResNet152 " + \
            "src/speaker_diarization/VBx/models/ResNet152_16kHz/nnet/raw_58.pth " + \
            self.speaker.inputPath + \
            self.vadDir + \
            self.fileList + \
            self.xvecDir + \
            "gpu"
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()
        output, errors = p.communicate()
        print(p.returncode, errors, output)

    def run(self):
        self.xvectors()