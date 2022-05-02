import json
import re
import difflib
import pandas as pd
from nltk.corpus import stopwords

class LoadDataAndProcessing():
    def __init__(self, data_file, label_file):
        with open(data_file,'r',encoding='utf-8') as f:
            self.data = json.load(f)
        self.label = pd.read_csv(label_file, delimiter = '\n', header = None)

    def textProcess(self,text):
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", text)  # remove URL
        text = text.lower() # lowercase the text
        text = re.sub(r'@[^ ]+', '', text) # replace mention
        # text = re.sub(r'#', '', text) # remove hashtag
        text = re.sub(r'([a-z])\1{2,}', r'\1', text) # character normalization
        text = re.sub(r'[^a-z ]', '', text) # remove non-letter characters
        
        stop_words = set(stopwords.words('english'))
        text_without_sw = [word for word in text.split() if not word in stop_words]
        text = (" ").join(text_without_sw) # remove stop words
        
        text = " ".join(text.split()) # remove duplicate spaces or newline
        text = text.strip()
        return text

    def loadData(self):
        tweet_source = []
        tweet_reply = []

        # go through each tweet group/line
        for group_index in self.data.keys():
            temp_source = []
            temp_reply = []
            tweet_group_data = self.data[group_index]["data"]
            
            for single_tweet_data in tweet_group_data[1:]:
                if 'in_reply_to_user_id' in single_tweet_data.keys():
                    text_sim = difflib.SequenceMatcher(None, self.textProcess(tweet_group_data[0]['text']), 
                                                      self.textProcess(single_tweet_data['text'])).quick_ratio()
                    if text_sim >= 0.9:
                        continue
                    else:
                        temp_reply.append(self.textProcess(single_tweet_data['text']))
    
            tweet_source.append(self.textProcess(tweet_group_data[0]['text']))
            tweet_reply.append(temp_reply)

        # create the label list with 0 or 1 
        label_list = []
        for group_index in self.data.keys():
            result_str = str(list(self.label.iloc[int(group_index)])[0])

            # rumour as 1 and non-rumour as 0
            if result_str == 'rumour':
                label_list.append(1)
            else:
                label_list.append(0)

        total_reply = []
        for reply_group in tweet_reply:
            replies = ''
            for single_reply in reply_group:
                replies += ' ' + single_reply
            total_reply.append(self.textProcess(replies))

        return tweet_source, total_reply, label_list
    
    def prepareDataset(self):
        tweet_source, total_reply, label_list = self.loadData()

        data_ready = []
        for i in range(len(label_list)):
            _dict = {}
            _dict['text_source'] = tweet_source[i]
            _dict['text_reply'] = total_reply[i]
            _dict['label'] = label_list[i]
            data_ready.append(_dict)
            
        return data_ready

class LoadTestDataAndProcessing():
    def __init__(self, tweets_file_path, tweet_data):
        self.tweets_file_path = tweets_file_path
        self.all_ids = pd.read_table(tweet_data, header=None)

    def textProcess(self,text):
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", text)  # remove URL
        text = text.lower() # lowercase the text

        text = re.sub(r'@[^ ]+', '', text) # replace mention
        # text = re.sub(r'#', '', text) # remove hashtag
        text = re.sub(r'([a-z])\1{2,}', r'\1', text) # character normalization
        text = re.sub(r'[^a-z ]', '', text) # remove non-letter characters
        
        stop_words = set(stopwords.words('english'))
        text_without_sw = [word for word in text.split() if not word in stop_words]
        text = (" ").join(text_without_sw) # remove stop words
        text = " ".join(text.split()) # remove duplicate spaces or newline
        text = text.strip()
        return text

    def get_tweet_group_data(self, tweets_file_path, id_list):
        data_list = []
        for tweet_id in id_list:
            file_name = tweets_file_path + tweet_id + ".json"
            with open(file_name) as f:
                data = json.load(f)
            data_list.append(data)
            
        return data_list
    
    def loadData(self):
        data = []
        for i in range(len(self.all_ids)):
            # get data for each group of tweets
            id_list = self.all_ids.iloc[i][0].split(",")
            data_list =  self.get_tweet_group_data(self.tweets_file_path, id_list)
            data.append(data_list)

        tweet_source = []
        tweet_reply = []

        for tweet_group_data in data:
            temp_source = []
            temp_reply = []
            
            for single_tweet_data in tweet_group_data[1:]:
                if 'in_reply_to_user_id' in single_tweet_data.keys():
                    text_sim = difflib.SequenceMatcher(None, self.textProcess(tweet_group_data[0]['text']), 
                                                      self.textProcess(single_tweet_data['text'])).quick_ratio()
                    if text_sim >= 0.9:
                        continue
                    else:
                        temp_reply.append(self.textProcess(single_tweet_data['text']))
    
            tweet_source.append(self.textProcess(tweet_group_data[0]['text']))
            tweet_reply.append(temp_reply)
            
        total_reply = []
        for reply_group in tweet_reply:
            replies = ''
            for single_reply in reply_group:
                replies += ' ' + single_reply
            total_reply.append(self.textProcess(replies))

        return tweet_source, total_reply
    
    def prepareDataset(self):
        tweet_source, total_reply = self.loadData()

        data_ready = []
        for i in range(len(tweet_source)):
            _dict = {}
            _dict['text_source'] = tweet_source[i]
            _dict['text_reply'] = total_reply[i]
            data_ready.append(_dict)
            
        return data_ready