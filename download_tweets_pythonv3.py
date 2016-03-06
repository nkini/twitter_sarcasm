#!/usr/bin/python

import sys
import urllib
import re
import json
import urllib.request

from bs4 import BeautifulSoup

import socket
socket.setdefaulttimeout(10)

cache = {}
mapper = {}

f1 = open('tweets-scrape.txt','w',encoding='utf-8')

'''
for line in open(sys.argv[2]):
    fields = line.rstrip('\n').split('\t')
    oldid = fields[0]
    newid = fields[1]
    mapper[oldid] = newid
'''

counter = 0

for line in open(sys.argv[1]):
 fields = line.rstrip('\n').split('\t')
 sid = fields[0]
 sen = fields[1]

  #url = 'http://twitter.com/intent/retweet?tweet_id=%s' % (sid)
  #print url
 tweet = None
 text = "Not Available"
 if sid in cache:
  text = cache[sid]
 else:
  try:
   url = "http://twitter.com/intent/retweet?tweet_id=" + sid
   f = urllib.request.urlopen(url)
   #Thanks to Aniruddha
   myhtml = f.read()
   #html = html.replace("</html>", "") + "</html>"
   #print (html)
   soup = BeautifulSoup(myhtml,'lxml')
   jstt = soup.find_all("div","tweet-text")
   tweets = list(set([x.get_text() for x in jstt]))
   #print len(tweets)
   #print (tweets)
   #print ("\t")(tweets)
   f1.write(sid + "\t" + sen + "\t" + tweets[0]+"\n")
   print(counter,"successful")
   counter+=1
  except Exception as e:
   print("error\ntweet id:",sid,'\n',sys.exc_info()[0])
   continue

f1.close()
