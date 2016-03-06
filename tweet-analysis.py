import re
from collections import defaultdict
from pprint import pprint
import operator
import pickle

class TweetAnalysis:
    
    def getWordCount(self):
        lst = re.findall('#[a-zA-Z]+',self.tweetstext)
        d = defaultdict(int)
        for item in lst:
            d[item.lower()] += 1
        #return d
        #print(len(d.keys()))
        pprint(sorted(d.items(), key=operator.itemgetter(1),reverse=True)[:10])


    def getTweetsWithHashtag(self, hashtag):
        h = hashtag.lower()
        for tweet in self.tweetlist:
            t = tweet.lower()
            if re.search(h+'[^a-z]',t,re.DOTALL):
                yield tweet


class SemEvalTraining(TweetAnalysis):

    def __init__(self):    
        self.tweetlist = []
        with open('semeval-train.txt', encoding="utf8") as f:
            #tweets = f.read().encode('ascii', 'ignore')
            for line in f:
                self.tweetlist.append(line.strip('\n').encode('ascii', 'ignore').decode())
        self.tweetstext = ' '.join(self.tweetlist)


SET = SemEvalTraining()
pprint(list(SET.getTweetsWithHashtag('if [a-zA-Z ]+then')))
#SET.getWordCount()


class ShereenTweets(TweetAnalysis):

    SARC = 0
    NOTSARC = 1
    BOTH = 2

    def __init__(self,category):
        self.tweetlist = []
        if category == self.SARC or category == self.BOTH:
            tw = pickle.load(open('sarc-tweets.pkl','rb'))
            self.tweetlist.extend(tw)
        if category == self.SARC or category == self.BOTH:
            tw = pickle.load(open('notsarc-tweets.pkl','rb'))
            self.tweetlist.extend(tw)
        self.tweetstext = ' '.join(self.tweetlist)

#ST = ShereenTweets(ShereenTweets.SARC)
#pprint(list(ST.getTweetsWithHashtag('if [a-zA-Z ]+then')))
#ST.getWordCount()
