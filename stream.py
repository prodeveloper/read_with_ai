"""
PDF Upload
As a user, I want to upload a PDF file to the application so that I can interact with its content using AI.
Page Range Selection
As a user, I want to specify a range of pages from the uploaded PDF that I'm interested in analyzing so that I can focus on relevant sections.
"""
import streamlit as st
import os
from services.presentation import PresentationService, UploadedFile
from services.integrations import PdfConverseIntegration
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.DEBUG)



def handle_file_uploaded(uploaded_file,st_file,prompt,gemini_key):
    file_bytes = st_file.getbuffer()
    pdfconverse = PdfConverseIntegration.initialize_services_by_bytes(file_bytes,gemini_key)
    page_to_summarize = st.number_input("Enter the page to summarize:", value=1)
    first_page = last_page = page_to_summarize - 1
    summary = PresentationService.get_summary(pdfconverse, first_page, last_page, uploaded_file,prompt)
    st.write(summary)


st.write("This app reads with you giving you summary of current page")
# Allow user to upload a PDF file
st_file = st.file_uploader("Choose a PDF file", type="pdf")
prompt = st.text_input("Enter a prompt:", value="Explain this to me concisely maximum 5 bullet points as simply as possible")
gemini_key =os.getenv("GEMINI_API_KEY")
password = st.text_input("Enter password:", type="password")
password_matches = password == os.getenv("PASSWORD")
if st_file is not None and password_matches:
    data = st_file.getvalue()
    uploaded_file = UploadedFile(name=st_file.name, type=st_file.type, size=st_file.size, data=data)
    handle_file_uploaded(uploaded_file,st_file,prompt,gemini_key)
else:
    st.write("Please upload a PDF file to proceed.")
