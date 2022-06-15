import subprocess


class SourceSeparationModel():
    def __init__(self):
        None

    def run(self, audioFile, outputPath):
        command = "spleeter separate -p spleeter:2stems -d " + str(0.5) + " -o " + outputPath + " " + audioFile.filePath
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()
        output, errors = p.communicate()
        print(p.returncode, errors, output)
