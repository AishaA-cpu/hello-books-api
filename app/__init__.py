from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Our database development workflow will be as follows:

# Set up the database on the Flask end once
# Generate migration files
# Apply the migration files

db = SQLAlchemy() #create an instance of SQLAlchemy
migrate = Migrate() # Create and instance of migrate to develop instructions and make chages to the DB

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #configure settings for SQLA
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development' # tells flask to connect to database using psycopg2


    # import models
    from app.models.book import Book

    db.init_app(app) # connects db to flask app
    migrate.init_app(app, db) # connects migrate to flask app and db
    
    from .routes import books_bp

    # register the blueprint
    app.register_blueprint(books_bp)

    #from .routes import hello_world_bp # essentially, we are telling the flask framework to import the blueprint we created

    


    #app.register_blueprint(hello_world_bp) # we are telling flask to register the blueprint we created so the server knows about it so it knows to use
                                        # the blue print we created for our routes/endpoints

    #from .routes import books_bp       # here  use the same create app because its all for the same app project
    #app.register_blueprint(books_bp)  

    return app 





















