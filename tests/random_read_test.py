
from random_read import gen_setup_intro, gen_book_of_day

def test_gen_setup_intro():
    query_params = {'password': 'wrong_password'}
    result = gen_setup_intro(query_params)
    assert result == False

def test_gen_book_of_day():
    file_name, stream, first_page, last_page, uploaded_file = gen_book_of_day()
  
    assert file_name is not None
    assert stream is not None
    assert first_page is not None
    assert first_page > 0
    assert last_page > 0
    assert first_page == last_page
    assert uploaded_file is not None
    