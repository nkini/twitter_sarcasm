# coding: utf-8
import pickle
from datetime import datetime
import glob
import sys

filelist = glob.glob(sys.argv[1])
twobjs = []
twidset = set()
for fname in filelist:
    l = pickle.load(open(fname,'rb'))
    for twobj in l:
        if twobj:
            if twobj['id'] in twidset:
                pass
            else:
                twidset.add(twobj['id'])
                twobjs.append(twobj)
            
timestamps = list(map(lambda x: x['timestamp'],twobjs))
times = list(map(lambda t:datetime.strptime(t,'%I:%M %p - %d %b %Y').timestamp(),timestamps))

print("max time",timestamps[times.index(max(times))])
print("max time",timestamps[times.index(min(times))])

filename = input('Give file name for the cumulative pickle: ')
pickle.dump(twobjs,open(filename+'.pkl','wb'))
