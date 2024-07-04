import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

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
