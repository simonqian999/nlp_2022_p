# COMP90042 Project 2022: Rumour Detection and Analysis on Twitter

> This project is to develop a rumour detection system and analyse the nature of rumours that are being spread on Twitter.
>> Task 1: 
Provided with a set of tweet IDs for the source tweets and their replies, to detect whether the source tweets are rumour or not.

>> Task 2:
Use your trained rumour classifier from task 1 and apply it to unlabelled COVID-19 tweets to detect rumours, and then perform analyses to understand the nature COVID-19 rumours and how they differ to non-rumours. 

##### Group Members:

- Chenyang Dong (Student ID: 1074314)
- Yue Fei (Student ID: 980377)
- Xinwei Qian (Student ID: 1068271)

##### Directory Structure
```
Peter
│   README.md
│
└─── code
│   │	README.md
│   │	BertForSequence.ipynb
│   │	Get Tweets.ipynb
│   │	Get Testset.ipynb
│   │	Preprocessing.ipynb
│   │	Prepare Dataset on Local.ipynb
│   │	Check Devset Prediction.ipynb
│   │	Bert.ipynb
│   │	Covid Analysis.ipynb
│   │	LoadData.py
│   │	RumourDataset.py
│   │	eval.py
│   └─── deprecated
│       │   Split File.ipynb
│   
└─── data
│   │   data_crawled.zip
│   │   data_prepared.zip
│   │   valid.train.ids.txt
│   │   valid.dev.ids.txt
│   │   valid.covid.ids.txt
│   │   valid.train.label.txt
│   │   valid.dev.label.txt
│   │   ...
│   │
│   └─── raw
│       │   train.label.txt
│       │   dev.label.txt
│       │   train.data.txt
│       │   dev.data.txt
│       │   test.data.txt
│       │   covid.data.txt
│       │   dev.baseline.txt
│   	└─── tweet-objects
│       	│   80080680482123777.json
│       	│   ...
│   │
│   └─── saved
│       │   train_input.pickle
│       │   dev_input.pickle
│       │   test_input.pickle
│       │   dev_to_predict_input.pickle
│       │   covid_input.pickle
│   
└───output 
    │   Parameters.txt
    │   test_prediction.csv
    │   dev_prediction.csv
    │   covid_prediction.csv

```