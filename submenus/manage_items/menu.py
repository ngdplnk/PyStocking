import os
import sys
import csv
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QListWidgetItem, QScrollArea, QWidget)
from PyQt5.QtGui import QFont

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
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.dropdown = QComboBox()
        self.dropdown.setFont(self.font)
        self.dropdown.addItems(["Books", "Office Items"])
        self.dropdown.currentIndexChanged.connect(self.update_list)
        self.layout.addWidget(self.dropdown)

        self.save_button = QPushButton("Save to Desktop")
        self.save_button.setFont(self.font)
        self.save_button.clicked.connect(self.save_to_desktop)
        self.layout.addWidget(self.save_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.list_widget = QListWidget()
        self.list_widget.setFont(self.font)
        self.list_widget.itemSelectionChanged.connect(self.update_buttons)
        self.scroll_layout.addWidget(self.list_widget)

        self.button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFont(self.font)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_item)
        self.button_layout.addWidget(self.edit_button)

        self.sum_button = QPushButton("Sum 1 to this item")
        self.sum_button.setFont(self.font)
        self.sum_button.setEnabled(False)
        self.sum_button.clicked.connect(self.sum_to_item)
        self.button_layout.addWidget(self.sum_button)

        self.subs_button = QPushButton("Substract 1 to this item")
        self.subs_button.setFont(self.font)
        self.subs_button.setEnabled(False)
        self.subs_button.clicked.connect(self.subs_from_item)
        self.button_layout.addWidget(self.subs_button)

        self.delete_button = QPushButton("Delete this Item")
        self.delete_button.setFont(self.font)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_item)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    item = QListWidgetItem(", ".join(row))
                    self.list_widget.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load items: {e}")

    def update_buttons(self):
        if self.list_widget.selectedItems():
            self.edit_button.setEnabled(True)
            self.sum_button.setEnabled(True)
            self.subs_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.sum_button.setEnabled(False)
            self.subs_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def save_to_desktop(self):
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
            save_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'latest_books.csv')
        else:
            file_path = LATEST_OFFICE_PATH
            save_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'latest_office.csv')

        try:
            with open(file_path, 'r') as file:
                data = file.read()
            with open(save_path, 'w') as file:
                file.write(data)
            QMessageBox.information(self, "Success", f"File saved to {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def edit_item(self):
        selected_item = self.list_widget.currentItem().text()
        fields = selected_item.split(", ")
        if self.dropdown.currentText() == "Books":
            self.edit_dialog = EditBookDialog(self, fields)
        else:
            self.edit_dialog = EditOfficeItemDialog(self, fields)
        self.edit_dialog.exec_()
        self.update_list()

    def sum_to_item(self):
        selected_item = self.list_widget.currentItem().text()
        fields = selected_item.split(", ")
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[1] == fields[1]:
                        row[-1] = str(int(row[-1]) + 1)
                        break

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            QMessageBox.information(self, "Success", "Item count updated successfully")
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update item: {e}")

    def subs_from_item(self):
        selected_item = self.list_widget.currentItem().text()
        fields = selected_item.split(", ")
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[1] == fields[1]:
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
        selected_item = self.list_widget.currentItem().text()
        fields = selected_item.split(", ")
        if self.dropdown.currentText() == "Books":
            file_path = LATEST_BOOKS_PATH
        else:
            file_path = LATEST_OFFICE_PATH

        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = [row for row in reader if row[1] != fields[1]]

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

        self.name_input = QLineEdit(fields[1])
        self.name_input.setFont(self.font)
        self.layout.addWidget(self.name_input)

        self.author_input = QLineEdit(fields[2])
        self.author_input.setFont(self.font)
        self.layout.addWidget(self.author_input)

        self.edition_input = QLineEdit(fields[3])
        self.edition_input.setFont(self.font)
        self.layout.addWidget(self.edition_input)

        self.pages_input = QLineEdit(fields[4])
        self.pages_input.setFont(self.font)
        self.layout.addWidget(self.pages_input)

        self.price_input = QLineEdit(fields[5])
        self.price_input.setFont(self.font)
        self.layout.addWidget(self.price_input)

        self.qtty_input = QLineEdit(fields[6])
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

        self.type_input = QLineEdit(fields[1])
        self.type_input.setFont(self.font)
        self.layout.addWidget(self.type_input)

        self.product_name_input = QLineEdit(fields[2])
        self.product_name_input.setFont(self.font)
        self.layout.addWidget(self.product_name_input)

        self.color_input = QLineEdit(fields[3])
        self.color_input.setFont(self.font)
        self.layout.addWidget(self.color_input)

        self.price_input = QLineEdit(fields[4])
        self.price_input.setFont(self.font)
        self.layout.addWidget(self.price_input)

        self.qtty_input = QLineEdit(fields[5])
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