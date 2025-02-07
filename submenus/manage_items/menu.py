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
DATA_PATH = os.path.join(PROGRAM_PATH, 'data')
CATS_SCHOOL_PATH = os.path.join(DATA_PATH, 'cats_school.pystk')
CATS_OFFICE_PATH = os.path.join(DATA_PATH, 'cats_office.pystk')
BRANDS_SCHOOL_PATH = os.path.join(DATA_PATH, 'brands_school.pystk')
BRANDS_OFFICE_PATH = os.path.join(DATA_PATH, 'brands_office.pystk')
STOCK_SCHOOL_PATH = os.path.join(DATA_PATH, 'stock_school.pystk')
STOCK_OFFICE_PATH = os.path.join(DATA_PATH, 'stock_office.pystk')
STOCK_BOOKS_PATH = os.path.join(DATA_PATH, 'stock_books.pystk')
EDITORIALS_PATH = os.path.join(DATA_PATH, 'editorials.pystk')

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
        self.dropdown.addItems(["School Items", "Office Items", "Books"])
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
            self.save_button = QPushButton("Save current spreadsheet to Desktop")
        else:
            self.save_button = QPushButton("Save current spreadsheet to Home")
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
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table_widget)

        self.button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFont(self.font)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_item)
        self.edit_button.setToolTip("Edit the selected item")
        self.button_layout.addWidget(self.edit_button)

        self.add_button = QPushButton("+1 to Units")
        self.add_button.setFont(self.font)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_to_inventory)
        self.add_button.setToolTip("Add 1 to the quantity of the selected item")
        self.button_layout.addWidget(self.add_button)

        self.subtract_button = QPushButton("-1 to Units")
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
            self.search_dropdown.addItems(["ID", "Title", "Author", "Editorial", "Edition", "Description", "Pages", "Photocopy Price", "Book Price", "Units"])
            self.table_widget.setColumnCount(10)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Title", "Author", "Editorial", "Edition", "Description", "Pages", "Photocopy Price", "Book Price", "Units"])
            self.search_bar.setPlaceholderText("Search Books...")
        elif self.dropdown.currentText() == "School Items":
            self.search_dropdown.addItems(["ID", "Category", "Item Name", "Brand", "Color", "Description", "Price", "Units", "Boxes"])
            self.table_widget.setColumnCount(9)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Category", "Item Name", "Brand", "Color", "Description", "Price", "Units", "Boxes"])
            self.search_bar.setPlaceholderText("Search School Items...")
        else:
            self.search_dropdown.addItems(["ID", "Category", "Item Name", "Brand", "Color", "Description", "Price", "Units", "Boxes"])
            self.table_widget.setColumnCount(9)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Category", "Item Name", "Brand", "Color", "Description", "Price", "Units", "Boxes"])
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
            file_path = STOCK_BOOKS_PATH
            numeric_columns = [0, 6, 7, 8, 9]  # ID, Pages, Photocopy Price, Book Price, Quantity
        elif self.dropdown.currentText() == "School Items":
            file_path = STOCK_SCHOOL_PATH
            numeric_columns = [0, 6, 7, 8]  # ID, Price, Units Quantity, Boxes Quantity
        else:
            file_path = STOCK_OFFICE_PATH
            numeric_columns = [0, 6, 7, 8]  # ID, Price, Units Quantity, Boxes Quantity
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                has_items = False
                for row in reader:
                    if search_text in row[search_index].lower():
                        row_position = self.table_widget.rowCount()
                        self.table_widget.insertRow(row_position)
                        for column, item in enumerate(row):
                            table_item = QTableWidgetItem(item)
                            table_item.setToolTip(item)  # Set tooltip to the same value as the content
                            if column in numeric_columns:
                                table_item = NumericTableWidgetItem(item)
                            self.table_widget.setItem(row_position, column, table_item)
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
            file_path = STOCK_BOOKS_PATH
            filename = f"Books_{current_time}.csv"
        if self.dropdown.currentText() == "School Items":
            file_path = STOCK_SCHOOL_PATH
            filename = f"School_Items_{current_time}.csv"
        else:
            file_path = STOCK_OFFICE_PATH
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
        elif self.dropdown.currentText() == "School Items":
            self.edit_dialog = EditSchoolItemDialog(self, fields)
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
            file_path = STOCK_BOOKS_PATH
        elif self.dropdown.currentText() == "School Items":
            file_path = STOCK_SCHOOL_PATH
        else:
            file_path = STOCK_OFFICE_PATH
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == fields[0]:
                        if self.dropdown.currentText() == "Books":
                            row[-1] = str(int(row[-1]) + 1)
                        elif self.dropdown.currentText() == "School Items":
                            row[-2] = str(int(row[-2]) + 1)
                        else:
                            row[-2] = str(int(row[-2]) + 1)
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
            file_path = STOCK_BOOKS_PATH
        elif self.dropdown.currentText() == "School Items":
            file_path = STOCK_SCHOOL_PATH
        else:
            file_path = STOCK_OFFICE_PATH
    
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == fields[0]:
                        if self.dropdown.currentText() == "Books":
                            current_qtty = int(row[-1])
                        elif self.dropdown.currentText() == "School Items":
                            current_qtty = int(row[-2])
                        else:
                            current_qtty = int(row[-2])
                        if current_qtty > 1:
                            if self.dropdown.currentText() == "Books":
                                row[-1] = str(current_qtty - 1)
                            elif self.dropdown.currentText() == "School Items":
                                row[-2] = str(current_qtty - 1)
                            else:
                                row[-2] = str(current_qtty - 1)
                        else:
                            if self.dropdown.currentText() == "Books":
                                reply = QMessageBox.question(self, 'Confirmation',
                                                                "This is the last unit of this book in the stock. Do you want to delete it?",
                                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if reply == QMessageBox.Yes:
                                    rows.remove(row)
                                    QMessageBox.information(self, "Success", "Book deleted successfully")
                                else:
                                    row[-1] = '1'
                            elif self.dropdown.currentText() == "School Items":
                                if int(row[-2]) == 0:
                                    reply = QMessageBox.critical(self, 'Error',
                                                                    "This school item is out of units. You cannot subtract more of them.",
                                                                    QMessageBox.Ok, QMessageBox.Ok)
                                else:
                                    if int(row[-1]) == 0:
                                        reply = QMessageBox.question(self, 'Confirmation',
                                                                    "This is the last unit of this school item in the stock. Do you want to delete it?",
                                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                        if reply == QMessageBox.Yes:
                                            rows.remove(row)
                                            QMessageBox.information(self, "Success", "School Item deleted successfully")
                                        else:
                                            row[-2] = '1'
                                    else:
                                        row[-2] = '0'
                            else:
                                if int(row[-2]) == 0:
                                    reply = QMessageBox.critical(self, 'Error',
                                                                    "This office item is out of units. You cannot subtract more of them.",
                                                                    QMessageBox.Ok, QMessageBox.Ok)
                                else:
                                    if int(row[-1]) == 0:
                                        reply = QMessageBox.question(self, 'Confirmation',
                                                                    "This is the last unit of this office item in the stock. Do you want to delete it?",
                                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                        if reply == QMessageBox.Yes:
                                            rows.remove(row)
                                            QMessageBox.information(self, "Success", "Office Item deleted successfully")
                                        else:
                                            row[-2] = '1'
                                    else:
                                        row[-2] = '0'
                        break

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
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
            file_path = STOCK_BOOKS_PATH
        elif self.dropdown.currentText() == "School Items":
            file_path = STOCK_SCHOOL_PATH
        else:
            file_path = STOCK_OFFICE_PATH
    
        try:
            if self.dropdown.currentText() == "Books":
                itype = "Book"
            elif self.dropdown.currentText() == "School Items":
                itype = "School Item"
            else:
                itype = "Office Item"
            reply = QMessageBox.question(self, 'Confirmation', f"Are you sure you want to delete this {itype} from the stock?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    rows = [row for row in reader if row[0] != fields[0]]
    
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
    
                QMessageBox.information(self, "Success", f"{itype} deleted successfully")
                self.update_list()
            else:
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete {itype}: {e}")

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

        self.load_editorials()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.id_label = QLabel(f"ID: {fields[0]}")
        self.id_label.setFont(self.font)
        self.layout.addWidget(self.id_label)

        self.form_layout = QVBoxLayout()
        
        self.name_layout = QHBoxLayout()
        self.name_label = QLabel("Title:")
        self.name_label.setFont(self.font)
        self.name_layout.addWidget(self.name_label)
        self.name_input = QLineEdit(fields[1])
        self.name_input = QLineEdit()
        self.name_input.setFont(self.font)
        self.name_input.setToolTip("Enter the title of the book.")
        self.name_layout.addWidget(self.name_input)
        self.form_layout.addLayout(self.name_layout)
        
        self.author_layout = QHBoxLayout()
        self.author_label = QLabel("Author:")
        self.author_label.setFont(self.font)
        self.author_layout.addWidget(self.author_label)
        self.author_input = QLineEdit(fields[2])
        self.author_input = QLineEdit()
        self.author_input.setFont(self.font)
        self.author_input.setToolTip("Enter the author of the book.")
        self.author_layout.addWidget(self.author_input)
        self.form_layout.addLayout(self.author_layout)
        
        self.editorial_layout = QHBoxLayout()
        self.editorial_label = QLabel("Editorial:")
        self.editorial_label.setFont(self.font)
        self.editorial_layout.addWidget(self.editorial_label)
        self.editorial_dropdown = QComboBox()
        self.editorial_dropdown.setFont(self.font)
        self.editorial_dropdown.setToolTip("Select or add an editorial.")
        self.editorial_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
        self.update_editorial_dropdown(fields[3])
        self.editorial_dropdown.currentIndexChanged.connect(self.check_add_editorial)
        self.editorial_layout.addWidget(self.editorial_dropdown)
        self.form_layout.addLayout(self.editorial_layout)

        self.edition_layout = QHBoxLayout()
        self.edition_label = QLabel("Edition:")
        self.edition_label.setFont(self.font)
        self.edition_layout.addWidget(self.edition_label)
        self.edition_input = QLineEdit(fields[4])
        self.edition_input = QLineEdit()
        self.edition_input.setFont(self.font)
        self.edition_input.setToolTip("Enter the edition of the book.")
        self.edition_layout.addWidget(self.edition_input)
        self.form_layout.addLayout(self.edition_layout)

        self.description_layout = QHBoxLayout()
        self.description_label = QLabel("Description:")
        self.description_label.setFont(self.font)
        self.description_layout.addWidget(self.description_label)
        self.description_input = QLineEdit(fields[5])
        self.description_input = QLineEdit()
        self.description_input.setFont(self.font)
        self.description_input.setToolTip("Enter the description of the book.")
        self.description_layout.addWidget(self.description_input)
        self.form_layout.addLayout(self.description_layout)
        
        self.pages_layout = QHBoxLayout()
        self.pages_label = QLabel("Pages:")
        self.pages_label.setFont(self.font)
        self.pages_layout.addWidget(self.pages_label)
        self.pages_input = QLineEdit(fields[6])
        self.pages_input = QLineEdit()
        self.pages_input.setFont(self.font)
        self.pages_input.setToolTip("Enter the number of pages in the book.")
        self.pages_layout.addWidget(self.pages_input)
        self.form_layout.addLayout(self.pages_layout)
        
        self.photocopyprice_layout = QHBoxLayout()
        self.photocopyprice_label = QLabel("Photocopy Price:")
        self.photocopyprice_label.setFont(self.font)
        self.photocopyprice_layout.addWidget(self.photocopyprice_label)
        self.photocopyprice_input = QLineEdit(fields[7])
        self.photocopyprice_input = QLineEdit()
        self.photocopyprice_input.setFont(self.font)
        self.photocopyprice_input.setToolTip("Enter the price of a photocopy of the book.")
        self.photocopyprice_layout.addWidget(self.photocopyprice_input)
        self.form_layout.addLayout(self.photocopyprice_layout)
        
        self.bookprice_layout = QHBoxLayout()
        self.bookprice_label = QLabel("Book Price:")
        self.bookprice_label.setFont(self.font)
        self.bookprice_layout.addWidget(self.bookprice_label)
        self.bookprice_input = QLineEdit(fields[8])
        self.bookprice_input = QLineEdit()
        self.bookprice_input.setFont(self.font)
        self.bookprice_input.setToolTip("Enter the price of the book.")
        self.bookprice_layout.addWidget(self.bookprice_input)
        self.form_layout.addLayout(self.bookprice_layout)
        
        self.qtty_layout = QHBoxLayout()
        self.qtty_label = QLabel("Units:")
        self.qtty_label.setFont(self.font)
        self.qtty_layout.addWidget(self.qtty_label)
        self.qtty_input = QLineEdit(fields[9])
        self.qtty_input.setFont(self.font)
        self.qtty_input.setToolTip("Enter the available units of the book.")
        self.qtty_layout.addWidget(self.qtty_input)
        self.form_layout.addLayout(self.qtty_layout)
        
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save Book Changes")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the changes made to the book")
        self.layout.addWidget(self.save_button)

    def load_editorials(self):
        self.editorials = set()
        if os.path.isfile(EDITORIALS_PATH):
            with open(EDITORIALS_PATH, 'r') as file:
                reader = csv.reader(file)
                self.editorials = set(row[0] for row in reader)
        else:
            with open(STOCK_BOOKS_PATH, 'r') as file:
                reader = csv.reader(file)
                self.editorials = set(row[3] for row in reader if row[3].strip())
            self.save_editorials(EDITORIALS_PATH, self.editorials)
    
    def save_editorials(self, file_path, editorials):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for editorial in sorted(editorials):
                writer.writerow([editorial])
    
    def update_editorial_dropdown(self, new_editorial=None):
        self.editorial_dropdown.clear()
        self.editorial_dropdown.addItem("")
        self.editorial_dropdown.addItem("Add Editorial...")
        self.editorial_dropdown.addItems(sorted(self.editorials))
        if new_editorial:
            self.editorial_dropdown.setCurrentText(new_editorial)
    
    def check_add_editorial(self):
        if self.editorial_dropdown.currentText() == "Add Editorial...":
            text, ok = QInputDialog.getText(self, "Add Editorial", "Enter new editorial name:")
            if ok and text:
                self.editorials.add(text)
                self.save_editorials()
                self.update_editorial_dropdown(text)
            if not ok:
                self.editorial_dropdown.setCurrentIndex(0)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.name_input.text() or "-",
            self.author_input.text() or "-",
            self.editorial_dropdown.currentText() or "-",
            self.edition_input.text() or "-",
            self.description_input.text() or "-",
            self.pages_input.text() or "-",
            self.photocopyprice_input.text() or "-",
            self.bookprice_input.text() or "-",
            self.qtty_input.text() or "-"
            ]
            
        file_path = STOCK_BOOKS_PATH
    
        # Ensure that title is not empty
        if data[1] == "-" or len(data[1].strip()) == 0:
            raise ValueError("Book Title cannot be empty.")
    
        # Ensure that author is not empty
        if data[2] == "-" or len(data[2].strip()) == 0:
            raise ValueError("Book Author cannot be empty.")
    
        # Ensure that editorial is not empty
        if data[3] == "-" or len(data[3].strip()) == 0:
            raise ValueError("Book Editorial cannot be empty.")
    
        # Ensure that pages is a non-zero positive integer
        try:
            pages = int(data[6])
            if pages <= 0:
                raise ValueError("Pages must be a positive integer.")
        except ValueError:
            raise ValueError("Invalid Pages value. It must be a positive integer.")
    
        # Ensure that at least one of bookprice or photocopyprice is a non-zero positive number
        photocopyprice = None
        bookprice = None
        if data[7] != "-":
            try:
                photocopyprice = float(data[7])
                if photocopyprice <= 0:
                    raise ValueError("Photocopy Price must be a positive number.")
            except ValueError:
                raise ValueError("Invalid Photocopy Price. It must be a positive number.")
        
        if data[8] != "-":
            try:
                bookprice = float(data[8])
                if bookprice <= 0:
                    raise ValueError("Book Price must be a positive number.")
            except ValueError:
                raise ValueError("Invalid Book Price. It must be a positive number.")
        
        if photocopyprice is None and bookprice is None:
            raise ValueError("At least one of Book Price or Photocopy Price must be provided and be a positive number.")
        
        # Ensure that quantity is a non-zero positive integer
        try:
            quantity = int(data[-1])
            if quantity <= 0:
                raise ValueError("Units must be a positive integer.")
        except ValueError:
            raise ValueError("Invalid Units. It must be a positive integer.")

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] != data[0] and row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and row[4] == data[4] and row[7] == data[7]:
                        QMessageBox.critical(self, "Error", "This book already exists!")
                        return
                for row in rows:
                    if row[0] == data[0]:
                        row[1] = data[1]
                        row[2] = data[2]
                        row[3] = data[3]
                        row[4] = data[4]
                        row[5] = data[5]
                        row[6] = data[6]
                        row[7] = data[7]
                        row[8] = data[8]
                        row[9] = data[9]
                        break
        
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            QMessageBox.information(self, "Success", "Item updated successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

class EditSchoolItemDialog(QDialog):
    def __init__(self, parent, fields):
        super().__init__(parent)
        self.setWindowTitle("Editing School Item")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.load_categories()
        self.load_brands()

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
        self.type_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
        self.update_category_dropdown(fields[1])
        self.type_dropdown.currentIndexChanged.connect(self.check_add_category)
        self.type_layout.addWidget(self.type_dropdown)
        self.form_layout.addLayout(self.type_layout)

        self.product_name_layout = QHBoxLayout()
        self.product_name_label = QLabel("Item Name:")
        self.product_name_label.setFont(self.font)
        self.product_name_layout.addWidget(self.product_name_label)
        self.product_name_input = QLineEdit(fields[2])
        self.product_name_input = QLineEdit()
        self.product_name_input.setFont(self.font)
        self.product_name_input.setToolTip("Enter the name of the item.")
        self.product_name_layout.addWidget(self.product_name_input)
        self.form_layout.addLayout(self.product_name_layout)
        
        self.brand_layout = QHBoxLayout()
        self.brand_label = QLabel("Brand:")
        self.brand_label.setFont(self.font)
        self.brand_layout.addWidget(self.brand_label)
        self.brand_dropdown = QComboBox()
        self.brand_dropdown.setFont(self.font)
        self.brand_dropdown.setToolTip("Select or add a brand.")
        self.brand_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
        self.update_brand_dropdown(fields[3])
        self.brand_dropdown.currentIndexChanged.connect(self.check_add_brand)
        self.brand_layout.addWidget(self.brand_dropdown)
        self.form_layout.addLayout(self.brand_layout)

        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Color:")
        self.color_label.setFont(self.font)
        self.color_layout.addWidget(self.color_label)
        self.color_input = QLineEdit(fields[4])
        self.color_input = QLineEdit()
        self.color_input.setFont(self.font)
        self.color_input.setToolTip("Enter the color of the item.")
        self.color_layout.addWidget(self.color_input)
        self.form_layout.addLayout(self.color_layout)
        
        self.description_layout = QHBoxLayout()
        self.description_label = QLabel("Description:")
        self.description_label.setFont(self.font)
        self.description_layout.addWidget(self.description_label)
        self.description_input = QLineEdit(fields[5])
        self.description_input = QLineEdit()
        self.description_input.setFont(self.font)
        self.description_input.setToolTip("Enter the description of the item.")
        self.description_layout.addWidget(self.description_input)
        self.form_layout.addLayout(self.description_layout)
        
        self.price_layout = QHBoxLayout()
        self.price_label = QLabel("Price:")
        self.price_label.setFont(self.font)
        self.price_layout.addWidget(self.price_label)
        self.price_input = QLineEdit(fields[6])
        self.price_input = QLineEdit()
        self.price_input.setFont(self.font)
        self.price_input.setToolTip("Enter the price of the item.")
        self.price_layout.addWidget(self.price_input)
        self.form_layout.addLayout(self.price_layout)
        
        self.units_layout = QHBoxLayout()
        self.units_label = QLabel("Units:")
        self.units_label.setFont(self.font)
        self.units_layout.addWidget(self.units_label)
        self.units_input = QLineEdit(fields[7])
        self.units_input.setFont(self.font)
        self.units_input.setToolTip("Enter the available units of the item.")
        self.units_layout.addWidget(self.units_input)
        self.form_layout.addLayout(self.units_layout)

        self.boxes_layout = QHBoxLayout()
        self.boxes_label = QLabel("Boxes:")
        self.boxes_label.setFont(self.font)
        self.boxes_layout.addWidget(self.boxes_label)
        self.boxes_input = QLineEdit(fields[8])
        self.boxes_input.setFont(self.font)
        self.boxes_input.setToolTip("Enter the available boxes of the item.")
        self.boxes_layout.addWidget(self.boxes_input)
        self.form_layout.addLayout(self.boxes_layout)
        
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save Item Changes")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the changes made to the school item")
        self.layout.addWidget(self.save_button)

        self.previous_category = fields[1] if len(fields) > 1 else ""
        self.previous_brand = fields[3] if len(fields) > 3 else ""

    def load_categories(self):
        self.school_categories = set()
        if os.path.isfile(CATS_SCHOOL_PATH):
            with open(CATS_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_categories = set(row[0] for row in reader)
        else:
            with open(STOCK_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_categories = set(row[1] for row in reader if row[1].strip())
            self.save_categories(CATS_SCHOOL_PATH, self.school_categories)

    def save_categories(self, file_path, categories):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for category in sorted(categories):
                writer.writerow([category])

    def load_brands(self):
        self.school_brands = set()
        if os.path.isfile(BRANDS_SCHOOL_PATH):
            with open(BRANDS_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_brands = set(row[0] for row in reader)
        else:
            with open(STOCK_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_brands = set(row[3] for row in reader if row[3].strip())
            self.save_brands(BRANDS_SCHOOL_PATH, self.school_brands)

    def save_brands(self, file_path, brands):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for brand in sorted(brands):
                writer.writerow([brand])
    
    def check_add_category(self):
        if self.type_dropdown.currentText() == "Add Category...":
            text, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
            if ok and text:
                self.school_categories.add(text)
                self.save_categories(CATS_SCHOOL_PATH, self.school_categories)
                self.update_category_dropdown(text)
            if not ok:
                self.type_dropdown.setCurrentIndex(0)

    def check_add_brand(self):
        if self.brand_dropdown.currentText() == "Add Brand...":
            text, ok = QInputDialog.getText(self, "Add Brand", "Enter new brand name:")
            if ok and text:
                self.school_brands.add(text)
                self.save_brands(BRANDS_SCHOOL_PATH, self.school_brands)
                self.update_brand_dropdown(text)
            if not ok:
                self.brand_dropdown.setCurrentIndex(0)

    def update_category_dropdown(self, new_category=None):
        self.type_dropdown.clear()
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        self.type_dropdown.addItems(sorted(self.school_categories))
        if new_category:
            self.type_dropdown.setCurrentText(new_category)

    def update_brand_dropdown(self, new_brand=None):
        self.brand_dropdown.clear()
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        self.brand_dropdown.addItems(sorted(self.school_brands))
        if new_brand:
            self.brand_dropdown.setCurrentText(new_brand)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.type_dropdown.currentText() or "-",
            self.product_name_input.text() or "-",
            self.brand_dropdown.currentText() or "-",
            self.color_input.text() or "-",
            self.description_input.text() or "-",
            self.price_input.text() or "-",
            self.units_input.text() or "-",
            self.boxes_input.text() or "-"
        ]
    
        file_path = STOCK_SCHOOL_PATH
    
        # Ensure that category is not empty
        if data[1] == "-" or len(data[1].strip()) == 0:
            raise ValueError("Category cannot be empty.")
    
        # Ensure that name is not empty
        if data[2] == "-" or len(data[2].strip()) == 0:
            raise ValueError("Product Name cannot be empty.")
    
        # Ensure that brand is not empty
        if data[3] == "-" or len(data[3].strip()) == 0:
            raise ValueError("Brand cannot be empty.")
    
        # Ensure that price is a non-zero positive number
        try:
            price = float(data[6])
            if price <= 0:
                raise ValueError("Price must be a positive number.")
        except ValueError:
            raise ValueError("Invalid Price. It must be a positive number.")
    
        # Ensure that at least one of units or boxes quantity is a non-zero positive integer
        units = None
        boxes = None
        if data[7] != "-":
            try:
                units = int(data[7])
                if units <= 0:
                    raise ValueError("Units must be a positive integer.")
            except ValueError:
                raise ValueError("Invalid Units. It must be a positive integer.")
        
        if data[8] != "-":
            try:
                boxes = int(data[8])
                if boxes <= 0:
                    raise ValueError("Boxes must be a positive integer.")
            except ValueError:
                raise ValueError("Invalid Boxes. It must be a positive integer.")
        
        if units is None and boxes is None:
            raise ValueError("At least one of Units or Boxes must be provided and be a positive integer.")

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] != data[0] and row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and row[4] == data[4] and row[6] == data[6]:
                        QMessageBox.critical(self, "Error", "This school item already exists!")
                        return
                for row in rows:
                    if row[0] == data[0]:
                        row[1] = data[1]
                        row[2] = data[2]
                        row[3] = data[3]
                        row[4] = data[4]
                        row[5] = data[5]
                        row[6] = data[6]
                        row[7] = data[7]
                        row[8] = data[8]
                        break
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            QMessageBox.information(self, "Success", "School item updated successfully")
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

        self.load_categories()
        self.load_brands()

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
        self.type_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
        self.update_category_dropdown(fields[1])
        self.type_dropdown.currentIndexChanged.connect(self.check_add_category)
        self.type_layout.addWidget(self.type_dropdown)
        self.form_layout.addLayout(self.type_layout)

        self.product_name_layout = QHBoxLayout()
        self.product_name_label = QLabel("Item Name:")
        self.product_name_label.setFont(self.font)
        self.product_name_layout.addWidget(self.product_name_label)
        self.product_name_input = QLineEdit(fields[2])
        self.product_name_input = QLineEdit()
        self.product_name_input.setFont(self.font)
        self.product_name_input.setToolTip("Enter the name of the item.")
        self.product_name_layout.addWidget(self.product_name_input)
        self.form_layout.addLayout(self.product_name_layout)
        
        self.brand_layout = QHBoxLayout()
        self.brand_label = QLabel("Brand:")
        self.brand_label.setFont(self.font)
        self.brand_layout.addWidget(self.brand_label)
        self.brand_dropdown = QComboBox()
        self.brand_dropdown.setFont(self.font)
        self.brand_dropdown.setToolTip("Select or add a brand.")
        self.brand_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
        self.update_brand_dropdown(fields[3])
        self.brand_dropdown.currentIndexChanged.connect(self.check_add_brand)
        self.brand_layout.addWidget(self.brand_dropdown)
        self.form_layout.addLayout(self.brand_layout)

        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Color:")
        self.color_label.setFont(self.font)
        self.color_layout.addWidget(self.color_label)
        self.color_input = QLineEdit(fields[4])
        self.color_input = QLineEdit()
        self.color_input.setFont(self.font)
        self.color_input.setToolTip("Enter the color of the item.")
        self.color_layout.addWidget(self.color_input)
        self.form_layout.addLayout(self.color_layout)
        
        self.description_layout = QHBoxLayout()
        self.description_label = QLabel("Description:")
        self.description_label.setFont(self.font)
        self.description_layout.addWidget(self.description_label)
        self.description_input = QLineEdit(fields[5])
        self.description_input = QLineEdit()
        self.description_input.setFont(self.font)
        self.description_input.setToolTip("Enter the description of the item.")
        self.description_layout.addWidget(self.description_input)
        self.form_layout.addLayout(self.description_layout)
        
        self.price_layout = QHBoxLayout()
        self.price_label = QLabel("Price:")
        self.price_label.setFont(self.font)
        self.price_layout.addWidget(self.price_label)
        self.price_input = QLineEdit(fields[6])
        self.price_input = QLineEdit()
        self.price_input.setFont(self.font)
        self.price_input.setToolTip("Enter the price of the item.")
        self.price_layout.addWidget(self.price_input)
        self.form_layout.addLayout(self.price_layout)
        
        self.units_layout = QHBoxLayout()
        self.units_label = QLabel("Units:")
        self.units_label.setFont(self.font)
        self.units_layout.addWidget(self.units_label)
        self.units_input = QLineEdit(fields[7])
        self.units_input.setFont(self.font)
        self.units_input.setToolTip("Enter the available units of the item.")
        self.units_layout.addWidget(self.units_input)
        self.form_layout.addLayout(self.units_layout)

        self.boxes_layout = QHBoxLayout()
        self.boxes_label = QLabel("Boxes:")
        self.boxes_label.setFont(self.font)
        self.boxes_layout.addWidget(self.boxes_label)
        self.boxes_input = QLineEdit(fields[8])
        self.boxes_input.setFont(self.font)
        self.boxes_input.setToolTip("Enter the available boxes of the item.")
        self.boxes_layout.addWidget(self.boxes_input)
        self.form_layout.addLayout(self.boxes_layout)
        
        self.layout.addLayout(self.form_layout)

        self.save_button = QPushButton("Save Item Changes")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.save_button.setToolTip("Save the changes made to the school item")
        self.layout.addWidget(self.save_button)

        self.previous_category = fields[1] if len(fields) > 1 else ""
        self.previous_brand = fields[3] if len(fields) > 3 else ""

    def load_categories(self):
        self.office_categories = set()
        if os.path.isfile(CATS_OFFICE_PATH):
            with open(CATS_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.office_categories = set(row[0] for row in reader)
        else:
            with open(STOCK_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.office_categories = set(row[1] for row in reader if row[1].strip())
            self.save_categories(CATS_OFFICE_PATH, self.office_categories)

    def save_categories(self, file_path, categories):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for category in sorted(categories):
                writer.writerow([category])

    def load_brands(self):
        self.office_brands = set()
        if os.path.isfile(BRANDS_OFFICE_PATH):
            with open(BRANDS_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.office_brands = set(row[0] for row in reader)
        else:
            with open(STOCK_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                self.office_brands = set(row[3] for row in reader if row[3].strip())
            self.save_brands(BRANDS_OFFICE_PATH, self.office_brands)

    def save_brands(self, file_path, brands):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for brand in sorted(brands):
                writer.writerow([brand])
    
    def check_add_category(self):
        if self.type_dropdown.currentText() == "Add Category...":
            text, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
            if ok and text:
                self.office_categories.add(text)
                self.save_categories(CATS_SCHOOL_PATH, self.office_categories)
                self.update_category_dropdown(text)
            if not ok:
                self.type_dropdown.setCurrentIndex(0)

    def check_add_brand(self):
        if self.brand_dropdown.currentText() == "Add Brand...":
            text, ok = QInputDialog.getText(self, "Add Brand", "Enter new brand name:")
            if ok and text:
                self.office_brands.add(text)
                self.save_brands(BRANDS_SCHOOL_PATH, self.office_brands)
                self.update_brand_dropdown(text)
            if not ok:
                self.brand_dropdown.setCurrentIndex(0)

    def update_category_dropdown(self, new_category=None):
        self.type_dropdown.clear()
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        self.type_dropdown.addItems(sorted(self.office_categories))
        if new_category:
            self.type_dropdown.setCurrentText(new_category)

    def update_brand_dropdown(self, new_brand=None):
        self.brand_dropdown.clear()
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        self.brand_dropdown.addItems(sorted(self.office_brands))
        if new_brand:
            self.brand_dropdown.setCurrentText(new_brand)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.type_dropdown.currentText() or "-",
            self.product_name_input.text() or "-",
            self.brand_dropdown.currentText() or "-",
            self.color_input.text() or "-",
            self.description_input.text() or "-",
            self.price_input.text() or "-",
            self.units_input.text() or "-",
            self.boxes_input.text() or "-"
        ]
    
        file_path = STOCK_OFFICE_PATH
    
        # Ensure that category is not empty
        if data[1] == "-" or len(data[1].strip()) == 0:
            raise ValueError("Category cannot be empty.")
    
        # Ensure that name is not empty
        if data[2] == "-" or len(data[2].strip()) == 0:
            raise ValueError("Product Name cannot be empty.")
    
        # Ensure that brand is not empty
        if data[3] == "-" or len(data[3].strip()) == 0:
            raise ValueError("Brand cannot be empty.")
    
        # Ensure that price is a non-zero positive number
        try:
            price = float(data[6])
            if price <= 0:
                raise ValueError("Price must be a positive number.")
        except ValueError:
            raise ValueError("Invalid Price. It must be a positive number.")
    
        # Ensure that at least one of units or boxes quantity is a non-zero positive integer
        units = None
        boxes = None
        if data[7] != "-":
            try:
                units = int(data[7])
                if units <= 0:
                    raise ValueError("Units must be a positive integer.")
            except ValueError:
                raise ValueError("Invalid Units. It must be a positive integer.")
        
        if data[8] != "-":
            try:
                boxes = int(data[8])
                if boxes <= 0:
                    raise ValueError("Boxes must be a positive integer.")
            except ValueError:
                raise ValueError("Invalid Boxes. It must be a positive integer.")
        
        if units is None and boxes is None:
            raise ValueError("At least one of Units or Boxes must be provided and be a positive integer.")

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] != data[0] and row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and row[4] == data[4] and row[6] == data[6]:
                        QMessageBox.critical(self, "Error", "This school item already exists!")
                        return
                for row in rows:
                    if row[0] == data[0]:
                        row[1] = data[1]
                        row[2] = data[2]
                        row[3] = data[3]
                        row[4] = data[4]
                        row[5] = data[5]
                        row[6] = data[6]
                        row[7] = data[7]
                        row[8] = data[8]
                        break
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            QMessageBox.information(self, "Success", "Office item updated successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

def open_manage_menu(parent):
    dialog = ManageItemsDialog(parent)
    dialog.exec_()
