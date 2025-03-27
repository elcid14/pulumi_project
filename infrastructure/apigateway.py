import pulumi
import pulumi_aws as aws

# Create API Gateway
api = aws.apigatewayv2.Api("shipmentAPI",
    protocol_type="HTTP"
)

# Create integration with Lambda function
integration = aws.apigatewayv2.Integration("lambdaIntegration",
    api_id=api.id,
    integration_type="AWS_PROXY",
    integration_uri=pulumi.Output.from_input(pulumi.export("lambda_arn"))
)

# Shipment creation route
route = aws.apigatewayv2.Route("createShipmentRoute",
    api_id=api.id,
    route_key="POST /create-shipment",
    target=f"integrations/{integration.id}"
)

# # Shipment update route
# route = aws.apigatewayv2.Route("updateShipmentRoute",
#     api_id = api.id,
#     route_key="POST /update-shipment",
#     target=f"integrations/{integration.id}"
# )

# # Shipment delete route
# route = aws.apigatewayv2.Route("deleteShipmentRoute", 
#     api_id = api.id,
#     route_key="DELETE /delete-shipment",
#     target=f"integrations/{integration.id}"                               
# )


# Deploy API Gateway
stage = aws.apigatewayv2.Stage("devStage",
    api_id=api.id,
    name="dev",
    auto_deploy=True
)

pulumi.export("api_gateway_url", stage.invoke_url)
