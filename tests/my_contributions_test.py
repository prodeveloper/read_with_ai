from io import BytesIO
from google.cloud import storage
from pypdf import PdfReader
import os
from config import ConfigLoader

def setup():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ConfigLoader().configs.GOOGLE_APPLICATION_CREDENTIALS
def test_gcloud_pdfreader_integration():
    setup()
    storage_client = storage.Client()
    blob = storage_client.bucket('books-to-master').blob('sample.pdf')
    file_stream = BytesIO()
    blob.download_to_file(file_stream)
    reader = PdfReader(file_stream)
    content_page_1 = reader.pages[0].extract_text()
    assert "Chencha" in content_page_1
    assert reader is not None