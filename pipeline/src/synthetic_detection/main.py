import torch
from torch.utils.data.dataloader import DataLoader
import torch.nn.functional as F
from src.synthetic_detection import models
from src.synthetic_detection.data import PrepASV19Dataset

class SyntheticDetectionModel():
    def __init__(self, speaker):
        self.speaker = speaker
        self.protocol = self.generateProtocolFile()

    def generateProtocolFile(self):
        return self.speaker.inputPath + "/protocol.csv"

    def run(self):
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        net = models.SSDNet1D()
        num_total_learnable_params = sum(i.numel() for i in net.parameters() if i.requires_grad)
        print('Number of learnable params: {}.'.format(num_total_learnable_params))

        checkpoint = torch.load('src/synthetic_detection/pretrained/Res_TSSDNet_time_frame_61_ASVspoof2019_LA_Loss_0.0017_dEER_0.74%_eEER_1.64%.pth', map_location=torch.device('cpu'))
        net.load_state_dict(checkpoint['model_state_dict'])
        net = net.to(device)
        net.eval()
        with torch.no_grad():
            softmaxAccuracy = 0
            numFiles = 0
            probs = torch.empty(0, 3).to(device)

            testSet = PrepASV19Dataset(self.protocol, self.speaker.inputPath, data_type="time_frame")
            testLoader = DataLoader(testSet, batch_size=64, shuffle=False, num_workers=4)
            for testBatch in testLoader:
                testSample, testLabel, subClass = testBatch

                numFiles += len(testLabel)
                testSample = testSample.to(device)
                testLabel = testLabel.to(device)
                infer = net(testSample)

                t1 = F.softmax(infer, dim=1)
                t2 = testLabel.unsqueeze(-1)
                row = torch.cat((t1, t2), dim=1)
                probs = torch.cat((probs, row), dim=0)

                infer = infer.argmax(dim=1)
                batch_acc = infer.eq(testLabel).sum().item()
                softmax_acc += batch_acc

        softmaxAccuracy = softmaxAccuracy / numFiles
        print("SMA", softmax_acc)
