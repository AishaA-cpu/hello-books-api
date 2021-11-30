from app import db

class BookGenre(db.Model):
    __tablename__ = "books_genre"
    book_id = db.Column("book_id", db.ForeignKey("book.id"), primary_key=True, nullable=False)
    genre_id = db.Column("genre_id", db.ForeignKey("genre.id"), primary_key=True, nullable=False)
