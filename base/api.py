import os
os.environ["GROQ_API_KEY"] = "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"
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Point Nemo is the farthest point from land",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)