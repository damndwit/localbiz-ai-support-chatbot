"""Streamlit interface for a configurable local-business FAQ chatbot."""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from faq_engine import FAQBot, load_faqs

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="LocalBiz | Customer Support",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_bot() -> FAQBot:
    return FAQBot(load_faqs(ROOT / "data" / "faqs.csv"))


@st.cache_data
def load_config() -> dict:
    with open(ROOT / "business.json", encoding="utf-8") as file:
        return json.load(file)


config = load_config()
try:
    bot = load_bot()
except (OSError, ValueError) as error:
    st.error(f"Could not load business FAQs: {error}")
    st.stop()

st.markdown(
    """
    <style>
    .block-container {max-width: 850px; padding-top: 2rem;}
    .hero {background:linear-gradient(125deg,#142c36,#203f4e);
           border-radius:17px; padding:25px 26px; color:#f8fafc;
           margin-bottom:23px; border:1px solid #315765;}
    .hero h1 {color:white; font-size:2.1rem; margin:0;}
    .hero p {color:#d5e8ed; margin:5px 0 0;}
    .eyebrow {color:#a8f1df; font-size:.76rem; letter-spacing:.11em;
              text-transform:uppercase; font-weight:750;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><div class="eyebrow">LocalBiz · Customer support demo</div>'
    f'<h1>{config["business_name"]}</h1>'
    f'<p>{config["tagline"]}</p></div>',
    unsafe_allow_html=True,
)
st.caption("Fictional business demo · Answers come from an approved FAQ, not live customer records.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": config["welcome_message"]}
    ]


def ask(question: str) -> None:
    """Append one customer question and the matched FAQ response."""
    if not question.strip():
        return
    reply = bot.answer(question)
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply.text,
        "match": reply.matched_question,
        "score": reply.confidence,
        "fallback": reply.is_fallback,
    })


with st.sidebar:
    st.title("⚙️ Business demo")
    st.markdown(f"**{config['business_name']}**")
    st.caption(config["contact_note"])
    st.divider()
    show_details = st.toggle("Show how matches work", value=False)
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": config["welcome_message"]}
        ]
        st.rerun()
    st.divider()
    st.caption("Customize business.json and data/faqs.csv to adapt this demo for another business.")
    st.caption("No paid API key or LLM service is required.")

st.subheader("Popular questions")
quick_questions = config.get("quick_questions", [])
columns = st.columns(2)
for number, question in enumerate(quick_questions):
    with columns[number % 2]:
        if st.button(question, key=f"quick_{number}", use_container_width=True):
            ask(question)

prompt = st.chat_input("Ask about hours, reservations, menu, Wi-Fi...")
if prompt:
    ask(prompt)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if show_details and message["role"] == "assistant" and "score" in message:
            if message.get("match"):
                st.caption(
                    f"Matched FAQ: {message['match']} · "
                    f"Similarity: {message['score']:.2f}"
                )
            elif message.get("fallback"):
                st.caption("No sufficiently close FAQ match. Used safe fallback.")

st.divider()
st.caption("Prototype for demonstration and learning. Verify every business policy before real-world use.")
