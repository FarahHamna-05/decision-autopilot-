import streamlit as st
from openai import OpenAI
import json

def generate_tasks(user_input):

    # Initialize client INSIDE function (important)
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

        try:
            tasks = json.loads(content)
        except:
            st.error("Invalid response from AI. Try again.")
            return []

        return tasks

    except Exception as e:
        st.error(f"Agent Error: {e}")
        return []
