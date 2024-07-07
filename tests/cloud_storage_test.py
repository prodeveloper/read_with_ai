#I want to print python version
import sys
print(sys.version)
import os
from dotenv import load_dotenv
from services.models import FirebaseCache
from services.integrations import FirebaseIntegration, PdfConverseIntegration
load_dotenv()



def test_cloud_storage():
    db = FirebaseIntegration.get_db()
    doc_ref = db.collection("users").document("alovelace")
    doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    users_ref = db.collection("users")
    #I want to assert that the document was created
    assert users_ref.document("alovelace").get().exists
    #delete the record
    doc_ref.delete()
    #I want to assert that the document was deleted
    assert not users_ref.document("alovelace").get().exists

def test_firebase_integration():
    db = FirebaseIntegration.get_db()
    assert db is not None       

def test_cache():
    cache = FirebaseCache()
    cache.set("test", "test")
    assert cache.get("test") == "test"

def test_cache_invalid_key():
    cache = FirebaseCache()
    assert cache.get("invalid_key") is None

def test_keys_loaded():
    assert os.getenv("GEMINI_API_KEY") is not None
    assert os.getenv("FIREBASE_SERVICE_ACCOUNT") is not None

def test_pdf_converse_integration():
    pdf_path = os.path.abspath("./files/sample.pdf")
    pdf_converse = PdfConverseIntegration.initialize_services_by_file_path(pdf_path, os.getenv("GEMINI_API_KEY"))
    assert pdf_converse is not None
def test_pdf_converse_integration_by_bytes():
    pdf_path = os.path.abspath("./files/sample.pdf")
    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()
    pdf_converse = PdfConverseIntegration.initialize_services_by_bytes(pdf_bytes, os.getenv("GEMINI_API_KEY"))
    assert pdf_converse is not None

