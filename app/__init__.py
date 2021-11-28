from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv # py-dotenv specifies to import .env like this
import os # this module is imported to read enviroment variables
# Our database development workflow will be as follows:

# Set up the database on the Flask end once
# Generate migration files
# Apply the migration files

db = SQLAlchemy() #create an instance of SQLAlchemy
migrate = Migrate() # Create and instance of migrate to develop instructions and make chages to the DB
load_dotenv() # import packages from the .env file so that os can see them


def create_app(test_config=None): # test_config is set to None as default so that it is not req.
    app = Flask(__name__)

    
    if not test_config:
        print("printing from dev database")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #configure settings for SQLA
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') # tells flask to connect to database using psycopg2
    else:
        print("printing from test database")
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #configure settings for SQLA
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI') # tells flask to connect to database using psycopg2
    
    # import models
    from app.models.book import Book
    from app.models.author import Author

    db.init_app(app) # connects db to flask app
    migrate.init_app(app, db) # connects migrate to flask app and db
    
    from .routes import books_bp, authors_bp
    
    
    # register the blueprint
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    #from .routes import hello_world_bp # essentially, we are telling the flask framework to import the blueprint we created

    


    #app.register_blueprint(hello_world_bp) # we are telling flask to register the blueprint we created so the server knows about it so it knows to use
                                        # the blue print we created for our routes/endpoints

    #from .routes import books_bp       # here  use the same create app because its all for the same app project
    #app.register_blueprint(books_bp)  

    return app 





















