import time
import os
import sys

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ['cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu']
interval = 10

if not os.path.exists(installpath+'/twitch_retention_results.sql'):
    f = file(installpath+'/twitch_retention_results.sql',  'w')
    f.close()
    con= sqlite3.connect(installpath+'/twitch_retention_results.sql')
    c = con.cursor()
    for streamer in streamers:
        #Create tables
        c.execute('''CREATE TABLE ''' + streamer + ''' 
            (
                date text, 
                total integer
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
    con = sqlite3.connect(installpath+'/twitch_retention_results.sql')
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
    con = sqlite3.connect(installpath+'/twitch_retention_results.sql')
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
        
def generateDates(dates,  datapoints):
    minDate = float(dates['min'])
    maxDate = float(dates['max'])
    timePassed = maxDate - minDate
    timeInterval = timePassed / interval
    dataPointLabelInterval = int(datapoints / interval)
    result = []
    for i in range(0, datapoints):
        if not i%dataPointLabelInterval:
            dateEpoch= minDate + timeInterval*i
            date = time.strftime("%d. %b %H:%M UTC",  time.gmtime(dateEpoch))
            result.append(date)
        else:
            result.append(' ')
    if result:
        return result
    
        
def addToResults(streamer,  date,  total):
    con = sqlite3.connect(installpath+'/twitch_retention_results.sql')
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
    
while 1:
    try:
        startTime = time.time()
        numberOfDataPoints = 0
        chart = pygal.Line(
           dots_size = 0.8,
           tooltip_font_size = 20, 
           show_only_major_dots = True,
           title = 'Overview for INTL retention challenge by madmaxx @madplaysHD', 
           y_title = 'Total average viewer retention time [min]'
           )
        for streamer in streamers:
            addToResults(streamer,  time.time(),  checkUserDB(streamer))
            results = checkResultDB(streamer)
            chart.add(streamer,  results)
            numberOfDataPoints = len(results)
        chart.x_labels_major_every = int(numberOfDataPoints/interval)
        chart.x_labels = generateDates(getTimespan(),  numberOfDataPoints)
        chart.x_label_rotation = 45
        chart.render_to_file('./retention.svg')
        print 'rendered'
        runTime = time.time() - startTime
        print ('runtime: ' + str(runTime) + ' sleeping for ' + str(360-runTime))
        if (360- runTime) > 0:
            time.sleep(360-runTime)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'exception! \n', sys.exc_info()[0]
        raise
        pass    
