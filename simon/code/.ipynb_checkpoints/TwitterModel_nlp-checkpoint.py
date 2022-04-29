import json
import os
import torch
from transformers import BertForSequenceClassification
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score

class TwitterModel():
    def __init__(self,model_name,num_labels):
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def get_predictions(self,dataloader, compute_acc=False):
        predictions = None
        correct = 0
        total = 0
        all_predictions, all_labels = [], []

        self.load_model(self.model)
        model = self.model.to(self.device)

        with torch.no_grad():
            # view all dataloader
            for data in dataloader:
                # move tensors to GPU
                if next(self.model.parameters()).is_cuda:
                    data = [t.to("cuda:0") for t in data if t is not None]


                tokens_tensors, segments_tensors, masks_tensors = data[:3]
                outputs = model(input_ids=tokens_tensors,
                                token_type_ids=segments_tensors,
                                attention_mask=masks_tensors)

                logits = outputs[0]
                _, pred = torch.max(logits.data, 1)
                #  calculate the classification accuracy of the dev set
                if compute_acc:
                    predictions = pred.detach().cpu().numpy().reshape(-1).tolist()
                    labels = data[3].cpu().numpy().reshape(-1).tolist()
                    all_predictions.extend(predictions)
                    all_labels.extend(labels)
                else:
                    predictions = pred.detach().cpu().numpy().reshape(-1).tolist()
                    all_predictions.extend(predictions)

        if compute_acc:
            auc = accuracy_score(all_labels, all_predictions)
            return all_predictions, auc
        return all_predictions

    def load_model(self,model, dir_path="./output", load_bert=False):
        checkpoint_dir = self.find_most_recent_state_dict(dir_path)
        checkpoint = torch.load(checkpoint_dir)
        if load_bert:
            checkpoint["model_state_dict"] = {k[5:]: v for k, v in checkpoint["model_state_dict"].items()
                                              if k[:4] == "bert" and "pooler" not in k}
        model.load_state_dict(checkpoint["model_state_dict"], strict=False)
        torch.cuda.empty_cache()
        print("{} loaded!".format(checkpoint_dir))

    def find_most_recent_state_dict(self,dir_path):
        """
        :param dir_path: the model files are stored
        :return: Returns the most recent model file path, sorted by the last digit of the model name
        """
        dic_lis = [i for i in os.listdir(dir_path)]
        if len(dic_lis) == 0:
            raise FileNotFoundError("can not find any state dict in {}!".format(dir_path))
        dic_lis = [i for i in dic_lis if "model" in i]
        dic_lis = sorted(dic_lis, key=lambda k: int(k.split(".")[-1]))
        return dir_path + "/" + dic_lis[-1]

    def save_state_dict(self, model, epoch, state_dict_dir="./output", file_path="a3.model"):
        """save parameter"""
        if not os.path.exists(state_dict_dir):
            os.mkdir(state_dict_dir)
        save_path = state_dict_dir + "/" + file_path + ".epoch.{}".format(str(epoch))
        model.to("cpu")
        torch.save({"model_state_dict": model.state_dict()}, save_path)
        model.to(self.device)
        print("{} saved!".format(save_path))

    def train(self,trainloader,devloader):

        self.load_model(self.model)
        model = self.model.to(self.device)
        model.train()
        # use Adam Optim
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

        EPOCHS = 2
        for epoch in range(EPOCHS):

            running_loss = 0.0

            for data in trainloader:
                tokens_tensors, segments_tensors, masks_tensors, labels = [t.to(self.device) for t in data]

                optimizer.zero_grad()

                outputs = model(input_ids=tokens_tensors,
                                token_type_ids=segments_tensors,
                                attention_mask=masks_tensors,
                                labels=labels)

                loss = outputs[0]
                # backward
                loss.backward()
                optimizer.step()

                # record batch loss
                running_loss += loss.item()

            # dev part
            _, acc = self.get_predictions(devloader, compute_acc=True)
            self.save_state_dict(model, epoch)
            print('[epoch %d] loss: %.3f, acc: %.3f' %
                  (epoch + 1, running_loss, acc))
            if acc >= 0.93:
                break

    def test(self,testloader,tweeter_id):

        predictions = self.get_predictions(testloader)
        for i, val in enumerate(predictions):
            if val == 1:
                predictions[i] = 'non-rumour'
            else:
                predictions[i] = 'rumour'

        result = {}
        for i, val in enumerate(tweeter_id):
            result[val] = predictions[i]

        item = json.dumps(result)
        with open('test-output.json', "w") as f:
            f.write(item)