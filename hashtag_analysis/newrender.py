from twython import Twython
import time
import pygal
import ast
import os
import sys
import sqlite3

def createDates(count):
    i = 0
    days = ['Competition start', '01. August 00:00 UTC', '01. August 12:00 UTC', '01 August 20:00 UTC Graph 1.0 is online! \o/', 
                '02. August 00:00 UTC',  '02. August 12:00 UTC', 
                '03. August 00:00 UTC',  '03. August 12:00 UTC', 
                '04. August 00:00 UTC',  '04. August 12:00 UTC', 
                '05. August 00:00 UTC',  '05. August 12:00 UTC']
    dates=[]
    for j in range(0, count+1):
        if j == 0:
            dates.append(days[0]) #comp start
        elif j == 144:
            dates.append(days[1]) # 01 august 00
        elif j == 216:
            dates.append(days[2]) # 01 August 12
        #elif j == 2641:
            #dates.append(days[3]) # 01 August 20
        elif j == 288:
            dates.append(days[4]) # 02 august 00
        elif j == 360:
            dates.append(days[5]) # 02 august 00
        elif j == 432:
            dates.append(days[6]) # 02 august 00
        elif j == 504:
            dates.append(days[7]) # 02 august 00
        elif j == 576:
            dates.append(days[8]) # 02 august 00
        elif j == 648:
            dates.append(days[9]) # 02 august 00
        elif j == 720:
            dates.append(days[10]) # 02 august 00
        elif j == 792:
            dates.append(days[11]) # 02 august 00
        else:
            dates.append(' ')
    return dates


firstStart = 1

TWITTER_APP_KEY = '' #supply the appropriate value
TWITTER_APP_KEY_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

hashtags=['#koibuINTL', '#EzekieliiiINTL', '#CohhcarnageINTL',
                    '#BajheeraINTL',  '#dmbrandonINTL', '#MYMALKAPONEINTL']

history = {'#dmbrandonINTL':[], '#CohhcarnageINTL':[], '#BajheeraINTL':[], 
    '#koibuINTL':[], '#EzekieliiiINTL':[], '#MYMALKAPONEINTL':[]}

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))

for hashtag in hashtags:
    con= sqlite3.connect(installpath+'/totals.sql')
    c = con.cursor()
    #print('''SELECT ''' + hashtag + ''' FROM totals''')
    c.execute('''SELECT ''' + hashtag[1:] + ''' FROM totals''')
    c.fetchall
    for row in c:
        history[hashtag].append(row[0])
    con.close()
print 'SQLite read'

total = {'#koibuINTL':history['#koibuINTL'][-1], '#EzekieliiiINTL':history['#EzekieliiiINTL'][-1], '#CohhcarnageINTL':history['#CohhcarnageINTL'][-1],
                    '#BajheeraINTL':history['#BajheeraINTL'][-1], '#dmbrandonINTL':history['#dmbrandonINTL'][-1],  '#MYMALKAPONEINTL':history['#MYMALKAPONEINTL'][-1]}

countedID = {'#koibuINTL':[], '#EzekieliiiINTL':[], '#CohhcarnageINTL':[],
                    '#BajheeraINTL':[], '#dmbrandonINTL':[],  '#MYMALKAPONEINTL':[]}

while True:
    chart = pygal.Line(
       x_labels_major_every = 48,
       show_only_major_dots = True,
       dots_size = 0.8,
       tooltip_font_size = 20, 
       )
    for hashtag in hashtags:
        try:
            search = t.search(q = hashtag,  count = 100, result_type = 'recent')
            tweets = search['statuses']
            for tweet in tweets:
                if not any(tweet['id_str'] in s for s in countedID[hashtag]):
                    if firstStart == 0:
                        total[hashtag] += 1
                    countedID[hashtag].append(tweet['id_str'])
            history[hashtag].append(total[hashtag])
            chart.add(hashtag, history[hashtag])
            time.sleep(7.5)
        except:
            pass
        renderlist = history[hashtag][0::10]
        chart.add(hashtag, renderlist)
    firstStart = 0
    count = len(renderlist)
    chart.x_labels = createDates(count)
    chart.x_label_rotation = 45
    chart.render_to_file('./media/uploads/tweets.svg')
    #chart.render_to_file('./tweets.svg')
    print 'rendered\n'
    with open('koibubackup', 'w') as f:
        f.write(str(history))
    sys.exit()
