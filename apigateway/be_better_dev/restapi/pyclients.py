import requests, os
from misc import load_from_yaml, save_to_yaml
# =============================================================================
INPUTS_PATH = 'inputs.yml'
INPUTS = load_from_yaml(INPUTS_PATH)
INPUTS = {} if not INPUTS else INPUTS
account_id = os.environ['AWS_ACCOUNT_ID_ROOT']
region = os.environ['AWS_DEFAULT_REGION']
# =============================================================================

# f"arn:aws:execute-api:us-east-1:{account_id}:{INPUTS['api_id']}/{stage_name}/GET/transactions"

## Not working due to probably CORS Issue.
def test_api_gateway(api_url, resourse=INPUTS['api_resource'], stage="*", method=INPUTS['api_method']):
    """
    Test the AWS API Gateway REST API.

    :param api_url: The base URL of the API Gateway REST API.
    """
    # Example GET request
    get_endpoint = f"{api_url}/{stage}/{method}/{resourse}"  # Replace with your endpoint
    get_params = {
        'transactionId': 5,
        'amount': 500,
        'type': 'PURCHASE'
    }
    try:
        response = requests.get(get_endpoint, params=get_params)
        print("GET request response:")
        print(response.status_code)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")

    # # Example POST request
    # post_endpoint = f"{api_url}/path_to_resource"  # Replace with your endpoint
    # post_data = {
    #     'key1': 'value1',
    #     'key2': 'value2'
    # }
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # try:
    #     response = requests.post(post_endpoint, json=post_data, headers=headers)
    #     print("POST request response:")
    #     print(response.status_code)
    #     print(response.json())
    # except requests.exceptions.RequestException as e:
    #     print(f"POST request failed: {e}")

if __name__ == "__main__":

    # Replace with your API Gateway base URL
    api_url = INPUTS['api_gateway_arn']
    test_api_gateway(api_url)
