# Rover Chatbot Memory System

[![.github/workflows/Develop.yml](https://github.com/amfelso/rover-chatbot/actions/workflows/Develop.yml/badge.svg)](https://github.com/amfelso/rover-chatbot/actions/workflows/Develop.yml)
[![.github/workflows/Release.yml](https://github.com/amfelso/rover-chatbot/actions/workflows/Release.yml/badge.svg?branch=release)](https://github.com/amfelso/rover-chatbot/actions/workflows/Release.yml)

This application automates the retrieval, processing, and embedding of Mars rover data into a memory system designed for Retrieval-Augmented Generation (RAG). The pipeline is built on AWS Step Functions and serverless architecture to orchestrate data processing with scalability and efficiency.

## Overview

The pipeline is designed to enable a chatbot with contextual memory, simulating the ability to "remember" and reference Mars Rover data in conversations. It performs the following steps:

1. **Fetch Chat and Logs**:

   - Retrieves chat messages and logs from the API endpoints.
   - Outputs relevant data and metadata for further processing.

2. **Generate and Store Memories**:

   - Processes chat data and stores memory entries in a structured format.
   - Stores these entries in a database or S3 bucket (if configured).

3. **Embed Memories into PineconeDB**:
   - Embeds memory entries into Pinecone for use in RAG workflows and chatbot conversations.

---

## Project Structure

- **`functions`**: Lambda functions for chat and log retrieval:
  - `rover_chat`: Handles chat interactions and memory generation.
  - `get_logs`: Retrieves logs for analysis and debugging.
- **`layers`**: Shared dependencies for Lambda functions.
- **`tests`**: Unit tests for pipeline components.
- **`template.yaml`**: AWS SAM template defining serverless resources.

---

## Setup and Deployment

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/amfelso/rover-chatbot.git
   cd rover-chatbot
   ```

2. **Set up your environment**

   ```bash
   make setup
   ```

   This will:

   - Install Python dependencies from `layers/rover_chat/requirements.txt`
   - Create a `.env` file from `.env.example`

3. **Configure your API keys**
   Edit the `.env` file with your actual API keys:
   ```bash
   PINECONE_API_KEY=your-pinecone-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   ```


### Available Make Commands

- `make check-tools` - Verify required tools installed
- `make setup` - Create venv, install dependencies, and create `.env`
- `make install` - Install Python dependencies only
- `make login` - Configure AWS credentials from `.env`
- `make test` - Run all tests (automatically loads `.env`)
- `make test-unit` - Run unit tests only
- `make test-integration` - Run integration tests only (requires deployed stack and API_ENDPOINT in `.env`)
- `make lint` - Run flake8 linter and SAM template validation
- `make build` - Build SAM application
- `make deploy` - Lint, test, build, and deploy to AWS
- `make clean` - Clean build artifacts, venv, and Python cache files

### Deploying the Pipeline

**Automatic Deployment:**
Pipeline will automatically deploy via Github Actions when code updates are merged to the release branch.

**Manual Deployment:**

```bash
make deploy
```

This will lint, test, build, and deploy the application to AWS using SAM. After deployment, the API endpoint will be written to `.env` as `WEBENDPOINT`.

---


## Tests

Tests ensure the functionality of individual Lambda functions and the pipeline as a whole.

```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only integration tests (requires deployed stack and API_ENDPOINT in .env)
make test-integration
```

**Note:**
- Unit tests can run locally without any AWS resources.
- Integration tests require the stack to be deployed and `API_ENDPOINT` to be set in `.env`.

---

## Resources

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html): Introduction to SAM specification, the SAM CLI, and serverless application concepts.
- [Pinecone Documentation](https://www.pinecone.io/docs/): Guide to setting up and managing vector embeddings for efficient RAG workflows.

---

For more details, see the source code and comments in each function directory.

4. **Deploy to AWS**:
   ```bash
   sam deploy --guided
   ```

---

## **Usage**

### **POST /chat**

- **Request**:

  - Endpoint: `/chat`
  - Method: `POST`
  - Payload:
    ```json
    {
      "user_prompt": "Hi Rover! How are you?",
      "conversation_id": "test",
      "earth_date": "2012-08-06"
    }
    ```

- **Response**:
  - Example:
    ```json
    {
      "response": "Today I explored Jezero Crater and captured images of layered sedimentary rocks!"
    }
    ```

---

### **GitHub Actions**

This repository includes automated workflows for:

- **Testing**: Runs `pytest` for unit tests.
- **Linting**: Runs `flake8` to ensure code quality.
- **Deployment**: Deploys the stack using AWS SAM.

---

## **Project Structure**

```
rover-chatbot/
├── README.md
├── template.yaml                # AWS SAM template
├── .gitignore                   # Git ignore file
├── .github/                     # GitHub Actions workflows
│   ├── workflows/
│   │   ├── Develop.yml
│   │   └── Release.yml
├── functions/                   # Lambda function code
│   ├── rover_chat/
│   │   ├── __init__.py
│   │   ├── app.py               # ChatProcessor Lambda handler
│   │   ├── helpers.py           # Helper functions
├── layers/                      # Lambda layer for shared dependencies
│   ├── rover_chat/
│   │   ├── requirements.txt
├── tests/                       # Unit tests
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_chat.py
│   ├── __init__.py
```

---

## **Future Enhancements**

- Support for additional endpoints (e.g., chat history, Rover status).
- Integration with more advanced memory systems for multi-turn conversations.
- Enhanced logging and monitoring with CloudWatch and X-Ray.

---

## **License**

This project is licensed under the MIT License. See `LICENSE` for details.

---
