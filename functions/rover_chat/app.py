from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Define logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    # Receive the user prompt from the event
    user_prompt = event["user_prompt"]
    logger.info(f"User prompt: {user_prompt}")

    response = "I'm good, thank you for asking!"
    return {
        "statusCode": 200,
        "body": response
    }


if __name__ == "__main__":
    # Test the function locally
    logger.info("Testing locally...")
    test_event = {"user_prompt": "Hi, how are you today?"}
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")