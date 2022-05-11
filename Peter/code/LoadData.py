import json
import re
import difflib
import pandas as pd
from nltk.corpus import stopwords

class LoadDataAndProcessing():
    def __init__(self, data_file):
        self.df = pd.read_json(data_file)

    def textProcess(self,text):
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', " ", text)  # remove URL
        text = text.lower() # lowercase the text
#         text = re.sub(r'@[^ ]+', ' ', text) # replace mention
#         text = re.sub(r'#', '', text) # remove hashtag
        text = re.sub(r'([a-z])\1{2,}', r'\1', text) # character normalization
        text = re.sub(r'[^a-z0-9 ]', ' ', text) # remove non alphanumeric character characters
        
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
            tweet_group_data = self.df["data"][group_index]
            first_tweet = self.textProcess(tweet_group_data[0]['text'])
            temp_source = first_tweet
            temp_reply = []
            
            for single_tweet_data in tweet_group_data[1:]:
                
                # check if the reply also comes from the source author
                # if so, add to the source based on similarity
                if single_tweet_data['user']['id'] == tweet_group_data[0]['user']['id']:
                    text_sim = difflib.SequenceMatcher(None, self.textProcess(tweet_group_data[0]['text']), 
                                                      self.textProcess(single_tweet_data['text'])).quick_ratio()
                    if text_sim < 0.9:
                        temp_source += ' ' + self.textProcess(single_tweet_data['text'])
                else: 
                    if single_tweet_data['in_reply_to_status_id'] != None:
                        single_reply = self.textProcess(single_tweet_data['text'])
                        if first_tweet in single_reply:
                            single_reply = single_reply.replace(first_tweet, "")
                        temp_reply.append(single_reply)
                    
            # add username and user description as data of source
            if tweet_group_data[0]['user']['verified']:
                temp_source += ' ' + tweet_group_data[0]['user']['username']
                temp_source += ' ' + tweet_group_data[0]['user']['description']
    
            tweet_source.append(self.textProcess(temp_source))
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