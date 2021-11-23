# Act and assert steps happen here 
# from app.routes import handle_books
# think of other test cases that can be created, based on your end points 
# notice we do not need to run flasjk server to test our routes, because client here serves as the clietnt
# get all books and return no records

import json

def test_get_all_books_with_no_records(client): # use the client fixture to run this test
    # "client" does not need to be imported from "conftest" because of the way the files are structured 
    # and the naming conventions


    #Act
    response = client.get("/books") # send a get request to the books endpoint, remeber this EP leads to the test db
    response_body  = response.get_json() # get the body of the request in the response body variable, turn the data into a json

    assert response.status_code == 200
    assert response_body == []

def test_get_book_by_id(client, two_saved_books): # use the two saved books fixture and client fixture
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 200 # assert the code you want to receive in the json body
    assert response_body == {
        "id": 1,
        "title" : "Ocean Book",
        "description": "watr 4eva"
    }

def test_get_book_by_id_returns_no_book_for_unavailable_book(client, two_saved_books):
    response = client.get('/books/3')
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None

def test_get_book_from_empty_database_returns_none(client):
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None

def test_get_all_books_in_database_returns_all_books_in_database(client, two_saved_books):
    response = client.get("/books")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title" : "Ocean Book",
        "description": "watr 4eva"
    }, {
        "id": 2,
        "title" : "Mountain Book",
        "description":"i luv to climb rocks"
    }]

def test_post_book_to_database_returns_success_code(client):
    response = client.post(
        "/books", json = {"title" : "Harry Potter",
        "description": "watr 4eva"}
        )

    response_body = response.get_json()
    assert response.status_code == 201


    # request body is received from client with information on the book to be created 
    # using the body, a new book instance is created 
    # new book instance is posted to database
    # book should be in data base 
    # client should get a success code
    # confirm that the database contains the book 
    # confirm that the status code is 200 

