import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def convert_dynamodb_item_to_dict(item):
    converted_item = {}
    for key, value in item.items():
        converted_item[key] = list(value.values())[0] if isinstance(value, dict) else value
    return converted_item

def dump_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items

def lambda_handler(event, context):
    table_name = "<dynamo_table>"  # Replace with your actual DynamoDB table name
    result = dump_table(table_name)
    return {
        'statusCode': 200,
        'body': json.dumps(result, cls=DecimalEncoder, indent=2)
    }
