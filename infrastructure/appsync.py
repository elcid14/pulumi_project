from pulumi_aws.appsync import GraphqlApi, GraphqlSchema

def create_appsync_api():
    # Create AppSync API first
    api = GraphqlApi("shippingApi",
        authentication_type="API_KEY",
        name="shipping-tracking-api"
    )
    
    # Then create schema
    schema = GraphqlSchema("shippingSchema",
        api_id=api.id,
        schema="""
        type Shipment {
            id: ID!
            containerNumber: String!
            status: String!
        }
        
        type Query {
            getShipment(id: ID!): Shipment
            listShipments: [Shipment]
        }
        
        type Mutation {
            createShipment(containerNumber: String!, status: String!): Shipment
        }
        """
    )
    
    return api, schema
