#!/usr/bin/env python

from collections import defaultdict

## =============================================================================

AUTH_TOKEN = None
awsRegion='us-east-1'
tableName='sugar'
timezone = 'America/Chicago'

authenticateURL = 'https://share1.dexcom.com/ShareWebServices/Services/General/LoginPublisherAccountByName'
userAgent = 'Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0'
applicationID = 'd8665ade-9673-4e27-9ff6-92db4ce13d13'

getDataURL = 'https://share1.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues'
minutes=1440 # 24 hours
maxCount=144 # 12 hours at every 5 minutes

trend_text=defaultdict(lambda: '<missing>',
                      {0: '-',
                       1: '2xUp',
                       2: 'Up',
                       3: 'Angle up',
                       4: 'Flat',
                       5: 'Angle down',
                       6: 'Down',
                       7: '2xDown',
                       8: 'No trend',
                       9: 'unavailable'})


from Rules import *

rules = [
        Rule('nominal').recentData(minute=10, second=10)
                    .between(100, 200)
                    .dampen(minute=30)
                    .log(),
        Rule('Low').recentData(minute=10, second=10)
                    .below(90)
                    .dampen(minute=30)
                    .log(),
        Rule('High').recentData(minute=10, second=10)
                    .above(200)
                    .dampen(minute=30)
                    .log(),
        Rule('Heading low-fast').recentData(minute=10, second=10)
                    .between(80, 150)
                    .trend('2xDown')
                    .dampen(minute=30)
                    .log(),
        Rule('Heading low').recentData(minute=10, second=10)
                    .between(80, 130)
                    .trend('Down')
                    .dampen(minute=30)
                    .log(),
        Rule('Heading high').recentData(minute=10, second=10)
                    .between(150, 200)
                    .trend('Up')
                    .dampen(minute=30)
                    .log(),
        Rule('Heading high-fast').recentData(minute=10, second=10)
                    .between(150, 200)
                    .trend('2xUp')
                    .dampen(minute=30)
                    .log(),
        ]

