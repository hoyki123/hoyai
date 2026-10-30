from prompts import SYSTEM_PROMPT


from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
client = Anthropic(default_headers={"x-session-id": "hoyai-dev"})  # proxy requires a session id

with open("evals/bugs/average.py") as f:
    notes = f.read()


# the proxy always replies as a stream, so use stream() and collect the full message
with client.messages.stream(
    model="claude-haiku-5-5",
    # model="claude-sonnet-5-5",  # smarter hints, costs more

    max_tokens=1024,  # required by the API; a ceiling, not a target
    thinking={"type": "disabled"},  # otherwise thinking can use up all of max_tokens
    system = SYSTEM_PROMPT,
    messages=[{"role": "user", "content": f"This code should print 4.0 but prints 2.0. Why?\n\n{notes}"}],
) as stream:
    response = stream.get_final_message()


print(response.content[0].text) 
