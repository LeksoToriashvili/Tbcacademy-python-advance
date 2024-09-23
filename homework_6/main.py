from dataclasses import replace

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, column
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from faker import Faker
import random

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    category = Column(String)
    pages = Column(Integer)
    date = Column(String)
    author = Column(Integer, ForeignKey('author.id'))


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(String)
    birth_place = Column(String)


def fill_author_table(session):
    fake = Faker()

    authors = [
        (fake.unique.first_name(),
         fake.unique.last_name(),
         fake.date_of_birth(minimum_age=18).strftime('%d.%m.%Y'),
         fake.city())
        for _ in range(500)]
    print(authors)

    for author in authors:
        session.add(Author(first_name=author[0], last_name=author[1], birth_date=author[2], birth_place=author[3]))
    session.commit()


def fill_book_table(session):
    fake = Faker()

    books = [
        (fake.unique.text(30)[0:-1],
         fake.word(),
         random.randint(10, 999),
         fake.date(),
         random.randint(1, 500))
        for _ in range(1000)]
    print(books)

    for book in books:
        session.add(Book(title=book[0], category=book[1], pages=book[2], date=book[3], author=book[4]))
    session.commit()


def print_book(book):
    print(f"""Title: {book.title}
    Category: {book.category}
    Pages: {book.pages}
    Issue date: {book.date}
    Author: {book.author}""")


def find_book_with_most_pages(session):
    book = session.query(Book).order_by(Book.pages.desc()).first()
    print_book(book)


def main():
    faker = Faker()

    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    fill_book_table(session)
    fill_author_table(session)

    find_book_with_most_pages(session)
    #find_book_average_pages(session)
    #find_youngest_author(session)
    #find_author_without_book(session)
    #find_authors_less_than_3_books(session)

    session.close()


if __name__ == '__main__':
    main()
