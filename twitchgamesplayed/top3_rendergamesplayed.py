import httplib
import time
import json
import os
import sys

import sqlite3
import pygal

installpath = os.path.abspath(os.path.dirname(sys.argv[0]))
streamers = ('cohhcarnage', 'ezekiel_iii', 'koibu')
totalLastGamePlayed = {'cohhcarnage':'', 'ezekiel_iii':'','koibu':''}
gamesPlayedAlready = {'cohhcarnage':36, 'ezekiel_iii':33,'koibu':47}

def readDB(streamer):
    gamelist = []
    con = sqlite3.connect(installpath + '/twitch_gamesplayed.sql')
    c = con.cursor()
    statement = 'SELECT game FROM ' + streamer + ' WHERE total >= 3600'
    c.execute(statement)
    results = c.fetchall()
    total = int(gamesPlayedAlready[streamer])
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
        title = 'number of games played by madmaxx @madplaysHD'
        )
    for streamer in streamers:
        total = readDB(streamer)
        chart.add(streamer,  int(total))
        totalLastGamePlayed[streamer] = lastTotal(streamer)
    chart.x_title = 'Total time played for most recent game: \n' + totalLastGamePlayed['koibu'] + ' koibu\n' + totalLastGamePlayed['cohhcarnage'] + ' cohhcarnage\n' +  totalLastGamePlayed['ezekiel_iii'] + ' ezekiel_iii\n'
    chart.render_to_file('./INTL_gamesplayed_top3.svg')
    print('rendered top 3,  timestamp: ' + str(time.time()))
    time.sleep(60)
