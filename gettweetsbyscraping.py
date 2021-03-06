from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import pickle
import time
import atexit
import json

query = '%23justkidding'
T = 0

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
    return 'https://twitter.com/i/search/timeline?vertical=default&q=%23justkidding%20lang%3Aen&src=typd&include_available_features=1&include_entities=1&lang=en&'+'max_position=TWEET-703272884786110466-'+str(max_pos)+'-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAgAAABAAAAAAAAAAIAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAA&reset_error_state=false'

def create_tweet_obj(tweet):
    obj = dict()
    try:
        obj['username'] = tweet.find('span','username').text
        obj['text'] = tweet.find('p','tweet-text').text.encode('utf8')
        obj['id'] = int(tweet['data-item-id'])
        obj['timestamp'] = tweet.find('a','tweet-timestamp')['title']
        return obj
    except KeyError as k:
        print(k)


sleep_for = 5
url = create_url('706772285470994432')

tweet_objs = []

while T < 1000:

    response = urlopen(url)
    resp_json = response.readall().decode('utf-8')
    jdict = json.loads(resp_json)
    html = jdict['items_html']
    soup = BeautifulSoup(html,'lxml')

    if T % 60 == 0 or T == 1 or T == 2:
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

    max_pos = tweets[-1]['data-item-id']

    url = create_url(max_pos)

    print(url)

    time.sleep(sleep_for)

    T += 1
