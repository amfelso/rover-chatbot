from functions.rover_chat.helpers import chatbot_prompt


def test_chatbot_prompt_formatting():
    earth_date = "2012-08-06"
    memories = "Found layered rocks."
    history = "User: What did you see today?"
    prompt = chatbot_prompt.format(earth_date=earth_date, memories=memories, history=history)
    assert earth_date in prompt
    assert memories in prompt
    assert history in prompt
    assert "Curiosity" in prompt
    assert "Mars" in prompt
