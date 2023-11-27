import json
import boto3
import logging

# Initialize logging
logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('test-schedule')  # Replace with your table name

    try:
        # Parse the JSON body from the event
        body = json.loads(event['body'])
        #logger.info(f"Received body: {body}")

        # Extract the primary key (e.g., 'id') from the body
        item_id = body['id']

        # Construct UpdateExpression and ExpressionAttributeValues
        update_expression = 'SET '
        expression_attribute_values = {}

        for key, value in body.items():
            if key != 'id':  # Skip the primary key
                update_expression += f"#{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value

        # Remove trailing comma and space
        update_expression = update_expression.rstrip(', ')

        # Log the update expression and values
        #logger.info(f"UpdateExpression: {update_expression}")
        #logger.info(f"ExpressionAttributeValues: {expression_attribute_values}")

        # Update item in DynamoDB
        response = table.update_item(
            Key={
                'id': item_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames={f"#{k}": k for k in body if k != 'id'},
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        #logger.info(f"Update response: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('Update successful')
        }

    except Exception as e:
        #logger.error(f"Error updating DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
