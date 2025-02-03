import os
import sys
import csv
import random

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
BOOKS_PATH = os.path.join(SAVES_PATH, 'books.pystk')
OFFICE_PATH = os.path.join(SAVES_PATH, 'office.pystk')

# Generate Books CSV
books_headers = ["ID", "Book Name", "Author", "Editorial", "Pages", "Photocopy price", "Book price", "Quantity"]
books_data = []

for i in range(1, 251):  # 250 books
    books_data.append([
        i,
        f"Book {i}",
        f"Author {random.randint(1, 50)}",
        f"Editorial {random.randint(1, 20)}",
        random.randint(100, 1000),
        round(random.uniform(1.5, 15.0), 2),
        round(random.uniform(10.0, 100.0), 2),
        random.randint(1, 50)
    ])

# Generate Office Items CSV
office_items_headers = ["ID", "Category", "Product Name", "Brand", "Color", "Price", "Quantity"]
categories = ["Stationery", "Electronics", "Furniture", "Accessories"]
brands = ["Brand A", "Brand B", "Brand C", "Brand D"]
colors = ["Red", "Blue", "Black", "White", "Green", "Yellow"]
office_items_data = []

for i in range(1, 220):  # 219 office items
    office_items_data.append([
        i,
        random.choice(categories),
        f"Product {i}",
        random.choice(brands),
        random.choice(colors),
        round(random.uniform(5.0, 200.0), 2),
        random.randint(1, 100)
    ])

# Save files
with open(BOOKS_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(books_headers)
    writer.writerows(books_data)

with open(OFFICE_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(office_items_headers)
    writer.writerows(office_items_data)
