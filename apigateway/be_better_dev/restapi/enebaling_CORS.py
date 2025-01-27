# To update the function for enabling API Gateway CORS, you need to add the necessary headers to the OPTIONS method of the resource. This includes setting up the OPTIONS method and enabling the appropriate integration response headers to handle CORS preflight requests.

import boto3

# Initialize the API Gateway client
apigateway_client = boto3.client('apigateway')

def create_resource(api_id, parent_id, path_part):
    # Create the resource
    response = apigateway_client.create_resource(
        restApiId=api_id,
        parentId=parent_id,
        pathPart=path_part
    )
    resource_id = response['id']

    # Enable CORS by adding an OPTIONS method to the resource
    enable_cors(api_id, resource_id)
    
    return response

def enable_cors(api_id, resource_id):
    # Create OPTIONS method
    apigateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )

    # Set up the method response for OPTIONS
    apigateway_client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': False,
            'method.response.header.Access-Control-Allow-Methods': False,
            'method.response.header.Access-Control-Allow-Origin': False
        },
        responseModels={
            'application/json': 'Empty'
        }
    )

    # Set up the integration response for OPTIONS
    apigateway_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        type='MOCK',
        requestTemplates={
            'application/json': '{"statusCode": 200}'
        }
    )

    apigateway_client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
            'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        },
        responseTemplates={
            'application/json': ''
        }
    )

# Example usage
api_id = 'your-api-id'
parent_id = 'your-parent-id'
path_part = 'your-path-part'

resource_response = create_resource(api_id, parent_id, path_part)
print(resource_response)
