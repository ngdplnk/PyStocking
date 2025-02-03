import os
import sys
import csv
import datetime
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QWidget, QInputDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
CATEGORIES_PATH = os.path.join(SAVES_PATH, 'cats.pystk')
BRANDS_PATH = os.path.join(SAVES_PATH, 'brands.pystk')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.pystk')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.pystk')

class ManageItemsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Items")
        self.setGeometry(100, 100, 1200, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.dropdown = QComboBox()
        self.dropdown.setFont(self.font)
        self.dropdown.addItems(["Books", "Office Items"])
        self.dropdown.setToolTip("Select the type of items to manage")
        self.dropdown.currentIndexChanged.connect(self.update_search_dropdown)
        self.layout.addWidget(self.dropdown)

        self.search_layout = QHBoxLayout()
        
        self.search_dropdown = QComboBox()
        self.search_dropdown.setFont(self.font)
        self.search_dropdown.setToolTip("Select the field to search items")
        self.search_layout.addWidget(self.search_dropdown)
        
        self.search_bar = QLineEdit()
        self.search_bar.setFont(self.font)
        self.search_bar.setToolTip("Type here to start searching items")
        self.search_bar.textChanged.connect(self.update_list)
        self.search_layout.addWidget(self.search_bar)
        
        self.layout.addLayout(self.search_layout)

        if sys.platform == "win32":
            self.save_button = QPushButton("Save Spreadsheet to Desktop")
        else:
            self.save_button = QPushButton("Save Spreadsheet to Home")
        self.save_button.setFont(self.font)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_to_desktop)
        self.save_button.setToolTip("Save the current list of items to a CSV file")
        self.layout.addWidget(self.save_button)

        self.table_widget = QTableWidget()
        self.table_widget.setFont(self.font)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.itemSelectionChanged.connect(self.update_buttons)
        self.table_widget.itemDoubleClicked.connect(self.edit_item)
        self.table_widget.setSortingEnabled(True)
        self.layout.addWidget(self.table_widget)

        self.button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFont(self.font)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_item)
        self.edit_button.setToolTip("Edit the selected item")
        self.button_layout.addWidget(self.edit_button)

        self.add_button = QPushButton("+1 to Quantity")
        self.add_button.setFont(self.font)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_to_inventory)
        self.add_button.setToolTip("Add 1 to the quantity of the selected item")
        self.button_layout.addWidget(self.add_button)

        self.subtract_button = QPushButton("-1 to Quantity")
        self.subtract_button.setFont(self.font)
        self.subtract_button.setEnabled(False)
        self.subtract_button.clicked.connect(self.subtract_from_inventory)
        self.subtract_button.setToolTip("Subtract 1 from the quantity of the selected item")
        self.button_layout.addWidget(self.subtract_button)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.setFont(self.font)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_item)
        self.delete_button.setToolTip("Delete the selected item from the stock")
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.update_search_dropdown()
        self.update_list()

    def update_search_dropdown(self):
        self.table_widget.setSortingEnabled(False)
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.search_dropdown.clear()
        if self.dropdown.currentText() == "Books":
            self.search_dropdown.addItems(["ID", "Book Name", "Author", "Editorial", "Pages", "Photocopy Price", "Book Price", "Quantity"])
            self.table_widget.setColumnCount(8)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Book Name", "Author", "Editorial", "Pages", "Photocopy Price", "Book Price", "Quantity"])
            self.search_bar.setPlaceholderText("Search Books...")
        else:
            self.search_dropdown.addItems(["ID", "Category", "Product Name", "Brand", "Color", "Price", "Quantity"])
            self.table_widget.setColumnCount(7)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Category", "Product Name", "Brand", "Color", "Price", "Quantity"])
            self.search_bar.setPlaceholderText("Search Office Items...")
        self.update_list()
        self.table_widget.setSortingEnabled(True)

    def update_list(self):
        self.table_widget.setSortingEnabled(False)  # Disable sorting
        self.table_widget.setRowCount(0)
        self.save_button.setEnabled(False)
        search_text = self.search_bar.text().lower()
        search_index = self.search_dropdown.currentIndex()
    
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
            numeric_columns = [0, 4, 5, 6, 7]  # ID, Pages, Photocopy Price, Book Price, Quantity
        else:
            file_path = LATEST_OFFICE_PATH
            numeric_columns = [0, 5, 6]  # ID, Price, Quantity
    
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                has_items = False
                for row in reader:
                    if search_text in row[search_index].lower():
                        row_position = self.table_widget.rowCount()
                        self.table_widget.insertRow(row_position)
                        for column, item in enumerate(row):
                            if column in numeric_columns:
                                self.table_widget.setItem(row_position, column, NumericTableWidgetItem(item))
                            else:
                                self.table_widget.setItem(row_position, column, QTableWidgetItem(item))
                        has_items = True
                if has_items:
                    self.save_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load items: {e}")
        self.table_widget.setSortingEnabled(True)  # Re-enable sorting

    def update_buttons(self):
        if self.table_widget.selectedItems():
            self.edit_button.setEnabled(True)
            self.add_button.setEnabled(True)
            self.subtract_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.add_button.setEnabled(False)
            self.subtract_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def save_to_desktop(self):
        current_time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M")
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
            filename = f"Books_{current_time}.csv"
        else:
            file_path = LATEST_OFFICE_PATH
            filename = f"Office_Items_{current_time}.csv"

        if sys.platform == "win32":
            save_path = os.path.join(os.getenv('USERPROFILE'), 'Desktop', filename)
        else:
            save_path = os.path.join(os.path.expanduser('~'), filename)

        backup_path = os.path.join(SAVES_PATH, filename)

        try:
            with open(file_path, 'r') as file:
                data = file.read()
            with open(save_path, 'w') as file:
                file.write(data)
            with open(backup_path, 'w') as file:
                file.write(data)
            if sys.platform == "win32":
                QMessageBox.information(self, "Success", f"{filename} successfully saved to Desktop")
            else:
                QMessageBox.information(self, "Success", f"{filename} successfully saved to Home")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def edit_item(self):
        selected_row = self.table_widget.currentRow()
        fields = [self.table_widget.item(selected_row, i).text() for i in range(self.table_widget.columnCount())]
        if self.dropdown.currentText() == "Books":
            self.edit_dialog = EditBookDialog(self, fields)
        else:
            self.edit_dialog = EditOfficeItemDialog(self, fields)
        self.edit_dialog.exec_()
        self.update_list()

    def add_to_inventory(self):
        selected_row = self.table_widget.currentRow()
        if selected_row == -1:
            return
    
        fields = [self.table_widget.item(selected_row, i).text() if self.table_widget.item(selected_row, i) else "" for i in range(self.table_widget.columnCount())]
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH
    
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == fields[0]:
                        row[-1] = str(int(row[-1]) + 1)
                        break
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            self.update_list()
            self.table_widget.selectRow(selected_row)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

    def subtract_from_inventory(self):
        selected_row = self.table_widget.currentRow()
        if selected_row == -1:
            return
    
        fields = [self.table_widget.item(selected_row, i).text() if self.table_widget.item(selected_row, i) else "" for i in range(self.table_widget.columnCount())]
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH
    
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == fields[0]:
                        current_qtty = int(row[-1])
                        if current_qtty > 1:
                            row[-1] = str(current_qtty - 1)
                        else:
                            reply = QMessageBox.question(self, 'Confirmation', 
                                                         "This is the last of this item in stock. Do you want to delete it?", 
                                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                rows.remove(row)
                            else:
                                row[-1] = '1'
                        break
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            if not current_qtty > 1 and reply == QMessageBox.Yes:
                QMessageBox.information(self, "Success", "Item removed from stock")
            self.update_list()
            self.table_widget.selectRow(selected_row)  # Reselect the previously selected row
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

    def delete_item(self):
        selected_row = self.table_widget.currentRow()
        if selected_row == -1:
            return
    
        fields = [self.table_widget.item(selected_row, i).text() for i in range(self.table_widget.columnCount())]
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH
    
        try:
            reply = QMessageBox.question(self, 'Confirmation', "Are you sure you want to delete this item from the stock?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    rows = [row for row in reader if row[0] != fields[0]]
    
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
    
                QMessageBox.information(self, "Success", "Item deleted successfully")
                self.update_list()
            else:
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete item: {e}")

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            try:
                return float(self.text()) < float(other.text())
            except ValueError:
                return self.text() < other.text()
        return super().__lt__(other)

class EditBookDialog(QDialog):
    def __init__(self, parent, fields):
        super().__init__(parent)
        self.setWindowTitle("Editing Book")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.id_label = QLabel(f"ID: {fields[0]}")
        self.id_label.setFont(self.font)
        self.layout.addWidget(self.id_label)

        self.form_layout = QVBoxLayout()
        
        self.name_layout = QHBoxLayout()
        self.name_label = QLabel("Book Name:")
        self.name_label.setFont(self.font)
        self.name_layout.addWidget(self.name_label)
        self.name_input = QLineEdit(fields[1] if len(fields) > 1 else "")
        self.name_input.setFont(self.font)
        self.name_input.setToolTip("Enter the name of the book")
        self.name_layout.addWidget(self.name_input)
        self.form_layout.addLayout(self.name_layout)
        
        self.author_layout = QHBoxLayout()
        self.author_label = QLabel("Author:")
        self.author_label.setFont(self.font)
        self.author_layout.addWidget(self.author_label)
        self.author_input = QLineEdit(fields[2] if len(fields) > 2 else "")
        self.author_input.setFont(self.font)
        self.author_input.setToolTip("Enter the author of the book")
        self.author_layout.addWidget(self.author_input)
        self.form_layout.addLayout(self.author_layout)
        
        self.edition_layout = QHBoxLayout()
        self.edition_label = QLabel("Editorial:")
        self.edition_label.setFont(self.font)
        self.edition_layout.addWidget(self.edition_label)
        self.edition_input = QLineEdit(fields[3] if len(fields) > 3 else "")
        self.edition_input.setFont(self.font)
        self.edition_input.setToolTip("Enter the edition of the book")
        self.edition_layout.addWidget(self.edition_input)
        self.form_layout.addLayout(self.edition_layout)
        
        self.pages_layout = QHBoxLayout()
        self.pages_label = QLabel("Pages:")
        self.pages_label.setFont(self.font)
        self.pages_layout.addWidget(self.pages_label)
        self.pages_input = QLineEdit(fields[4] if len(fields) > 4 else "")
        self.pages_input.setFont(self.font)
        self.pages_input.setToolTip("Enter the number of pages in the book")
        self.pages_layout.addWidget(self.pages_input)
        self.form_layout.addLayout(self.pages_layout)
        
        self.photocopyprice_layout = QHBoxLayout()
        self.photocopyprice_label = QLabel("Photocopy Price:")
        self.photocopyprice_label.setFont(self.font)
        self.photocopyprice_layout.addWidget(self.photocopyprice_label)
        self.photocopyprice_input = QLineEdit(fields[5] if len(fields) > 5 else "")
        self.photocopyprice_input.setFont(self.font)
        self.photocopyprice_input.setToolTip("Enter the price of a photocopy of the book")
        self.photocopyprice_layout.addWidget(self.photocopyprice_input)
        self.form_layout.addLayout(self.photocopyprice_layout)
        
        self.bookprice_layout = QHBoxLayout()
        self.bookprice_label = QLabel("Book Price:")
        self.bookprice_label.setFont(self.font)
        self.bookprice_layout.addWidget(self.bookprice_label)
        self.bookprice_input = QLineEdit(fields[6] if len(fields) > 6 else "")
        self.bookprice_input.setFont(self.font)
        self.bookprice_input.setToolTip("Enter the price of the book")
        self.bookprice_layout.addWidget(self.bookprice_input)
        self.form_layout.addLayout(self.bookprice_layout)
        
        self.qtty_layout = QHBoxLayout()
        self.qtty_label = QLabel("Quantity:")
        self.qtty_label.setFont(self.font)
        self.qtty_layout.addWidget(self.qtty_label)
        self.qtty_input = QLineEdit(fields[7] if len(fields) > 7 else "")
        self.qtty_input.setFont(self.font)
        self.qtty_input.setToolTip("Enter the available quantity of the book")
        self.qtty_layout.addWidget(self.qtty_input)
        self.form_layout.addLayout(self.qtty_layout)
        
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the changes made to the book")
        self.layout.addWidget(self.save_button)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.name_input.text() or "-",
            self.author_input.text() or "-",
            self.edition_input.text() or "-",
            self.pages_input.text() or "-",
            self.photocopyprice_input.text() or "-",
            self.bookprice_input.text() or "-",
            self.qtty_input.text() or "-"
        ]
        
        # Ensure that name is not empty or a single sign
        if data[1] == "-" or len(data[1].strip()) == 0:
            QMessageBox.critical(self, "Error", "Name cannot be empty.")
            return
        
        # Ensure that photocopyprice is a non-zero positive number
        try:
            photocopyprice = float(data[5])
            if photocopyprice <= 0:
                raise ValueError("Photocopy Price must be a positive number.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid Photocopy Price. It must be a positive number.")
            return
        
        # Ensure that qtty is a non-zero positive number
        try:
            qtty = int(data[7])
            if qtty <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid Quantity. It must be a positive integer.")
            return
        
        try:
            with open(LATEST_BOOKS_PATH, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] != data[0] and row[1] == data[1] and row[2] == data[2]:
                        QMessageBox.critical(self, "Error", "This book already exists!")
                        return
        
            with open(LATEST_BOOKS_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        
            QMessageBox.information(self, "Success", "Item updated successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

class EditOfficeItemDialog(QDialog):
    def __init__(self, parent, fields):
        super().__init__(parent)
        self.setWindowTitle("Editing Office Item")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.id_label = QLabel(f"ID: {fields[0]}")
        self.id_label.setFont(self.font)
        self.layout.addWidget(self.id_label)

        self.form_layout = QVBoxLayout()
        
        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("Category:")
        self.type_label.setFont(self.font)
        self.type_layout.addWidget(self.type_label)
        self.type_dropdown = QComboBox()
        self.type_dropdown.setFont(self.font)
        self.type_dropdown.setToolTip("Select or add a category.")
        self.type_dropdown.setMaxVisibleItems(10)
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        self.load_categories()
        self.type_dropdown.setCurrentText(fields[1] if len(fields) > 1 else "")
        self.type_dropdown.currentIndexChanged.connect(self.check_add_category)
        self.type_layout.addWidget(self.type_dropdown)
        self.form_layout.addLayout(self.type_layout)
        
        self.product_name_layout = QHBoxLayout()
        self.product_name_label = QLabel("Product Name:")
        self.product_name_label.setFont(self.font)
        self.product_name_layout.addWidget(self.product_name_label)
        self.product_name_input = QLineEdit(fields[2] if len(fields) > 2 else "")
        self.product_name_input.setFont(self.font)
        self.product_name_input.setToolTip("Enter the name of the product")
        self.product_name_layout.addWidget(self.product_name_input)
        self.form_layout.addLayout(self.product_name_layout)
        
        self.brand_layout = QHBoxLayout()
        self.brand_label = QLabel("Brand:")
        self.brand_label.setFont(self.font)
        self.brand_layout.addWidget(self.brand_label)
        self.brand_dropdown = QComboBox()
        self.brand_dropdown.setFont(self.font)
        self.brand_dropdown.setToolTip("Select or add a brand.")
        self.brand_dropdown.setMaxVisibleItems(10)
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        self.load_brands()
        self.brand_dropdown.setCurrentText(fields[3] if len(fields) > 3 else "")
        self.brand_dropdown.currentIndexChanged.connect(self.check_add_brand)
        self.brand_layout.addWidget(self.brand_dropdown)
        self.form_layout.addLayout(self.brand_layout)
        
        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Color:")
        self.color_label.setFont(self.font)
        self.color_layout.addWidget(self.color_label)
        self.color_input = QLineEdit(fields[4] if len(fields) > 4 else "")
        self.color_input.setFont(self.font)
        self.color_input.setToolTip("Enter the color of the product")
        self.color_layout.addWidget(self.color_input)
        self.form_layout.addLayout(self.color_layout)
        
        self.price_layout = QHBoxLayout()
        self.price_label = QLabel("Price:")
        self.price_label.setFont(self.font)
        self.price_layout.addWidget(self.price_label)
        self.price_input = QLineEdit(fields[5] if len(fields) > 5 else "")
        self.price_input.setFont(self.font)
        self.price_input.setToolTip("Enter the price of the product")
        self.price_layout.addWidget(self.price_input)
        self.form_layout.addLayout(self.price_layout)
        
        self.qtty_layout = QHBoxLayout()
        self.qtty_label = QLabel("Quantity:")
        self.qtty_label.setFont(self.font)
        self.qtty_layout.addWidget(self.qtty_label)
        self.qtty_input = QLineEdit(fields[6] if len(fields) > 6 else "")
        self.qtty_input.setFont(self.font)
        self.qtty_input.setToolTip("Enter the available quantity of the product")
        self.qtty_layout.addWidget(self.qtty_input)
        self.form_layout.addLayout(self.qtty_layout)
        
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the changes made to the office item")
        self.layout.addWidget(self.save_button)

        self.previous_category = fields[1] if len(fields) > 1 else ""
        self.previous_brand = fields[3] if len(fields) > 3 else ""

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
        self.update_category_dropdown()

    def save_categories(self):
        with open(CATEGORIES_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            for category in sorted(self.categories):
                writer.writerow([category])

    def check_add_category(self):
        if self.type_dropdown.currentText() == "Add Category...":
            text, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
            if ok and text:
                self.categories.add(text)
                self.save_categories()
                self.update_category_dropdown(text)
            else:
                self.type_dropdown.blockSignals(True)
                self.type_dropdown.setCurrentText(self.previous_category)
                self.type_dropdown.blockSignals(False)

    def update_category_dropdown(self, new_category=None):
        self.type_dropdown.blockSignals(True)
        self.type_dropdown.clear()
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        self.type_dropdown.addItems(sorted(self.categories))
        if new_category:
            self.type_dropdown.setCurrentText(new_category)
        self.type_dropdown.blockSignals(False)

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
        self.update_brand_dropdown()

    def save_brands(self):
        with open(BRANDS_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            for brand in sorted(self.brands):
                writer.writerow([brand])

    def check_add_brand(self):
        if self.brand_dropdown.currentText() == "Add Brand...":
            text, ok = QInputDialog.getText(self, "Add Brand", "Enter new brand name:")
            if ok and text:
                self.brands.add(text)
                self.save_brands()
                self.update_brand_dropdown(text)
            else:
                self.brand_dropdown.blockSignals(True)
                self.brand_dropdown.setCurrentText(self.previous_brand)
                self.brand_dropdown.blockSignals(False)

    def update_brand_dropdown(self, new_brand=None):
        self.brand_dropdown.blockSignals(True)
        self.brand_dropdown.clear()
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        self.brand_dropdown.addItems(sorted(self.brands))
        if new_brand:
            self.brand_dropdown.setCurrentText(new_brand)
        self.brand_dropdown.blockSignals(False)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.type_dropdown.currentText() or "-",
            self.product_name_input.text() or "-",
            self.brand_dropdown.currentText() or "-",
            self.color_input.text() or "-",
            self.price_input.text() or "-",
            self.qtty_input.text() or "-"
        ]
    
        # Ensure that category is not empty or a single sign
        if data[1] == "-" or len(data[1].strip()) == 0:
            QMessageBox.critical(self, "Error", "Category cannot be empty.")
            return
    
        # Ensure that product name is not empty or a single sign
        if data[2] == "-" or len(data[2].strip()) == 0:
            QMessageBox.critical(self, "Error", "Product Name cannot be empty.")
            return
    
        # Ensure that price is a non-zero positive number
        try:
            price = float(data[5])
            if price <= 0:
                raise ValueError("Price must be a positive number.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid Price. It must be a positive number.")
            return
    
        # Ensure that qtty is a non-zero positive number
        try:
            qtty = int(data[6])
            if qtty <= 0:
                raise ValueError("Quantity must be a positive number.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid Quantity. It must be a positive integer.")
            return
    
        try:
            with open(LATEST_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == data[0]:
                        row[1] = data[1]
                        row[2] = data[2]
                        row[3] = data[3]
                        row[4] = data[4]
                        row[5] = data[5]
                        row[6] = data[6]
                        break
    
            with open(LATEST_OFFICE_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            QMessageBox.information(self, "Success", "Item updated successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

def open_manage_menu(parent):
    dialog = ManageItemsDialog(parent)
    dialog.exec_()
