import json
import logging
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from helpers import get_relevant_memories, chatbot_prompt
from datetime import datetime

# Get the current date
current_date = datetime.now()
formatted_date = current_date.strftime('%Y-%m-%d')

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pinecone_plugin_interface.logging").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize ChatOpenAI
chat_model = ChatOpenAI(
    model="gpt-4",
    openai_api_key=OPENAI_API_KEY
)


def rover_chatbot(question: str, conversation_id: str, earth_date: str):
    """Interact with the Rover chatbot using LangChain."""

    # Get relevant memories
    logger.info(f"Getting relevant memories for question: {question}")
    memories = get_relevant_memories(question)
    formatted_memories = "\n".join(
        f"- Memory from {mem['metadata'].get('date')}: {mem['metadata'].get('text')}"
        for mem in memories
    )
    logger.info(f"Found {len(memories)} relevant memories.")

    # Create the ConversationChain with prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", chatbot_prompt),
            ("human", question),
        ]
    )
    chain = prompt | chat_model
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: DynamoDBChatMessageHistory(
            table_name="SessionTable", session_id=session_id
        ),
        input_messages_key="question",
        history_messages_key="history",
    )
    config = {"configurable": {"session_id": conversation_id}}
    logger.info("Running the conversation chain...")
    response = chain_with_history.invoke(
        {
            "earth_date": earth_date,
            "memories": formatted_memories,
            "question": question
        },
        config=config
    )
    logger.info("Completed the conversation chain.")
    return response.content


def lambda_handler(event, context):
    # Load the post body
    try:
        body = json.loads(event["body"])
        user_prompt = body["user_prompt"]
        logger.info(f"User prompt: {user_prompt}")
        conversation_id = body["conversation_id"]
        logger.info(f"Conversation ID: {conversation_id}")
        earth_date = body["earth_date"]
        logger.info(f"Earth date: {earth_date}")
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 400,
            "body": "Invalid request body"
        }

    response = rover_chatbot(user_prompt, conversation_id, earth_date)

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
            "user_prompt": "Hi Rover! What did you do yesterday?",
            "conversation_id": formatted_date,
            "earth_date": "2012-08-07"
        }),
        'isBase64Encoded': False
    }
    result = lambda_handler(test_event, None)
    logger.info(f"Result: {result}")
