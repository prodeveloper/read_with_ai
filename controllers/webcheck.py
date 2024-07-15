from tests import cloud_storage_test, integrations_test
import streamlit as st
def firebase_works():
    try:
        cloud_storage_test.test_firebase_integration()
        return True
    except Exception as e:
        st.write("Firebase failed with message",e)
        return False
def pdf_converse_works():
    try:
        cloud_storage_test.test_pdf_converse_integration()
        return True
    except Exception as e:
        st.write("PDF Converse failed with message",e)
        return False
def pdf_converse_works_by_bytes():
    try:
        cloud_storage_test.test_pdf_converse_integration_by_bytes()
        return True
    except Exception as e:
        st.write("PDF Converse failed with message",e)
        return False
    
def can_read_credentials():
    try:
        cloud_storage_test.test_keys_loaded()
        return True
    except Exception as e:
        st.write("Credentials failed with message",e)
        return False
def main():
    st.write("Checking if the services work")
    if firebase_works():
        st.write("1. Firebase works")
    if pdf_converse_works():
        st.write("2. PDF Converse works")
    if pdf_converse_works_by_bytes():
        st.write("3. PDF Converse works by bytes")
    if can_read_credentials():
        st.write("4. Credentials are loaded")
    

    