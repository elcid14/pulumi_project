from celery import Celery
import os
import redis
import psycopg2
import boto3
import json

app = Celery("tasks",
    broker=os.getenv("SQS_QUEUE_URL"),
    backend=os.getenv("REDIS_URL")
)

# Redis Client
redis_client = redis.StrictRedis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

# PostgreSQL Connection
conn = psycopg2.connect(os.getenv("RDS_DB_URL"))
cursor = conn.cursor()

# SNS Client
sns_client = boto3.client("sns", region_name="us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

@app.task(bind=True)
def process_shipping_update(self, message):
    """Processes shipping update, stores in Redis, updates DB, triggers WebSocket and AppSync"""
    try:
        container_id = message["container_id"]
        status = message["status"]

        # Update PostgreSQL
        cursor.execute("UPDATE shipments SET status = %s WHERE container_id = %s", (status, container_id))
        conn.commit()

        # Store in Redis cache
        redis_client.set(container_id, status, ex=3600)

        # Send notification to SNS for AppSync Subscription
        sns_message = json.dumps({
            "container_id": container_id,
            "status": status
        })
        sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=sns_message)

        return f"Container {container_id} updated to {status}"
    except Exception as e:
        self.retry(exc=e)
