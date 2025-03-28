"""An AWS Python Pulumi program"""

import pulumi # type: ignore
from pulumi_aws import s3 # type: ignore
from redis import create_redis
from sqs import create_sqs_queue
from apigateway import create_api_gateway
# from ecs import create_ecs_cluster
from monitoring import setup_cloudwatch
from rds import create_rds_postgresql
from lambdafunction import create_shipment_lambda
from dotenv import load_dotenv

# load dotenv
load_dotenv()

# Create an AWS resources
redis_instance = create_redis()
sqs_queue = create_sqs_queue()
lambda_function_create_shipment = create_shipment_lambda(sqs_queue)
api_gateway = create_api_gateway(lambda_function_create_shipment)
# ecs_cluster = create_ecs_cluster()
# rds_instance = create_rds_postgresql()


# instantiate cloudwatch
setup_cloudwatch()

# Define exports
pulumi.export("sqs_url", sqs_queue.url)
pulumi.export("create_shipment_lambda", lambda_function_create_shipment)
# pulumi.export("rds_endpoint", rds_instance.endpoint)
pulumi.export("api_gateway", api_gateway)
pulumi.export("redis_endpoint", redis_instance.cache_nodes[0]["address"])


