import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    return response.choices[0].message.content

print("AI Agent is ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = chat_with_gpt(user_input)
    print("AI:", response)