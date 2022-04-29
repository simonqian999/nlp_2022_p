import json
import re
import difflib

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
        tweeter_source = []
        tweeter_replay = []

        with open(self.file) as f:
            data = f.readlines()
            for line in data:
                line = json.loads(line)
                temp = []
                str1 = None
                for tweeter in line:
                    if not tweeter['in_reply_to_status_id']:
                        str1 = self.textProcess(tweeter['text']).lower()
                        tweeter_source.append(str1)
                    else:
                        str2 = self.textProcess(tweeter['text']).lower()
                        res_sim = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
                        if res_sim >= 0.93:
                            continue
                        else:
                            temp.append(str2)
                tweeter_replay.append(temp)

        # rumour is 0  non-rumour is 1

        with open(self.label) as f:
            data = f.read()
            data = json.loads(data)
            tweeter_label_id = data

        label = []  # train-->label
        for i, value in enumerate(tweeter_label_id.values()):
            if value == 'non-rumour':
                label += [1]
            else:
                label += [0]

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