import sqlite3
from faker import Faker
import random
import datetime


#find book with id and print info
def print_book(conn, id):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM book WHERE id={id}')
    book = cursor.fetchone()
    print(f"""Title: {book[1]}
    Category: {book[2]}
    Pages: {book[3]}
    Issue date: {book[4]}
    Author: {get_author(conn, book[5])}""")


def print_author(author):
    print(f"""Name: {author[1]} {author[2]}
    Birth date: {author[3]}
    Birth place: {author[4]}""")


#return author first name and last name by its id
def get_author(conn, id):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM author WHERE id={id}')
    author = cursor.fetchone()
    return f"{author[1]} {author[2]}"


# remove book table if exists, then create book table with random data
def create_book_table(conn):
    fake = Faker()
    cur = conn.cursor()

    query = "DROP TABLE IF EXISTS book"
    cur.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        pages INTEGER NOT NULL,
        date TEXT NOT NULL,
        author INTEGER NOT NULL)
    """
    cur.execute(query)

    books = tuple(
        (fake.unique.text(30)[0:-1],
         fake.word(),
         random.randint(10, 999),
         fake.date(),
         random.randint(1, 500))
        for _ in range(1000))

    query ="INSERT INTO book (title, category, pages, date, author) VALUES (?, ?, ?, ?, ?)"

    cur.executemany(query, books)


# remove author table if exists, then create author table with random data
def create_author_table(conn):
    fake = Faker()
    cur = conn.cursor()

    query = "DROP TABLE IF EXISTS author"
    cur.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            birth_place TEXT NOT NULL)
        """
    cur.execute(query)/home/lexo/Tbcacademy-python-advance/homework_5/venv/bin/python3

    authors = tuple(
        (fake.unique.first_name(),
         fake.unique.last_name(),
         fake.date_of_birth(minimum_age=18).strftime('%d.%m.%Y'),
         fake.city())
        for _ in range(500))

    query = "INSERT INTO author (first_name, last_name, birth_date, birth_place) VALUES (?, ?, ?, ?)"

    cur.executemany(query, authors)


def find_book_with_most_pages(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    data = cursor.fetchall()

    m = max(data, key=lambda x: x[3])
    print("Book with most pages:")
    print_book(conn, m[0])
    print()


def find_book_average_pages(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    data = cursor.fetchall()

    avg = sum(map(lambda x: x[3], data)) / len(data)
    print(f"Average number of pages of all books: {avg}")
    print()


def find_youngest_author(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM author")
    data = cursor.fetchall()

    author = max(data, key=lambda x: datetime.datetime.strptime(x[3], '%d.%m.%Y'))
    print("Youngest author:")
    print_author(author)
    print()


def find_author_without_book(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM author")
    authors = set(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("SELECT author FROM book")
    books = set(map(lambda x: x[0], cursor.fetchall()))
    authors_wo_books = list(authors - books)

    print("Authors without any book:")
    for author in authors_wo_books:
        print("\t", get_author(conn, author))
    print()


def find_authors_less_than_3_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM author")
    authors = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("SELECT author FROM book")
    books = list(map(lambda x: x[0], cursor.fetchall()))

    count = 0
    print("5 authors with less than 3 books:")
    for author in authors:
        if count > 4:
            break
        if books.count(author) < 3:
            print("\t", get_author(conn, author))
            count += 1


def main():
    conn = sqlite3.connect('database.sqlite3')

    create_book_table(conn)
    create_author_table(conn)
    conn.commit()

    find_book_with_most_pages(conn)
    find_book_average_pages(conn)
    find_youngest_author(conn)
    find_author_without_book(conn)
    find_authors_less_than_3_books(conn)

    conn.close()


if __name__ == '__main__':
    main()
