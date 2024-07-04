"""
PDF Upload
As a user, I want to upload a PDF file to the application so that I can interact with its content using AI.
Page Range Selection
As a user, I want to specify a range of pages from the uploaded PDF that I'm interested in analyzing so that I can focus on relevant sections.
"""
import streamlit as st
import os
from pdfconverse import PDFConverse
from pdfconverse.models import FilePath,GeminiSetup
from services.models import FirebaseCache
import logging 
from hashlib import md5

from dotenv import load_dotenv
load_dotenv()

# Set up your PDF path and Gemini API key. Assuming you have a .env file with the Gemini API key
pdf_path = FilePath(path="./map_reduce.pdf")

gemini_setup=GeminiSetup(api_key=os.getenv("GEMINI_API_KEY"),model="gemini-1.5-flash")

# Initialize PDFConverse
pdfconverse = PDFConverse(pdf_path=pdf_path, gemini_setup=gemini_setup)
st.write("This app gives you summaries of pdfs")

#get beginning of the pdf
page_to_summarize = st.number_input("Enter the page to summarize:", value=1)
first_page=last_page=page_to_summarize-1
#I want to store the summary on an infile database in such a way that I first check if the prompt has been given before if so take it from there if not then give the prompt
key: str = md5(f"summary_{first_page}_{last_page}_{pdf_path.path}".encode('utf-8')).hexdigest()
summary = FirebaseCache().get(key)
if summary is None:
    logging.info(msg = f"No summary found for {key}, generating new summary")
    summary = pdfconverse.page(page_start=first_page, page_end=last_page).prompt("Explain this to me concisely maximum 5 bullet points as simply as possible")
    FirebaseCache().set(key, summary)
    

st.write("The key for the page is: ",key)
st.write(summary)