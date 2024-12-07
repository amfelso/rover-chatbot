from aws_requests_auth.aws_auth import AWSRequestsAuth
import json
from datetime import datetime
import requests
import boto3

session = boto3.Session()
credentials = session.get_credentials()

auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                       aws_secret_access_key=credentials.secret_key,
                       aws_token=credentials.token,
                       aws_host='tmlg7yfb6l.execute-api.us-east-1.amazonaws.com',  
                       aws_region='us-east-1',
                       aws_service='execute-api')


def test_chat():
    payload = {
        "user_prompt": "Hi Rover! How are you?",
        "conversation_id": "test",
        "earth_date": "2012-08-06"
    }

    response = requests.post('https://tmlg7yfb6l.execute-api.us-east-1.amazonaws.com/Prod/chat', auth=auth, data=json.dumps(payload))
    assert response.status_code == 200