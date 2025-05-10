import streamlit as st
from google import genai

import os
from dotenv import load_dotenv

load_dotenv()

# Function to generate content using Gemini
def generate_content(subject, job, topics):
    client = genai.Client(api_key=os.getenv("api_key"), vertexai=False)
    prompt = f"""
        I am learning {subject} to become a {job}. Below is the list of topics I have studied so far:
        {', '.join(topics)}.

        Your task:
        1. Generate **exactly 5 practice questions** for each topic listed above.
        2. Ensure all questions are **practical and relevant** to real-world {job} applications.
        3. Do **not include questions** unrelated to the topics provided.
        4. Do **not provide answers** to the questions.

        Output format:
        - Use a **well-structured assignment format**.
        - Write in **clear and professional language**.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    return response.text

st.title("AI Practice Question Generator")

with st.form("input_form"):
    job = st.text_input("ENTER COURSE/JOB TITLE", placeholder="e.g. Data Scientist")
    subject = st.text_input("ENTER SUBJECT", placeholder="e.g. python")
    topics = st.text_area("enter topics (comma-separated)", placeholder="e.g. Topic 1, Topic 2, Topic 3")
    submitted = st.form_submit_button("Generate Questions")

if submitted:
    topics_list = [t.strip() for t in topics.split(",")]
    ai_response = generate_content(subject, job, topics_list)
    st.session_state['ai_response'] = ai_response
    st.markdown("### Generated Practice Questions")
    st.write(ai_response)

