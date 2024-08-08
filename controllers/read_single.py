"""
PDF Upload
As a user, I want to upload a PDF file to the application so that I can interact with its content using AI.
Page Range Selection
As a user, I want to specify a range of pages from the uploaded PDF that I'm interested in analyzing so that I can focus on relevant sections.
"""
import streamlit as st
import os
from commands.reader import ReadSinglePageCmd
from services.presentation import PresentationService, UploadedFile
from services.integrations import PdfConverseIntegration
import logging
from dotenv import load_dotenv
from config import ConfigLoader
load_dotenv()
import asyncio



def main():
    st.write("This app reads with you giving you summary of current page")
    # Allow user to upload a PDF file
    st_file = st.file_uploader("Choose a PDF file", type="pdf")
    prompt = ConfigLoader().get_prompt()
    page_to_summarize = st.number_input("Enter the page to summarize:", value=0)
    if st_file is not None and page_to_summarize > 0:
        data = st_file.getvalue()
        uploaded_file = UploadedFile(name=st_file.name, data=data)
        readcmd = ReadSinglePageCmd(
            page_no=page_to_summarize,
            prompt=prompt,
            uploaded_file=uploaded_file,
            st_file=st_file
        )
        asyncio.run(readcmd.run())
        st.write(readcmd.summary)
    else:
        st.write("Please upload a PDF file and select a page to summarize.")
