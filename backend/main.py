import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

while True:
    user = input("You: ")

    if user == "exit":
        break

    response = model.generate_content(user)

    print("AI:", response.text)