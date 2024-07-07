import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from pdfconverse.models import FilePath, GeminiSetup
from pdfconverse import PDFConverse

load_dotenv()

class FirebaseIntegration:
    def __init__(self):
        self.db = None

    def setup(self):
        # Check if the app is already initialized. This fails if the app is not initialized. or if you try to initialize it twice. 
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    @staticmethod
    def get_db():
        db = FirebaseIntegration()
        if not db.db:
            db.setup()
        return db.db
    def get_collection(self, collection_name: str):
        return self.db.collection(collection_name)
    def get_document(self, collection_name: str, document_id: str):
        return self.db.collection(collection_name).document(document_id)
    
class PdfConverseIntegration:
    @staticmethod
    def initialize_services_by_file_path(file_name,gemini_key):
        file_path = FilePath(path=file_name)
        gemini_setup = GeminiSetup(api_key=gemini_key, model="gemini-1.5-flash")
        return PDFConverse(gemini_setup=gemini_setup, file_path=file_path)
    @staticmethod
    def initialize_services_by_bytes(file_bytes,gemini_key):
        gemini_setup = GeminiSetup(api_key=gemini_key, model="gemini-1.5-flash")
        return PDFConverse(gemini_setup=gemini_setup, bytes=file_bytes)
