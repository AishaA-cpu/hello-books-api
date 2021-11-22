# Act and assert steps happen here 
#from app.routes import handle_books

# get all books and return no records


def test_get_all_books_with_no_records(client): # use the client fixture to run this test
    # "client" does not need to be imported from "conftest" because of the way the files are structured 
    # and the naming conventions


    #Act
    response = client.get("/books") # send a get request to the books endpoint, remeber this EP leads to the test db
    response_body  = response.get_json() # get the body of the request in the response body variable, turn the data into a json

    assert response.status_code == 200
    assert response_body == []

    


def test_get_book_by_id(client, two_saved_books):
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title" : "Ocean Book",
        "description": "watr 4eva"
    }