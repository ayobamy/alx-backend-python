# Python Generators

## Task 0
- `def connect_db():` connects to the mysql database server
- `def create_database(connection):` creates the database ALX_prodev if it does not exist
- `def connect_to_prodev():` connects the the ALX_prodev database in MYSQL
- `def create_table(connection):` creates a table user_data if it does not exists with the required fields
- `def insert_data(connection, data):` inserts data in the database if it does not exist

## Task 1
- `def stream_users():` create a generator that streams rows from an SQL database one by one

## Task 2
- `stream_users_in_batches(batch_size):` func that fetches rows in batches
- `def batch_processing(batch_size):` func that processes each batch to filter users over the age of *25*

## Task 3
- `def lazy_paginate(page_size):`  a generator function lazy paginates

## Task 4
- `stream_user_ages():` func that yields user ages one by one
- `calculate_average_age(conn):` func that calculates average ages
