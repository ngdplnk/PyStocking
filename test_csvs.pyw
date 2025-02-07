import os
import sys
import csv
import random

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
DATA_PATH = os.path.join(PROGRAM_PATH, 'data')
STOCK_SCHOOL_PATH = os.path.join(DATA_PATH, 'stock_school.pystk')
STOCK_OFFICE_PATH = os.path.join(DATA_PATH, 'stock_office.pystk')
STOCK_BOOKS_PATH = os.path.join(DATA_PATH, 'stock_books.pystk')

# Generate Books CSV
books_data = []
num_books = random.randint(237, 1024)

for i in range(1, num_books + 1):
    books_data.append([
        i,
        f"Book Title {i}",
        f"Author {random.randint(1, 100)}",
        f"Editorial {random.randint(1, 50)}",
        f"Edition {random.randint(1, 10)}",
        f"Description of Book {i}",
        random.randint(100, 1000),
        round(random.uniform(1.5, 15.0), 2),
        round(random.uniform(10.0, 100.0), 2),
        random.randint(1, 50)
    ])

# Generate School Items CSV
categories = ["Stationery", "Electronics", "Furniture", "Accessories", "Sports", "Art Supplies"]
brands = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E", "Brand F"]
colors = ["Red", "Blue", "Black", "White", "Green", "Yellow", "Purple", "Orange"]
school_items_data = []
num_school_items = random.randint(237, 1024)

for i in range(1, num_school_items + 1):
    school_items_data.append([
        i,
        random.choice(categories),
        f"Item Name {i}",
        random.choice(brands),
        random.choice(colors),
        f"Description of Item {i}",
        round(random.uniform(5.0, 200.0), 2),
        random.randint(1, 200),
        random.randint(1, 50)
    ])

# Generate Office Items CSV
office_items_data = []
num_office_items = random.randint(237, 1024)

for i in range(1, num_office_items + 1):
    office_items_data.append([
        i,
        random.choice(categories),
        f"Item Name {i}",
        random.choice(brands),
        random.choice(colors),
        f"Description of Item {i}",
        round(random.uniform(5.0, 200.0), 2),
        random.randint(1, 200),
        random.randint(1, 50)
    ])

# Save files
with open(STOCK_BOOKS_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(books_data)

with open(STOCK_SCHOOL_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(school_items_data)

with open(STOCK_OFFICE_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(office_items_data)
