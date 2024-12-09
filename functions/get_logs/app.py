import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from urllib.parse import urlparse

# Get the current date
current_date = datetime.now()
formatted_date = current_date.strftime('%Y-%m-%d')

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define logger
logger = logging.getLogger()
if not logger.hasHandlers():  # Prevent duplicate handlers during testing
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)  # Set logging level


def fetch_memory_text_boto3(s3_url):
    """
    Fetch the content of a text file from an S3 URL using boto3.

    Args:
        s3_url (str): The S3 URL of the text file.

    Returns:
        str: The content of the text file.
    """
    try:
        # Parse the S3 URL to extract bucket and key
        parsed_url = urlparse(s3_url)
        bucket_name = parsed_url.netloc.split('.')[0] if '.s3.amazonaws.com' \
                      in parsed_url.netloc else parsed_url.netloc
        key = parsed_url.path.lstrip('/')
        logger.info(f"Bucket: {bucket_name}, Key: {key}")

        # Create an S3 client
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read().decode('utf-8')

    except (NoCredentialsError, PartialCredentialsError):
        logger.error("Error: AWS credentials not found or incomplete.")
    except Exception as e:
        logger.error(f"Error fetching S3 memory file: {e}")

    return None


def lambda_handler(event, context):
    # Validate post body
    body = json.loads(event["body"])
    earth_date = body["earth_date"]
    if not earth_date:
        return {
            "statusCode": 400,
            "body": "Invalid request body"
        }
    logger.info(f"Earth date: {earth_date}")

    pipeline_table = os.getenv("PIPELINE_TABLE", "PipelineTransactionLog")

    try:
        # Get the logs from the pipeline table in DynamoDB for the given earth date
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(pipeline_table)
        response = table.get_item(
            Key={
                'EarthDate': earth_date
            }
        )['Item']
        photos = [x['img_src'] for x in response.get("Lambda1__FetchImages")["output"]]
        logger.info(f"Photos: {photos}")
        
        memories = []
        urls = response.get("Lambda2__GenerateMemories")["output"]
        logger.info(f"Memory URLs: {urls}")
        for s3_url in urls:
            response = fetch_memory_text_boto3(s3_url)
            if response:
                memories.append(response)

        # Create the response in format [{"img_src": "url", "memory": "text"}]
        response = []
        for i in range(len(photos)):
            response.append({
                "img_src": photos[i],
                "memory": memories[i]
            })
        logger.info(f"Response generated successfully.")
        logger.debug(f"Response: {response}")

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
             "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            },
            "body": "Internal server error"
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
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
        'body': json.dumps({
            "earth_date": "2012-08-09"
        }),
        'isBase64Encoded': False
    }
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")
