from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)

    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    rating = Column(Integer)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="reviews")
