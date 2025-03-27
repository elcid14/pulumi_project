import pulumi_aws as aws

def setup_cloudwatch():
    cloudwatch = aws.cloudwatch.MetricAlarm("taskFailuresAlarm",
        comparison_operator="GreaterThanThreshold",
        evaluation_periods=1,
        metric_name="FailedTaskCount",
        namespace="AWS/ECS",
        period=60,
        statistic="Sum",
        threshold=1,
        alarm_description="Alarm if ECS worker task fails"
    )

    return cloudwatch
