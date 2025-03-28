from pulumi_aws import aws
import pulumi
import json

def create_shipment_lambda(sqs_resource , sqs_url: str):
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

    # defined lambda
    lambda_function = aws.lambda_.Function("createShipmentLambda",
    role=lambda_role.arn,
    runtime="python3.9",
    handler="lambda_function.lambda_handler",
    memory_size=128,
    timeout=10,
    code=pulumi.AssetArchive({
        ".": pulumi.FileAsset("../backend/lambdas/createShipment.py")
    }),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "SQS_QUEUE_URL": sqs_url
        }
    )
    )
    
    return lambda_function