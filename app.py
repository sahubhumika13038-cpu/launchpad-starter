import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("My First AI App")
text = st.text_area("Type something:")

if st.button("Go"):
    with st.spinner("Thinking..."):
        reply = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"Summarize this in 3 bullet points: {text}",
        )
    st.write(reply.text)