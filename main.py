import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv()

# Function to generate content using Gemini
def generate_content(topics, num_questions):
    client = genai.Client(api_key=os.getenv("api_key"), vertexai=False)
    system_prompt = f"""
        You are an expert SQL assignment creator for business analysis.
        Your responsibilities:

        - Generate a set of challenging, diverse, and practical SQL questions based on the provided topics. If no topics are specified or the user requests "all", cover a broad range of essential SQL concepts.
        - Ensure the number of questions matches the user's request.
        - Each question must be relevant to real-world business analyst scenarios and require deep understanding of SQL.
        
        - Provide a single, well-structured SQL sample dataset (CREATE TABLE and INSERT statements) that is sufficient to solve all questions.
        - Ensure all questions can be solved using only the provided sample data.
        - Use clear, professional language and organize the output in a well-structured assignment format.
       """
    
    user_prompt = (
        f"Assignment Request:\n"
        f"- Topics: {', '.join(topics) if topics else 'All'}\n"
        f"- Number of Questions: {num_questions}\n"
       
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=user_prompt,
    )
    return response.text
    

st.title("SQL Practice Question Generator")


with st.form("input_form"):
   
    topics = st.text_area("Enter SQL Topics (comma-separated)", placeholder="e.g. Topic 1, Topic 2, Topic 3")
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=100)
    submitted = st.form_submit_button("Generate Questions")

if submitted:
    topics_list = [t.strip() for t in topics.split(",")]
    ai_response = generate_content(topics_list, num_questions)
    st.session_state['ai_response'] = ai_response
    st.markdown("### Generated Practice Questions")
    st.write(ai_response)

