from functions.rover_chat import app


def test_chat():
    input_payload = {
        'resource': '/chat',
        'path': '/chat',
        'httpMethod': 'POST',
        'headers': None,
        'multiValueHeaders': None,
        'queryStringParameters': None,
        'multiValueQueryStringParameters': None,
        'pathParameters': None,
        'stageVariables': None,
        'requestContext': {
            'resourceId': 'resource-id',
            'resourcePath': '/chat',
            'httpMethod': 'POST',
            'extendedRequestId': 'extended-request-id',
            'requestTime': '04/Dec/2024:09:58:01 +0000',
            'path': '/chat',
            'accountId': 'account-id',
            'protocol': 'HTTP/1.1',
            'stage': 'test-invoke-stage',
            'domainPrefix': 'testPrefix',
            'requestTimeEpoch': 1733306281143,
            'requestId': 'request-id',
            'identity': {
                'cognitoIdentityPoolId': None,
                'cognitoIdentityId': None,
                'apiKey': 'test-invoke-api-key',
                'principalOrgId': None,
                'cognitoAuthenticationType': None,
                'userArn': 'arn:aws:iam::account-id:root',
                'apiKeyId': 'test-invoke-api-key-id',
                'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'accountId': 'account-id',
                'caller': 'account-id',
                'sourceIp': 'test-invoke-source-ip',
                'accessKey': 'access-key',
                'cognitoAuthenticationProvider': None,
                'user': 'account-id'
            },
            'domainName': 'testPrefix.testDomainName',
            'apiId': 'api-id'
        },
        'body': '{\n  "user_prompt": "Hello Rover! What did you explore today?"\n}',
        'isBase64Encoded': False
    }

    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
