"""
PDF Upload
As a user, I want to upload a PDF file to the application so that I can interact with its content using AI.
Page Range Selection
As a user, I want to specify a range of pages from the uploaded PDF that I'm interested in analyzing so that I can focus on relevant sections.
"""
import streamlit as st
import os
from pdfconverse import PDFConverse
from pdfconverse.models import FilePath, GeminiSetup
from services.models import FirebaseCache
import logging
from hashlib import md5
from dotenv import load_dotenv
load_dotenv()

def generate_unique_file_name(uploaded_file):
    file_md5 = md5(uploaded_file.getbuffer()).hexdigest()
    return f"{file_md5}{file_md5}.pdf"

def generate_unique_key(page_start, page_end, file_name):
    return md5(f"summary_{page_start}_{page_end}_{file_name}".encode('utf-8')).hexdigest()

def initialize_services(file_name):
    pdf_path = FilePath(path=file_name)
    gemini_setup = GeminiSetup(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-1.5-flash")
    return PDFConverse(pdf_path=pdf_path, gemini_setup=gemini_setup)

def get_summary(pdfconverse, page_start, page_end, file_name):
    key: str = generate_unique_key(page_start, page_end, file_name)
    summary = FirebaseCache().get(key)
    if summary is None:
        logging.info(msg=f"No summary found for {key}, generating new summary")
        summary = pdfconverse.page(page_start=page_start, page_end=page_end).prompt("Explain this to me concisely maximum 5 bullet points as simply as possible")
        FirebaseCache().set(key, summary)
    return summary

def handle_successful_upload(uploaded_file):
    # Save the uploaded file to a temporary location
    file_name = generate_unique_file_name(uploaded_file)
    with open(file_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Initialize PDFConverse
    pdfconverse = initialize_services(file_name)
    page_to_summarize = st.number_input("Enter the page to summarize:", value=1)
    first_page = last_page = page_to_summarize - 1

    summary = get_summary(pdfconverse, first_page, last_page, file_name)
    st.write(summary)


st.write("This app gives you summaries of PDFs")
# Allow user to upload a PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    handle_successful_upload(uploaded_file)
else:
    st.write("Please upload a PDF file to proceed.")
