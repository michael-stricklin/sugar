#!/usr/bin/env python

from __future__ import print_function

import sys, os
import json
import logging
from operator import attrgetter

import config
from boundedSet import BoundedSet
from unmarshal import unmarshal_dynamodb_json

logging.root.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)


#TODO: back-populate Values at first start-up from DB
Values = BoundedSet(maxlen=144, key=attrgetter('system_time'))

class DataPoint(object):
    def __init__(self, system_time=None, Value=None, trend_text=None, timestring=None, **kwargs):
        self.system_time = system_time
        self.value = Value
        self.trend_text = trend_text
        self.timestring = timestring
    def msg(self):
        return '{} {} {}'.format(self.value, self.trend_text, self.timestring)

def handler(event, context):
    for record in (r for r in event['Records'] if 'INSERT' == r['eventName']):
        if 'INSERT' == record['eventName']:
            dp = unmarshal_dynamodb_json(record['dynamodb']['NewImage'])
            dp = DataPoint(**dp)
            Values.add(dp)
        log.info('Values sz %d', len(Values))
        for r in config.rules:
            log.info("Try rule %s", r)
            r.test(Values)

    log.info("Successfully processed %d records.", len(event['Records']))
    return True

if __name__ == '__main__':
    sys.exit(handler(None, None))