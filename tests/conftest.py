# holds all the fixtures, this pretty much handles the arrange step of pytest

import pytest # import the pytest module for testting
from app import create_app # import the defined create app module so we can always create an instance of the app for testing
from app import db # import the database 
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING": True}) # makes sure we swap to a testing database because testing is true

    with app.app_context(): # within this context of our app, this version of our app, the testing database
        db.create_all() # create a database, create a db solely in the test environment # generate test database
        yield app # provide the calling test with that database

    with app.app_context(): # within this context of our app
        db.drop_all() # clean up the database created , drop it 


@pytest.fixture
def client(app): # makes the request, calls the routes, will be used to send HTTP requests to endpoints 
    return app.test_client()


@pytest.fixture
def two_saved_books(app): # call the app fixture, create a fixture that saves two books in the db
    # arrange
    ocean_book = Book( # create book instance
        title= "Ocean Book",
        description= "watr 4eva"
    )
    mountain_book = Book( #create book instance
        title="Mountain Book",
        description= "i luv to climb rocks"
    )

    db.session.add_all([ocean_book, mountain_book]) # add the books to the database, this is an alternative to add all instances as a list
    # instead of adding one after the other 
    db.session.commit()  #commit the book to the database





