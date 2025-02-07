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
DATA_PATH = os.path.join(PROGRAM_PATH, 'data')
STOCK_SCHOOL_PATH = os.path.join(DATA_PATH, 'stock_school.pystk')
STOCK_OFFICE_PATH = os.path.join(DATA_PATH, 'stock_office.pystk')
STOCK_BOOKS_PATH = os.path.join(DATA_PATH, 'stock_books.pystk')
CATS_SCHOOL_PATH = os.path.join(DATA_PATH, 'cats_school.pystk')
CATS_OFFICE_PATH = os.path.join(DATA_PATH, 'cats_office.pystk')
BRANDS_SCHOOL_PATH = os.path.join(DATA_PATH, 'brands_school.pystk')
BRANDS_OFFICE_PATH = os.path.join(DATA_PATH, 'brands_office.pystk')
EDITORIALS_PATH = os.path.join(DATA_PATH, 'editorials.pystk')

class AddItemsDialog(QDialog):
    def __init__(self, parent=None):
        global school_count
        global office_count
        global books_count

        super().__init__(parent)
        self.setWindowTitle("Add Items to Stock")
        self.setGeometry(100, 100, 400, 300)
    
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
        try:
            os.makedirs(SAVES_PATH, exist_ok=True)
            os.makedirs(DATA_PATH, exist_ok=True)

            if not os.path.isfile(STOCK_SCHOOL_PATH):
                with open(STOCK_SCHOOL_PATH, 'w') as file:
                    pass
            if not os.path.isfile(STOCK_OFFICE_PATH):
                with open(STOCK_OFFICE_PATH, 'w') as file:
                    pass
            if not os.path.isfile(STOCK_BOOKS_PATH):
                with open(STOCK_BOOKS_PATH, 'w') as file:
                    pass

            with open(STOCK_SCHOOL_PATH, 'r') as file:
                school_count = sum(1 for line in file if line.strip())
            with open(STOCK_OFFICE_PATH, 'r') as file:
                office_count = sum(1 for line in file if line.strip())
            with open(STOCK_BOOKS_PATH, 'r') as file:
                books_count = sum(1 for line in file if line.strip())
    
            self.load_categories()
            self.load_brands()
            self.load_editorials()
        except Exception as e:
            print(e)
    
        self.dropdown = QComboBox()
        self.dropdown.addItems(["School Items", "Office Items", "Books"])
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
        self.school_categories = set()
        self.office_categories = set()
        if os.path.isfile(CATS_SCHOOL_PATH):
            with open(CATS_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_categories = set(row[0] for row in reader)
        else:
            with open(STOCK_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_categories = set(row[1] for row in reader if row[1].strip())
            self.save_categories(CATS_SCHOOL_PATH, self.school_categories)
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
        self.school_brands = set()
        self.office_brands = set()
        if os.path.isfile(BRANDS_SCHOOL_PATH):
            with open(BRANDS_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_brands = set(row[0] for row in reader)
        else:
            with open(STOCK_SCHOOL_PATH, 'r') as file:
                reader = csv.reader(file)
                self.school_brands = set(row[3] for row in reader if row[3].strip())
            self.save_brands(BRANDS_SCHOOL_PATH, self.school_brands)
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
        global school_count
        global office_count
        global books_count
    
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
            self.setWindowTitle("Add Books to Stock")

            new_id = self.get_next_available_id(STOCK_BOOKS_PATH)
            self.id_label = QLabel(f"ID: {new_id}")
            self.id_label_font = QFont()
            self.id_label_font.setPointSize(14)
            self.id_label.setFont(self.id_label_font)
            self.form_layout.addWidget(self.id_label)
            
            self.name_layout = QHBoxLayout()
            self.name_label = QLabel("Title:")
            self.name_label.setFont(self.id_label_font)
            self.name_layout.addWidget(self.name_label)
            self.name_input = QLineEdit()
            self.name_input.setFont(self.id_label_font)
            self.name_input.setToolTip("Enter the title of the book.")
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
            
            self.editorial_layout = QHBoxLayout()
            self.editorial_label = QLabel("Editorial:")
            self.editorial_label.setFont(self.id_label_font)
            self.editorial_layout.addWidget(self.editorial_label)
            self.editorial_dropdown = QComboBox()
            self.editorial_dropdown.setFont(self.id_label_font)
            self.editorial_dropdown.setToolTip("Select or add an editorial.")
            self.editorial_dropdown.setMaxVisibleItems(10)  # Set the maximum number of visible items
            self.update_editorial_dropdown()
            self.editorial_dropdown.currentIndexChanged.connect(self.check_add_editorial)
            self.editorial_layout.addWidget(self.editorial_dropdown)
            self.form_layout.addLayout(self.editorial_layout)

            self.edition_layout = QHBoxLayout()
            self.edition_label = QLabel("Edition:")
            self.edition_label.setFont(self.id_label_font)
            self.edition_layout.addWidget(self.edition_label)
            self.edition_input = QLineEdit()
            self.edition_input.setFont(self.id_label_font)
            self.edition_input.setToolTip("Enter the edition of the book.")
            self.edition_layout.addWidget(self.edition_input)
            self.form_layout.addLayout(self.edition_layout)

            self.description_layout = QHBoxLayout()
            self.description_label = QLabel("Description:")
            self.description_label.setFont(self.id_label_font)
            self.description_layout.addWidget(self.description_label)
            self.description_input = QLineEdit()
            self.description_input.setFont(self.id_label_font)
            self.description_input.setToolTip("Enter the description of the book.")
            self.description_layout.addWidget(self.description_input)
            self.form_layout.addLayout(self.description_layout)
            
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
            self.qtty_label = QLabel("Units:")
            self.qtty_label.setFont(self.id_label_font)
            self.qtty_layout.addWidget(self.qtty_label)
            self.qtty_input = QLineEdit("1")
            self.qtty_input.setFont(self.id_label_font)
            self.qtty_input.setToolTip("Enter the available units of the book.")
            self.qtty_layout.addWidget(self.qtty_input)
            self.form_layout.addLayout(self.qtty_layout)

        elif self.dropdown.currentText() == "School Items":
            self.setWindowTitle("Add School Items to Stock")

            new_id = self.get_next_available_id(STOCK_SCHOOL_PATH)
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
            self.product_name_label = QLabel("Item Name:")
            self.product_name_label.setFont(self.id_label_font)
            self.product_name_layout.addWidget(self.product_name_label)
            self.product_name_input = QLineEdit()
            self.product_name_input.setFont(self.id_label_font)
            self.product_name_input.setToolTip("Enter the name of the item.")
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
            self.color_input.setToolTip("Enter the color of the item.")
            self.color_layout.addWidget(self.color_input)
            self.form_layout.addLayout(self.color_layout)
            
            self.description_layout = QHBoxLayout()
            self.description_label = QLabel("Description:")
            self.description_label.setFont(self.id_label_font)
            self.description_layout.addWidget(self.description_label)
            self.description_input = QLineEdit()
            self.description_input.setFont(self.id_label_font)
            self.description_input.setToolTip("Enter the description of the item.")
            self.description_layout.addWidget(self.description_input)
            self.form_layout.addLayout(self.description_layout)
            
            self.price_layout = QHBoxLayout()
            self.price_label = QLabel("Price:")
            self.price_label.setFont(self.id_label_font)
            self.price_layout.addWidget(self.price_label)
            self.price_input = QLineEdit()
            self.price_input.setFont(self.id_label_font)
            self.price_input.setToolTip("Enter the price of the item.")
            self.price_layout.addWidget(self.price_input)
            self.form_layout.addLayout(self.price_layout)
            
            self.units_layout = QHBoxLayout()
            self.units_label = QLabel("Units:")
            self.units_label.setFont(self.id_label_font)
            self.units_layout.addWidget(self.units_label)
            self.units_input = QLineEdit("1")
            self.units_input.setFont(self.id_label_font)
            self.units_input.setToolTip("Enter the available units of the item.")
            self.units_layout.addWidget(self.units_input)
            self.form_layout.addLayout(self.units_layout)

            self.boxes_layout = QHBoxLayout()
            self.boxes_label = QLabel("Boxes:")
            self.boxes_label.setFont(self.id_label_font)
            self.boxes_layout.addWidget(self.boxes_label)
            self.boxes_input = QLineEdit("1")
            self.boxes_input.setFont(self.id_label_font)
            self.boxes_input.setToolTip("Enter the available boxes of the item.")
            self.boxes_layout.addWidget(self.boxes_input)
            self.form_layout.addLayout(self.boxes_layout)

        else:
            self.setWindowTitle("Add Office Items to Stock")

            new_id = self.get_next_available_id(STOCK_OFFICE_PATH)
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
            self.product_name_label = QLabel("Item Name:")
            self.product_name_label.setFont(self.id_label_font)
            self.product_name_layout.addWidget(self.product_name_label)
            self.product_name_input = QLineEdit()
            self.product_name_input.setFont(self.id_label_font)
            self.product_name_input.setToolTip("Enter the name of the item.")
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
            self.color_input.setToolTip("Enter the color of the item.")
            self.color_layout.addWidget(self.color_input)
            self.form_layout.addLayout(self.color_layout)
            
            self.description_layout = QHBoxLayout()
            self.description_label = QLabel("Description:")
            self.description_label.setFont(self.id_label_font)
            self.description_layout.addWidget(self.description_label)
            self.description_input = QLineEdit()
            self.description_input.setFont(self.id_label_font)
            self.description_input.setToolTip("Enter the description of the item.")
            self.description_layout.addWidget(self.description_input)
            self.form_layout.addLayout(self.description_layout)
            
            self.price_layout = QHBoxLayout()
            self.price_label = QLabel("Price:")
            self.price_label.setFont(self.id_label_font)
            self.price_layout.addWidget(self.price_label)
            self.price_input = QLineEdit()
            self.price_input.setFont(self.id_label_font)
            self.price_input.setToolTip("Enter the price of the item.")
            self.price_layout.addWidget(self.price_input)
            self.form_layout.addLayout(self.price_layout)
            
            self.units_layout = QHBoxLayout()
            self.units_label = QLabel("Units:")
            self.units_label.setFont(self.id_label_font)
            self.units_layout.addWidget(self.units_label)
            self.units_input = QLineEdit("1")
            self.units_input.setFont(self.id_label_font)
            self.units_input.setToolTip("Enter the available units of the item.")
            self.units_layout.addWidget(self.units_input)
            self.form_layout.addLayout(self.units_layout)

            self.boxes_layout = QHBoxLayout()
            self.boxes_label = QLabel("Boxes:")
            self.boxes_label.setFont(self.id_label_font)
            self.boxes_layout.addWidget(self.boxes_label)
            self.boxes_input = QLineEdit("1")
            self.boxes_input.setFont(self.id_label_font)
            self.boxes_input.setToolTip("Enter the available boxes of the item.")
            self.boxes_layout.addWidget(self.boxes_input)
            self.form_layout.addLayout(self.boxes_layout)

    def check_add_category(self):
        if self.type_dropdown.currentText() == "Add Category...":
            text, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
            if ok and text:
                if self.dropdown.currentText() == "School Items":
                    self.school_categories.add(text)
                    self.save_categories(CATS_SCHOOL_PATH, self.school_categories)
                else:
                    self.office_categories.add(text)
                    self.save_categories(CATS_OFFICE_PATH, self.office_categories)
                self.update_category_dropdown(text)
            if not ok:
                self.type_dropdown.setCurrentIndex(0)

    def check_add_brand(self):
        if self.brand_dropdown.currentText() == "Add Brand...":
            text, ok = QInputDialog.getText(self, "Add Brand", "Enter new brand name:")
            if ok and text:
                if self.dropdown.currentText() == "School Items":
                    self.school_brands.add(text)
                    self.save_brands(BRANDS_SCHOOL_PATH, self.school_brands)
                else:
                    self.office_brands.add(text)
                    self.save_brands(BRANDS_OFFICE_PATH, self.office_brands)
                self.update_brand_dropdown(text)
            if not ok:
                self.brand_dropdown.setCurrentIndex(0)
    
    def check_add_editorial(self):
        if self.editorial_dropdown.currentText() == "Add Editorial...":
            text, ok = QInputDialog.getText(self, "Add Editorial", "Enter new editorial name:")
            if ok and text:
                self.editorials.add(text)
                self.save_editorials()
                self.update_editorial_dropdown(text)
            if not ok:
                self.editorial_dropdown.setCurrentIndex(0)

    def update_category_dropdown(self, new_category=None):
        self.type_dropdown.clear()
        self.type_dropdown.addItem("")
        self.type_dropdown.addItem("Add Category...")
        if self.dropdown.currentText() == "School Items":
            self.type_dropdown.addItems(sorted(self.school_categories))
        else:
            self.type_dropdown.addItems(sorted(self.office_categories))
        if new_category:
            self.type_dropdown.setCurrentText(new_category)

    def update_brand_dropdown(self, new_brand=None):
        self.brand_dropdown.clear()
        self.brand_dropdown.addItem("")
        self.brand_dropdown.addItem("Add Brand...")
        if self.dropdown.currentText() == "School Items":
            self.brand_dropdown.addItems(sorted(self.school_brands))
        else:
            self.brand_dropdown.addItems(sorted(self.office_brands))
        if new_brand:
            self.brand_dropdown.setCurrentText(new_brand)
    
    def update_editorial_dropdown(self, new_editorial=None):
        self.editorial_dropdown.clear()
        self.editorial_dropdown.addItem("")
        self.editorial_dropdown.addItem("Add Editorial...")
        self.editorial_dropdown.addItems(sorted(self.editorials))
        if new_editorial:
            self.editorial_dropdown.setCurrentText(new_editorial)

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
            self.editorial_dropdown.setCurrentIndex(0)
            self.edition_input.clear()
            self.description_input.clear()
            self.pages_input.clear()
            self.photocopyprice_input.clear()
            self.bookprice_input.clear()
            self.qtty_input.setText("1")
        else:
            self.type_dropdown.setCurrentIndex(0)
            self.product_name_input.clear()
            self.brand_dropdown.setCurrentIndex(0)
            self.color_input.clear()
            self.description_input.clear()
            self.price_input.clear()
            self.units_input.setText("1")
            self.boxes_input.setText("1")

    def save_item(self):
        global school_count
        global office_count
        global books_count
        try:
            if self.dropdown.currentText() == "Books":
                new_id = self.get_next_available_id(STOCK_BOOKS_PATH)
                data = [
                    new_id,
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

            elif self.dropdown.currentText() == "School Items":
                new_id = self.get_next_available_id(STOCK_SCHOOL_PATH)
                data = [
                    new_id,
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

            else:
                new_id = self.get_next_available_id(STOCK_OFFICE_PATH)
                data = [
                    new_id,
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
    
            exists = False
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if self.dropdown.currentText() == 'Books':
                        if row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and data[4] == row[4] and row[7] == data[7]:
                            row[-1] = str(int(row[-1]) + int(data[-1]))
                            existent_item = row[1]
                            added_item_count = int(data[-1])
                            exists = True
                            break
                    else:
                        if self.dropdown.currentText() == 'School Items':
                            if row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and row[4] == data[4] and row[6] == data[6]:
                                row[-1] = str(int(row[-1]) + int(data[-1]))
                                row[-2] = str(int(row[-2]) + int(data[-2]))
                                existent_item = row[2]
                                added_boxes_count = int(data[-1])
                                added_units_count = int(data[-2])
                                exists = True
                                break
                        else:
                            if row[1] == data[1] and row[2] == data[2] and row[3] == data[3] and row[4] == data[4] and row[6] == data[6]:
                                row[-1] = str(int(row[-1]) + int(data[-1]))
                                row[-2] = str(int(row[-2]) + int(data[-2]))
                                existent_item = row[2]
                                added_boxes_count = int(data[-1])
                                added_units_count = int(data[-2])
                                exists = True
                                break
    
            if not exists:
                rows.append(data)
    
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    
            if self.dropdown.currentText() == "Books":
                books_count += 1
            elif self.dropdown.currentText() == "School Items":
                school_count += 1
            else:
                office_count += 1
    
            self.clear_fields()
            self.update_form()
    
            if exists:
                if self.dropdown.currentText() == 'Books':
                    QMessageBox.information(self, "Success", f'Added {added_item_count} unit(s) to the already saved "{existent_item}" book in the stock.')
                
                elif self.dropdown.currentText() == 'School Items':
                    QMessageBox.information(self, "Success", f'Added {added_units_count} unit(s) and {added_boxes_count} box(es) to the already saved "{existent_item}" school item in the stock.')
                else:
                    QMessageBox.information(self, "Success", f'Added {added_units_count} unit(s) and {added_boxes_count} box(es) to the already saved "{existent_item}" office item in the stock.')
            else:
                if self.dropdown.currentText() == 'Books':
                    QMessageBox.information(self, "Success", "Book added to the stock.")
                elif self.dropdown.currentText() == 'School Items':
                    QMessageBox.information(self, "Success", "School item added to the stock.")
                else:
                    QMessageBox.information(self, "Success", "Office item added to the stock.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

def open_add_menu(parent):
    dialog = AddItemsDialog(parent)
    dialog.exec_()
