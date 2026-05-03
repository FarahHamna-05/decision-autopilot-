import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_tasks(user_input):

    prompt = f"""
    Convert the following situation into structured tasks.

    Situation: {user_input}

    Return ONLY valid JSON list like:
    [
      {{
        "name": "...",
        "time": number,
        "priority": 1-10,
        "energy": 1-10,
        "regret": 1-10
      }}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        tasks = json.loads(content)
        return tasks

    except Exception as e:
        print("Agent Error:", e)
        return []
