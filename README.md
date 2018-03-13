# Sugar

AWS lambda function to query Dexcom servers, download blood glucose values, and save data away in AWS DynamoDB.
Load should be low enough (for a single user) to keep usage within non-expiring Free Tier limits (see https://aws.amazon.com/free/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

AWS account.
Configuration for AWS lambda.
Configuration for AWS DynamoDB.
(Optionally) Configuration for AWS CloudWatch.


### Installing

## Built With
python 2.7
Requests v2.6.0 http://docs.python-requests.org/en/master/
pytz 2018.3 http://pytz.sourceforge.net/
urllib3 1.10 (requests dependency) https://pypi.python.org/pypi/urllib3/1.10