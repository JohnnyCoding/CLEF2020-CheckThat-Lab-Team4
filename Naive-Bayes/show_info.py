import csv
import json
import pprint
import sys
import classifier
import requests

TWEET_TEXT_FIELD = 'full_text'
TWEET_RETWEETED_STATUS_FIELD = 'retweeted_status'
TWEET_ENTITIES_FIELD = 'entities'
TWEET_TAGS_FIELD = 'hashtags'
TWEET_TAG_TEXT_FIELD = 'text'


def print_tags(tweet):
    tags = tweet[TWEET_ENTITIES_FIELD][TWEET_TAGS_FIELD]
    pprint.pprint(tags)


def get_text_from_tweet(tweet):
    if TWEET_RETWEETED_STATUS_FIELD in tweet:
        return tweet[TWEET_RETWEETED_STATUS_FIELD][TWEET_TEXT_FIELD]

    return tweet[TWEET_TEXT_FIELD]


def print_text(tweet):
    tweet_text = get_text_from_tweet(tweet)
    pprint.pprint(tweet_text)


TRAINING_DATASET_FILE = "data/training_dataset.csv"
CSV_TWEET_LABEL_FIELD = "label"


def get_training_data():
    dictionary = {}
    with open(TRAINING_DATASET_FILE, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            label = row[CSV_TWEET_LABEL_FIELD]
            if label in dictionary:
                dictionary[label] += 1
            else:
                dictionary[label] = 1

    print(dictionary)


if __name__ == '__main__':
    number_of_tweets = int(sys.argv[1])
    url = "http://ip2020.herokuapp.com/all_unfiltered_tweets/" + str(number_of_tweets)
    json_content = requests.get(url).json()
    tweets = json.loads(json_content)

    for i in range(number_of_tweets):
        print(i)
        print_text(tweets[i])
        print_tags(tweets[i])
        # pprint.pprint(tweets[i])
        print(classifier.is_news(tweets[i]))
        print("--------------------")
