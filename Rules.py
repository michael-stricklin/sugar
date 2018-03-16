#!/usr/bin/env python

from __future__ import print_function
import sys
from time import time
import logging

import boto3

import config

log = logging.getLogger(__name__)

## =============================================================================
# utility
def _lastDatapoint(data):
    return sorted(data)[-1]
def _normalize_seconds(hour=0, minute=0, second=0):
    return (hour*60*60)+(minute*60)+second

## =============================================================================
class Rule(object):
    def __init__(self, msg):
        self.msg = msg
        self.rules = []
        self.actions = []
    def check(self, rule):
        self.rules.append(rule)
        return self
    def action(self, action):
        self.actions.append(action)
        return self
    def recentData(self, hour=0, minute=0, second=0):
        window = _normalize_seconds(hour, minute, second)
        self.rules.append(lambda data: _lastDatapoint(data).system_time+window >= int(time()))
        return self
    # true if last datapoint is between 'low' and 'high'
    def between(self, low, high):
        self.rules.append(lambda data: low <= _lastDatapoint(data).value <= high)
        return self
    # true if below 'high'
    def below(self, high):
        self.rules.append(lambda data: _lastDatapoint(data).value <= high)
        return self
    # true if above 'low'
    def above(self, low):
        self.rules.append(lambda data: _lastDatapoint(data).value >= low)
        return self
    def trend(self, trend_value):
        self.rules.append(lambda data: _lastDatapoint(data).trend == trend_value)
        return self
    def dampen(self, hour=0, minute=0, second=0):
        window = _normalize_seconds(hour, minute, second)
        class Test(object):
            def __init__(self):
                self.last_alert = 0
            def __call__(self, data):
                if (self.last_alert + window <= int(time())):
                    self.last_alert = int(time())
                    return True
                return False
        self.rules.append(Test())
        return self

    def noAction(self):
        self.actions.append(lambda: None)
        return self
    def log(self):
        self.actions.append(lambda msg: log.info("LogAction %s", msg))
        return self


    def __str__(self):
        return ' '.join(('Rule', self.msg))
    def test(self, data):
        if all(test(data) for test in self.rules):
            last = _lastDatapoint(data)
            [action(' '.join((self.msg, last.msg()))) for action in self.actions]

## =============================================================================

class SMSAction(object):
    sns = boto3.client('sns', region_name=config.awsRegion)

    #topic = sns.create_topic(Name='notifications')
    #topic_arn = topic['TopicArn']

    def __init__(self, phone_number):
        self.phone_number = phone_number
        #sns.subscribe(TopicArn=topic_arn, Protocol='sms', Endpoint=phone_number)
    def action(self, msg):
        #sns.publish(TopicArn=topic_arn, Message=msg)
        SMS.sns.publish(PhoneNumber=self.phone_number, Message=msg)



## =============================================================================
# have within window (RecentData)
# value between hi & low (InRange)
# trend is xxx (Trend)
# not triggered in past xxx (Dampen)
# then alert (Alert)


def main(argv=None):
    import json
    from Data import cleanRepr
    import sample_data

    r = Rule('sam').recentData(450).between(100, 300).trend('2xDown')
    values = set()
    data = json.loads(sample_data.jsonStr)
    values.update(cleanRepr(data))
    print(values)
    for d in values:
        print(d)
    r.test(values)


if __name__ == '__main__':
    sys.exit(main())


