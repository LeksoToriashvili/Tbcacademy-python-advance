import faker
import sqlite3


def create_authors_table(conn):
    cur = conn.cursor()

    query = """CREATE TABLE IF NOT EXISTS authors (
    id integer PRIMARY KEY,
    name text NOT NULL,
    surname text NOT NULL,
    birth_date text NOT NULL,
    birth_place text NOT NULL,
    );"""

    cur.execute(query)
    conn.commit()

    from faker import Faker
    fake = Faker()
    names = [fake.unique.name() for i in range(500)]
    birth_dates = [fake.date() for i in range(500)]
    cities = [fake.city() for i in range(500)]

    query ='''INSERT INTO authors (name, surname, birth_date, birth_place)'''


def create_books_table():
    pass


def main():
    conn = sqlite3.connect('database.sqlite3')
    create_authors_table(conn)

    conn.close()


if __name__ == '__main__':
    main()
