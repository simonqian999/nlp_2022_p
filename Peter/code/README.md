# Code
> If you want to reuse the code, please follow the order and instructions. 
>> Most of notebooks are labelled with sections clearly, please check and follow the sections.

### Get Tweets.ipynb
- Use this notebook to crawl the tweets.
- Please make sure your crawled data naming with '_all' after (eg. train_data_all.json).
### Get Testset.ipynb
- Use this notebook to merge all json file of single tweet into one testset like trainset and devset.
- You will get "test_data_all.json" in data folder.
### Preprocessing.ipynb
- Use this notebook to preprocess the data including format changing, replies filter and so on (text preprocess will be made in LoadData.py).
- By following the process, you will get files end with '_prepared' which means the data is prepared to use. For example, from your crawled data "train_data_all.json", you will get "train_data_prepared".
### Prepare Dataset on Local.ipynb
- Use this notebook to prepare the data input for bert modelling (optional).
- You will get pickle file through this. If you want to use them, put them into right place mentioned in BertForSequence.ipynb. 
### LoadData.py
- Contain a class to load and process on the input (mainly on text and choice).
### RumourDataset.py
- Contain a class to prepare the dataset format for model to use.
### BertForSequence.ipynb
- Use this notebook for modelling (train, evaluation, test).
- When use this notebook in Colab, make sure you upload two python file above in session and also you have the same Google Drive directory and needed files put in (files end with 'prepared' or input pickle file and "valid.label" file).
### Check Devset Prediction.ipynb
- Use this notebook to check the prediction performance on devset (double check afterwards as it's already done in BertForSequence.ipynb with a good pipeline).
### Covid Analysis.ipynb
- Use this notebook to check the analysis on covid data for task 2.