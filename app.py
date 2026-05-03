import streamlit as st
import time
import pandas as pd
import os

from optimizer import optimize_tasks
from agent import generate_tasks

# ✅ ADD DEBUG LINE HERE
st.write("Secrets working:", "OPENAI_API_KEY" in st.secrets)

st.set_page_config(page_title="Decision Autopilot Agent", layout="wide")
