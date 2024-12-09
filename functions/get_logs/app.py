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
formatted_date = current_date.strftime("%Y-%m-%d")

# Load environment variables from .env file
load_dotenv()

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
        bucket_name = (
            parsed_url.netloc.split(".")[0]
            if ".s3.amazonaws.com" in parsed_url.netloc
            else parsed_url.netloc
        )
        key = parsed_url.path.lstrip("/")
        logger.info(f"Bucket: {bucket_name}, Key: {key}")

        # Create an S3 client
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return response["Body"].read().decode("utf-8")

    except (NoCredentialsError, PartialCredentialsError):
        logger.error("Error: AWS credentials not found or incomplete.")
    except Exception as e:
        logger.error(f"Error fetching S3 memory file: {e}")

    return None


def lambda_handler(event, context):
    # Validate get params
    params = event["queryStringParameters"]
    earth_date = params["earth_date"]
    if not earth_date:
        return {"statusCode": 400, "body": "Invalid request body"}
    logger.info(f"Earth date: {earth_date}")

    pipeline_table = os.getenv("PIPELINE_TABLE", "PipelineTransactionLog")

    try:
        # Get the logs from the pipeline table in DynamoDB for the given earth date
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(pipeline_table)
        response = table.get_item(Key={"EarthDate": earth_date}).get("Item")
        if not response:
            logger.warning(f"No logs found for the given date.")
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                },
                "body": json.dumps({"logs": []}),
            }

        photos = [x["img_src"] for x in response.get("Lambda1__FetchImages").get("output", [])]
        logger.info(f"Photos: {photos}")

        memories = []
        urls = response.get("Lambda2__GenerateMemories").get("output", [])
        logger.info(f"Memory URLs: {urls}")
        for s3_url in urls:
            response = fetch_memory_text_boto3(s3_url)
            if response:
                memories.append(response)

        # Create the response in format [{"img_src": "url", "memory": "text"}]
        response = []
        for i in range(len(photos)):
            response.append({"img_src": photos[i], "memory": memories[i]})
        logger.info(f"Response generated successfully.")
        logger.debug(f"Response: {response}")

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
            },
            "body": "Internal server error",
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
        "body": json.dumps({"logs": response}),
    }


if __name__ == "__main__":
    # Test the function locally
    logger.info("Testing locally...")
    test_event = {
        "resource": "/logs",
        "path": "/logs",
        "httpMethod": "GET",
        "headers": None,
        "multiValueHeaders": None,
        "queryStringParameters": {"earth_date": "2012-08-12"},
        "multiValueQueryStringParameters": {"earth_date": ["2012-08-12"]},
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "nn9e51",
            "resourcePath": "/logs",
            "httpMethod": "GET",
            "extendedRequestId": "CiH_sHqgIAMF8dg=",
            "requestTime": "09/Dec/2024:16:52:52 +0000",
            "path": "/logs",
            "accountId": "056785171326",
            "protocol": "HTTP/1.1",
            "stage": "test-invoke-stage",
            "domainPrefix": "testPrefix",
            "requestTimeEpoch": 1733763172093,
            "requestId": "79839435-2c8c-43a4-a8b2-5d6f8a4c579d",
            "identity": {
                "cognitoIdentityPoolId": None,
                "cognitoIdentityId": None,
                "apiKey": "test-invoke-api-key",
                "principalOrgId": None,
                "cognitoAuthenticationType": None,
                "userArn": "arn:aws:iam::056785171326:user/August",
                "apiKeyId": "test-invoke-api-key-id",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "accountId": "056785171326",
                "caller": "AIDAQ2OFI6N7EB4BVXOHV",
                "sourceIp": "test-invoke-source-ip",
                "accessKey": "ASIAQ2OFI6N7DUVCPH3Q",
                "cognitoAuthenticationProvider": None,
                "user": "AIDAQ2OFI6N7EB4BVXOHV",
            },
            "domainName": "testPrefix.testDomainName",
            "apiId": "tmlg7yfb6l",
        },
        "body": None,
        "isBase64Encoded": False,
    }
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")
