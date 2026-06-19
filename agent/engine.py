from openai import OpenAI
from agent.prompt import SYSTEM_PROMPT

client = OpenAI(api_key="YOUR_API_KEY")

def get_action(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content