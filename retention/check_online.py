import time
import os
import sys
import json
import httplib
import ast

import sqlite3

init = 1
installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ['cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu']
streamCameOnline = {'cohhcarnage':0,  'dmbrandon':0,  'ezekiel_iii':0,  'mym_alkapone':0,  'koibu':0}
streamerLastReturn = {'cohhcarnage':0,  'dmbrandon':0,  'ezekiel_iii':0,  'mym_alkapone':0,  'koibu':0}
client_ID = ''
interval = 10

if init == 1:
    con= sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + '''Session 
            (
                start, 
                end text
            )
        ''')
    con.commit()
    con.close()

if not os.path.exists(installpath+'/twitch_retention_streamtimes.sql'):
    f = file(installpath+'/twitch_retention_streamtimes.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + ''' 
            (
                date text, 
                online integer,
                onlineSince text
            )
        ''')
    con.commit()
    con.close()
    print 'DB created'

def addSession(start, end):
    con = sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    c = con.cursor()
    insertlist = [start,  end]
    c.execute('''
        INSERT INTO ''' + streamer + '''Session VALUES
        ( 
            ?,
            ?
        )''', insertlist)
    con.commit()
    con.close()
    
def streamOnline(streamer):
    try:
        url = 'api.twitch.tv' 
        con = httplib.HTTPSConnection(url)
        con.request('GET',  '/kraken/streams/' + streamer,  '',  {'Client-ID':client_ID})
        reply = con.getresponse()
        reply = json.load(reply)
        if not reply['stream']:
            print(streamer + ' is OFFLINE at timestamp ' + str(time.time()))
            streamerLastReturn[streamer] = 0
            return False
        else:
            print(streamer + ' is ONLINE at timestamp ' + str(time.time()))
            streamerLastReturn[streamer] = 1
            return True
    except:
        print 'error,  returning last return value'
        if streamerLastReturn[streamer] == 0:
            return False
        else:
            return True
        pass
        
def addToDB(streamer, status,  cameOnline):
    insertlist = [time.time(),  status,  cameOnline]
    con = sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    c = con.cursor()
    c.execute('''
        INSERT INTO ''' + streamer + ''' VALUES
        ( 
            ?,
            ?,
            ?
        )''', insertlist)
    con.commit()
    con.close()

while 1:
    '''try:'''
    startTime = time.time()
    for streamer in streamers:
        if streamOnline(streamer):
            if streamCameOnline[streamer] == 0: #if streamer just came online
                addToDB(streamer,  1,  time.time())
                streamCameOnline[streamer] = time.time()
            else:
                addToDB(streamer,  1,  streamCameOnline[streamer])
        else:
            if streamCameOnline[streamer] != 0: # streamer was online, is now offline
                addSession(streamCameOnline[streamer],  time.time())
                streamCameOnline[streamer] = 0
            addToDB(streamer,  0,  'NaN')
    duration = time.time() - startTime
    if duration < 120:
        time.sleep(120-duration)
    '''except KeyboardInterrupt:
        sys.exit()
    except:
        print 'exception! \n', sys.exc_info()[2:]
        pass '''
