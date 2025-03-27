import json
import os
import boto3

sqs = boto3.client("sqs")
queue_url = os.environ["SQS_QUEUE_URL"]

def lambda_handler(event, context):
    body = json.loads(event["body"])

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(body)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Shipment req received", "messageId": response["MessageId"]})
    }
