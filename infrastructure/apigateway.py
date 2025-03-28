import pulumi
import pulumi_aws as aws

# Create API Gateway

def create_api_gateway(lambda_func):
    # Create HTTP API
    api = aws.apigatewayv2.Api("shipmentAPI", 
        protocol_type="HTTP",
        route_selection_expression="$request.method $request.path"
    )
    
    # Create Lambda integration
    integration = aws.apigatewayv2.Integration("lambdaIntegration",
        api_id=api.id,
        integration_type="AWS_PROXY",
        integration_method="POST",
        connection_type="INTERNET",
        integration_uri=lambda_func.invoke_arn
    )
    
    # Create route
    aws.apigatewayv2.Route("createShipmentRoute",
        api_id=api.id,
        route_key="POST /create-shipment",
        target=pulumi.Output.format("integrations/{0}", integration.id)
    )
    
    # Lambda permission to allow API Gateway to invoke the function
    aws.lambda_.Permission("apiGatewayLambdaPermission",
        action="lambda:InvokeFunction",
        function=lambda_func.name,
        principal="apigateway.amazonaws.com",
        source_arn=pulumi.Output.format("{0}/*/*/*", api.execution_arn)
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
    aws.apigatewayv2.Stage("devStage",
        api_id=api.id,
        name="dev",
        auto_deploy=True)
