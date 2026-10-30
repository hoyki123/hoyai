from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
client = Anthropic()

print("Hoy AI is alive.")
