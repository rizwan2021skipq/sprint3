from __future__ import print_function

import boto3
import json

print('Loading function')


def handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    mod_event=json.loads(event['body'])
    operation=mod_event['operation']
    #operation = event['operation']
    table_name=mod_event['tableName']

    #if 'tableName' in event:
    dynamo = boto3.resource('dynamodb').Table(table_name)

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'read': lambda x: dynamo.get_item(**x),
        'update': lambda x: dynamo.update_item(**x),
        'delete': lambda x: dynamo.delete_item(**x),
        'list': lambda x: dynamo.scan(**x),
        'echo': lambda x: x,
        'ping': lambda x: 'pong'
    }

    if operation in operations:
        
        response=operations[operation](mod_event.get('payload'))
        return {'statusCode':200, "body": json.dumps(response), 'headers': { 'Content-Type': 'application/json' }}
        
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))