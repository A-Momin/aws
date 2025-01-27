### [AWS API Gateway to Lambda Tutorial in Python | Build a REST API](https://www.youtube.com/watch?v=uFsaiEhr1zs)

-   [Slides](./Gateway_to_Lambda.pdf)

```python
# apigateway_lambdahandler.py

import json

print('Loading function')

def lambda_handler(event, context):
	#1. Parse out query string params
	transactionId = event['queryStringParameters']['transactionId']
	transactionType = event['queryStringParameters']['type']
	transactionAmount = event['queryStringParameters']['amount']

	print('transactionId=' + transactionId)
	print('transactionType=' + transactionType)
	print('transactionAmount=' + transactionAmount)

	#2. Construct the body of the response object
	transactionResponse = {}
	transactionResponse['transactionId'] = transactionId
	transactionResponse['type'] = transactionType
	transactionResponse['amount'] = transactionAmount
	transactionResponse['message'] = 'Hello from Lambda land'

	#3. Construct http response object
	responseObject = {}
	responseObject['statusCode'] = 200
	responseObject['headers'] = {}
	responseObject['headers']['Content-Type'] = 'application/json'
	responseObject['body'] = json.dumps(transactionResponse)

	#4. Return the response object
	return responseObject
```

-   [APIEndpoint](https://v9oadws2h3.execute-api.us-east-1.amazonaws.com/dev/transactions?transactionId=5&type=PURCHASE&amount=500)

### [AWS API Gateway to Lambda Tutorial in Python | Build a HTTP API (2/2)](https://www.youtube.com/watch?v=M91vXdjve7A)

-   [Slides](./Gateway_to_Lambda_HTTP.pdf)
