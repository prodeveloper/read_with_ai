
from services.presentation import PresentationService, UploadedFile, KeyDetails
from unittest.mock import MagicMock

def test_generate_unique_file_name():
    expected = "test_file098f6bcd4621d373cade4e832627b4f6.pdf"
    uploaded_file = UploadedFile(name="test_file", type="pdf", size=100, data=b"test")
    assert PresentationService.generate_unique_file_name(uploaded_file) == expected
def test_generate_unique_key():
    expected = "summary_1_10_test_file_098f6bcd4621d373cade4e832627b4f6"
    uploaded_file = UploadedFile(name="test_file", type="pdf", size=100, data=b"test")
    key_details = KeyDetails(page_start=1, page_end=10, uploaded_file=uploaded_file)
    assert PresentationService.generate_unique_key(key_details) == expected

def test_generate_summary():
    mock_pdfconverse = MagicMock()
    mock_pdfconverse.page.return_value.prompt.return_value = "Mocked Summary"
    prompt = "Help me put this as a mece list"
    uploaded_file = UploadedFile(name="test_file", type="pdf", size=100, data=b"test")
    assert PresentationService.get_summary(mock_pdfconverse, 1, 10, uploaded_file,prompt) == "Mocked Summary"