import sys
import os
import socket
import string
import time
import hashlib

import sqlite3

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
HOST="irc.twitch.tv"
PORT=6667
NICK=""
IDENT=""
oauth=""
readbuffer=""
streamers = ['cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu']
viewers = {'cohhcarnage':[],  'dmbrandon':[],  'ezekiel_iii':[],  'mym_alkapone':[],  'koibu':[]}
firstStart = 1
i = 0

s=socket.socket( )
s.connect((HOST, PORT))
s.send("PASS oauth:%s\r\n" % oauth)
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, NICK))

if not os.path.exists(installpath+'/twitch_retention.sql'):
    f = file(installpath+'/twitch_retention.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + ''' 
            (
                date text, 
                hash text,
                joinTime text,
                leaveTime text,
                duration text
            )
        ''')
    con.commit()
    con.close()
    print 'DB created'

def addToDB(command,  streamer,  hash,  join,  leave,  duration):
    con= sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    if command == 'join':
        insertlist = [join,  hash,  join,  leave, duration]
        c.execute('''
            INSERT INTO ''' + streamer + ''' VALUES
            ( 
                ?,
                ?,
                ?,
                ?,
                ?
            )''', insertlist)
        con.commit()
        con.close()
    
    if command == 'leave':
        statement = "UPDATE " + streamer + " SET leaveTime = '" + leave + "', duration = '" + duration + "' WHERE hash = '" + hash + "' AND date = (SELECT MAX(date) FROM " + streamer + " WHERE hash = '" + hash + "')"
        c.execute(statement)
        con.commit()
        con.close()
            
def checkDB(command, streamer, hash):
    con = sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    if command == 'chk_leave_empty':
        c.execute(
            "SELECT leaveTime FROM " + streamer + 
            " WHERE hash = '" + hash + 
            "' AND leaveTime = 'NaN' AND date = (SELECT MAX(date) FROM " + streamer +
            " WHERE hash = '" + hash + "')"
        )
        result = c.fetchone()
        if not result:
            con.close()
            return False
        else:
            c.execute(
                "SELECT joinTime FROM " + streamer + 
                " WHERE hash = '" + hash + 
                "' AND leaveTime = 'NaN' AND date = (SELECT MAX(date) FROM " + streamer +
                " WHERE hash = '" + hash + "')"
            )
            result = c.fetchone()
            result = result[0]
            return result
    
    if command == 'chk_avg_duration':
        total = 0
        i = 1.
        c.execute('''SELECT duration FROM ''' + streamer + ''' WHERE duration NOT = "NaN"''')
        result = c.fetchall()
        if not result:
            con.close()
            return False
        else:
            for line in result:
                total += int(line)
                i += 1
            average = total / i
        con.close()
        return average
    

while 1:
    try:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        for line in temp:
            line=string.rstrip(line)
            line=string.split(line)
            '''if not line[1] == 'PRIVMSG':
                print line'''        
                
            if line[1] == "376" and firstStart == 1:
                firstStart = 0
                for streamer in streamers:
                    s.send("JOIN #" + streamer + "\r\n")
                
            if(line[0]=="PING"):
                s.send("PONG %s\r\n" % line[1])
                
            '''if not i%60:
                for streamer in streamers:
                    s.send("WHO #" + streamer + "\r\n")'''
                    
            if line[1] == "JOIN":
                streamer = line[2][1:]
                hash = hashlib.sha256(line[0]).hexdigest()
                join = time.time()
                leave = 'NaN'
                duration = 'NaN'
                addToDB('join',  streamer,  hash,  str(join), leave,  duration)
                print('JOIN ' + line[0] + ' at timestamp: ' + str(join) + ' for streamer: ' + streamer)
                
            if line[1] == "PART":
                streamer = line[2][1:]
                hash = hashlib.sha256(line[0]).hexdigest()
                join = checkDB('chk_leave_empty',  streamer,  hash)
                if join:
                    leave = time.time()
                    duration = leave - float(join)
                    addToDB('leave',  streamer,  hash,  str(join),  str(leave),  str(duration))
                    print('PART ' + line[0] + ' at timestamp: ' + str(time.time()) + ' for streamer: ' + streamer)
                    
            if not i%3600: #once every hour
                for streamer in streamers:
                    s.send("PART #" + streamer + "\r\n")
                for streamer in streamers:
                    s.send("JOIN #" + streamer + "\r\n")
        time.sleep(1)
        i += 1
    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'exception! \n', sys.exc_info()[0]
        raise
        pass
