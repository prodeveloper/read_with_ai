from collections import namedtuple
import random
from services.integrations import BlobStorageIntegration
from services.presentation import UploadedFile
from models.random_read_data import TodayBook


File = namedtuple("File", ["name", "stream","page_start","page_end"])
files_list =[
    File(
        name="designing_data_intensive.pdf", 
        stream="Data Engineering", 
        page_start=19, 
        page_end=700
    ),
    File(
        name="Designing_Distributed_Systems_Burns.pdf", 
        stream="System Design Interview", 
        page_start=36, 
        page_end=206
    ),
    File(
        name="System_design_interview_alex.pdf", 
        stream="System Design Interview", 
        page_start=8, 
        page_end=325
    ),
    File(
        name="cracking_coding_interview.pdf", 
        stream="coding", 
        page_start=35, 
        page_end=662
    ),

]

custom_files_list = [
    File(
        name="mobile_payments.pdf",
        stream="jp_morgan",
        page_start=13,
        page_end=126
    ),
]

def gen_book_of_day(stream=None):        
    file = get_file(stream)
    first_page = last_page = random.randint(file.page_start, file.page_end)
    stream = file.stream
    file_name=file.name
    file_data = BlobStorageIntegration().file_stream_from_blob_storage(file.name, "books-to-master")
    uploaded_file = UploadedFile(name=file.name,data=file_data)
    today_book = TodayBook(file_name, stream, first_page, last_page, uploaded_file)
    return today_book

def get_file(stream=None):
    if stream:
        files = [file for file in custom_files_list if file.stream == stream]
        if not files:
            raise BookStreamNotFound(f"No files found for stream: {stream}")
    else:
        files = files_list
    return random.choice(files)


class BookStreamNotFound(Exception):
    """Raised when a book stream is not found"""
