from twython import Twython
import time
import sqlite3
import os
import sys

init = 0

TWITTER_APP_KEY = '' 
TWITTER_APP_KEY_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    #'#dmbrandonINTL', '#CohhcarnageINTL', '#BajheeraINTL', '#koibuINTL', '#EzekieliiiINTL', 
hashtags=['#dmbrandonINTL', '#CohhcarnageINTL', '#BajheeraINTL', '#koibuINTL', '#EzekieliiiINTL', '#MYMALKAPONEINTL']
                    
countedID = {'#koibuINTL':[], '#EzekieliiiINTL':[], '#CohhcarnageINTL':[],
                    '#BajheeraINTL':[], '#dmbrandonINTL':[],  '#MYMALKAPONEINTL':[]}
                    
waitFor = {'#koibuINTL':0, '#EzekieliiiINTL':0, '#CohhcarnageINTL':0,
                    '#BajheeraINTL':0, '#dmbrandonINTL':0,  '#MYMALKAPONEINTL':0}
                    
failed = {'#koibuINTL':0, '#EzekieliiiINTL':0, '#CohhcarnageINTL':0,
                    '#BajheeraINTL':0, '#dmbrandonINTL':0,  '#MYMALKAPONEINTL':0}
                    
firstStatus = {'#koibuINTL':494649709618012160, '#EzekieliiiINTL':494652273989931008, '#CohhcarnageINTL':494649788101832704,
                    '#BajheeraINTL':494649645872594944,  '#dmbrandonINTL':494649251545509888, '#MYMALKAPONEINTL':494654219157114880}
                    
installpath = os.path.abspath(os.path.dirname(sys.argv[0]))

if not os.path.exists(installpath+'/koibu.sql'):
    f = file(installpath+'/koibu.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/koibu.sql')
    c = con.cursor()
    
    #Create tables
    c.execute('''CREATE TABLE koibuINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    c.execute('''CREATE TABLE EzekieliiiINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    c.execute('''CREATE TABLE CohhcarnageINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    c.execute('''CREATE TABLE BajheeraINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    c.execute('''CREATE TABLE dmbrandonINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    c.execute('''CREATE TABLE MYMALKAPONEINTL
        (
            date text, 
            statusID text unique, 
            total real            
        )
    ''')
    con.commit()
    con.close()
    print 'DB created'


    
def addDB(hashtag,  date,  status, total):
    con= sqlite3.connect(installpath+'/koibu.sql')
    c = con.cursor()
    insertlist = [date,  status,  total]
    if hashtag == '#koibuINTL':
        c.execute('''
            INSERT INTO koibuINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    elif hashtag == '#EzekieliiiINTL':
        c.execute('''
            INSERT INTO EzekieliiiINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    elif hashtag == '#CohhcarnageINTL':
        c.execute('''
            INSERT INTO CohhcarnageINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    elif hashtag == '#BajheeraINTL':
        c.execute('''
            INSERT INTO BajheeraINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    elif hashtag == '#dmbrandonINTL':
        c.execute('''
            INSERT INTO dmbrandonINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    elif hashtag == '#MYMALKAPONEINTL':
        c.execute('''
            INSERT INTO MYMALKAPONEINTL VALUES
            ( 
                ?,
                ?,
                ?
            )''', insertlist)
    con.commit()
    con.close()

def getTotal(hashtag):
    con= sqlite3.connect(installpath+'/koibu.sql')
    c = con.cursor()
    if hashtag == '#koibuINTL':
        c.execute('''SELECT count(*) FROM koibuINTL''')
    elif hashtag == '#EzekieliiiINTL':
        c.execute('''SELECT count(*) FROM EzekieliiiINTL''')
    elif hashtag == '#CohhcarnageINTL':
        c.execute('''SELECT count(*) FROM CohhcarnageINTL''')
    elif hashtag == '#BajheeraINTL':
        c.execute('''SELECT count(*) FROM BajheeraINTL''')
    elif hashtag == '#dmbrandonINTL':
        c.execute('''SELECT count(*) FROM dmbrandonINTL''')
    elif hashtag == '#MYMALKAPONEINTL':
        c.execute('''SELECT count(*) FROM MYMALKAPONEINTL''')
    total = c.fetchone()
    total = total[0]
    total = int(total)
    con.close()
    return(total)
    
def getMinID(hashtag):
    con= sqlite3.connect(installpath+'/koibu.sql')
    c = con.cursor()
    if hashtag == '#koibuINTL':
        c.execute('''
            SELECT statusID FROM koibuINTL WHERE statusID = (SELECT MIN(statusID) FROM koibuINTL)''')
    elif hashtag == '#EzekieliiiINTL':
        c.execute('''
            SELECT statusID FROM EzekieliiiINTL WHERE statusID = (SELECT MIN(statusID) FROM EzekieliiiINTL)''')
    elif hashtag == '#CohhcarnageINTL':
        c.execute('''
        SELECT statusID FROM CohhcarnageINTL WHERE statusID = (SELECT MIN(statusID) FROM CohhcarnageINTL)''')
    elif hashtag == '#BajheeraINTL':
        c.execute('''
        SELECT statusID FROM BajheeraINTL WHERE statusID = (SELECT MIN(statusID) FROM BajheeraINTL)''')
    elif hashtag == '#dmbrandonINTL':
        c.execute('''
        SELECT statusID FROM dmbrandonINTL WHERE statusID = (SELECT MIN(statusID) FROM dmbrandonINTL)''')
    elif hashtag == '#MYMALKAPONEINTL':
        c.execute('''
        SELECT statusID FROM MYMALKAPONEINTL WHERE statusID = (SELECT MIN(statusID) FROM MYMALKAPONEINTL)''')
    maxID = c.fetchone()
    maxID = maxID[0]
    maxID = int(maxID)
    con.close()
    return(maxID)
def checkExistence(hashtag,  statusID):
    con= sqlite3.connect(installpath+'/koibu.sql')
    c = con.cursor()
    list = [statusID]
    if hashtag == '#koibuINTL':
        c.execute('''SELECT total FROM koibuINTL WHERE statusID = ?''',  list)
    elif hashtag == '#EzekieliiiINTL':
        c.execute('''SELECT total FROM EzekieliiiINTL WHERE statusID = ?''',  list)
    elif hashtag == '#CohhcarnageINTL':
        c.execute('''SELECT total FROM CohhcarnageINTL WHERE statusID = ?''',  list)
    elif hashtag == '#BajheeraINTL':
        c.execute('''SELECT total FROM BajheeraINTL WHERE statusID = ?''',  list)
    elif hashtag == '#dmbrandonINTL':
        c.execute('''SELECT total FROM dmbrandonINTL WHERE statusID = ?''',  list)
    elif hashtag == '#MYMALKAPONEINTL':
        c.execute('''SELECT total FROM MYMALKAPONEINTL WHERE statusID = ?''',  list)
    results = c.fetchone()
    con.close()
    if results:
        return(True)
    else:
        return(False)
            
    
while True:    
    for hashtag in hashtags:
        if waitFor[hashtag] > 0:
            #print('waiting ' + str(waitFor[hashtag]) + ' more iterations ' + hashtag)
            waitFor[hashtag] -= 1
            if failed[hashtag] > 50:
                waitFor[hashtag] = 50
            elif failed[hashtag] > 10 :
                print(hashtag + ' FAILED TO RETURN ANYTHING ' + failed[hashtag]  + ' times')
            continue
        try:
            if init == 1:
                if hashtag != '#MYMALKAPONEINTL':
                    print (hashtag + ' on init 1')
                    search = t.search(q = hashtag,  count = 100,  result_type = 'recent',  until = '2014-08-02')
                    tweets = search['statuses']
                    starttime = time.time()
                    i = 1
                    for tweet in tweets:
                        addDB(hashtag,  tweet['created_at'],  tweet['id_str'],  i)
                        i += 1
                    print(str(i) + ' entries added')
                elif hashtag == '#MYMALKAPONEINTL':
                    print('alkapone initialized! ' + hashtag)
                    init = 0
                    print 'init is now zero'
                    search = t.search(q = hashtag,  count = 100,  result_type = 'recent')
                    tweets = search['statuses']
                    i = 1
                    for tweet in tweets:
                        addDB(hashtag,  tweet['created_at'],  tweet['id_str'],  i)
                        i += 1
                    print(str(i) + ' entries added')
            elif init == 0:
                lowestID = getMinID(hashtag) 
                i = getTotal(hashtag)
                start = i
                search = t.search(q = hashtag,  count = 100, result_type = 'recent', max_id = lowestID-1,  until = '2014-08-02')
                tweets = search['statuses']
                starttime = time.time()
                if not tweets:
                    print('search result returned empty for  ' + hashtag)
                    waitFor[hashtag] = 5
                else:
                    failed[hashtag] = 0
                for tweet in tweets:
                    if not checkExistence(hashtag,  tweet['id_str']): # only do this if its not yet in DB
                        i += 1
                        addDB(hashtag,  tweet['created_at'],  tweet['id_str'],  i)
                        print ('tweet found ' + tweet['created_at'] [4:19]+ ' added for ' + hashtag + ' total: ' + str(i))
                #print (str(i-start) + ' entries added for ' + hashtag)
                timediff = (time.time()-starttime)
                timediff2 = 3-timediff
                if not timediff2 < 0:
                    #print('that took ' + str(timediff) + ' seconds, now sleeping for ' + str(timediff2))
                    time.sleep(timediff2)
                #else:
                   # print('that took ' + str(timediff) + ' seconds. Continuing')
        except KeyboardInterrupt:
            raise
        except:
            print 'exception!', sys.exc_info()[0]
            time.sleep(60)
            pass
