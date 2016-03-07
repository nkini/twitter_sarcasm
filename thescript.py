# coding: utf-8
filelist = glob.glob('./scraped-with-NOT-*.pkl')
filelist
twobjs = []
twidset = set()
for fname in filelist:
    l = pickle.load(open(fname,'rb'))
    for twobj in l:
        if twobj['id'] in twidset:
            pass
        else:
            twidset.add(twobj['id'])
            twobjs.append(twobj)
            
timestamps = list(map(lambda x: x['timestamp'],twobjs))
times = list(map(lambda t:datetime.strptime(t,'%I:%M %p - %d %b %Y').timestamp(),timestamps))
times.index(min(times))
times.index(max(times))
timestamps[0]
timestamps[2860]
pickle.dump(twobjs,open('scraped-with-NOT-until-13Jan2016.pkl','wb'))
