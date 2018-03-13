#!/usr/bin/env python

from __future__ import print_function
import os, sys
import logging

import config
## =============================================================================

Values = set()
logging.root.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)


def handler(event, context):
    for r in config.rules:
        log.info("Try rule %s", r)
        r.test(Values)
    return True

def test(event, context):
    handler(event, context)
    return None


if __name__ == '__main__':
    sys.exit(test(None, None))


