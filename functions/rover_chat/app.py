from dotenv import load_dotenv
import logging
import json

# Load environment variables from .env file
load_dotenv()

# Define logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    # Receive the user prompt from the event
    body = json.loads(event["body"])
    user_prompt = body["user_prompt"]
    logger.info(f"User prompt: {user_prompt}")

    response = "I'm good, thank you for asking!"
    return {
        "statusCode": 200,
        "body": response
    }


if __name__ == "__main__":
    # Test the function locally
    logger.info("Testing locally...")
    test_event = {
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
                'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
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
        'body': '{\n  "user_prompt": "Hi, how are you today?"\n}',
        'isBase64Encoded': False
    }
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")