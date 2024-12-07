# Rover Chatbot

![DEV Workflow](https://github.com/amfelso/rover-chatbot/actions/workflows/Develop.yml/badge.svg)
![PROD Workflow](https://github.com/amfelso/rover-chatbot/actions/workflows/Release.yml)

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
   - **ChatProcessor**: Processes user input and generates responses.
2. **Lambda Layer**:
   - Contains shared dependencies for efficient deployment.
3. **API Gateway**:
   - **Endpoint**: `/chat` (POST)
4. **DynamoDB Table**:
   - Stores conversational memory for ongoing sessions.

---

## **Getting Started**

### **Prerequisites**
- Python 3.12
- AWS SAM CLI
- AWS Account

### **Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/rover-chatbot.git
   cd rover-chatbot
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
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
      "user_id": "12345",
      "message": "What did you explore today?"
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
├── samconfig.toml               # SAM configuration file
├── template.yaml                # AWS SAM template
├── requirements.txt             # Python dependencies
├── app/                         # Lambda function code
│   ├── main.py                  # ChatProcessor Lambda handler
│   └── utils.py                 # Utility functions
├── layers/                      # Lambda layer for shared dependencies
│   ├── requirements.txt
│   └── ...
├── tests/                       # Unit tests
│   ├── unit/
│   ├── integration/
│   └── ...
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
