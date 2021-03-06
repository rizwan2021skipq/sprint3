''' This file is used to create a topic and subscribe to it'''

import boto3
import lambda_folder.constants as constants
from botocore.exceptions import ClientError

#topic_arn='arn:aws:sns:us-east-2:315997497220:alarms_testing'
topic_name=constants.TOPIC_NAME
my_topic_arn=constants.TOPIC_ARN

# Find  region of user
AWS_REGION = boto3.Session().region_name
# Choose SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)
response_sns = sns_client.list_topics()  

list_topics_arn=[] 
for each_reg in response_sns['Topics']:     
    list_topics_arn.append(each_reg['TopicArn'])


# If topic already exists then do nothing, else create it and subscribe  to it
if my_topic_arn in list_topics_arn:
    pass
else:
    topic=sns_client.create_topic(Name=topic_name)
    topic_arn=topic['TopicArn']
    
    # Subscription of email
    email_subs_arn=sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=constants.EMAIL,
        
        ReturnSubscriptionArn=True
    )
    
    # Subscription of lambda function
    lambda_subs_arn=sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='LAMBDA',
        Endpoint=constants.LAMBDA_ARN,
        
        ReturnSubscriptionArn=True
    )



