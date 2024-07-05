from hashlib import md5
from pydantic import BaseModel, validator
import logging
from services.models import FirebaseCache
logging.basicConfig(level=logging.DEBUG)

class UploadedFile(BaseModel):
    name: str
    type: str
    size: int
    data: bytes

class KeyDetails(BaseModel):
    page_start: int
    page_end: int
    uploaded_file: UploadedFile


    @validator('page_end')
    def check_page_range(cls, page_end, values):
        if 'page_start' in values and page_end < values['page_start']:
            raise ValueError('page_end must be greater than or equal to page_start')
        return page_end
    

class PresentationService:
    @staticmethod
    def generate_unique_file_name(uploaded_file: UploadedFile):
        file_md5 = md5(uploaded_file.data).hexdigest()
        return f"{uploaded_file.name}{file_md5}.pdf"
    @staticmethod
    def generate_unique_key(key_details: KeyDetails):
        file_md5 = md5(key_details.uploaded_file.data).hexdigest()
        return f"summary_{key_details.page_start}_{key_details.page_end}_{key_details.uploaded_file.name}_{file_md5}"
    @staticmethod
    def get_summary(pdfconverse, page_start:int, page_end:int, uploaded_file: UploadedFile,prompt:str):
        key_details = KeyDetails(page_start=page_start, page_end=page_end, uploaded_file=uploaded_file)
        key: str = PresentationService.generate_unique_key(key_details)
        summary = FirebaseCache().get(key)
        if summary is None:
            logging.debug(msg=f"No summary found for {key}, generating new summary")
            summary = pdfconverse.page(page_start=page_start, page_end=page_end).prompt(prompt)
        FirebaseCache().set(key, summary)
        return summary

        