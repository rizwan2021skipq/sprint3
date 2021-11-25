'''File to Create DynamoDB Table'''

# Importing Libarires
import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import core
import boto3
import lambda_folder.constants as constants

# Selecting region
region=boto3.Session().region_name
client_dynamodb = boto3.client('dynamodb', region)


response = client_dynamodb.list_tables()
list_table=response['TableNames']
table_name=constants.TABLE_NAME


# Checking whether table already exists else we will create it
if  table_name in list_table:
    pass
    
else:

    table = client_dynamodb.create_table (
        TableName = constants.TABLE_NAME,
           KeySchema = [
               {
                   'AttributeName': 'Subject',
                   'KeyType': 'HASH'
               },
               {
                   'AttributeName': 'Message',
                   'KeyType': 'RANGE'
               }
               
               
               ],
               AttributeDefinitions = [
                   {
                       'AttributeName': 'Subject',
                       'AttributeType': 'S'
                   },
                   {
                       'AttributeName': 'Message',
                       'AttributeType': 'S'
                   },
                   
                   
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits':10,
                    'WriteCapacityUnits':10
                }
              
        )
