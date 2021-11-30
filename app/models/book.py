from sqlalchemy.orm import backref
from app import db # give us access to the SQLA db


class Book(db.Model): #inherit from db's set models
    id = db.Column(db.Integer, primary_key=True, autoincrement= True) # create a column in the DB
    title = db.Column(db.String) # create a column named title and data type string
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates= "books")
    genres = db.relationship("Genre", secondary="books_genre", backref = "books")
    
    #__tablename__ = "books" we can reset the default table name SQLA sets using this line
    def to_dict(self):
        genres = []
        for genre in self.genres:
            genres.append(genre.name)

        if self.author:
            author = self.author.name
        else:
            author = None

        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "genres" : genres,
            "author" : author
        }
