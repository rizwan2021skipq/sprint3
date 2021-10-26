
import boto3
region=boto3.Session().region_name
print(region)
#dynamodb = boto3.resource('dynamodb', region)
#table=dynamodb.Table('NEWS')

'''
table = dynamodb.create_table (
    TableName = 'NEWS',
       KeySchema = [
           {
               'AttributeName': 'Name',
               'KeyType': 'HASH'
           },
           {
               'AttributeName': 'Email',
               'KeyType': 'RANGE'
           }
           ],
           AttributeDefinitions = [
               {
                   'AttributeName': 'Name',
                   'AttributeType': 'S'
               },
               {
                   'AttributeName':'Email',
                   'AttributeType': 'S'
               }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }
          
    )
'''    
'''
response = table.put_item(
Item = { 
     'Name': 'Kelvin Gala',
     'Email': 'kelvingalabuzi@handson.cloud'
       }
)
'''
#print(response)
