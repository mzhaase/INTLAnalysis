from twython import Twython
import time
import pygal
import ast

def createDates(count):
    i = 0
    days = ['02. August 00:00 UTC', '03. August 00:00 UTC', '04. August 00:00 UTC', '05. August 00:00 UTC']
    dates=[]
    for j in range(0, count+1):
        if j == 6*60:
            dates.append('01.August 12:00 UTC')
        elif j >= 12*60:
            if not count%1440: #if the day is 24*60 searches (1day)
                dates.append(days[i])
                i += 1
            else:
                dates.append(' ')
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

countedID=[]

with open('koibubackup', 'r') as r:
    for line in r:
        history = ast.literal_eval(line)

hashtags=['#koibuINTL', '#EzekieliiiINTL', '#CohhcarnageINTL',
                    '#BajheeraINTL',  '#dmbrandonINTL', '#MYMALKAPONEINTL']

total = {'#koibuINTL':history['#koibuINTL'][-1], '#EzekieliiiINTL':history['#EzekieliiiINTL'][-1], '#CohhcarnageINTL':history['#CohhcarnageINTL'][-1],
                    '#BajheeraINTL':history['#BajheeraINTL'][-1], '#dmbrandonINTL':history['#dmbrandonINTL'][-1],  '#MYMALKAPONEINTL':history['#MYMALKAPONEINTL'][-1]}

#history = {'#koibuINTL':[], '#EzekieliiiINTL':[], '#CohhcarnageINTL':[],
                    #'#BajheeraINTL':[], '#dmbrandonINTL':[],  '#MYMALKAPONEINTL':[]}

countedID = {'#koibuINTL':[], '#EzekieliiiINTL':[], '#CohhcarnageINTL':[],
                    '#BajheeraINTL':[], '#dmbrandonINTL':[],  '#MYMALKAPONEINTL':[]}

while True:
    chart = pygal.Line(
       x_labels_major_every = 60,
       show_only_major_dots = True,
       dots_size = 0.8,
       tooltip_font_size = 20)
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
    firstStart = 0
    count = len(history['#koibuINTL'])
    chart.x_labels = createDates(count)
    chart.x_label_rotation = 45
    #chart.render_to_file('./media/uploads/tweets.svg')
    chart.render_to_file('tweets.svg')
    print 'rendered\n'
    with open('koibubackup', 'w') as f:
        f.write(str(history))
