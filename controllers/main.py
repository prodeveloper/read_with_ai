import os
from pdfconverse import PDFConverse
from pdfconverse.models import FilePath,GeminiSetup

from dotenv import load_dotenv
load_dotenv()

# Set up your PDF path and Gemini API key. Assuming you have a .env file with the Gemini API key
pdf_path = FilePath(path="./map_reduc.pdf")

gemini_setup=GeminiSetup(api_key=os.getenv("GEMINI_API_KEY"),model="gemini-1.5-flash")

# Initialize PDFConverse
pdfconverse = PDFConverse(pdf_path=pdf_path, gemini_setup=gemini_setup)

# Get a summary of the first page
summary = pdfconverse.page(page_start=0, page_end=0).prompt("Give me a summary")
print(summary)