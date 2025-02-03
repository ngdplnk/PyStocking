import os
import sys
import csv
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QInputDialog)
from PyQt5.QtGui import QFont

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
CATEGORIES_PATH = os.path.join(SAVES_PATH, 'cats.pystk')
BRANDS_PATH = os.path.join(SAVES_PATH, 'brands.pystk')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.pystk')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.pystk')

class AddItemsDialog(QDialog):
    def __init__(self, parent=None):
        global books_count
        global office_count
        super().__init__(parent)
        self.setWindowTitle("Add Items")
        self.setGeometry(100, 100, 400, 300)
    
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
        try:
            os.makedirs(SAVES_PATH, exist_ok=True)
    
            if not os.path.isfile(LATEST_BOOKS_PATH):
                with open(LATEST_BOOKS_PATH, 'w') as file:
                    pass
            if not os.path.isfile(LATEST_OFFICE_PATH):
                with open(LATEST_OFFICE_PATH, 'w') as file:
                    pass
    
            with open(LATEST_BOOKS_PATH, 'r') as file:
                books_count = sum(1 for line in file if line.strip())
            with open(LATEST_OFFICE_PATH, 'r') as file:
                office_count = sum(1 for line in file if line.strip())
    
            self.load_categories()
            self.load_brands()
        except Exception as e:
            print(e)
    
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Books", "Office Items"])
        self.dropdown_font = QFont()
        self.dropdown_font.setPointSize(14)
        self.dropdown.setFont(self.dropdown_font)
        self.dropdown.currentIndexChanged.connect(self.update_form)
        self.dropdown.setToolTip("Select the type of item you want to add.")
        self.layout.addWidget(self.dropdown)
    
        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
    
        self.save_button = QPushButton("Save")
        self.save_button_font = QFont()
        self.save_button_font.setPointSize(14)
        self.save_button.setFont(self.save_button_font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the item to the stock.")
        self.layout.addWidget(self.save_button)
    
        self.update_form()

    def load_categories(self):
        self.categories = set()
        if os.path.isfile(CATEGORIES_PATH):
            with open(CATEGORIES_PATH, 'r') as file:
                reader = csv.reader(file)
                self.categories = set(row[0] for row in reader)
        else:
            with open(LATEST_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.categories = set(row[1] for row in reader if row[1].strip())
            self.save_categories()

    def save_categories(self):
        with open(CATEGORIES_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            for category in sorted(self.categories):
                writer.writerow([category])

    def load_brands(self):
        self.brands = set()
        if os.path.isfile(BRANDS_PATH):
            with open(BRANDS_PATH, 'r') as file:
                reader = csv.reader(file)
                self.brands = set(row[0] for row in reader)
        else:
            with open(LATEST_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.brands = set(row[3] for row in reader if row[3].strip())
            self.save_brands()

    def save_brands(self):
        with open(BRANDS_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            for brand in sorted(self.brands):
                writer.writerow([brand])

    def get_next_available_id(self, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                ids = sorted(int(row[0]) for row in reader if row[0].isdigit())
                for i in range(1, len(ids) + 2):
                    if i not in ids:
                        return i
        except Exception as e:
            print(e)
        return 1

    def update_form(self):
        global books_count
        global office_count
    
        # Clear the form layout
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            if child.layout():
                self.clear_layout(child.layout())
    
        # Create a new form layout
        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
    
        if self.dropdown.currentText() == "Books":
            new_id = self.get_next_available_id(LATEST_BOOKS_PATH)
            self.id_label = QLabel(f"ID: {new_id}")
            self.id_label_font = QFont()
            self.id_label_font.setPointSize(14)
            self.id_label.setFont(self.id_label_font)
            self.form_layout.addWidget(self.id_label)
            
            self.name_layout = QHBoxLayout()
            self.name_label = QLabel("Book Name:")
            self.name_label.setFont(self.id_label_font)
            self.name_layout.addWidget(self.name_label)
            self.name_input = QLineEdit()
            self.name_input.setFont(self.id_label_font)
            self.name_input.setToolTip("Enter the name of the book.")
            self.name_layout.addWidget(self.name_input)
            self.form_layout.addLayout(self.name_layout)
            
            self.author_layout = QHBoxLayout()
            self.author_label = QLabel("Author:")
            self.author_label.setFont(self.id_label_font)
            self.author_layout.addWidget(self.author_label)
            self.author_input = QLineEdit()
            self.author_input.setFont(self.id_label_font)
            self.author_input.setToolTip("Enter the author of the book.")
            self.author_layout.addWidget(self.author_input)
            self.form_layout.addLayout(self.author_layout)
            
            self.edition_layout = QHBoxLayout()
            self.edition_label = QLabel("Editorial:")
            self.edition_label.setFont(self.id_label_font)
            self.edition_layout.addWidget(self.edition_label)
            self.edition_input = QLineEdit()
            self.edition_input.setFont(self.id_label_font)
            self.edition_input.setToolTip("Enter the edition of the book.")
            self.edition_layout.addWidget(self.edition_input)
            self.form_layout.addLayout(self.edition_layout)
            
            self.pages_layout = QHBoxLayout()
            self.pages_label = QLabel("Pages:")
            self.pages_label.setFont(self.id_label_font)
            self.pages_layout.addWidget(self.pages_label)
            self.pages_input = QLineEdit()
            self.pages_input.setFont(self.id_label_font)
            self.pages_input.setToolTip("Enter the number of pages in the book.")
            self.pages_layout.addWidget(self.pages_input)
            self.form_layout.addLayout(self.pages_layout)
            
            self.photocopyprice_layout = QHBoxLayout()
            self.photocopyprice_label = QLabel("Photocopy Price:")
            self.photocopyprice_label.setFont(self.id_label_font)
            self.photocopyprice_layout.addWidget(self.photocopyprice_label)
            self.photocopyprice_input = QLineEdit()
            self.photocopyprice_input.setFont(self.id_label_font)
            self.photocopyprice_input.setToolTip("Enter the price of a photocopy of the book.")
            self.photocopyprice_layout.addWidget(self.photocopyprice_input)
            self.form_layout.addLayout(self.photocopyprice_layout)
            
            self.bookprice_layout = QHBoxLayout()
            self.bookprice_label = QLabel("Book Price:")
            self.bookprice_label.setFont(self.id_label_font)
            self.bookprice_layout.addWidget(self.bookprice_label)
            self.bookprice_input = QLineEdit()
            self.bookprice_input.setFont(self.id_label_font)
            self.bookprice_input.setToolTip("Enter the price of the book.")
            self.bookprice_layout.addWidget(self.bookprice_input)
            self.form_layout.addLayout(self.bookprice_layout)
            
            self.qtty_layout = QHBoxLayout()
            self.qtty_label = QLabel("Quantity:")
            self.qtty_label.setFont(self.id_label_font)
            self.qtty_layout.addWidget(self.qtty_label)
            self.qtty_input = QLineEdit("1")
            self.qtty_input.setFont(self.id_label_font)
            self.qtty_input.setToolTip("Enter the available quantity of the book.")
            self.qtty_layout.addWidget(self.qtty_input)
            self.form_layout.addLayout(self.qtty_layout)
        else:
            new_id = self.get_next_available_id(LATEST_OFFICE_PATH)
            self.id_label = QLabel(f"ID: {new_id}")
            self.id_label_font = QFont()
            self.id_label_font.setPointSize(14)
            self.id_label.setFont(self.id_label_font)
            self.form_layout.addWidget(self.id_label)
            
            self.type_layout = QHBoxLayout()
            self.type_label = QLabel("Category:")
            self.type_label.setFont(self.id_label_font)
            self.type_layout.addWidget(self.type_label)
            self.type_dropdown = QComboBox()
            self.type_dropdown.setFont(self.id_label_font)
            self.type_dropdown.setToolTip("Select or add a category.")
            self.type_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
            self.update_category_dropdown()
            self.type_dropdown.currentIndexChanged.connect(self.check_add_category)
            self.type_layout.addWidget(self.type_dropdown)
            self.form_layout.addLayout(self.type_layout)
            
            self.product_name_layout = QHBoxLayout()
            self.product_name_label = QLabel("Product Name:")
            self.product_name_label.setFont(self.id_label_font)
            self.product_name_layout.addWidget(self.product_name_label)
            self.product_name_input = QLineEdit()
            self.product_name_input.setFont(self.id_label_font)
            self.product_name_input.setToolTip("Enter the name of the product.")
            self.product_name_layout.addWidget(self.product_name_input)
            self.form_layout.addLayout(self.product_name_layout)
            
            self.brand_layout = QHBoxLayout()
            self.brand_label = QLabel("Brand:")
            self.brand_label.setFont(self.id_label_font)
            self.brand_layout.addWidget(self.brand_label)
            self.brand_dropdown = QComboBox()
            self.brand_dropdown.setFont(self.id_label_font)
            self.brand_dropdown.setToolTip("Select or add a brand.")
            self.brand_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
            self.update_brand_dropdown()
            self.brand_dropdown.currentIndexChanged.connect(self.check_add_brand)
            self.brand_layout.addWidget(self.brand_dropdown)
            self.form_layout.addLayout(self.brand_layout)
            
            self.color_layout = QHBoxLayout()
            self.color_label = QLabel("Color:")
            self.color_label.setFont(self.id_label_font)
            self.color_layout.addWidget(self.color_label)
            self.color_input = QLineEdit()
            self.color_input.setFont(self.id_label_font)
            self.color_input.setToolTip("Enter the color of the product.")
            self.color_layout.addWidget(self.color_input)
            self.form_layout.addLayout(self.color_layout)
            
            self.price_layout = QHBoxLayout()
            self.price_label = QLabel("Price:")
            self.price_label.setFont(self.id_label_font)
            self.price_layout.addWidget(self.price_label)
            self.price_input = QLineEdit()
            self.price_input.setFont(self.id_label_font)
            self.price_input.setToolTip("Enter the price of the product.")
            self.price_layout.addWidget(self.price_input)
            self.form_layout.addLayout(self.price_layout)
            
            self.qtty_layout = QHBoxLayout()
            self.qtty_label = QLabel("Quantity:")
            self.qtty_label.setFont(self.id_label_font)
            self.qtty_layout.addWidget(self.qtty_label)
            self.qtty_input = QLineEdit("1")
            self.qtty_input.setFont(self.id_label_font)
            self.qtty_input.setToolTip("Enter the available quantity of the product.")
            self.qtty_layout.addWidget(self.qtty_input)
            self.form_layout.addLayout(self.qtty_layout)

    def check_add_category(self):
        if self.type_dropdown.currentText() == "Add Category...":
            text, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
            if ok and text:
                self.categories.add(text)
                self.save_categories()
                self.update_category_dropdown(text)
            if not ok:
                self.type_dropdown.setCurrentIndex(0)

    def check_add_brand(self):
        if self.brand_dropdown.currentText() == "Add Brand...":
            text, ok = QInputDialog.getText(self, "Add Brand", "Enter new brand name:")
            if ok and text:
                self.brands.add(text)
                self.save_brands()
                self.update_brand_dropdown(text)
            if not ok:
                self.brand_dropdown.setCurrentIndex(0)

    def update_category_dropdown(self, new_category=None):
        self.type_dropdown.clear()
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        self.type_dropdown.addItems(sorted(self.categories))
        if new_category:
            self.type_dropdown.setCurrentText(new_category)

    def update_brand_dropdown(self, new_brand=None):
        self.brand_dropdown.clear()
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        self.brand_dropdown.addItems(sorted(self.brands))
        if new_brand:
            self.brand_dropdown.setCurrentText(new_brand)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            if child.layout():
                self.clear_layout(child.layout())

    def clear_fields(self):
        if self.dropdown.currentText() == "Books":
            self.name_input.clear()
            self.author_input.clear()
            self.edition_input.clear()
            self.pages_input.clear()
            self.photocopyprice_input.clear()
            self.bookprice_input.clear()
            self.qtty_input.setText("1")
        else:
            self.type_dropdown.setCurrentIndex(0)
            self.product_name_input.clear()
            self.type_dropdown.setCurrentIndex(0)
            self.color_input.clear()
            self.price_input.clear()
            self.qtty_input.setText("1")

    def save_item(self):
        global books_count
        global office_count
        try:
            if self.dropdown.currentText() == "Books":
                new_id = self.get_next_available_id(LATEST_BOOKS_PATH)
                data = [
                    new_id,
                    self.name_input.text() or "-",
                    self.author_input.text() or "-",
                    self.edition_input.text() or "-",
                    self.pages_input.text() or "-",
                    self.photocopyprice_input.text() or "-",
                    self.bookprice_input.text() or "-",
                    self.qtty_input.text() or "1"
                ]
    
                file_path = LATEST_BOOKS_PATH
    
                # Ensure that name is not empty or a single sign
                if data[1] == "-" or len(data[1].strip()) == 0:
                    raise ValueError("Book Name cannot be empty.")
    
                # Ensure that photocopyprice is a non-zero positive number
                try:
                    photocopyprice = float(data[5])
                    if photocopyprice <= 0:
                        raise ValueError("Photocopy Price must be a positive number.")
                except ValueError:
                    raise ValueError("Invalid Photocopy Price. It must be a positive number.")
    
            else:
                new_id = self.get_next_available_id(LATEST_OFFICE_PATH)
                data = [
                    new_id,
                    self.type_dropdown.currentText() or "-",
                    self.product_name_input.text() or "-",
                    self.brand_dropdown.currentText() or "-",
                    self.color_input.text() or "-",
                    self.price_input.text() or "-",
                    self.qtty_input.text() or "1"
                ]
    
                file_path = LATEST_OFFICE_PATH
    
                # Ensure that category is not empty or a single sign
                if data[1] == "-" or len(data[1].strip()) == 0:
                    raise ValueError("Category cannot be empty.")
    
                # Ensure that name is not empty or a single sign
                if data[2] == "-" or len(data[2].strip()) == 0:
                    raise ValueError("Product Name cannot be empty.")
    
                # Ensure that price is a non-zero positive number
                try:
                    price = float(data[5])
                    if price <= 0:
                        raise ValueError("Price must be a positive number.")
                except ValueError:
                    raise ValueError("Invalid Price. It must be a positive number.")
    
            # Ensure that qtty is a non-zero positive number
            try:
                qtty = int(data[-1])
                if qtty <= 0:
                    raise ValueError("Quantity must be a positive number.")
            except ValueError:
                raise ValueError("Invalid Quantity. It must be a positive integer.")
    
            exists = False
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if self.dropdown.currentText() == 'Books':
                        if row[1] == data[1] and row[2] == data[2]:
                            row[-1] = str(int(row[-1]) + int(data[-1]))
                            existent_item = row[1]
                            added_item_count = int(data[-1])
                            exists = True
                            break
                    else:
                        if row[2] == data[2] and row[3] == data[3]:
                            row[-1] = str(int(row[-1]) + int(data[-1]))
                            existent_item = row[2]
                            added_item_count = int(data[-1])
                            exists = True
                            break
    
            if not exists:
                rows.append(data)
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            if self.dropdown.currentText() == "Books":
                books_count += 1
            else:
                office_count += 1
    
            self.clear_fields()
            self.update_form()
    
            if exists:
                QMessageBox.information(self, "Success", f'Added {added_item_count} existence(s) to the already present "{existent_item}" {self.dropdown.currentText()[:-1]} in the stock.')
            else:
                QMessageBox.information(self, "Success", "Item added to the stock.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

def open_add_menu(parent):
    dialog = AddItemsDialog(parent)
    dialog.exec_()