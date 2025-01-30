import os
import sys
import csv
import datetime
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.csv')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.csv')

class ManageItemsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Items")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.dropdown = QComboBox()
        self.dropdown.setFont(self.font)
        self.dropdown.addItems(["Books", "Office Items"])
        self.dropdown.currentIndexChanged.connect(self.update_search_dropdown)
        self.layout.addWidget(self.dropdown)

        self.search_layout = QHBoxLayout()
        self.search_dropdown = QComboBox()
        self.search_dropdown.setFont(self.font)
        self.search_layout.addWidget(self.search_dropdown)

        self.search_bar = QLineEdit()
        self.search_bar.setFont(self.font)
        self.search_bar.setPlaceholderText(f"Search {self.dropdown.currentText()}...")
        self.search_bar.textChanged.connect(self.update_list)
        self.search_layout.addWidget(self.search_bar)

        self.layout.addLayout(self.search_layout)

        if sys.platform == "win32":
            self.save_button = QPushButton("Save Spreadsheet to Desktop")
        else:
            self.save_button = QPushButton("Save Spreadsheet to Home")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_to_desktop)
        self.layout.addWidget(self.save_button)

        self.table_widget = QTableWidget()
        self.table_widget.setFont(self.font)
        self.table_widget.setColumnCount(8)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.itemSelectionChanged.connect(self.update_buttons)
        self.table_widget.itemDoubleClicked.connect(self.edit_item)
        self.layout.addWidget(self.table_widget)

        self.button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFont(self.font)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_item)
        self.button_layout.addWidget(self.edit_button)

        self.add_button = QPushButton("Add 1")
        self.add_button.setFont(self.font)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_to_inventory)
        self.button_layout.addWidget(self.add_button)

        self.subtract_button = QPushButton("Subtract 1")
        self.subtract_button.setFont(self.font)
        self.subtract_button.setEnabled(False)
        self.subtract_button.clicked.connect(self.subtract_from_inventory)
        self.button_layout.addWidget(self.subtract_button)

        self.delete_button = QPushButton("Delete this Item")
        self.delete_button.setFont(self.font)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_item)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.update_search_dropdown()
        self.update_list()

    def update_search_dropdown(self):
        self.search_dropdown.clear()
        if self.dropdown.currentText() == "Books":
            self.search_dropdown.addItems(["ID", "Book Name", "Author", "Edition", "Pages", "Photocopy Price", "Book Price", "Quantity"])
            self.table_widget.setHorizontalHeaderLabels(["ID", "Book Name", "Author", "Edition", "Pages", "Photocopy Price", "Book Price", "Quantity"])
        else:
            self.search_dropdown.addItems(["ID", "Category", "Product Name", "Brand", "Color", "Price", "Quantity"])
            self.table_widget.setHorizontalHeaderLabels(["ID", "Category", "Product Name", "Brand", "Color", "Price", "Quantity"])
        self.update_list()

    def update_list(self):
        self.table_widget.setRowCount(0)
        search_text = self.search_bar.text().lower()
        search_index = self.search_dropdown.currentIndex()

        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if search_text in row[search_index].lower():
                        row_position = self.table_widget.rowCount()
                        self.table_widget.insertRow(row_position)
                        for column, item in enumerate(row):
                            self.table_widget.setItem(row_position, column, QTableWidgetItem(item))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load items: {e}")

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
        current_time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M")
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
    
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            with open(save_path, 'w') as file:
                file.write(data)
            QMessageBox.information(self, "Success", f"File saved to {save_path}")
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
        fields = [self.table_widget.item(selected_row, i).text() for i in range(self.table_widget.columnCount())]
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

            QMessageBox.information(self, "Success", "Item count updated successfully")
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

    def subtract_from_inventory(self):
        selected_row = self.table_widget.currentRow()
        fields = [self.table_widget.item(selected_row, i).text() for i in range(self.table_widget.columnCount())]
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
                                                         "This is the last item in inventory. Do you want to delete it?", 
                                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                rows.remove(row)
                            else:
                                row[-1] = '1'
                        break

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Success", "Item removed from inventory")
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

    def delete_item(self):
        selected_row = self.table_widget.currentRow()
        fields = [self.table_widget.item(selected_row, i).text() for i in range(self.table_widget.columnCount())]
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = [row for row in reader if row[0] != fields[0]]

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            QMessageBox.information(self, "Success", "Item deleted successfully")
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete item: {e}")

class EditBookDialog(QDialog):
    def __init__(self, parent, fields):
        super().__init__(parent)
        self.setWindowTitle("Edit Book")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.id_label = QLabel(f"ID: {fields[0]}")
        self.id_label.setFont(self.font)
        self.layout.addWidget(self.id_label)

        self.name_input = QLineEdit(fields[1] if len(fields) > 1 else "")
        self.name_input.setFont(self.font)
        self.layout.addWidget(self.name_input)

        self.author_input = QLineEdit(fields[2] if len(fields) > 2 else "")
        self.author_input.setFont(self.font)
        self.layout.addWidget(self.author_input)

        self.edition_input = QLineEdit(fields[3] if len(fields) > 3 else "")
        self.edition_input.setFont(self.font)
        self.layout.addWidget(self.edition_input)

        self.pages_input = QLineEdit(fields[4] if len(fields) > 4 else "")
        self.pages_input.setFont(self.font)
        self.layout.addWidget(self.pages_input)

        self.price_input = QLineEdit(fields[5] if len(fields) > 5 else "")
        self.price_input.setFont(self.font)
        self.layout.addWidget(self.price_input)

        self.qtty_input = QLineEdit(fields[6] if len(fields) > 6 else "")
        self.qtty_input.setFont(self.font)
        self.layout.addWidget(self.qtty_input)

        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.name_input.text() or "-",
            self.author_input.text() or "-",
            self.edition_input.text() or "-",
            self.pages_input.text() or "-",
            self.price_input.text() or "-",
            self.qtty_input.text() or "-"
        ]

        try:
            with open(LATEST_BOOKS_PATH, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == data[0]:
                        row[1:] = data[1:]
                        break

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
        self.setWindowTitle("Edit Office Item")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.id_label = QLabel(f"ID: {fields[0]}")
        self.id_label.setFont(self.font)
        self.layout.addWidget(self.id_label)

        self.type_input = QLineEdit(fields[1] if len(fields) > 1 else "")
        self.type_input.setFont(self.font)
        self.layout.addWidget(self.type_input)

        self.product_name_input = QLineEdit(fields[2] if len(fields) > 2 else "")
        self.product_name_input.setFont(self.font)
        self.layout.addWidget(self.product_name_input)

        self.color_input = QLineEdit(fields[3] if len(fields) > 3 else "")
        self.color_input.setFont(self.font)
        self.layout.addWidget(self.color_input)

        self.price_input = QLineEdit(fields[4] if len(fields) > 4 else "")
        self.price_input.setFont(self.font)
        self.layout.addWidget(self.price_input)

        self.qtty_input = QLineEdit(fields[5] if len(fields) > 5 else "")
        self.qtty_input.setFont(self.font)
        self.layout.addWidget(self.qtty_input)

        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button)

    def save_item(self):
        data = [
            self.id_label.text().split(": ")[1],
            self.type_input.text() or "-",
            self.product_name_input.text() or "-",
            self.color_input.text() or "-",
            self.price_input.text() or "-",
            self.qtty_input.text() or "-"
        ]

        try:
            with open(LATEST_OFFICE_PATH, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == data[0]:
                        row[1:] = data[1:]
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