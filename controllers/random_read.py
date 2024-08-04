import streamlit as st
from config import ConfigLoader
from commands.reader import RandomReadCmd
import asyncio


def main(stream=None):
    password_verified = gen_setup_intro(query_params=st.query_params)
    if password_verified:
        readcmd = RandomReadCmd(stream)
        asyncio.run(readcmd.run())
        st.write(f"Today stream {readcmd.today_book.stream} and book is {readcmd.today_book.file_name} page {readcmd.today_book.first_page}")
        st.write(readcmd.summary)
        st.write("-------------------- <-- END OF SUMMARY --> --------------------")
        st.write("The full content is below")
        st.write(readcmd.full_text)


def gen_setup_intro(query_params):
    entered_password = query_params.get("password", "")
    password_verified = True if entered_password == ConfigLoader().configs.LOCAL_PASSWORD else False
    return  password_verified




