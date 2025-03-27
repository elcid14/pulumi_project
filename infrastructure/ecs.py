import pulumi_aws as aws
import json

def create_ecs_cluster():
    # ECS Cluster
    cluster = aws.ecs.Cluster("celeryCluster")

    # Task Definition for Celery worker
    task_definition = aws.ecs.TaskDefinition("celeryTask",
        family="celeryWorkers",
        container_definitions=json.dumps([{
            "name": "celery",
            "image": "your-celery-image",
            "cpu": 512,
            "memory": 1024,
            "essential": True,
            "environment": [
                {"name": "SQS_QUEUE_URL", "value": "your_sqs_url"},
                # {"name": "REDIS_URL", "value": "your_redis_url"}
            ]
        }])
    )

    # ECS Service with auto-scaling
    service = aws.ecs.Service("celeryService",
        cluster=cluster.id,
        task_definition=task_definition.arn,
        desired_count=2,
    )

    return cluster
