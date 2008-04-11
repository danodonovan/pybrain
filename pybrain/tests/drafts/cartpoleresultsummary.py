__author__ = 'Tom Schaul, tom@idsia.ch'


import os
from scipy import array, reshape

from nesexperiments import pickleReadDict

filedir = '../temp/cartpole/'
allfiles = os.listdir(filedir)
alldata = {}
for f in allfiles:
    if f[-7:] == '.pickle':
        runid = f[-12:-7]
        runtype = f[:-14]
        allfits = array(map(lambda x:x[1], pickleReadDict('../temp/cartpole/'+f[:-7])))
        if runtype not in alldata:
            alldata[runtype] = []
        alldata[runtype].append(allfits)

for runtype, res in alldata.items():
    print 'Experiment type:', runtype
    print 'Number of runs:', len(res)
    print 'Number of episodes for all runs', map(len, res)
    successes = filter(lambda x: max(x) >= 100000, res)
    print 'Successful runs:', len(successes)
    if len(successes) > 0:
        print 'Number of episodes for successful runs', map(len, successes)
        print 'Average number of episodes until success (not considering failures):',  sum(map(len, successes))/float(len(successes))
    failures = filter(lambda x: max(x) < 100000, res)
    if len(failures) > 0:
        print '(best fitness, nb of episodes) for failed runs:', zip(map(max, failures),map(len, failures))
        print 'Average fitness (among failures):',  sum(map(max, failures))/float(len(failures))
    print '\n\n'
    
    
    
    
            
            