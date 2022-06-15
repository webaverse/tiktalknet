import time
import datetime
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import hamming_loss, accuracy_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from transformers import (
    AutoTokenizer, AutoModel,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding, AdamW, get_scheduler,
    get_linear_schedule_with_warmup
)
import pyarrow as pa
from tqdm.auto import tqdm
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import datasets
import random
from sklearn.metrics import classification_report


class DomainAndTopicDetectionModel():
    def __init__(self, speaker):
        self.speaker = speaker

    def format_time(self, elapsed):
        elapsedRounded = int(round((elapsed)))
        return str(datetime.timedelta(seconds=elapsedRounded))

    def run(self):
        modelFile = sys.argv[1]
        testFile = sys.argv[2]
        testLabelFile = sys.argv[3]

        checkpoint = "bert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels = 6)
        stateDict = torch.load(modelFile, map_location='cpu')
        model.load_state_dict(stateDict)
        model.eval()
        
        device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        model.to(device)

        testCsv = pd.read_csv(testFile)
        testCsvLabels = pd.read_csv(testLabelFile)

        subTokens = tokenizer.batch_encode_plus(
            testCsv["comment_text"].tolist(),
            max_length = 200,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )

        subSeq = torch.tensor(subTokens['input_ids'])
        subMask = torch.tensor(subTokens['attention_mask'])

        subData = TensorDataset(subSeq, subMask)
        batchSize = 256
        subDataloader = DataLoader(subData, batch_size=batchSize)

        t0 = time.time()

        for step, batch in enumerate(subDataloader):
            if step % 40 == 0 and not step == 0:
                elapsed = self.formatTime(time.time() - t0)
                print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(subDataloader), elapsed))
            bInputIds = batch[0].to(device)
            bInputMask = batch[1].to(device)
            with torch.no_grad():
                outputs = model(bInputIds, bInputMask)
                pred_probs = torch.sigmoid(outputs.logits)
                if step == 0: predictions = pred_probs.cpu().detach().numpy()
                else: predictions = np.append(predictions, pred_probs.cpu().detach().numpy(), axis=0)
        
        categories = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        predictions_df = pd.DataFrame(predictions, columns=categories)
        print("  predictions_df.shape = ", predictions_df.shape)
        print("  len(predictions_df) = ", len(predictions_df))

        submission = pd.concat([testCsv["id"], predictions_df], axis=1)
        print("  submission.shape = ", submission.shape)
        print("  submission = \n", submission)

        submission.to_csv('text_classification_result.csv', index=False, header=True)