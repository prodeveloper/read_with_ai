from services.books_to_master import files_list
import streamlit as st
import random
from services.integrations import PdfConverseIntegration, BlobStorageIntegration
from services.presentation import PresentationService, UploadedFile
from config import ConfigLoader


def main():
    st.write("This app gives a random quick summary from the books I am currently reading")
    password_verified = gen_setup_intro(query_params=st.query_params)
    if password_verified:
        prompt = st.text_input("Enter a prompt:", value="Explain this to me concisely maximum 5 bullet points as simply as possible")
        summary,stream, file_name, first_page = gen_summary(prompt)
        st.write(f"Today stream {stream} and book is {file_name} page {first_page}")
        st.write(summary)

def gen_book_of_day():        
    file = random.choice(files_list)
    first_page = last_page = random.randint(file.page_start, file.page_end)
    stream = file.stream
    file_name=file.name
    file_data = BlobStorageIntegration().file_stream_from_blob_storage(file.name, "books-to-master")
    uploaded_file = UploadedFile(name=file.name,data=file_data)
    return file_name, stream,first_page, last_page, uploaded_file

def gen_setup_intro(query_params):
    entered_password = query_params.get("password", "")
    password_verified = True if entered_password == ConfigLoader().configs.LOCAL_PASSWORD else False
    return  password_verified
def gen_summary(prompt):
    file_name, stream, first_page, last_page, uploaded_file = gen_book_of_day()
    pdfconverse = PdfConverseIntegration.initialize_services_by_bytes(uploaded_file.data,ConfigLoader().configs.GEMINI_API_KEY)
    summary = PresentationService.get_summary(pdfconverse, first_page, last_page, uploaded_file,prompt)
    return summary, stream, file_name, first_page



