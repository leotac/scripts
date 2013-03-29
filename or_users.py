#!/usr/bin/env python
import urllib2,sys
from BeautifulSoup import BeautifulSoup
from time import strftime
from pandas import DataFrame, rolling_mean
from datetime import datetime, timedelta

def log(msg):
    with open("/home/leo/dev/scripts/log","a") as log_:
        log_.write(strftime("%Y-%m-%d %H:%M:%S") + " - " + msg + "\n")

def log_n_quit(msg):
    log(msg)
    sys.exit()


url = "http://forum.ondarock.it"
try:
    handle = urllib2.urlopen(url)
except:
    log_n_quit("could not open url")

soup = BeautifulSoup(handle, convertEntities=BeautifulSoup.HTML_ENTITIES)

stat = soup.find('h4','statistics_head')
line = stat.contents[0]
print line
users = line.split()[0]

record = strftime("%Y-%m-%d %H:%M:%S") + ',' + users + ','
print record
with open("/home/leo/dev/scripts/users.csv", "a") as csvfile:
    csvfile.write(record)
try:
    dd = DataFrame.from_csv("/home/leo/dev/scripts/users.csv",parse_dates=True, sep='|',header=0)
except:
    log_n_quit("could not load dataframe")

#roll_mean = series[-48*4:].mean()
start = datetime.now() - timedelta(days=2)
try:
    roll_mean = dd.ix[[x for x in dd.index if x>start]]['online_users'].mean()
    print roll_mean
    with open("/home/leo/dev/scripts/users.csv", "a") as csvfile:
        csvfile.write(str(roll_mean) + "\n")   
except:
    log_n_quit("could not compute mean")

log("Added users and mean.")

