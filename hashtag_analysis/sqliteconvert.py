import time
import sqlite3
import os
import sys

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
hashtags=['#dmbrandonINTL', '#CohhcarnageINTL', '#BajheeraINTL', '#koibuINTL', '#EzekieliiiINTL', '#MYMALKAPONEINTL']

if not os.path.exists(installpath+'/totals.sql'):
    f = file(installpath+'/totals.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/totals.sql')
    c = con.cursor()
    
    #Create tables
    c.execute('''CREATE TABLE totals
        (
            date text unique, 
            koibuINTL real,
            EzekieliiiINTL real,
            CohhcarnageINTL real,
            BajheeraINTL real,
            dmbrandonINTL real,
            MYMALKAPONEINTL real
        )
    ''')
    con.commit()
    con.close()
    print 'DB created'

def addDB(date,  koibuINTL,  EzekieliiiINLT,  CohhcarnageINTL,  BahjeeraINTL,  dmbrandonINTL,  MYMALALKAPONEINTL):
    con= sqlite3.connect(installpath+'/totals.sql')
    c = con.cursor()
    '''if hashtag == '#koibuINTL':
        insertlist = [date,  total,  ]
    elif hashtag == '#EzekieliiiINTL':
    elif hashtag == '#CohhcarnageINTL':
    elif hashtag == '#BahjeeraINTL':
    elif hashtag == '#dmbrandonINTL':
    elif hashtag == '#MYMALKAPONEINTL':    
    insertlist = [date,  hashtag,  total]'''
    insertlist = [date,  koibuINTL,  EzekieliiiINLT,  CohhcarnageINTL,  BahjeeraINTL,  dmbrandonINTL,  MYMALALKAPONEINTL]
    c.execute('''
        INSERT INTO totals VALUES
        ( 
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )''', insertlist)
    con.commit()
    con.close()

def getTotal(hashtag):
    con= sqlite3.connect(installpath+'/totals.sql')
    c = con.cursor()
    c.execute('''SELECT ''' + hashtag[1:] + ''' from totals WHERE ''' + hashtag[1:] + ''' = (SELECT MAX(''' + hashtag[1:] + ''') FROM totals)''')
    total = c.fetchone()
    if not total:
       # print('none found for ' + hashtag)
        con.close()
        return(0)
    else:
        total = total[0]
        total = int(total)
        #print('totals for ' + hashtag + 'are ' + str(total))
        con.close()
        return(total)
    

kcon= sqlite3.connect(installpath+'/koibu.sql')
kc = kcon.cursor()
for day in ['Thu Jul 31',  'Fri Aug 01']:
    for hour in range(0, 24):
        if hour < 10:
            hour = '0' + str(hour)
        for minute in range (0,  60):
            if minute < 10:
                minute = '0' + str(minute)
            datestring = '\'' + day + ' ' + str(hour) + ':' + str(minute) + '%\''
            totals = {'#koibuINTL':0, '#EzekieliiiINTL':0, '#CohhcarnageINTL':0,
                    '#BajheeraINTL':0, '#dmbrandonINTL':0,  '#MYMALKAPONEINTL':0}
            for hashtag in hashtags:
                kc.execute('SELECT * FROM ' + hashtag[1:] + ' WHERE date LIKE ' + datestring)
                totals[hashtag] = len(kc.fetchall()) + getTotal(hashtag)
            addDB(datestring,  totals['#koibuINTL'], totals['#EzekieliiiINTL'],  totals['#CohhcarnageINTL'],
                    totals['#BajheeraINTL'], totals['#dmbrandonINTL'],  totals['#MYMALKAPONEINTL'])
            print('added totals for ' + datestring + 
                '\n koibu: ' + str(totals['#koibuINTL']) +
                '\n Ezekiel ' + str(totals['#EzekieliiiINTL']) +
                '\n Cohhcarnage ' + str(totals['#CohhcarnageINTL']) +
                '\n Bajheera ' + str(totals['#BajheeraINTL']) +
                '\n dmbrandon ' + str(totals['#dmbrandonINTL']) +
                '\n MYMalkapone ' + str(totals['#MYMALKAPONEINTL']))
kcon.close()
            
    
    
