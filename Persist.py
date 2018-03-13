#!/usr/bin/env python

from __future__ import print_function
import sys
import logging

import boto3

import config

## =============================================================================
log = logging.getLogger(__name__)

res = boto3.resource('dynamodb', region_name=config.awsRegion)

table = res.Table(config.tableName)

# values need to be a collection of class w method 'dict'
def persist(values):
    #log.debug("writing new values")
    with table.batch_writer() as batch:
        for v in values:
            #log.debug("persist %s", str(v))
            batch.put_item(Item=v.dict())

def test():
    pass

if __name__ == '__main__':
    sys.exit(test())

