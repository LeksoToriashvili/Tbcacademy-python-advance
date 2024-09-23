In there are several functions which provides functionality of program:

- create_book_table(conn)  
    removes the table named book if exists and create new one with newly generated data   

- create_author_table(conn)   
    removes the table named author if exists and create new one with newly generated data   

- find_book_with_most_pages(conn)  
    finds book which contains most number of pages

- find_youngest_author(conn)  
    finds youngest author

- find_author_without_book(conn)  
    finds author which has no any book in database

- find_authors_less_than_3_books(conn)  
    finds 5 authors which has less than 3 books