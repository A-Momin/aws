import requests, os
from misc import load_from_yaml, save_to_yaml
# =============================================================================
INPUTS_PATH = 'inputs.yml'
INPUTS = load_from_yaml(INPUTS_PATH)
account_id = os.environ['AWS_ACCOUNT_ID_ROOT']
region = os.environ['AWS_DEFAULT_REGION']
# =============================================================================

def test_get_person(api_url):
    """
    Test the getPerson route with a GET request.

    :param api_url: The base URL of the API Gateway HTTP API.
    """
    route = "/getPerson"
    params = {
        "personId": "123"
    }
    response = requests.get(api_url + route, params=params)
    print(f"GET {route} response status code: {response.status_code}")
    print(f"GET {route} response body: {response.json()}")

def test_create_person(api_url):
    """
    Test the createPerson route with a POST request.

    :param api_url: The base URL of the API Gateway HTTP API.
    """
    route = "/createPerson"
    payload = {
        "name": "John Doe",
        "age": 30
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(api_url + route, json=payload, headers=headers)
    print(f"POST {route} response status code: {response.status_code}")
    print(f"POST {route} response body: {response.json()}")

if __name__ == "__main__":
    # Replace with your API Gateway base URL
    api_url = f"https://{INPUTS['api_id']}.execute-api.{region}.amazonaws.com/dev"
    print(api_url)

    test_get_person(api_url)
    test_create_person(api_url)
