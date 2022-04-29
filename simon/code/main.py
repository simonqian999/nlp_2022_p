import argparse
from LoadData_nlp import *
from DataSet_nlp import *
from torch.utils.data import DataLoader
from TwitterModel_nlp import *
import warnings
warnings.filterwarnings("ignore")
def main():
        train_file = "../data/train_data.json"
        train_label_file = "../data/project-data/train.label.txt"
        dev_file = "../data/clean_dev_data.json"
        dev_label_file =  "../data/project-data/dev.label.txt"
        load_twitter_train_data = LoadDataAndProcessing(train_file,train_label_file)
        load_twitter_dev_data = LoadDataAndProcessing(dev_file,dev_label_file)
        
        train_input = load_twitter_train_data.loadData()
        dev_input = load_twitter_dev_data.loadData()

        trainset = TaskOneDataset(train_input)
        devset = TaskOneDataset(dev_input)

        trainloader = DataLoader(trainset, batch_size=1, collate_fn=trainset.create_mini_batch)
        devloader = DataLoader(devset, batch_size=1, collate_fn=devset.create_mini_batch)

        model = TwitterModel("bert-base-uncased",2)
        model.train(trainloader,devloader)


if __name__ == '__main__':
    main()