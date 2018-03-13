#!/usr/bin/env python

from __future__ import print_function
import sys
import time
from datetime import datetime
import json
import re
import pytz

import config

## =============================================================================
"""
"DT": "\/Date(1495330624000-0700)\/"
"ST": "\/Date(1495334145000)\/"
"WT": "\/Date(1495323472000)\/"
"Trend": 8
"Value": 254

"TS": 1519269373
"system_time": 1519264874
"trend_text": "angle up"
"timestring": "2018-02-21 20:01:14 CST"
"day": 20180221

"""

## =============================================================================
timezone = pytz.timezone(config.timezone)

class Data(object):
    def __init__(self, DT, ST, WT, Trend, Value, *args, **kwargs):
        self.DT = DT
        self.ST = ST
        self.WT = WT
        self.Trend = Trend
        self.Value = Value
        self.trend_text = config.trend_text[Trend]
        self.system_time = parseASPDate(ST)
        self.TS = int(time.time())
        dt = datetime.fromtimestamp(self.system_time, tz=timezone)
        self.timestring = dt.strftime("%Y-%m-%d %X %Z")
        self.day = int(dt.strftime("%Y%m%d"))
    def timestamp(self):
        return self.system_time
    def msg(self):
        return '{} {}'.format(self.Value, self.trend_text)
    def trend():
        return self.trend_text
    @classmethod
    def fromDict(cls, d):
        return cls(**d)
    def cleanKeys(self):
        d = self.__dict__.copy()
        return d
    def value(self):
        return self.Value
    def toJson(self):
        return json.dumps(self.cleanKeys())
    def __str__(self):
        return self.toJson()
    def __lt__(self, other):
        return self.system_time < other.system_time
    def dict(self):
        return self.cleanKeys()




def parseASPDate(datestring):
    # example: "\/Date(1495330624000-0700)\/"
    timepart = datestring.split('(')[1].split(')')[0] # peel out between parens
    timepart = re.split(r'\D', timepart) # \D is *not* digit
    try:
        millis = int(timepart[0])
        tz = int(timepart[1])
    except IndexError:
        tz = 0
    adjustedseconds = millis / 1000 + tz * 36 # 36 = 60*60/100
    return adjustedseconds

def cleanRepr(value):
    return Data.fromDict(value)


## =============================================================================



def test():
    jsonStr = """[{"DT":"\/Date(1495333623000-0700)\/",
                "ST":"\/Date(1495337144000)\/",
    "Trend":8,
    "Value":245,
                "WT":"\/Date(1495326471000)\/"}]"""

    data = json.loads(jsonStr)
    for d in cleanRepr(data):
        print(d)

if __name__ == '__main__':
    sys.exit(test())


