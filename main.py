import streamlit as st
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Import Gemini API client
from google.generativeai import GenerativeModel, configure

load_dotenv()

st.set_page_config(page_title="Roast My Resume", page_icon="📃", layout="centered")

st.title("Roast My Resume 📃")
st.write(
    "Upload your resume, and we'll provide *harsh* feedback on how to improve it according to your needs!"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF format only)", type=["pdf"]
)

job_role = st.text_input(
    "What job role are you applying for?",
    placeholder="e.g., Software Engineer, Data Scientist, etc."
)

roast = st.button("Roast! 🔥")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file.read()))
    return file.read().decode("utf-8")

if roast and uploaded_file and job_role:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()

        prompt = f"""Alright, let's roast this resume. I need you to mercilessly (but constructively) tear it apart.

        Focus on these areas and tell me what's weak, what's missing, and what just plain stinks:
        1.  Content Impact: Does it grab attention, or is it a snooze-fest?
        2.  Skills Showcase: Are the skills highlighted effectively, or are they buried?
        3.  Experience Descriptions: Do they scream accomplishment, or whisper daily tasks?
        4.  Targeted Torching (for {job_role if job_role else 'general job applications'}): What specific flaws will hold it back for this role?

        Resume content:
        {file_content}

        Give me the brutal truth in a clear, actionable format. Don't hold back."""

        # Set up Gemini client
        configure(api_key=GEMINI_API_KEY)
        model = GenerativeModel("gemini-2.0-flash")

        response = model.generate_content(prompt)

        st.markdown("### Roast Results 🔥")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
