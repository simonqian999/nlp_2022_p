import json
import re
import difflib
import pandas as pd
class LoadDataAndProcessing():
    def __init__(self,tweets_file_path,tweet_data,tweet_label):
        self.tweets_file_path = tweets_file_path
        self.tweet_data = tweet_data
        self.label = tweet_label
        
    def textProcess(self,text):
        text = re.sub("@[\w]*", "", text)  # 去@
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", text)  # 去URL
        text = re.sub('[\n\t-]', '', text)
        text = text.strip()
        return text

    def get_tweet_list(self,tweets_file_path,id_list):
        text_list = []
        for i in id_list:
            file_name = tweets_file_path + i + ".json"
            with open(file_name) as f:
                json_data = json.load(f)
            text_list.append(json_data)
        return text_list
    
    def loadData(self):
        all_ids = pd.read_table(self.tweet_data,header=None)
        data = []
        for i in range(len(all_ids)):
            list_id = list(all_ids.iloc[i])
            list_sub_id = list_id[0].split(",")
            text_list_sub =  self.get_tweet_list(self.tweets_file_path,list_sub_id)
            data.append(text_list_sub)
        tweeter_source = []
        tweeter_replay = []
        text_p1 = ""
        text_p2 = ""
        no_source = 0
        for tweet_data_list in data:
            temp_source = ""
            temp_reply = []
            source_tweet = tweet_data_list[0]['text']
            source_num = 0
            for tweet in tweet_data_list:
                if  'in_reply_to_user_id' not  in tweet.keys():
                    source_num = source_num + 1
            if  source_num == 0:
                text_p1 = self.textProcess(tweet['text']).lower()
                temp_source = temp_source + source_tweet
            elif  source_num > 1:
                for tweet in tweet_data_list:
                    if  'in_reply_to_user_id' not  in tweet.keys():
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        else:
                            temp_reply.append(text_p2)
            else:
                for tweet in tweet_data_list:
                    if  'in_reply_to_user_id' not  in tweet.keys():
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        else:
                            temp_reply.append(text_p2)
            no_source = no_source +1    
            tweeter_source.append(temp_source)                          
            tweeter_replay.append(temp_reply)     
            
        data_label = pd.read_csv(self.label, sep=" ", header=None)
        label = []
        for i in data.keys():
            index = int(i)
            #print(data_label.iloc[index])
            result_str = str(list(data_label.iloc[index])[0])
            #print(result_str)
            if result_str == 'rumour':
                label.append(0)
            else:
                label.append(1)

        total_replay = []
        for i in tweeter_replay:
            temp = ''
            for line in i:
                temp += line
            total_replay.append(temp)

        input_value = []
        for i in range(len(label)):
            temp = {}
            temp['text'] = tweeter_source[i]
            temp['textb'] = total_replay[i]
            temp['label'] = label[i]
            input_value.append(temp)

        return input_value

    def loadTestData(self):
        all_ids = pd.read_table(tweet_data,header=None)
        data = []
        for i in range(len(all_ids)):
            list_id = list(all_ids.iloc[i])
            list_sub_id = list_id[0].split(",")
            text_list_sub =  self.get_tweet_list(self.tweets_file_path,list_sub_id)
            data.append(text_list_sub)
        tweeter_source = []
        tweeter_replay = []
        tweeter_id = []
        text_p1 = ""
        text_p2 = ""
        no_source = 0
        for tweet_data_list in data:
            temp_source = ""
            temp_reply = []
            #print(tweet_data_list[0])
            source_tweet = tweet_data_list[0]
            source_num = 0
            for tweet in tweet_data_list:
                if  not tweet['in_reply_to_status_id']:
                    source_num = source_num + 1
            if  source_num == 0:
                text_p1 = self.textProcess(source_tweet['text']).lower()
                temp_source = temp_source + text_p1
                tweeter_id.append(source_tweet['id_str'])
            elif  source_num > 1:
                for tweet in tweet_data_list:
                    if  not tweet['in_reply_to_status_id']:
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                        tweeter_id.append(tweet['id_str'])
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        else:
                            temp_reply.append(text_p2)
            else:
                for tweet in tweet_data_list:
                    if  not tweet['in_reply_to_status_id']:
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        elif res_sim <= 0.01:
                            pass
                        else:
                            temp_reply.append(text_p2)
            no_source = no_source +1    
            tweeter_source.append(temp_source)                          
            tweeter_replay.append(temp_reply)     

        total_replay = []
        for i in tweeter_replay:
            temp = ''
            for line in i:
                temp += line
            total_replay.append(temp)

        input_value = []
        for i in range(len(tweeter_source)):
            temp = {}
            temp['text'] = tweeter_source[i]
            temp['textb'] = total_replay[i]
            input_value.append(temp)

        return input_value,tweeter_id
    
    
class LoadTestAndProcessing():
    def __init__(self,tweets_file_path,tweet_data):
        self.tweets_file_path = tweets_file_path
        self.tweet_data = tweet_data
        
    def textProcess(self,text):
        text = re.sub("@[\w]*", "", text)  # 去@
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", text)  # 去URL
        text = re.sub('[\n\t-]', '', text)
        text = text.strip()
        return text

    def get_tweet_list(self,tweets_file_path,id_list):
        text_list = []
        for i in id_list:
            file_name = tweets_file_path + i + ".json"
            with open(file_name) as f:
                json_data = json.load(f)
            text_list.append(json_data)
        return text_list

    def loadTestData(self):
        all_ids = pd.read_table(tweet_data,header=None)
        data = []
        for i in range(len(all_ids)):
            list_id = list(all_ids.iloc[i])
            list_sub_id = list_id[0].split(",")
            text_list_sub =  self.get_tweet_list(self.tweets_file_path,list_sub_id)
            data.append(text_list_sub)
        tweeter_source = []
        tweeter_replay = []
        tweeter_id = []
        text_p1 = ""
        text_p2 = ""
        no_source = 0
        for tweet_data_list in data:
            temp_source = ""
            temp_reply = []
            #print(tweet_data_list[0])
            source_tweet = tweet_data_list[0]
            source_num = 0
            for tweet in tweet_data_list:
                if  not tweet['in_reply_to_status_id']:
                    source_num = source_num + 1
            if  source_num == 0:
                text_p1 = self.textProcess(source_tweet['text']).lower()
                temp_source = temp_source + text_p1
                tweeter_id.append(source_tweet['id_str'])
            elif  source_num > 1:
                for tweet in tweet_data_list:
                    if  not tweet['in_reply_to_status_id']:
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                        tweeter_id.append(tweet['id_str'])
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        else:
                            temp_reply.append(text_p2)
            else:
                for tweet in tweet_data_list:
                    if  not tweet['in_reply_to_status_id']:
                        text_p1 = self.textProcess(tweet['text']).lower()
                        temp_source = temp_source + text_p1
                    else:
                        text_p2 = self.textProcess(tweet['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, text_p1, text_p2).quick_ratio()
                        if res_sim >= 0.93:
                            pass
                        elif res_sim <= 0.01:
                            pass
                        else:
                            temp_reply.append(text_p2)
            no_source = no_source +1    
            tweeter_source.append(temp_source)                          
            tweeter_replay.append(temp_reply)     

        total_replay = []
        for i in tweeter_replay:
            temp = ''
            for line in i:
                temp += line
            total_replay.append(temp)

        input_value = []
        for i in range(len(tweeter_source)):
            temp = {}
            temp['text'] = tweeter_source[i]
            temp['textb'] = total_replay[i]
            input_value.append(temp)

        return input_value,tweeter_id