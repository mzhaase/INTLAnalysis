import httplib
import time
import json
import os
import sys

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
client_ID = ''
streamers = ('cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu',  'thejustinflynn')

if not os.path.exists(installpath+'/twitch_gamesplayed.sql'):
    f = file(installpath+'/twitch_gamesplayed.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/twitch_gamesplayed.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + ''' 
            (
                date text, 
                game,
                total real            
            )
        ''')
    con.commit()
    con.close()
    print 'DB created'

def addDB(streamer,  date,  game, total):
    con= sqlite3.connect(installpath+'/twitch_gamesplayed.sql')
    c = con.cursor()
    insertlist = [date,  game,  total]
    c.execute('''
        INSERT INTO ''' + streamer + ''' VALUES
        ( 
            ?,
            ?,
            ?
        )''', insertlist)
    con.commit()
    print('Added game ' + game + ' for streamer ' + streamer + ' at ' + str(date))
    con.close()
    
def doesGameExist(streamer,  game):
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = '''SELECT * FROM ''' + streamer + ''' WHERE game = \"''' + game + '\"'
    c.execute(statement)
    c.fetchone()
    if not c.fetchone():
        con.close()
        return False
    else:
        con.close()
        return True
        
def getTotal(streamer,  game):
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = '''SELECT total FROM ''' + streamer + ''' WHERE game = \"''' + game + '''\" AND date = (SELECT MAX(date) FROM ''' + streamer + ''')'''
    c.execute(statement)
    total = c.fetchone()
    if not total:
        total = 0
    else:
        total = float(total[0])
        con.close()
    return total
    
def getLastDate(streamer, game):
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = '''SELECT date FROM ''' + streamer + ''' WHERE game = \"''' + game + '''\" AND date = (SELECT MAX(date) FROM ''' + streamer + ''')'''
    c.execute(statement)
    total = c.fetchone()
    if not total:
        total = 0
    else:
        total = float(total[0])
    con.close()
    return total

def getGamePlayed(streamer):
    url = 'api.twitch.tv' 
    con = httplib.HTTPSConnection(url)
    con.request('GET',  '/kraken/streams/' + streamer,  '',  {'Client-ID':client_ID})
    reply = con.getresponse()
    return(reply)
    
while True:
    try:
        for streamer in streamers:
            startTime = time.time()
            gameJSON = json.load(getGamePlayed(streamer))
            if gameJSON['stream'] == None or gameJSON['stream'] == 'Null':
                game = 'offline'
            else:
                game = gameJSON['stream']['channel']['game']
            game.replace('"', '')
            if game:
                if doesGameExist(streamer,  game):
                    total = getTotal(streamer,  game)
                    lastDate= getLastDate(streamer,  game)
                    total += time.time() - lastDate
                else:
                    total = 1
                addDB(streamer,  time.time(), game,  total)
            runTime = time.time() - startTime
            print ('runtime: ' + str(runTime))
            if runTime < 10:
                time.sleep(10-runTime)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'exception! \n', sys.exc_info()[0]
        raise
        pass
