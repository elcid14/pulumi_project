import pulumi_aws as aws
import pulumi


s3_bucket = aws.s3.Bucket("lambdaCodeBucket")

# Upload lambda for createShipment
s3_object = aws.s3.BucketObject("lambdaCode",
    bucket=s3_bucket.id,
    source=pulumi.FileAsset("lambda.zip")
)
