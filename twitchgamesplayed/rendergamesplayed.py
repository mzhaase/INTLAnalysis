import httplib
import time
import json
import os
import sys

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ('cohhcarnage',  'dmbrandon',  'ezekiel_iii',  'mym_alkapone',  'koibu',  'thejustinflynn')
totalLastGamePlayed = {'cohhcarnage':'',  'dmbrandon':'',  'ezekiel_iii':'',  'mym_alkapone':'',  'koibu':'',  'thejustinflynn':''}

def readDB(streamer):
    gamelist = []
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = 'SELECT game FROM ' + streamer + ' WHERE total >= 3600'
    c.execute(statement)
    results = c.fetchall()
    total = 1
    if results:
        for entry in results:
            if not entry[0] in gamelist:
                gamelist.append(entry[0])
                total += 1
        con.close()
        return(total)
    else:
        con.close()
        return 1
    
def lastTotal(streamer):
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = ('SELECT total FROM ' + streamer + ' ORDER BY date DESC LIMIT 1')
    c.execute(statement)
    total = c.fetchone()
    if total:
        total = total[0]
        hours = int(total/3600)
        minutes = int((total - hours*3600)/60)
        seconds = int(total - hours*3600 - minutes*60)
        if hours < 10:
            hours = '0' + str(hours)
        if minutes < 10:
            minutes = '0' + str(minutes)
        if seconds <10:
            seconds = '0' + str(seconds)
        string = str(hours) + ':' + str(minutes) + ':' + str(seconds)
        con.close()
        return string
    else:
        con.close()
        return 'No last game'
        
while True:
    chart = pygal.HorizontalBar(
        x_labels_major_every = 1,
        show_only_major_dots = True,
        title = 'number of games played since 9. of August by madmaxx @madplaysHD'
        )
    for streamer in streamers:
        total = readDB(streamer)
        chart.add(streamer,  int(total))
        totalLastGamePlayed[streamer] = lastTotal(streamer)
    chart.x_title = 'Total time played for most recent game: \n' + totalLastGamePlayed['koibu'] + ' koibu\n' + totalLastGamePlayed['cohhcarnage'] + ' cohhcarnage\n' +  totalLastGamePlayed['dmbrandon'] + ' dmbrandon\n' + totalLastGamePlayed['ezekiel_iii'] + ' ezekiel_iii\n' + totalLastGamePlayed['mym_alkapone'] + ' mym_alkapone\n' + totalLastGamePlayed['thejustinflynn'] + ' thejustinflynn\n'
    chart.render_to_file('./INTL_gamesplayed.svg')
    print('rendered,  timestamp: ' + str(time.time()))
    time.sleep(60)
