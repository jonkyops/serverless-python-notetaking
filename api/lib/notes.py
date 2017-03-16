import datetime
import json
import uuid
import boto3
from lib.build_response import success
from lib.build_response import failure

DYNAMODB = boto3.client('dynamodb')

def create_note(event, context):
    # Request body is passed in as a JSON encoded string in 'event.body'
    data = json.loads(event['body'])
    parameter = {
        # - 'userId': because users are authenticated via Cognito User Pool, we
        #       will use the User Pool sub (a UUID) of the authenticated user
        # - 'noteId': a unique uuid
        # - 'content': parsed from request body
        # - 'attachment': parsed from request body
        # - 'createdAt': current Unix timestamp
        'TableName': 'notes',
        'Item': {
            'userId': {'S': str(event['requestContext']
                                ['authorizer']
                                ['claims']
                                ['sub'])},
            'noteId': {'S': str(uuid.uuid1())},
            'content': {'S': str(data['content'])},
            'attachment': {'S': str(data['attachment'])},
            'createdAt': {'S': str(datetime.datetime.now())}
        }
    }

    try:
        DYNAMODB.put_item(**parameter)
        body = parameter['Item']
        return success(body)
    except:
        return failure(body)

def read_note(event, context):
    parameter = {
        'TableName': 'notes',
        'Key': {
            'userId': {'S': str(event['requestContext']
                                ['authorizer']
                                ['claims']
                                ['sub'])},
            'noteId': {'S': str(event['pathParameters']['id'])}
        }
    }

    try:
        result = DYNAMODB.get_item(**parameter)
        if result['Item']:
            return success(result['Item'])
        else:
            return failure({'status':False, 'error': 'Item not found'})
    except:
        return failure({'status':False, 'result': str(result)})

def read_all(event, context):
    parameter = {
        'TableName': 'notes',
        'KeyConditionExpression': 'userId = :userId',
        'ExpressionAttributeValues': {
            ':userId': {'S': str(event['requestContext']
                                 ['authorizer']
                                 ['claims']
                                 ['sub'])},
        }
    }

    try:
        result = DYNAMODB.query(**parameter)
        if result['Items']:
            return success(result['Items'])
        else:
            return failure({'status':False, 'error': 'Items not found'})
    except:
        return failure({'status':False, 'result': str(result)})

def update_note(event, context):
    data = json.loads(event['body'])
    parameter = {
        'TableName': 'notes',
        'Key': {
            'userId': {'S': str(event['requestContext']
                                ['authorizer']
                                ['claims']
                                ['sub'])},
            'noteId': {'S': str(event['pathParameters']['id'])}
        },
        'UpdateExpression': 'SET content = :content, attachment = :attachment',
        'ExpressionAttributeValues': {
            ':attachment': {'S': str(data['attachment'])} if data['attachment'] else None,
            ':content':{'S': str(data['content'])} if data['content'] else None
        },
        'ReturnValues': 'ALL_NEW'
    }

    try:
        DYNAMODB.update_item(**parameter)
        return success({'status':True})
    except:
        return failure({'status':False})

def delete_note(event, context):
    parameter = {
        'TableName': 'notes',
        'Key': {
            'userId': {'S': str(event['requestContext']
                                ['authorizer']
                                ['claims']
                                ['sub'])},
            'noteId': {'S': str(event['pathParameters']['id'])}
        }
    }

    try:
        DYNAMODB.delete_item(**parameter)
        return success({'status':True})
    except:
        return failure({'status':False})
