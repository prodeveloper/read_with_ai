from models.books_to_master import files_list
import streamlit as st
from services.integrations import PdfConverseIntegration
from services.presentation import PresentationService
from config import ConfigLoader
from models.random_read_data import TodayBook
from models.books_to_master import gen_book_of_day
from pypdf import PdfReader


def main():
    password_verified = gen_setup_intro(query_params=st.query_params)
    if password_verified:
        prompt = "Explain this to me concisely maximum 5 bullet points as simply as possible. Use metaphors and analogies to explain the concepts."
        summary,today_book = gen_summary(prompt,gen_book_of_day)
        st.write(f"Today stream {today_book.stream} and book is {today_book.file_name} page {today_book.first_page}")
        st.write(summary)
        st.write("-------------------- <-- END OF SUMMARY --> --------------------")
        st.write("The full content is below")
        st.write(get_text(today_book))
    



def gen_setup_intro(query_params):
    entered_password = query_params.get("password", "")
    password_verified = True if entered_password == ConfigLoader().configs.LOCAL_PASSWORD else False
    return  password_verified
def gen_summary(prompt, gen_book_of_day:callable):
    today_book: TodayBook = gen_book_of_day()
    pdfconverse = PdfConverseIntegration.initialize_services_by_bytes(today_book.uploaded_file.data,ConfigLoader().configs.GEMINI_API_KEY)
    summary = PresentationService.get_summary(pdfconverse, today_book.first_page, today_book.last_page, today_book.uploaded_file,prompt)
    return summary, today_book
def get_text(today_book: TodayBook):
    reader = PdfReader(today_book.uploaded_file.data)
    page = reader.pages[today_book.first_page]
    text = page.extract_text()
    return text



