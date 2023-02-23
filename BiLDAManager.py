from BILDA.BiLDA import BiLDA
import sys
import importlib
import json
from pprint import pprint
import time

importlib.reload(sys)
# sys.setdefaultencoding('utf8')

def stringify_list(tweet_list):
    s = ''
    for tweet in tweet_list:
        # for now, we remove tokens that are hashtags (i.e. tokens that contain the hashtag symbol at the start)
        # we can later remove this if-not and rerun again
        if not tweet.startswith('#'):
            s += tweet + ' '
    return s.strip()

# [run once only] to collate the tweet messages and deserialize json file to text file
def deserialize_json_and_serialize_to_text(json_file, output_file='english.txt'):
    with open(json_file, 'r') as input_file:
        loaded_json = json.load(input_file)
    with open(output_file, 'w', encoding='utf8') as output:
        for username_key in loaded_json.keys():
            for tweet_data in loaded_json[username_key]['data']:
                output.write(stringify_list(tweet_data['tweet_body']) + '\n')
    print('successfully deserialized to ' + output_file)

def deserialize_json_and_serialize_to_text_2(json_file, output_file='english.txt'):
    with open(json_file, 'r') as input_file:
        loaded_json = json.load(input_file)
    with open(output_file, 'w', encoding='utf8') as output:
        for tweet_data in loaded_json:
            output.write(stringify_list(tweet_data['tweet_body']) + '\n')
    print('successfully deserialized(2) to ' + output_file)

def get_topics(topic_file, output_file='topics_' + str(int(time.time())) +  '.json'):
    topic_lines = []
    topic_dict = {}
    with open(topic_file, 'r', encoding='utf8') as input_file:
        topic_lines = input_file.readlines()
    # pprint(topic_lines)
    prev_topic = ''
    for line in topic_lines:
        if "Topic" in line:
            key = line.replace(':\n', '')
            topic_dict[key] = {'en':'', 'fil':''}
            prev_topic = key
        else:
            en_word, en_dist, fil_word, fil_dist = line.split()
            topic_dict[prev_topic]['en'] += en_word + ' '
            topic_dict[prev_topic]['fil'] += fil_word + ' '
    serialize_to_json(output_file, topic_dict)
    print('successfully serialzed json to ' + output_file)


def serialize_to_json(filename, data):
    with open(filename, 'w') as output_file:
        json.dump(data, output_file, indent=4)
        print("successfully serialized json to " + filename)

def deserialize_json_to_text_cluster_format(json_file, output_file):
    with open(json_file, 'r') as input_file:
        loaded_json = json.load(input_file)
    with open(output_file, 'w', encoding='utf8') as output:
        for username_key in loaded_json.keys():
            for tweet_data in loaded_json[username_key]['data']:
                output.write(stringify_list(tweet_data['tweet_body']) + '\n')
    print('successfully deserialized to ' + output_file)

def deserialize_json_format_to_json_basis_format(json_file, output_file):
    with open(json_file, 'r') as input_file:
        loaded_json = json.load(input_file)
        # pprint(loaded_json)
        tweet_id = 1
        new_json = []

        for key in loaded_json.keys():
            for data in loaded_json[key]['data']:
                temp = {}
                temp['tweet_id'] = tweet_id
                temp['author'] = key
                temp['topic'] = data['topic']
                temp['tweet_message'] = data['tweet_message']
                temp['tweet_body'] = data['tweet_body']
                temp['created_at'] = data['created_at']
                tweet_id += 1
                new_json.append(temp)
        pprint(new_json, indent=4)
    with open(output_file, 'w') as output:
        json.dump(new_json, output, indent=4)
    print('successfully deserialized to ' + output_file)

def smallify_json(json_file, output_file):
    with open(json_file, 'r') as input_file:
        loaded_json = json.load(input_file)
        # pprint(loaded_json)
        tweet_id = 1
        new_json = []
        for data in loaded_json:
            temp = {}
            temp['author'] = data['author']
            temp['topic'] = data['topic']
            temp['tweet_message'] = data['tweet_message']
            temp['tweet_body'] = data['tweet_body']
            temp['created_at'] = data['created_at']
            new_json.append(temp)
        pprint(new_json, indent=4)
    with open(output_file, 'w') as output:
        json.dump(new_json, output, indent=4)
    print('successfully deserialized to ' + output_file)


def setup_and_run_bilda(english_txt, tagalog_txt):
    bilda = BiLDA()
    bilda.config(0.2, 0.5, 6, 50)
    bilda.readData(english_txt, tagalog_txt)
    bilda.sampler()
    bilda.updateParameter()

    output_file = 'topic_word_' + str(int(time.time())) + '.txt'
    bilda.creat_file(output_file)

    # serialize to json
    get_topics(topic_file=output_file)


if __name__ == "__main__":

    english_path = "english_text.txt"
    tagalog_path = "tagalog_text.txt"

    setup_and_run_bilda(english_path, tagalog_path)






