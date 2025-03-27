import pulumi_aws as aws

def create_redis():
    redis_cluster = aws.elasticache.Cluster("celeryRedisCluster",
        cluster_id="celery-redis-cluster",
        engine="redis",
        engine_version="6.0",
        node_type="cache.t3.micro",
        num_cache_nodes=1,
        port=6379,

        tags={
            "Name": "Celery Redis Cluster",
            "Environment": "Development",
            "ManagedBy": "Pulumi"
        }
    )

    return redis_cluster