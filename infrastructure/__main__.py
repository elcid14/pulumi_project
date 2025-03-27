"""An AWS Python Pulumi program"""

import pulumi # type: ignore
from pulumi_aws import s3 # type: ignore
from redis import create_redis
from sqs import create_sqs_queue
from ecs import create_ecs_cluster
from monitoring import setup_cloudwatch
from rds import create_rds_postgresql

# Create an AWS resource 
bucket = s3.BucketV2('my-bucket')
redis_instance = create_redis()
sqs_queue = create_sqs_queue()
ecs_cluster = create_ecs_cluster()
rds_instance = create_rds_postgresql()

# instantiate cloudwatch
setup_cloudwatch()

# Define exports
pulumi.export('bucket_name', bucket.id)
pulumi.export("sqs_url", sqs_queue.url)
pulumi.export("rds_endpoint", rds_instance.endpoint)
pulumi.export("redis_endpoint", redis_instance.cache_nodes[0]["address"])


