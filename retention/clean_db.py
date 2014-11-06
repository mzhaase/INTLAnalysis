import time
import os
import sys

import sqlite3

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ['cohhcarnage', 'ezekiel_iii', 'dmbrandon']

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
    
def deleteRecords(streamer,  lastValidDate, nextValidDate):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    statement = "DELETE FROM " + streamer + " WHERE date > " + str(lastValidDate) + " AND date < " + str(nextValidDate)
    print statement
    c.execute(statement)
    con.commit()
    con.close()
    
def checkRecords(sinceTime):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    c.execute("SELECT MIN(date) FROM mym_alkapone WHERE date > " + str(sinceTime))
    result = c.fetchone()
    result = result[0]
    con.close()
    if result:
        return result
    else:
        return False
    
lastDate = 0
while 1:
    lastValidDate = float(checkRecords(lastDate))
    if lastDate == 0:
        lastDate = lastValidDate
    lastDate += 360
    if checkRecords(lastDate):
        nextValidDate = float(checkRecords(lastDate))
        for streamer in streamers:
            deleteRecords(streamer,  lastValidDate,  nextValidDate)
    else:
        break

