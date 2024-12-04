import pydantic


class ChatRequest(pydantic.BaseModel):
    user_prompt: str