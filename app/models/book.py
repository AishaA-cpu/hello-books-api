from app import db # give us access to the SQLA db


class Book(db.Model): #inherit from db's set models
    id = db.Column(db.Integer, primary_key=True, autoincrement= True) # create a column in the DB
    title = db.Column(db.String) # create a column named title and data type string
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates= "books")
    #__tablename__ = "books" we can reset the default table name SQLA sets using this line
