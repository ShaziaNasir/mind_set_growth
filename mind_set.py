import streamlit as st
import json
import random
import datetime
import os

# Constants
CHALLENGES = [
    "Try something you've never done before.",
    "Ask for feedback and learn from it.",
    "Embrace a mistake you made today and reflect on it.",
    "Spend 15 minutes learning a new skill.",
    "Write down 3 things you struggled with but improved on."
]

QUOTES = [
    "Mistakes are proof that you are trying.",
    "The only way to learn is through effort.",
    "Your brain is like a muscle – the more you use it, the stronger it gets.",
    "Success comes from perseverance, not perfection.",
    "Challenges are opportunities to grow."
]

DATA_FILE = "growth_data.json"

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"entries": [], "goals": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Streamlit UI
st.set_page_config(page_title="Growth Mindset Challenge", layout="centered")
st.title("🌱 Growth Mindset Challenge App")

data = load_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Today's Challenge", "Reflect", "Set Goal", "Progress"])

# Session state for current challenge
if "today_challenge" not in st.session_state:
    st.session_state.today_challenge = random.choice(CHALLENGES)
    st.session_state.today_quote = random.choice(QUOTES)

# Pages
if page == "Today's Challenge":
    st.subheader("💡 Today's Challenge")
    st.info(st.session_state.today_challenge)
    st.subheader("💬 Motivation")
    st.success(st.session_state.today_quote)

elif page == "Reflect":
    st.subheader("📝 Reflect on the Challenge")
    st.markdown(f"**Challenge:** {st.session_state.today_challenge}")
    reflection = st.text_area("Write your reflection here:")
    if st.button("Save Reflection"):
        if reflection.strip():
            data['entries'].append({
                "date": str(datetime.date.today()),
                "challenge": st.session_state.today_challenge,
                "entry": reflection.strip()
            })
            save_data(data)
            st.success("Reflection saved!")
        else:
            st.warning("Please write something before saving.")

elif page == "Set Goal":
    st.subheader("🎯 Set a New Goal")
    goal = st.text_input("Your goal:")
    if st.button("Save Goal"):
        if goal.strip():
            data['goals'].append({
                "date": str(datetime.date.today()),
                "goal": goal.strip()
            })
            save_data(data)
            st.success("Goal saved!")
        else:
            st.warning("Please enter a goal before saving.")

elif page == "Progress":
    st.subheader("📖 Past Reflections")
    if data['entries']:
        for entry in data['entries'][-5:][::-1]:  # Last 5 entries, latest first
            st.markdown(f"**{entry['date']}** - {entry['challenge']}")
            st.write(f"🖋️ {entry['entry']}")
            st.markdown("---")
    else:
        st.info("No reflections yet.")

    st.subheader("✅ Your Goals")
    if data['goals']:
        for goal in data['goals'][-5:][::-1]:
            st.write(f"📆 {goal['date']} - 🎯 {goal['goal']}")
    else:
        st.info("No goals set yet.")

