import pulumi_aws as aws
import pulumi
import json

def create_ecs_cluster():
    # ECS Cluster
    cluster = aws.ecs.Cluster("celeryCluster")
    # Import SQS and Redis outputs
    sqs_queue_url = pulumi.Output.from_input(pulumi.export("sqs_queue_url"))
    redis_cluster = pulumi.Output.from_input(pulumi.export("redis_endpoint"))
    redis_endpoint = redis_cluster.cache_nodes.apply(lambda nodes: nodes[0]["address"])
    rds_endpoint = pulumi.Output.from_input(pulumi.export("rds_endpoint"))

    # Task Definition for Celery worker
    task_definition = aws.ecs.TaskDefinition(
        "celeryTask",
        family="celeryWorkers",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        cpu="512",
        memory="1024",
        execution_role_arn="arn:aws:iam::your-account-id:role/ecsTaskExecutionRole",
        container_definitions=pulumi.Output.all(sqs_queue_url, redis_endpoint, rds_endpoint).apply(lambda args: json.dumps([
            {
                "name": "celery",
                "image": "",
                "cpu": 512,
                "memory": 1024,
                "essential": True,
                "command": ["celery", "-A", "tasks", "worker", "--loglevel=info"],
                "environment": [
                    {"name": "SQS_QUEUE_URL", "value": args[0]},
                    {"name": "REDIS_URL", "value": f"redis://{args[1]}:6379/0"},
                    {"name": "DATABASE_URL", "value":args[2]}
                ]
            }
        ]))
    )

    # Fargate service
    fargate_service = aws.ecs.Service("celeryService",
        cluster=cluster.id,
        task_definition=task_definition.arn,
        desired_count=2,
        launch_type="FARGATE"
    )

    return cluster
