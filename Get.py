#!/usr/bin/env python

from __future__ import print_function
import sys, os
import requests
import config
import logging

## =============================================================================

log = logging.getLogger(__name__)

_headers = {'Content-Type' : 'application/json'
           ,'Accept' : 'application/json'
           ,'User-Agent' : config.userAgent
           }
_params = {'minutes': config.minutes
          ,'maxCount': config.maxCount
          ,'sessionId': config.AUTH_TOKEN
          }
                 
def getValues():
    try:
        _params['sessionId'] = config.AUTH_TOKEN

        resp = requests.post(config.getDataURL, headers=_headers, params=_params)
        resp.raise_for_status()

        return resp.json()
    except NameError:
        raise EnvironmentError('credentials not set up')
    except ValueError:
        raise EnvironmentError('error in response')
    except requests.exceptions.RequestException as e:
        log.error('error in http request %s', e)
        raise EnvironmentError('error in http request')

def test(event, context):
    auth = authenticate()
    print("auth key: ", auth)
    return auth

if __name__ == '__main__':
    sys.exit(test(None, None))

