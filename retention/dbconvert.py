import time
import os
import sys

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ['cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu']
interval = 10

if not os.path.exists(installpath+'/twitch_retention_results_nosquat.sql'):
    f = file(installpath+'/twitch_retention_results_nosquat.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + ''' 
            (
                date text, 
                total integer,
                online text
            )
        ''')
    con.commit()
    con.close()
    print 'DB created'
    
def checkUserDB(streamer):
    con = sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    total = 0
    i = 1.
    c.execute("SELECT duration FROM " + streamer + " WHERE duration != 'NaN'")
    result = c.fetchall()
    if not result:
        con.close()
        return False
    else:
        for line in result:
            total += float(line[0])
            i += 1
        average = total / i
    con.close()
    return average
    
def checkResultDB(streamer):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    c.execute("SELECT total FROM " + streamer + " ORDER BY date")
    results = c.fetchall()
    con.close()
    resultList = []
    if not results:
        return [0, 0]
    else:
        for result in results:
            resultList.append(result[0])
        return resultList
    
def getTimespan():
    con = sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    c.execute("SELECT MAX(date) FROM mym_alkapone")
    maxDate = c.fetchone()
    if maxDate:
        maxDate = maxDate[0]
    c.execute("SELECT MIN(date) FROM mym_alkapone")
    minDate = c.fetchone()
    if minDate: 
        minDate = minDate[0]
    if minDate and maxDate:
        return({'min':minDate, 'max':maxDate})
    else:
        return False
    
def addToResults(streamer,  date,  total):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    insertlist = [date,  int(total/60)]
    c.execute('''
        INSERT INTO ''' + streamer + ''' VALUES
        ( 
            ?,
            ?
        )''', insertlist)
    con.commit()
    con.close()
    
timespan = getTimespan()
min = float(timespan[0])
max = (timespan[1])
datapoints = int((max - min) / 360)
for i in range(0,  datapoints):
    
