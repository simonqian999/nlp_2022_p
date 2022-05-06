import json
import re
import difflib
import pandas as pd
from nltk.corpus import stopwords

class LoadDataAndProcessing():
    def __init__(self, data_file):
        self.df = pd.read_json(data_file)

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
        for group_index in range(len(self.df)):
            temp_source = []
            temp_reply = []
            tweet_group_data = self.df["data"][group_index]
            
            for single_tweet_data in tweet_group_data[1:]:
                if 'in_reply_to_status_id' != None:
                    text_sim = difflib.SequenceMatcher(None, self.textProcess(tweet_group_data[0]['text']), 
                                                      self.textProcess(single_tweet_data['text'])).quick_ratio()
                    if text_sim >= 0.9:
                        continue
                    else:
                        temp_reply.append(self.textProcess(single_tweet_data['text']))
    
            tweet_source.append(self.textProcess(tweet_group_data[0]['text']))
            tweet_reply.append(temp_reply)

        # create the label list with 0 or 1 
        label_list = None
        if len(self.df.columns) == 2:
            label_list = list(self.df['label'])

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
        for i in range(len(tweet_source)):
            _dict = {}
            _dict['text_source'] = tweet_source[i]
            _dict['text_reply'] = total_reply[i]
            if label_list != None:
                _dict['label'] = label_list[i]
            data_ready.append(_dict)
            
        return data_ready