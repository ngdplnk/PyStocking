import os
import sys
import csv
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox)
from PyQt5.QtGui import QFont

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.csv')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.csv')

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
except Exception as e:
    print(e)

class AddItemsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Items")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Books", "Office Items"])
        self.dropdown_font = QFont()
        self.dropdown_font.setPointSize(14)
        self.dropdown.setFont(self.dropdown_font)
        self.dropdown.currentIndexChanged.connect(self.update_form)
        self.layout.addWidget(self.dropdown)

        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save")
        self.save_button_font = QFont()
        self.save_button_font.setPointSize(14)
        self.save_button.setFont(self.save_button_font)
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button)

        self.update_form()

    def update_form(self):
        for i in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(i).widget().deleteLater()

        if self.dropdown.currentText() == "Books":
            self.id_label = QLabel(f"ID: {books_count + 1}")
            self.id_label_font = QFont()
            self.id_label_font.setPointSize(14)
            self.id_label.setFont(self.id_label_font)
            self.form_layout.addWidget(self.id_label)
            self.name_input = QLineEdit()
            self.name_input_font = QFont()
            self.name_input_font.setPointSize(14)
            self.name_input.setFont(self.name_input_font)
            self.name_input.setPlaceholderText("Book Name")
            self.form_layout.addWidget(self.name_input)
            self.author_input = QLineEdit()
            self.author_input_font = QFont()
            self.author_input_font.setPointSize(14)
            self.author_input.setFont(self.author_input_font)
            self.author_input.setPlaceholderText("Author")
            self.form_layout.addWidget(self.author_input)
            self.edition_input = QLineEdit()
            self.edition_input_font = QFont()
            self.edition_input_font.setPointSize(14)
            self.edition_input.setFont(self.edition_input_font)
            self.edition_input.setPlaceholderText("Edition")
            self.form_layout.addWidget(self.edition_input)
            self.pages_input = QLineEdit()
            self.pages_input_font = QFont()
            self.pages_input_font.setPointSize(14)
            self.pages_input.setFont(self.pages_input_font)
            self.pages_input.setPlaceholderText("Pages")
            self.form_layout.addWidget(self.pages_input)
            self.photocopyprice_input = QLineEdit()
            self.photocopyprice_input_font = QFont()
            self.photocopyprice_input_font.setPointSize(14)
            self.photocopyprice_input.setFont(self.photocopyprice_input_font)
            self.photocopyprice_input.setPlaceholderText("Photocopy Price")
            self.form_layout.addWidget(self.photocopyprice_input)
            self.bookprice_input = QLineEdit()
            self.bookprice_input_font = QFont()
            self.bookprice_input_font.setPointSize(14)
            self.bookprice_input.setFont(self.bookprice_input_font)
            self.bookprice_input.setPlaceholderText("Book Price")
            self.form_layout.addWidget(self.bookprice_input)
            self.qtty_input = QLineEdit()
            self.qtty_input_font = QFont()
            self.qtty_input_font.setPointSize(14)
            self.qtty_input.setFont(self.qtty_input_font)
            self.qtty_input.setPlaceholderText("Quantity")
            self.form_layout.addWidget(self.qtty_input)
        else:
            self.id_label = QLabel(f"ID: {office_count + 1}")
            self.id_label_font = QFont()
            self.id_label_font.setPointSize(14)
            self.id_label.setFont(self.id_label_font)
            self.form_layout.addWidget(self.id_label)
            self.type_input = QLineEdit()
            self.type_input_font = QFont()
            self.type_input_font.setPointSize(14)
            self.type_input.setFont(self.type_input_font)
            self.type_input.setPlaceholderText("Category")
            self.form_layout.addWidget(self.type_input)
            self.product_name_input = QLineEdit()
            self.product_name_input_font = QFont()
            self.product_name_input_font.setPointSize(14)
            self.product_name_input.setFont(self.product_name_input_font)
            self.product_name_input.setPlaceholderText("Product Name")
            self.form_layout.addWidget(self.product_name_input)
            self.brand_input = QLineEdit()
            self.brand_input_font = QFont()
            self.brand_input_font.setPointSize(14)
            self.brand_input.setFont(self.brand_input_font)
            self.brand_input.setPlaceholderText("Brand")
            self.form_layout.addWidget(self.brand_input)
            self.color_input = QLineEdit()
            self.color_input_font = QFont()
            self.color_input_font.setPointSize(14)
            self.color_input.setFont(self.color_input_font)
            self.color_input.setPlaceholderText("Color")
            self.form_layout.addWidget(self.color_input)
            self.price_input = QLineEdit()
            self.price_input_font = QFont()
            self.price_input_font.setPointSize(14)
            self.price_input.setFont(self.price_input_font)
            self.price_input.setPlaceholderText("Price")
            self.form_layout.addWidget(self.price_input)
            self.qtty_input = QLineEdit()
            self.qtty_input_font = QFont()
            self.qtty_input_font.setPointSize(14)
            self.qtty_input.setFont(self.qtty_input_font)
            self.qtty_input.setPlaceholderText("Quantity")
            self.form_layout.addWidget(self.qtty_input)

    def save_item(self):
        global books_count
        global office_count
        try:
            if self.dropdown.currentText() == "Books":
                data = [
                    books_count + 1,
                    self.name_input.text() or "-",
                    self.author_input.text() or "-",
                    self.edition_input.text() or "-",
                    self.pages_input.text() or "-",
                    self.photocopyprice_input.text() or "-",
                    self.bookprice_input.text() or "-",
                    self.qtty_input.text() or "1"
                ]
                file_path = LATEST_BOOKS_PATH
                if not data[-3].isnumeric():
                    raise ValueError("Invalid Photocopy Price")
            else:
                data = [
                    office_count + 1,
                    self.type_input.text() or "-",
                    self.product_name_input.text() or "-",
                    self.brand_input.text() or "-",
                    self.color_input.text() or "-",
                    self.price_input.text() or "-",
                    self.qtty_input.text() or "1"
                ]
                file_path = LATEST_OFFICE_PATH
                if not data[-2].isnumeric():
                    raise ValueError("Invalid Item Price")

            if data[1] == "-":
                return
            if not data[-1].isnumeric():
                raise ValueError("Invalid Quantity")
            
            exists = False
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[1] == data[1] and row[2] == data[2]:
                        row[-1] = str(int(row[-1]) + int(data[-1]))
                        exists = True
                        break

            if not exists:
                rows.append(data)

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
            if file_path == LATEST_BOOKS_PATH:
                books_count += 1
            else:
                office_count += 1
            
            if not exists:
                QMessageBox.information(self, "Success", "Item added successfully")
            else:
                QMessageBox.information(self, "Success", "Item count updated successfully")
            
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ensure you filled all the required fields correctly")
            print(e)

def open_add_menu(parent):
    dialog = AddItemsDialog(parent)
    dialog.exec_()