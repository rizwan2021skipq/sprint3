''' This file can be used to subscribe to a SNS topic'''

# Import boto3 library
import boto3
import constants
# Find region of user
AWS_REGION = boto3.Session().region_name
# Choose SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)


def subscribe(topic_arn, protocol, endpoint):
    '''
    Function subscribe(topic, protocol, endpoint)
    
    Description  : A function that can be used to create topic 
    
    Arguments    : topic: str
                   The ARN of topic to subscribe to
                   protocol: str 
                   The protocol of communication, in our case we choose it to be email
                   endpoint: str
                   The email address which needs to be subscribed
                    
    
    Return       : type: str
                   Returns subscription ARN
    '''

    
    subscription = sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol=protocol,
    Endpoint=endpoint,
    ReturnSubscriptionArn=True)['SubscriptionArn']
    return subscription


# ===============================Main code=============================================

# ARN of topic to which the email needs to be subscribed
topic_arn = constants.TOPIC_ARN
# Defining protocol of communication
protocol = 'LAMBDA'
#protocol = 'email'
# Email address
endpoint = 'arn:aws:lambda:us-east-2:315997497220:function:InfraStackRizwan-loggerlambda7BA3B318-XCPO1vGRhJD4'

# Calling the function
response = subscribe(topic_arn, protocol, endpoint)
