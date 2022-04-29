import json
import re
import difflib
import pandas as pd
class LoadDataAndProcessing():
    def __init__(self,file,label):
        self.file = file
        self.label = label

    def textProcess(self,text):
        text = re.sub("@[\w]*", "", text)  # 去@
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", text)  # 去URL
        text = re.sub('[\n\t-]', '', text)
        text = text.strip()
        return text

    def loadData(self):
        f = open(self.file)
        data = json.load(f)
        #print(data.keys())
        tweeter_source = []
        tweeter_replay = []
        text_p1 = ""
        text_p2 = ""
        no_source = 0
        for key in data.keys():
            temp_source = ""
            temp_reply = []
            tweet_data_list = data[key]["data"]
            source_tweet = tweet_data_list[0]
            source_num = 0
            for tweet in tweet_data_list:
                if  'in_reply_to_user_id' not  in tweet.keys():
                    source_num = source_num + 1
            if  source_num == 0:
                text_p1 = self.textProcess(tweet['text']).lower()
                temp_source = temp_source + text_p1
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
        tweeter_test_source = []
        tweeter_test_replay = []
        tweeter_id = []
        with open(self.file) as f:
            data = f.readlines()
            for line in data:
                line = json.loads(line)
                temp = []
                str1 = None
                for tweeter in line:
                    if not tweeter['in_reply_to_status_id']:
                        str1 = self.textProcess(tweeter['text']).lower()
                        tweeter_test_source.append(str1)
                        tweeter_id.append(tweeter['id_str'])
                    else:
                        str2 = self.textProcess(tweeter['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
                        if res_sim >= 0.93:
                            continue
                        elif res_sim <= 0.01:
                            continue
                        else:
                            temp.append(str2)
                tweeter_test_replay.append(temp)

        # assert (len(tweeter_test_source) == len(tweeter_test_replay))

        total_replay_test = []
        for i in tweeter_test_replay:
            temp = ''
            for line in i:
                temp += line
            total_replay_test.append(temp)

        input_value_test = []
        for i in range(len(tweeter_test_source)):
            temp = {}
            temp['text'] = tweeter_test_source[i]
            temp['textb'] = total_replay_test[i]
            input_value_test.append(temp)

        return input_value_test,tweeter_id