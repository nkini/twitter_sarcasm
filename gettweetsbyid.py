# coding: utf-8
import tweepy
import pickle
import sys
import time
import json
import atexit
import os.path

import accesskeys as ak
auth = tweepy.OAuthHandler(ak.consumer_key, ak.consumer_secret)
auth.set_access_token(ak.access_token, ak.access_token_secret)

api = tweepy.API(auth)
not_retrieved = []

tweets = []
count = 0
sleep_for = 5.05


@atexit.register
def write_to_files():
    global count,tweets,not_retrieved
    fn = sys.argv[1]+'-tweets-'+str(count)+'.pkl'
    if os.path.exists(fn):
        fn += "-1"
    f1 = open(fn,'wb')
    pickle.dump(tweets,f1)
    fn = sys.argv[1]+'-not_retrieved_ids-'+str(count)+'.pkl'
    if os.path.exists(fn):
        fn += "-1"
    f2 = open(fn,'wb')
    pickle.dump(not_retrieved,f2)
    f1.close()
    f2.close()
    tweets = []
    not_retrieved = []

for line in open(sys.argv[1]):
    
    fields = line.rstrip('\n').split('\t')
    sid    = int(fields[0])
    sen    = fields[1]

    try:
        count += 1
        if count % 100 == 0:
            write_to_files()
        time.sleep(sleep_for)
        print("fetching tweet #%d, with tweetid %d" % (count,sid))
        sobj = api.get_status(sid)
        sobj._json['is_sarcastic'] = sen == "SARCASM"
        tweets.append(sobj._json)

    except tweepy.error.RateLimitError as e:
        not_retrieved.append((sid,'Rate limit error'))
        print("Oops! Rate limit error!")
        print("Last retrieved = ", sid)
        write_to_files()
        break

    except tweepy.error.TweepError as e:
        print(e)
        not_retrieved.append((sid,json.loads(e.__dict__['reason'].replace("'","\""))[0]['message']))
        print(sid)

    except Exception as e:
        print("An unknown exception occurred",e)
