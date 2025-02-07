# Rover Chatbot

![DEV Workflow](https://github.com/amfelso/rover-chatbot/actions/workflows/Develop.yml/badge.svg)
![PROD Workflow](https://github.com/amfelso/rover-chatbot/actions/workflows/Release.yml/badge.svg)

The Rover Chatbot is an AWS-based application that enables users to interact with a conversational Mars rover assistant. It uses AWS Lambda, API Gateway, and DynamoDB to process chat requests, manage conversational memory, and respond dynamically using GPT-powered logic.

---

## **Features**

- **/chat API Endpoint**: A POST endpoint for user interactions with the chatbot.
- **Conversational Memory**: DynamoDB table stores past conversations for context and personalization.
- **Serverless Architecture**: Built using AWS Lambda, API Gateway, and a shared Lambda layer for reusable dependencies.
- **Automated CI/CD**: GitHub Actions for testing, linting, and deployment.
- **Quality Control**: Includes `pytest` for unit testing and `flake8` for code linting.

---

## **Architecture**

### **Key Resources**
1. **Lambda Functions**:
   - **RoverChatFunction**: Processes user input and generates responses. Located in [functions/rover_chat/app.py](functions/rover_chat/app.py).
2. **Lambda Layer**:
   - Contains shared dependencies for efficient deployment. Located in [layers/rover_chat/requirements.txt](layers/rover_chat/requirements.txt).
3. **API Gateway**:
   - **Endpoint**: `/chat` (POST)
4. **DynamoDB Table**:
   - Stores conversational memory for ongoing sessions.

---

## **Getting Started**

### **Prerequisites**
- Python 3.9
- AWS SAM CLI
- AWS Account

### **Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/amfelso/rover-chatbot.git
   cd rover-chatbot
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r layers/rover_chat/requirements.txt
   ```

3. **Run SAM Build**:
   ```bash
   sam build
   ```

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

## **Development**

### **Testing**
Run unit tests with `pytest`:
```bash
pytest tests/unit
```

### **Linting**
Check code quality with `flake8`:
```bash
flake8 .
```

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
