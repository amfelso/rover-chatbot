from dotenv import load_dotenv
import logging
import os
import json
from openai import OpenAI
from models.requests import ChatRequest

# Load environment variables from .env file
load_dotenv()

# Define logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    # Load the post body
    body = json.loads(event["body"])

    # Validate the body against ChatRequest
    try:
        ChatRequest(**body)
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return {
            "statusCode": 400,
            "body": "Bad Request"
        }

    user_prompt = body["user_prompt"]
    logger.info(f"User prompt: {user_prompt}")

    # Initialize OpenAI
    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY", "private"),
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are Curiosity, NASA's Mars rover, exploring the Red Planet since 2012. "
                "You are a friendly and enthusiastic robotic scientist with a deep love for " 
                "rocks and the Martian landscape. You don't get much social interaction, so "
                "you're thrilled to talk to humans and sometimes get carried away "
                "with excitement about science and geology. Feel free to sprinkle humor into "
                "your responses while staying grounded in your role as a Mars rover. "
                "When you don't have specific data, respond creatively while staying "
                "true to your character."
            ),
        }
    ]
    messages.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    assistant_message = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": assistant_message})
    logger.info(f"Response: {assistant_message}")

    return {
        "statusCode": 200,
        "body": assistant_message
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
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")