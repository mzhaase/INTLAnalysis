import time
import os
import sys
import json
import httplib

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ['cohhcarnage', 'ezekiel_iii', 'dmbrandon',  'mym_alkapone',  'koibu']
client_ID = ''
interval = 10
     

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
    
def checkUserDB(streamer,  onlineSince):
    con = sqlite3.connect(installpath+'/twitch_retention.sql')
    c = con.cursor()
    
    scon = sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    sc = scon.cursor()
    sc.execute("SELECT * FROM " + streamer + "Session")
    sresult = c.fetchall()
    
    total = 0
    i = 1.
    
    if sresult:
        for line in sresult:
            c.execute("SELECT duration FROM " + streamer + " WHERE joinTime >= " + line[0] + " AND join time <= " + line[1])
            result = c.fetchall()
            if result:
                for line in result:
                    if line[0] == 'NaN':
                        total += time.time() - float(onlineSince)
                    else:
                        total += float(line[0])
                    i += 1
                scon.close()
            else:
                scon.close()
                    
    c.execute("SELECT duration FROM " + streamer + " WHERE joinTime >= " + onlineSince + " OR leaveTime = 'NaN'")
    result = c.fetchall()
    print 'fetchall'
    if not result:
        con.close()
        return False
    else:
        for line in result:
            if line[0] == 'NaN':
                total += time.time() - float(onlineSince)
            else:
                total += float(line[0])
            i += 1
        average = total / i
        average = int(average/60)
    con.close()
    if not average:
        return 0
    else:
        return average
    
def checkResultDB(streamer):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()    
    c.execute("SELECT total FROM " + streamer + " ORDER BY date")
    results = c.fetchall()
    con.close()
    resultList = []
    if not results:
        return [30, 30, 30, 30]
    else:
        for result in results:
            resultList.append(result[0])
        return resultList
        
def checkMaxResult(streamer):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    c.execute("SELECT MAX(total) FROM " + streamer)
    result = c.fetchone()
    result = result[0]
    con.close()
    if not result:
        return 1
    else:
        return result

def getTimespan():
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
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
    if dataPointLabelInterval == 0:
        dataPointLabelInterval = 1
    result = []
    j = 0
    for i in range(0, datapoints):
        if not i%dataPointLabelInterval:
            dateEpoch= minDate + timeInterval * j
            j += 1
            date = time.strftime("%d. %b %H:%M UTC",  time.gmtime(dateEpoch))
            result.append(date)
        else:
            result.append(' ')
    if result:
        return result
    
        
def addToResults(streamer,  total,  online):
    con = sqlite3.connect(installpath+'/twitch_retention_results_nosquat.sql')
    c = con.cursor()
    insertlist = [time.time(),  int(total),  online]
    c.execute('''
        INSERT INTO ''' + streamer + ''' VALUES
        ( 
            ?,
            ?,
            ?
        )''', insertlist)
    con.commit()
    con.close()
    
def streamOnline(streamer):
    con = sqlite3.connect(installpath+'/twitch_retention_streamtimes.sql')
    c = con.cursor()
    c.execute("SELECT online FROM " + streamer + " WHERE date = (SELECT MAX(DATE) FROM " + streamer + ")")
    status = c.fetchone()
    status = status[0]
    c.execute("SELECT onlineSince FROM " + streamer + " WHERE date = (SELECT MAX(DATE) FROM " + streamer + ")")
    onlineSince = c.fetchone()
    onlineSince = onlineSince[0]
    con.close()
    return({'status':status,  'onlineSince':onlineSince})

    
while 1:
    try:
        startTime = time.time()
        numberOfDataPoints = 0
        chart = pygal.Line(
           dots_size = 0.8,
           tooltip_font_size = 20, 
           show_only_major_dots = True,
           title = 'Overview for INTL retention challenge, only counting when stream is online by madmaxx @madplaysHD', 
           y_title = 'Total average viewer retention time [min]'
           )
        for streamer in streamers:
            if streamOnline(streamer)['status'] == 1: #if stream is online
                total = checkUserDB(streamer,  streamOnline(streamer)['onlineSince'])
                addToResults(streamer,  total,  1)
            else: #if stream is offline
                addToResults(streamer,  checkMaxResult(streamer),  0)
            results = checkResultDB(streamer)
            chart.add(streamer,  results)
            numberOfDataPoints = len(results)
        chart.x_labels_major_every = int(numberOfDataPoints/interval)
        chart.x_labels = generateDates(getTimespan(),  numberOfDataPoints)
        chart.x_label_rotation = 45
        chart.render_to_file('./retention_noleave.svg')
        print 'rendered'
        runTime = time.time() - startTime
        print ('runtime: ' + str(runTime) + ' sleeping for ' + str(360-runTime))
        if (360- runTime) > 0:
            time.sleep(360-runTime)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'exception! \n', sys.exc_info()[0]
        pass
