# read info from lineage csv for evaluation

import csv
from pprint import pprint

CSVNAME = "lineages-NEW.csv"


class eid():
    def __init__(self, i):
        self.date = i[0]
        self.source = i[2]
        self.lineage = i[3]
        self.taper = i[4]
        self.transferer = i[5]
        self.uploader = i[6]
        self.subject = i[7]
        self.notes = i[8]
        self.recording = i[9]

#____________________________________________________

def opencsv():
    with open(CSVNAME, 'rb') as f:
        reader = csv.reader(f)
        csv_list = list(reader)
        
    return csv_list
    
#____________________________________________________

def makeDict(l):
    ldict = {}
    for n in l[1:]:
        if n[1] not in ldict:
            ldict[n[1]] = eid(n)
        
    return ldict

#____________________________________________________

def ldict():
    
    l = opencsv()    
    d = makeDict(l)
    
    return d
    
    #tapers = []
    #for n in d:
    #    if d[n].taper != "" and d[n].taper not in tapers:
            #print d[n].taper
    #        tapers.append(d[n].taper)

        
    #    if d[n].taper == "" and d[n].recording == "AUD":
    #        print n
    #        print d[n].notes
    #        print
    #        print("_________________________________________________________")
    #        print("_________________________________________________________")
    #        print

#____________________________________________________

