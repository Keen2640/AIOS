from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_action(user_input):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )
    return response.text