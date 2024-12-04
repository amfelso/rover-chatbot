from functions.rover_chat import app


def test_chat():
    input_payload = {"user_prompt": "Hi, how are you today?"}

    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
