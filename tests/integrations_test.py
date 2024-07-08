from services.integrations import BlobStorageIntegration, PdfConverseIntegration
from config import ConfigLoader
from pypdf import PdfReader
from pdfconverse import PDFConverse



def test_file_stream_from_blob_storage():
    file_path = "sample.pdf"
    bucket_name = "books-to-master"
    file_stream = BlobStorageIntegration().file_stream_from_blob_storage(file_path, bucket_name)
    assert file_stream is not None

def test_initialize_services_by_bytes():
    file_path = "sample.pdf"
    bucket_name = "books-to-master"
    file_stream = BlobStorageIntegration().file_stream_from_blob_storage(file_path, bucket_name)
    gemini_key = ConfigLoader().configs.GEMINI_API_KEY
    pdf_converse_integration: PDFConverse = PdfConverseIntegration.initialize_services_by_bytes(file_stream, gemini_key)
    assert pdf_converse_integration is not None
    assert isinstance(pdf_converse_integration, PDFConverse)
    pdf_doc = PdfReader(file_stream)
    assert pdf_doc is not None
    text_contained = "Chencha"
    assert text_contained in pdf_doc.pages[0].extract_text()

