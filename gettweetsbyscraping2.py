from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import pickle
import time
import atexit
import json

query = '%23justkidding'


@atexit.register
def write_to_files():
    global T,tweet_objs
    fn = "scraped-with-JUSTKIDDING-"+str(T)+'.pkl'
    if os.path.exists(fn):
        fn += "-1"
    f1 = open(fn,'wb')
    pickle.dump(tweet_objs,f1)
    f1.close()
    tweet_objs = []


def create_url(max_pos):
    global query
    return "https://twitter.com/i/search/timeline?vertical=default&lang=en&q="+query+\
          "&include_available_features=1&include_entities=1&max_position="+max_pos+\
          "&reset_error_state=false"


def create_tweet_obj(tweet):
    obj = dict()
    obj['username'] = tweet.find('span','username').text
    obj['text'] = tweet.find('p','tweet-text').text.encode('utf8')
    obj['id'] = int(tweet['data-item-id'])
    obj['timestamp'] = tweet.find('a','tweet-timestamp')['title']
    return obj


url = 'https://twitter.com/search?q='+query+'&lang=en'
sleep_for = 5.1

tweet_objs = []

response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html,'lxml')

tweets = soup.find_all('li','js-stream-item')

for tweet in tweets:
    if tweet.find('p','tweet-text'):
        tweet_objs.append(create_tweet_obj(tweet))


first_tweet_id = tweets[3]['id']
max_pos = "TWEET-"+tweets[0]['id']+"-"+tweets[-1]['id']

url = create_url(max_pos)

print(url)

time.sleep(sleep_for)

T = 1

while T < 1000:

    response = urlopen(url)
    resp_json = response.readall().decode('utf-8')
    jdict = json.loads(resp_json)
    html = jdict['items_html']
    soup = BeautifulSoup(html,'lxml')

    if T % 60 == 0:
        write_to_files()

    print("Run No.",T)

    tweets = soup.find_all('li','js-stream-item')

    if not tweets:
        print("no tweets were found by tweets = soup.find_all('li','js-stream-item')")
        write_to_files()
        break

    for tweet in tweets:
        if tweet.find('p','tweet-text'):
            tweet_objs.append(create_tweet_obj(tweet))

    if not jdict['has_more_items']:
        write_to_files()
        break

    print(tweets[0])
    print(tweets[-1])
    max_pos = "TWEET-"+tweets[0]['id']+"-"+tweets[-1]['id']

    url = create_url(max_pos)

    print(url)

    time.sleep(sleep_for)

    T += 1
