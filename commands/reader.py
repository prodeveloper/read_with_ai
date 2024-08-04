from models.books_to_master import gen_book_of_day, gen_custom_book_of_day
from services.integrations import PdfConverseIntegration
from services.presentation import PresentationService, UploadedFile
from config import ConfigLoader
from pypdf import PdfReader
import asyncio

class RandomReadCmd:
    today_book = None
    summary = None
    prompt = None
    full_text = None
    run_state= None
    stream=None
    def __init__(self,stream:str=None):
        self.stream = stream
        self.run_state = False

    async def run(self):
        if self.stream:
            self.today_book = gen_custom_book_of_day(self.stream)
        else:
            self.today_book = gen_book_of_day()
        self.prompt = ConfigLoader().get_prompt()
        await self.gen_summary()
        self.get_text()
        self.run_state = True

    async def gen_summary(self):
        pdfconverse = PdfConverseIntegration.initialize_services_by_bytes(
            self.today_book.uploaded_file.data,
            ConfigLoader().configs.GEMINI_API_KEY
        )
        self.summary = PresentationService.get_summary(
            pdfconverse, 
            self.today_book.first_page, 
            self.today_book.last_page, 
            self.today_book.uploaded_file,
            self.prompt
        )
    
    def get_text(self):
        reader = PdfReader(self.today_book.uploaded_file.data)
        page = reader.pages[self.today_book.first_page]
        self.full_text = page.extract_text()

class ReadSinglePageCmd:
    page_no:int = None
    prompt: str = None
    full_text: str = None
    summary: str = None
    run_state: bool = None
    uploaded_file: UploadedFile = None
    gemini_key: str = None
    st_file = None
    file_name: str = None

    def __init__(self,*,page_no:int,prompt:str,uploaded_file:UploadedFile,st_file):
        self.page_no = page_no
        self.prompt = prompt
        self.uploaded_file = uploaded_file
        self.run_state = False
        self.gemini_key = ConfigLoader().configs.GEMINI_API_KEY
        self.st_file = st_file

    async def run(self):
        self._gen_file_name()
        self._save_file()
        self._gen_summary()
        self.run_state = True
    

    def _gen_file_name(self):
        self.file_name = PresentationService.generate_unique_file_name(self.uploaded_file)
    
    def _save_file(self):
        with open(self.file_name, "wb") as f:
            f.write(self.st_file.getbuffer())
    def _gen_summary(self):
        pdfconverse = PdfConverseIntegration.initialize_services_by_file_path(self.file_name,self.gemini_key)
        first_page = last_page = self.page_no -1
        self.summary = PresentationService.get_summary(pdfconverse,first_page,last_page,self.uploaded_file,self.prompt)
    def __getattr__(self, name):
        if not self.run_state:
            raise RuntimeError("Command has not run. Try running the command first.")
        return self.__dict__.get(name)