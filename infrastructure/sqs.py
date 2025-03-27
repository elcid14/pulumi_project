import pulumi_aws as aws

def create_sqs_queue():
    queue = aws.sqs.Queue("celeryQueue")

    return queue
