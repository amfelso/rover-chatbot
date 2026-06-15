
import pytest
import requests
import os
from dotenv import load_dotenv
from requests_aws4auth import AWS4Auth
import boto3

load_dotenv()
API_ENDPOINT = os.environ.get("API_ENDPOINT")


def get_aws_auth():
    """Get AWS SigV4 auth for API Gateway requests"""
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    credentials = session.get_credentials()
    return AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        session.region_name or "us-east-1",
        "execute-api"
    )


@pytest.mark.xfail
def test_chat():
    payload = {
        "user_prompt": "Hi Rover! How are you?",
        "conversation_id": "test",
        "earth_date": "2012-08-06"
    }
    url = f"{API_ENDPOINT}chat"
    auth = get_aws_auth()
    response = requests.post(url, json=payload, auth=auth)

    assert response.status_code == 200
