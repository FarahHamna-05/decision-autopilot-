import streamlit as st
import pandas as pd
from optimizer import optimize_tasks

st.set_page_config(page_title="Decision Autopilot")

st.title("🧠 Decision Autopilot")
st.write("I decide what you should do.")

# Inputs
num_tasks = st.number_input("Number of tasks", 1, 5, 3)

tasks = []

for i in range(num_tasks):
    st.subheader(f"Task {i+1}")

    name = st.text_input(f"Task Name {i+1}", key=i)
    time = st.number_input(f"Time (hrs) {i+1}", 0.5, 10.0, 1.0, key=f"time{i}")
    priority = st.slider(f"Priority {i+1}", 1, 10, 5, key=f"p{i}")
    energy = st.slider(f"Energy {i+1}", 1, 10, 5, key=f"e{i}")
    regret = st.slider(f"Regret {i+1}", 1, 10, 5, key=f"r{i}")

    tasks.append({
        "name": name if name else f"Task {i+1}",
        "time": time,
        "priority": priority,
        "energy": energy,
        "regret": regret
    })

st.markdown("---")

available_time = st.number_input("Available Time", 1.0, 24.0, 5.0)
energy_limit = st.slider("Energy Limit", 1, 20, 10)

# Weights
st.subheader("⚙️ Preferences")
w1 = st.slider("Priority Weight", 0.0, 2.0, 1.0)
w2 = st.slider("Regret Weight", 0.0, 2.0, 1.0)
w3 = st.slider("Energy Penalty", 0.0, 2.0, 1.0)

# Mode (AFTER weights)
mode = st.selectbox("Your Mode", ["Normal", "Low Energy", "High Focus"])

if mode == "Low Energy":
    w3 = w3 * 1.5
elif mode == "High Focus":
    w1 = w1 * 1.5

# Run optimization
if st.button("🚀 Decide for me"):

    selected, rejected = optimize_tasks(tasks, available_time, energy_limit, w1, w2, w3)

    # Show results
    st.subheader("✅ Do This")
    for t in selected:
        st.write(f"👉 {t['name']}")

    st.subheader("❌ Skip This")
    for t in rejected:
        st.write(f"👉 {t['name']}")

    # Explanation
    st.subheader("🧠 Why these decisions?")
    for t in selected:
        st.write(
            f"👉 **{t['name']}** chosen because: "
            f"High Priority ({t['priority']}), "
            f"High Regret ({t['regret']}), "
            f"Manageable Energy ({t['energy']}) → Score: {t['score']}"
        )

    # Chart
    df = pd.DataFrame(tasks)
    df["Score"] = [
        w1*t["priority"] + w2*t["regret"] - w3*t["energy"]
        for t in tasks
    ]

    st.subheader("📊 Task Scores")
    st.bar_chart(df.set_index("name")["Score"])

    # Recalculate
    if st.button("❌ I skipped a task, recalculate"):
        st.experimental_rerun()
