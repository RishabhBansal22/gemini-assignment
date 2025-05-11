import streamlit as st
from google import genai

import os
from dotenv import load_dotenv

load_dotenv()

# Function to generate content using Gemini
def generate_content(topics):
    client = genai.Client(api_key=os.getenv("api_key"), vertexai=False)
    prompt = f"""
        I am learning SQL to become a Buiseness analyst. Below is the list of topics I have studied so far:
        {', '.join(topics)}.

        Your task:
        1. Generate **exactly 5 practice questions** for each topic listed above.
        2. Ensure all questions are **practical and relevant** to real-world buiseness analyst job applications.
        3. Do **not include questions** unrelated to the topics provided.
        4. Do **not provide answers** to the questions.
        5. Always Provide sample data in sql query language to solve quesions and ensure that all quesions must be able to solve with the sample data.
        6. Ensure the questions are **diverse** and cover different aspects of the topics.

        Output format:
        - Use a **well-structured assignment format**.
        - Write in **clear and professional language**.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    return response.text
    

st.title("SQL Practice Question Generator")


with st.form("input_form"):
   
    topics = st.text_area("Enter SQl Topics (comma-separated)", placeholder="e.g. Topic 1, Topic 2, Topic 3")
    submitted = st.form_submit_button("Generate Questions")

if submitted:
    topics_list = [t.strip() for t in topics.split(",")]
    ai_response = generate_content( topics_list)
    st.session_state['ai_response'] = ai_response
    st.markdown("### Generated Practice Questions")
    st.write(ai_response)

