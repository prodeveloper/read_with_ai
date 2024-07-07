from services.books_to_master import files_list
import streamlit as st
import random
from services.integrations import PdfConverseIntegration
from services.presentation import PresentationService, UploadedFile
import configparser
import os
from collections import namedtuple
from config import ConfigLoader




def gen_book_of_day():        
    file = random.choice(files_list)
    first_page = last_page = random.randint(file.page_start, file.page_end)
    file_name = "files/"+file.name
    stream = file.stream
    with open(file_name, "rb") as f:
        file_data = f.read()
    uploaded_file = UploadedFile(name=file.name,data=file_data)
    return file_name, stream,first_page, last_page, uploaded_file

def gen_setup_intro():
    st.write("This app gives a random quick summary from the books I am currently reading")
    query_params = st.query_params
    entered_password = query_params.get("password", "")
    password_verified = True if entered_password == ConfigLoader().configs.LOCAL_PASSWORD else False
    return  password_verified
def display_summary():
    prompt = st.text_input("Enter a prompt:", value="Explain this to me concisely maximum 5 bullet points as simply as possible")
    file_name, stream, first_page, last_page, uploaded_file = gen_book_of_day()
    pdfconverse = PdfConverseIntegration.initialize_services_by_file_path(file_name,ConfigLoader().configs.GEMINI_API_KEY)
    summary = PresentationService.get_summary(pdfconverse, first_page, last_page, uploaded_file,prompt)
    st.write(f"Today stream {stream} and book is {file_name} page {first_page}")
    st.write(summary)


password_verified = gen_setup_intro()

if password_verified:
    display_summary()

