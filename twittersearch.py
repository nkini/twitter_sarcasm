# coding: utf-8
from TwitterSearch import *
import pickle
import time

tso = TwitterSearchOrder()
tso.set_keywords(['#lol'])
tso.set_language('en')

flog = open('twittersearch.log','w')

import accesskeys as ak

ts = TwitterSearch(
    consumer_key = ak.consumer_key,
    consumer_secret = ak.consumer_secret,
    access_token = ak.access_token,
    access_token_secret = ak.access_token_secret)


sleep_for = 5.1      # you should be able to go down to 5 seconds
last_num_queries = 0
retrieved_tweets = set()
number_of_repeat_tweets = 0

try:
    tweetpkl = open('lol.pkl','wb')
    tweets = []
    for tweet in ts.search_tweets_iterable(tso):
        tweets.append(tweet)
        if tweet['id'] in retrieved_tweets:
            print("tweet has already been retrieved")
            number_of_repeat_tweets += 1
        else:
            retrieved_tweets.add(tweet['id'])

        cur_num_queries,tweets_recd = ts.get_statistics()
        if not last_num_queries == cur_num_queries:
            print("Queries done: %i. Tweets received: %i" % ts.get_statistics())
            last_num_queries = cur_num_queries
            print("Sleeping for",sleep_for,"seconds")
            time.sleep(sleep_for)

    pickle.dump(tweets,tweetpkl)
    print("Wrote tweets to file",tweetpkl.name)
    print("number_of_repeat_tweets: ",number_of_repeat_tweets)
    tweetpkl.close()

except TwitterSearchException as e:
    if e.code < 1000:
        print("HTTP status based exception: %i - %s" % (e.code, e.message))
    else:
        print("Regular exception: %i - %s" % (e.code, e.message))
    pickle.dump(tweets,tweetpkl)
    print("Wrote tweets to file",tweetpkl.name)
    print("number_of_repeat_tweets: ",number_of_repeat_tweets)
    tweetpkl.close()

except Exception as e:
    pickle.dump(tweets,tweetpkl)
    print("Wrote tweets to file",tweetpkl.name)
    print("number_of_repeat_tweets: ",number_of_repeat_tweets)
    tweetpkl.close()

flog.close()
