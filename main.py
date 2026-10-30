from prompts import SYSTEM_PROMPT


from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
client = Anthropic(default_headers={"x-session-id": "hoyai-dev"})  # proxy requires a session id

with open("evals/bugs/average.py") as f:
    notes = f.read()

# send the whole conversation to Claude and return its reply as text.
# the proxy always replies as a stream, so use stream() and collect the full message
def ask_model(messages):
    with client.messages.stream(
        model="claude-haiku-5-5",
        # model="claude-sonnet-5-5",  # smarter hints, costs more
        max_tokens=1024,  # required by the API; a ceiling, not a target
        thinking={"type": "disabled"},  # otherwise thinking can use up all of max_tokens
        system=SYSTEM_PROMPT,  # how Hoy should behave: hints, never answers
        messages=messages,  # the conversation so far
    ) as stream:
        response = stream.get_final_message()
    # content is a list of blocks; the first one holds the reply text
    return response.content[0].text

history = []
while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    if user_input == "reset":
        history = []
        print("Hoy: Conversation cleared.")
        continue
    history.append({"role": "user", "content": user_input})
    reply = ask_model(history)
    history.append({"role": "assistant", "content": reply})

    print("Hoy:", reply)
