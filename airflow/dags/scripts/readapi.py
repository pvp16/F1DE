import requests
import csv
from flatten_json import flatten
import time

def readf1():
    f = csv.writer(open("/opt/airflow/data/f1results.csv","a",newline=''))
    f.writerow(['season','round','raceName','circuitId','circuitName','latitude','longitude','locality','country','date','driverNumber','position','positionText','points',
    'driverId','permanentNumber','code','givenName','familyName','dateOfBirth','driverNationality','constructorId','constructorName','constructorNationality','grid','laps','status',
    'millis','raceTime','fastestLapRank', 'fastestLap', 'fastestLapTime', 'units','averageSpeed'])


    offs = 0
    while True:
        res = requests.get(f"http://ergast.com/api/f1/results.json?limit=1000&offset={offs}").json() 
        num = int(res['MRData']['total'])
        if num<offs:
            print("I'm done")
            break

        for x in res['MRData']['RaceTable']['Races']:
            for y in x['Results']:
                
                f.writerow([x['season'],x['round'],x['raceName'], 
                x['Circuit']['circuitId'],x['Circuit']['circuitName'],x['Circuit']['Location']['lat'],x['Circuit']['Location']['long'],x['Circuit']['Location']['locality'],x['Circuit']['Location']['country'],x['date'],
                y['number'], y['position'],y['positionText'], y['points'], 
                y['Driver']['driverId'],y['Driver'].get('permanentNumber'),y['Driver'].get('code'),y['Driver']['givenName'],y['Driver']['familyName'],y['Driver']['dateOfBirth'],y['Driver']['nationality'],
                y['Constructor']['constructorId'],y['Constructor']['name'],y['Constructor']['nationality'],y['grid'],y['laps'],y['status'],y.get('Time',{}).get('millis'),y.get('Time',{}).get('time')
                ,y.get('FastestLap',{}).get('rank'),y.get('FastestLap',{}).get('lap'),y.get('FastestLap',{}).get('Time',{}).get('time')
                ,y.get('FastestLap',{}).get('AverageSpeed',{}).get('units'),y.get('FastestLap',{}).get('AverageSpeed',{}).get('speed')])
        offs = offs + 1000
        time.sleep(1)