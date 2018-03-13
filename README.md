# Sugar

AWS lambda function to query Dexcom servers, download blood glucose values, and save data away in AWS DynamoDB.

Load should be low enough (for a single user) to keep usage within non-expiring Free Tier limits (see https://aws.amazon.com/free/)

### Prerequisites

- Dexcom share account
  * account username for Share account
  * password from Share account
- AWS account.
- Configuration for AWS lambda.
- Configuration for AWS DynamoDB.
- (Optionally) Configuration for AWS CloudWatch.

## Background

The [Dexcom Share](https://www.dexcom.com/get-started-cgm) [Continuous Glucode Monitor](https://en.wikipedia.org/wiki/Continuous_glucose_monitor) (CGM) samples blood glucose at five minute intervals, forwards them to an iPhone or Android device, then mirrors the values to a Dexcom cloud account.

This AWS lambda function authenticates to the Dexcom server and dowloades the latest values on the same 5 minute cycle. These values are stored in an AWS dynamoDB table.



### Installing

This infrastructure is set up on the us-east-1 region, primarily because it supports [SMS messaging](https://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html).


1. Create DynamoDB [table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#):
     * Table name *sugar*
     * Primary key *day* type *Number*
     * Select *Add sort key*
     * Sort key *system_time* type *Number*
     * Select "Create" (leaving default settings").
2. Create an AWS [IAM Role](https://console.aws.amazon.com/iam/home#/roles) allowing **AmazonDynamoDBFullAccess** and **CloudWatchLogsFullAccess**. Name this role **SugarRole**
   - *Note: it is possible (and probably good practice) to limit the AmazonDynamoDBFullAccess policy to solely the *sugar* table created in step 1.*
3. Create an AWS [lambda function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/create)
 - Author from scratch.
 - Name: *sugar*
 - Runtime: *Python 2.7*
 - Role: *Choose an existing role*
 - Existing role: *sugarRole*
2. Configure function
   1. In **Designer** pane, add "CloudWatch Events", then configure:
      * Rule: Create a new rule
      * Rule name: Every5Minutes
      * Rule description: Trigger every 5 minutes
      * Schedule: cron(0/5 * ? * * *)
   2. Click "sugar" within the Designer pane.
   3. From GitHub, download [lambda package](https://github.com/michael-stricklin/sugar/releases/download/v1.0.0/sugar.zip).
   4. Within the **Function code** pane:
      * Code entry type: Upload a .ZIP file
      * Runtime: Python 2.7
      * Handler: scrape.handler
      * Function package: select "Upload", then navigate to the zip-file downloaded in 2iii (sugar.zip).
   5. In **Environment variables** pane:
      * Add an environment variable "ACCOUNT" with a value of your Dexcom account username.
      * Add an environment variable "PASS" with a value of your Dexcom account password.
   6. In **Basic settings** pane:
      * Increase timeout to *5 sec*. 3 seconds is likely enough, but the handler is wating for web responses from Dexcom, so it's better to be patient.
   7. (Optional) Edit the file *config.py* within **Edit code inline**, and change *timezone* to an appropriate value. Possible values can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List), in the *TZ* column.
   8. Click "Save" (upper-right corner)
3. Incoming values may be browsed in [Dynamo console](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=sugar)
4. Execution logs may be viewed in [CloudWatch](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=/aws/lambda/sugar;streamFilter=typeLogStreamPrefix)
   

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
