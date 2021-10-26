''' This file can be used to create a SNS topic
'''

# Import boto3 library
import boto3
import constants

# Find  region of user
AWS_REGION = boto3.Session().region_name

# Choose SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)




def create_topic(name):
    '''
    Function create_topic(name)
    
    Description  : A function that can be used to create topic 
    
    Arguments    : name: str
                   The name of the SNS topic to be created
                    
    
    Return       : Returns a topic after creating it
    '''
    
    topic = sns_client.create_topic(Name=name)
    return topic
    

# Creating SNS 

# Choosing topic name
topic_name = constants.TOPIC_NAME

# Calling create topic function
topic = create_topic(topic_name)
