import streamlit as st

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

load_dotenv(override=True)

google_api_key = os.getenv('GOOGLE_API_KEY')

#Check if api key exist or not

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

##################################################################################################

# Set page config
st.set_page_config(page_title="Document & Research Paper Summarizer")

# Heading
st.title("📄 Document & Research Paper Summarizer")

# File uploader
uploaded_file = st.file_uploader("Upload your document (PDF)", type=["pdf"])

# Add a submit button to confirm upload
submit_file = st.button("Submit File")

# Initialize session state for extracted text
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""


if uploaded_file and submit_file:
    st.success(f"File uploaded: {uploaded_file.name}")
    pdf_reader = PdfReader(uploaded_file)

    full_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            full_text += text

    st.session_state.extracted_text = full_text  # Store in session for later use
    st.success("✅ Document processed. Now choose summarization type and click Summarize.")

# Dropdown to choose summarization type
summary_type = st.selectbox("Choose summarization type", ["Short", "Brief", "Descriptive", "Bullet Points"])

# Summarize button
summarize_btn = st.button("Summarize")

if summarize_btn:
    if not st.session_state.extracted_text:
        st.warning("Please upload and submit a file first.")

    else:
        sys_prompt = """
        You are a document summarizing agent. You can get the document either in PDF, TXT or DOCX format.
        Depending on the type of summarization, you need to provide a summary of the document. 
        """

        user_prompt = f"The document information is shared next, {st.session_state.extracted_text}. The user has asked the summarization type to be {summary_type}."

        messages = [{"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}]

        gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        model_name = "gemini-2.0-flash"

        with st.spinner("Generating summary..."):
            response = gemini.chat.completions.create(model=model_name, messages=messages)
            answer = response.choices[0].message.content

        st.markdown("### 📃 Summary")
        st.markdown(answer, unsafe_allow_html=True)







