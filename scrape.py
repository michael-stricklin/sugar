#!/usr/bin/env python

from __future__ import print_function
import os, sys
import logging

import config
from Authorize import authenticate
from Get import getValues
from Data import cleanRepr
from Persist import persist

## =============================================================================

Values = dict()
logging.root.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)


def handler(event, context):
    for retry in (1,2,3):
        try:
            if config.AUTH_TOKEN is None:
                config.AUTH_TOKEN = authenticate()
            log.debug("Values sz %d", len(Values))
            log.debug(' '.join(map(str, sorted(Values.keys()))))

            new_values = {v.timestamp(): v for v in map(cleanRepr, getValues())}
            for k in Values.keys():
                new_values.pop(k, None)

            log.debug('Values %s', sorted(Values.keys()))
            #log.debug('Values {}', ' '.join(map(sorted(Values.keys()))))
            log.debug('New values %s', new_values.keys())

            Values.update(new_values)
            persist(new_values.values())
            return True
        except EnvironmentError as e:
            config.AUTH_TOKEN = None
            log.error('Authentication error %s', e)
    log.error('Authentication retry failure %s', e)
    return False

def test(event, context):
    handler(event, context)
    return None


if __name__ == '__main__':
    sys.exit(test(None, None))


