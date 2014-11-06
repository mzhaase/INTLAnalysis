import time
import sqlite3
import os
import sys
import ast

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
##dmbrandonINTL', '#CohhcarnageINTL', '#BajheeraINTL', , '#EzekieliiiINTL', '#MYMALKAPONEINTL'
hashtags=['#koibuINTL', '#dmbrandonINTL', '#CohhcarnageINTL', '#BajheeraINTL', '#EzekieliiiINTL', '#MYMALKAPONEINTL']

def addDB(date,  koibuINTL,  EzekieliiiINLT,  CohhcarnageINTL,  BahjeeraINTL,  dmbrandonINTL,  MYMALALKAPONEINTL):
    con= sqlite3.connect(installpath+'/totals.sql')
    c = con.cursor()
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

with open('koibubackup', 'r') as r:
    for line in r:
        history = ast.literal_eval(line)
'''for hashtag in hashtags:
    total = getTotal(hashtag)
    j = 0
    for entry in history[hashtag]:
        if j >= 12*60:
            history[hashtag][j] += total
            #print total
            print('updated entry ' + str(j))'''
    
#koibubackup is datapoint every 45 sec, so 4 points = 3 minutes    
i = 960

for day in ['Sat Aug 02',  'Sun Aug 03']:
    for hour in range(0, 24):
        if hour < 10:
            hour = '0' + str(hour)
        for minute in range (0,  60):
            i += 1  
            if minute < 10:
                minute = '0' + str(minute)
            datestring = '\'' + day + ' ' + str(hour) + ':' + str(minute)
            totalsstart = {'#koibuINTL':32623, '#EzekieliiiINTL':12643, '#CohhcarnageINTL':12265,
                    '#BajheeraINTL':4635, '#dmbrandonINTL':21842,  '#MYMALKAPONEINTL':84456}
            offset = {'#koibuINTL':16420, '#EzekieliiiINTL':2712, '#CohhcarnageINTL':2830,
                    '#BajheeraINTL':3413, '#dmbrandonINTL':9968,  '#MYMALKAPONEINTL':36811}
            totals = {'#koibuINTL':0, '#EzekieliiiINTL':0, '#CohhcarnageINTL':0,
                    '#BajheeraINTL':0, '#dmbrandonINTL':0,  '#MYMALKAPONEINTL':0}
            for hashtag in hashtags:
                if i >= len(history[hashtag]):
                    print('list index out of range for ' + hashtag + ' at index ' + str(i))
                    sys.exit()
                else:
                    totals[hashtag] = history[hashtag][i] + totalsstart[hashtag] - offset[hashtag]
            addDB(datestring,  totals['#koibuINTL'], totals['#EzekieliiiINTL'],  totals['#CohhcarnageINTL'],
                    totals['#BajheeraINTL'], totals['#dmbrandonINTL'],  totals['#MYMALKAPONEINTL'])
            print('added totals for ' + datestring + 
                '\n koibu: ' + str(totals['#koibuINTL']) +
                '\n Ezekiel ' + str(totals['#EzekieliiiINTL']) +
                '\n Cohhcarnage ' + str(totals['#CohhcarnageINTL']) +
                '\n Bajheera ' + str(totals['#BajheeraINTL']) +
                '\n dmbrandon ' + str(totals['#dmbrandonINTL']) +
                '\n MYMalkapone ' + str(totals['#MYMALKAPONEINTL']))
