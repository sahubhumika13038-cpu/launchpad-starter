import streamlit as st
from google import genai
from datetime import date

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
MODEL = "gemini-3.8-flash"  # if you get a 404, copy the current name from AI Studio

SAMPLE = """Bhaiya kal subah tak 50 samosa chahiye, party hai 5 baje.
Aur haan, pichle hafte ka 2000 rupay baaki hai, Friday tak de dena.
Also can you send the bill on WhatsApp? Thanks - Rakesh"""

st.set_page_config(page_title="ChatToTasks", page_icon="✅")
st.title("✅ ChatToTasks")
st.caption("Paste a messy WhatsApp or email message. Get clear tasks and a ready reply.")

if "text" not in st.session_state:
    st.session_state.text = ""

if st.button("Try a sample message"):
    st.session_state.text = SAMPLE

text = st.text_area("Paste your message here:", key="text", height=200)
tone = st.selectbox("Reply tone", ["Polite", "Friendly", "Formal"])

if st.button("Make my task list", type="primary"):
    if not text.strip():
        st.warning("Please paste a message first.")
    else:
        prompt = f"""You help small business owners and freelancers in India.
Today's date is {date.today().strftime('%A, %d %B %Y')}.
The message may be in English, Hindi, or Hinglish.

Read the message below and reply in English using exactly these sections:

## Tasks
A markdown table with columns: Task | Due date | Priority (High/Medium/Low).
Turn words like "kal", "Friday", "tomorrow" into real dates.

## Money or Numbers
Any amounts, quantities or times mentioned. Write "None" if there are none.

## Questions to Clarify
Anything unclear that I should ask the sender. Write "None" if clear.

## Draft Reply
A short reply to the sender in the same language they used. Tone: {tone}.

Message:
{text}"""
        try:
            with st.spinner("Reading your message..."):
                reply = client.models.generate_content(model=MODEL, contents=prompt)
            st.markdown(reply.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
