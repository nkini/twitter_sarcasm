import atexit
import json
import os
import pickle
import time
import unittest
from urllib.request import urlopen

from bs4 import BeautifulSoup
from selenium import webdriver

query = '%23justkidding'
T = 0
tweet_objs = []
html_source = ''
global_sel = None


class Sel(unittest.TestCase):
    def setUp(self):
        global global_sel
        global_sel = self
        firefox_profile = webdriver.FirefoxProfile()

        firefox_profile.add_extension("./quickjava-2.0.7-fx.xpi")
        firefox_profile.set_preference("thatoneguydotnet.QuickJava.curVersion", "2.0.6.1") ## Prevents loading the 'thank you for installing screen'
        firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Images", 2)  ## Turns images off
        firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.AnimatedImage", 2)  ## Turns animated images off

        self.driver = webdriver.Firefox(firefox_profile)
        self.driver.implicitly_wait(30)
        self.base_url = "https://twitter.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_sel(self):
        driver = self.driver
        #driver.get(self.base_url + "/search?q=%23justkidding lang%3Aen until%3A2016-01-13 since%3A2015-02-14&src=typd")
        driver.get(self.base_url + "/search?q=%23justkidding&lang=en&src=typd")
        global T, html_source
        for i in range(1,2000):
            T = i
            print("scroll #",i)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            if i % 50 == 0:
                handle_with_bs()


def write_to_files():
    global T,tweet_objs
    fn = "scraped-with-JUSTKIDDING-"+str(T)+'.pkl'
    if os.path.exists(fn):
        fn += "-1"
    f1 = open(fn,'wb')
    pickle.dump(tweet_objs,f1)
    f1.close()
    tweet_objs = []


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


@atexit.register
def handle_with_bs():
    global T, global_sel
    soup = BeautifulSoup(global_sel.driver.page_source.encode('utf-8'),'lxml')

    tweets = soup.find_all('li','js-stream-item')

    for tweet in tweets:
        if tweet.find('p','tweet-text'):
            tweet_objs.append(create_tweet_obj(tweet))

    write_to_files()

if __name__ == "__main__":
    unittest.main()
