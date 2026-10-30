from prompts import SYSTEM_PROMPT


from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
client = Anthropic(default_headers={"x-session-id": "hoyai-dev"})  # proxy requires a session id

# the proxy always replies as a stream, so use stream() and collect the full message
with client.messages.stream(
    model="claude-haiku-5-5",
    # model="claude-sonnet-5-5",  # smarter hints, costs more

    max_tokens=200,
    system = SYSTEM_PROMPT,
    messages=[{"role": "user", "content": "hello"}],
) as stream:
    response = stream.get_final_message()


print(response.content[0].text) 
