from torch.utils.data import Dataset
from transformers import BertTokenizer
import torch
from sklearn.utils import shuffle
from torch.nn.utils.rnn import pad_sequence

class TaskOneDataset(Dataset):
    def __init__(self, data_dic):
        self.max_seq_len = 500
        self.corpus_length = len(data_dic)
        self.line = shuffle(data_dic)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def __len__(self):
        return self.corpus_length

    def __getitem__(self, item):


        text_one, text_two, label = self.line[item]['text'], self.line[item]['textb'], self.line[item][
            'label']

        word_pieces = ["[CLS]"]
        tokens_a = self.tokenizer.tokenize(text_one)
        word_pieces += tokens_a + ["[SEP]"]
        len_a = len(word_pieces)

        # second senctence BERT tokens
        tokens_b = self.tokenizer.tokenize(text_two)[:self.max_seq_len - len_a]
        word_pieces += tokens_b + ["[SEP]"]
        len_b = len(word_pieces) - len_a

        ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
        segments_tensor = torch.tensor([0] * len_a + [1] * len_b, dtype=torch.long)

        return (torch.tensor(ids), segments_tensor, torch.tensor([label]))

    def create_mini_batch(self, samples):
        tokens_tensors = [s[0] for s in samples]
        segments_tensors = [s[1] for s in samples]

        if samples[0][2] is not None:
            label_ids = torch.stack([s[2] for s in samples])
        else:
            label_ids = None

        # zero pad same length
        tokens_tensors = pad_sequence(tokens_tensors,
                                      batch_first=True)
        segments_tensors = pad_sequence(segments_tensors,
                                        batch_first=True)

        masks_tensors = torch.zeros(tokens_tensors.shape,
                                    dtype=torch.long)
        masks_tensors = masks_tensors.masked_fill(tokens_tensors != 0, 1)
        #print(tokens_tensors, segments_tensors, masks_tensors, label_ids)
        return tokens_tensors, segments_tensors, masks_tensors, label_ids


class TaskTestDataset(Dataset):
    def __init__(self, data_dic):
        self.max_seq_len = 500
        self.corpus_length = len(data_dic)
        self.line = shuffle(data_dic)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def __len__(self):
        return self.corpus_length

    def __getitem__(self, item):

        text_one, text_two = self.line[item]['text'], self.line[item]['textb']

        word_pieces = ["[CLS]"]
        tokens_a = self.tokenizer.tokenize(text_one)
        word_pieces += tokens_a + ["[SEP]"]
        len_a = len(word_pieces)

        tokens_b = self.tokenizer.tokenize(text_two)[:self.max_seq_len - len_a]
        word_pieces += tokens_b + ["[SEP]"]
        len_b = len(word_pieces) - len_a

        ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
        segments_tensor = torch.tensor([0] * len_a + [1] * len_b, dtype=torch.long)

        return (torch.tensor(ids),segments_tensor)

    def create_mini_batch(self,samples):
        tokens_tensors = [s[0] for s in samples]
        segments_tensors = [s[1] for s in samples]

        label_ids = None


        tokens_tensors = pad_sequence(tokens_tensors,
                                      batch_first=True)
        segments_tensors = pad_sequence(segments_tensors,
                                        batch_first=True)


        masks_tensors = torch.zeros(tokens_tensors.shape,
                                    dtype=torch.long)
        masks_tensors = masks_tensors.masked_fill(tokens_tensors != 0, 1)

        #print(tokens_tensors)
        #print(segments_tensors)
        #print(masks_tensors)
        #print(kabek_ids)
        return tokens_tensors, segments_tensors, masks_tensors, label_ids