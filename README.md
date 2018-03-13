# Sugar

AWS lambda function to query Dexcom servers, download blood glucose values, and save data away in AWS DynamoDB.

Load should be low enough (for a single user) to keep usage within non-expiring Free Tier limits (see https://aws.amazon.com/free/)

### Prerequisites

- AWS account.
- Configuration for AWS lambda.
- Configuration for AWS DynamoDB.
- (Optionally) Configuration for AWS CloudWatch.

## Background

The [Dexcom Share](https://www.dexcom.com/get-started-cgm) [Continuous Glucode Monitor](https://en.wikipedia.org/wiki/Continuous_glucose_monitor) (CGM) samples blood glucose at five minute intervals, forwards them to an iPhone or Android device, then mirrors the values to a Dexcom cloud account.

This AWS lambda function authenticates to the Dexcom server and dowloades the latest values on the same 5 minute cycle. These values are stored in an AWS dynamoDB table.



### Installing

This infrastructure is set up on the us-east-1 region, primarily because it supports [SMS messaging](https://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html).


1. Create an AWS [lambda function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/create)
 - Author from scratch.
 - Name: sugar
 - Runtime: Python 2.7
 - Role: Create a custom role
2. Configure function
 a In Designer, add "CloudWatch Events", then configure:
      * Rule: Create a new rule
      * Rule name: Every5Minutes
      * Rule description: Trigger every 5 minutes
      * Schedule: cron(0/5 * ? * * *)
 b Click "Save" (upper-right corner)
 c Click "sugar" within the Designer pane.
 d Package code: run "make" within source directory. This will create a deployable zip file "sugar.zip"
 e Within the Function code pane:
      * Code entry type: Upload a .ZIP file
      * Runtime: Python 2.7
      * Handler: scrape.handler
      * Function package: select "Upload", then navigate to the zip-file created in 2d.

## Built With
- python 2.7
- [Requests v2.6.0](http://docs.python-requests.org/en/master/)
- [pytz 2018.3](http://pytz.sourceforge.net/)
- [urllib3 1.10](https://pypi.python.org/pypi/urllib3/1.10) (requests dependency)


## Acknowledgments

[Nightscout bridge](https://github.com/nightscout) project, which provides roughly the same functionality to a Mongo database.
[Scott Hanselman](http://www.hanselman.com/blog/BridgingDexcomShareCGMReceiversAndNightscout.aspx), who reverse engineered the Dex REST API.

## TODO

Integrate as a subproject of NightScout.
