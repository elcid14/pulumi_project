import pulumi_aws as aws
import pulumi
import json

def create_shipment_lambda(sqs_queue):
    # execution role
    lambda_role = aws.iam.Role("lambdaRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"}
        }]
    })
    )

    # execution policy
    aws.iam.RolePolicyAttachment("lambdaExecutionPolicy",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )
    
    # attach lambda execution policy
    sqs_policy = aws.iam.Policy("sqsSendMessagePolicy",
    policy=sqs_queue.arn.apply(lambda arn: f"""{{
        "Version": "2012-10-17",
        "Statement": [{{
            "Effect": "Allow",
            "Action": "sqs:SendMessage",
            "Resource": "{arn}"
        }}]
    }}""")
)
    
    aws.iam.RolePolicyAttachment("attachSQSPolicy",
    role=lambda_role.name,
    policy_arn=sqs_policy.arn
        )


    # defined lambda
    lambda_function = aws.lambda_.Function("createShipmentLambda",
    role=lambda_role.arn,
    runtime="python3.9",
    handler="createShipment.lambda_handler",
    memory_size=128,
    timeout=10,
    code=pulumi.FileArchive("../backend/lambdas"), 
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "SQS_QUEUE_URL": sqs_queue.url
        }
    )
    )
    
    return lambda_function