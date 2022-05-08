from torch.utils.data import Dataset
from transformers import BertTokenizer
import torch
from sklearn.utils import shuffle
from torch.nn.utils.rnn import pad_sequence

class RumourDataset(Dataset):
    def __init__(self, data, maxlen):
        self.data = data

        if maxlen > 512:
            self.maxlen = 512
        else:
            self.maxlen = maxlen
            
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):

        text_source, text_reply = self.data[index]['text_source'], self.data[index]['text_reply']

        if len(self.data[index]) == 3:
            label = self.data[index]['label']
        else:
            label = None
          
        tokens = ["[CLS]"]
        tokens_source = self.tokenizer.tokenize(text_source)[:self.maxlen - 2]
        tokens += tokens_source + ["[SEP]"]
        len_source = len(tokens)
        
        len_reply = 0
        if len_source < self.maxlen:
            tokens_reply = self.tokenizer.tokenize(text_reply)[:self.maxlen - len_source - 1]
            tokens += tokens_reply + ["[SEP]"]
            len_reply = len(tokens) - len_source

        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids_tensor = torch.tensor(tokens_ids) # Converting the list to a pytorch tensor
        segments_tensor = torch.tensor([0] * len_source + [1] * len_reply, dtype=torch.long)[:self.maxlen]

        if len(self.data[index]) == 3:
            return tokens_ids_tensor, segments_tensor, torch.tensor([label])
        else:
            return tokens_ids_tensor, segments_tensor

    def create_mini_batch(self, samples):
        tokens_ids_tensors = [s[0] for s in samples]
        segments_tensors = [s[1] for s in samples]

        if len(samples[0]) == 3:
            label_ids = torch.stack([s[2] for s in samples])

        # zero pad same length
        tokens_ids_tensors = pad_sequence(tokens_ids_tensors, batch_first=True)
        segments_tensors = pad_sequence(segments_tensors, batch_first=True)

        masks_tensors = torch.zeros(tokens_ids_tensors.shape, dtype=torch.long)
        masks_tensors = masks_tensors.masked_fill(tokens_ids_tensors != 0, 1)

        if len(samples[0]) == 3:
            return tokens_ids_tensors, segments_tensors, masks_tensors, label_ids
        else:
            return tokens_ids_tensors, segments_tensors, masks_tensors