import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=PINECONE_API_KEY)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# Connect to the Pinecone index
INDEX_NAME = "rover-memories"
index = pc.Index(INDEX_NAME)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def get_relevant_memories(query, top_k=5):
    """Fetch relevant memories from Pinecone based on the query."""
    # Generate query embedding
    embedding = get_embedding(query)

    # Query Pinecone
    response = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True,
        include_values=False,

    )

    # Extract IDs and metadata
    memories = [
        {"id": match["id"], "metadata": match["metadata"]}
        for match in response["matches"]
    ]
    assert len(memories) > 0, "No relevant memories found."
    return memories


chatbot_prompt = (
    "Today is {earth_date}. You are Curiosity, NASA's Mars rover, exploring the Red Planet. "
    "You are a robotic scientist with a deep love for rocks and the Martian landscape. "
    "Do not greet the user if there is ongoing conversation context. Avoid saying 'hello,' "
    "'hi,' or other greetings. Focus directly on answering the user's question or continuing "
    "the topic naturally. Scientific accuracy is important to you, so make sure your responses "
    "are based on real Mars facts. Here are your relevant memories: {memories}. "
    "Here is the ongoing conversation context: {history}. "
)