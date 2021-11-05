import boto3
import lambda_folder.constants as constants
from botocore.exceptions import ClientError

#topic_arn='arn:aws:sns:us-east-2:315997497220:alarms_testing'
topic_name="automatednew"
'''
lambda_client = boto3.client('lambda')

response = lambda_client.list_functions(
    
    FunctionVersion='ALL',
   
    MaxItems=50
)
tot=response['Functions']
print(response['Functions'][0])
print(len(response['Functions']))
list_lambdas=[]
x=0
while x< len(tot):
    list_lambdas.append(tot[x]['Handler'])
print(list_lambdas)
'''
# Find  region of user
AWS_REGION = boto3.Session().region_name
# Choose SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)
response_sns = sns_client.list_topics()  

list_topics_arn=[] 
for each_reg in response_sns['Topics']:     
    list_topics_arn.append(each_reg['TopicArn'])

topic=sns_client.create_topic(Name=topic_name)
topic_arn=topic['TopicArn']
email_subs_arn=sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=constants.EMAIL,
    
    ReturnSubscriptionArn=True
)

lambda_subs_arn=sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='LAMBDA',
    Endpoint=constants.LAMBDA_ARN,
    
    ReturnSubscriptionArn=True
)



#subs=sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
#print("done")

#print(subs)
#print(subs['Subscriptions'][0]['SubscriptionArn'])


'''
topic_arn = client.get_topic_attributes(
    TopicArn='string'
)
   '''


'''
if topic_arn in list_topics_arn:
    pass

else:
'''    
    
#topic = sns_client.create_topic(Name=topic_name)

# Choosing topic name


# Calling create topic function
#topic = create_topic(topic_name)


