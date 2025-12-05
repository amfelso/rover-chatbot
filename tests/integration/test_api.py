
import pytest
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_ENDPOINT = os.environ.get("API_ENDPOINT")


@pytest.mark.xfail
def test_chat():
    payload = {
        "user_prompt": "Hi Rover! How are you?",
        "conversation_id": "test",
        "earth_date": "2012-08-06"
    }
    url = f"{API_ENDPOINT}chat"
    response = requests.post(url, data=json.dumps(payload))
    assert response.status_code == 200
