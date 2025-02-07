import sys
import os
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSizePolicy, QHBoxLayout, QMessageBox, QScrollArea, QVBoxLayout, QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView, QToolTip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QCursor
from submenus.add_items.menu import open_add_menu
from submenus.manage_items.menu import open_manage_menu
from submenus.advanced_options.menu import open_advanced_options_menu

# Get PATHS
if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
DATA_PATH = os.path.join(PROGRAM_PATH, 'data')
STOCK_SCHOOL_PATH = os.path.join(DATA_PATH, 'stock_school.pystk')
STOCK_OFFICE_PATH = os.path.join(DATA_PATH, 'stock_office.pystk')
STOCK_BOOKS_PATH = os.path.join(DATA_PATH, 'stock_books.pystk')
ICON_PATH = os.path.join(PROGRAM_PATH, 'assets', 'icon.ico')

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window icon
        if os.path.isfile(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        # Window title
        self.setWindowTitle("PyStocking - Main Menu")

        # Set window size
        self.setGeometry(100, 100, 900, 500)

        self.font = QFont()
        self.font.setPointSize(14)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title label
        title_label = QLabel("Welcome to PyStocking!")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Available items label
        line_count = self.get_line_count()
        line_count_label = QLabel(self.update_line_count(line_count))
        line_count_font = QFont()
        line_count_font.setPointSize(18)
        line_count_label.setFont(line_count_font)
        line_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(line_count_label)

        # Buttons layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Add items button
        add_button = QPushButton("Add Items")
        add_button.setFont(self.font)
        add_button.setToolTip("Add new items to the stock")
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setFixedHeight(60)
        buttons_layout.addWidget(add_button)

        # Manage items button
        manage_button = QPushButton("Manage and Search Items")
        manage_button.setFont(self.font)
        manage_button.setToolTip("Manage and search items from the stock")
        manage_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        manage_button.setFixedHeight(60)
        buttons_layout.addWidget(manage_button)

        # Advanced options button
        advanced_options_button = QPushButton("Advanced Options")
        advanced_options_button.setFont(self.font)
        advanced_options_button.setToolTip("Open advanced options")
        advanced_options_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        advanced_options_button.setFixedHeight(60)
        buttons_layout.addWidget(advanced_options_button)

        # Exit button
        exit_button = QPushButton("Close program")
        exit_button.setFont(self.font)
        exit_button.setToolTip("Exit the program")
        exit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        exit_button.setFixedHeight(60)
        buttons_layout.addWidget(exit_button)

        # Add buttons layout to main layout
        layout.addLayout(buttons_layout)

        central_widget.setLayout(layout)

        # Adjust button widths to match the title width
        self.adjust_button_widths(title_label, [add_button, manage_button, advanced_options_button, exit_button])

        # Connect button actions
        add_button.clicked.connect(lambda: (open_add_menu(self), self.update_line_count_and_check_stock(line_count_label)))
        manage_button.clicked.connect(lambda: (open_manage_menu(self), self.update_line_count_and_check_stock(line_count_label)))
        advanced_options_button.clicked.connect(lambda: (open_advanced_options_menu(self), self.update_line_count_and_check_stock(line_count_label)))
        exit_button.clicked.connect(self.close)

        # Initial check stock levels and update line count
        self.update_line_count_and_check_stock(line_count_label)

    def adjust_button_widths(self, reference_label, buttons):
        reference_width = reference_label.sizeHint().width()
        for button in buttons:
            button.setFixedWidth(reference_width)

    # Get line count - Create file
    def get_line_count(self):
        try:
            line_count = {
                'school': 0,
                'office': 0,
                'books': 0
            }
            # Ensure the directory exists
            os.makedirs(PROGRAM_PATH, exist_ok=True)
            os.makedirs(SAVES_PATH, exist_ok=True)
            os.makedirs(DATA_PATH, exist_ok=True)
            os.makedirs(os.path.dirname(STOCK_SCHOOL_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(STOCK_OFFICE_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(STOCK_BOOKS_PATH), exist_ok=True)

            # Ensure the file exists
            if not os.path.isfile(STOCK_SCHOOL_PATH):
                with open(STOCK_SCHOOL_PATH, 'w') as file:
                    pass  # Create an empty file if it doesn't exist
            if not os.path.isfile(STOCK_OFFICE_PATH):
                with open(STOCK_OFFICE_PATH, 'w') as file:
                    pass  # Create an empty file if it doesn't exist
            if not os.path.isfile(STOCK_BOOKS_PATH):
                with open(STOCK_BOOKS_PATH, 'w') as file:
                    pass  # Create an empty file if it doesn't exist

            # Get line count
            with open(STOCK_SCHOOL_PATH, 'r') as file:
                line_count['school'] = sum(1 for _ in file)
            with open(STOCK_OFFICE_PATH, 'r') as file:
                line_count['office'] = sum(1 for _ in file)
            with open(STOCK_BOOKS_PATH, 'r') as file:
                line_count['books'] = sum(1 for _ in file)
            return line_count
        except Exception as e:
            return f"Error: {e}"

    def update_line_count_and_check_stock(self, line_count_label):
        line_count = self.get_line_count()
        line_count_label.setText(self.update_line_count(line_count))
        self.check_stock_levels()

    def update_line_count(self, line_count):
        if line_count['books'] == 0 and line_count['office'] == 0 and line_count['school'] == 0:
            line_count_label = "No items in stock"
        elif line_count['books'] == 0 and line_count['office'] == 0:
            line_count_label = f"There are {line_count['school']} school item(s) in stock"
        elif line_count['books'] == 0 and line_count['school'] == 0:
            line_count_label = f"There are {line_count['office']} office item(s) in stock"
        elif line_count['office'] == 0 and line_count['school'] == 0:
            line_count_label = f"There are {line_count['books']} book(s) in stock"
        elif line_count['books'] == 0:
            line_count_label = f"There are {line_count['office']} office item(s) and {line_count['school']} school item(s) in stock"
        elif line_count['office'] == 0:
            line_count_label = f"There are {line_count['books']} book(s) and {line_count['school']} school item(s) in stock"
        elif line_count['school'] == 0:
            line_count_label = f"There are {line_count['books']} book(s) and {line_count['office']} office item(s) in stock"
        else:
            line_count_label = f"There are {line_count['books']} book(s), {line_count['office']} office item(s), and {line_count['school']} school item(s) in stock"
        return line_count_label

    def check_stock_levels(self):
        low_stock_school_items = []
        low_stock_office_items = []

        # Check school items
        with open(STOCK_SCHOOL_PATH, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 9:
                    units = int(row[7]) if row[7].isdigit() else 0
                    boxes = int(row[8]) if row[8].isdigit() else 0
                    if boxes < 10 or units < 15:
                        low_stock_school_items.append((row[0], row[2], units, boxes))

        # Check office items
        with open(STOCK_OFFICE_PATH, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 9:
                    units = int(row[7]) if row[7].isdigit() else 0
                    boxes = int(row[8]) if row[8].isdigit() else 0
                    if boxes < 10 or units < 15:
                        low_stock_office_items.append((row[0], row[2], units, boxes))

        if low_stock_school_items or low_stock_office_items:
            self.display_low_stock_alert(low_stock_school_items, low_stock_office_items)

    def display_low_stock_alert(self, low_stock_school_items, low_stock_office_items):
        dialog = QDialog(self)
        dialog.setWindowTitle("Low Stock Alert")
        dialog.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout(dialog)

        lowstock_title_label = QLabel("Low Stock Alert")
        lowstock_title_font = QFont()
        lowstock_title_font.setPointSize(24)
        lowstock_title_font.setBold(True)
        lowstock_title_label.setFont(lowstock_title_font)
        lowstock_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(lowstock_title_label)

        alert_label = QLabel("The following items are low in stock:")
        alert_font = QFont()
        alert_font.setPointSize(14)
        alert_label.setFont(alert_font)
        alert_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(alert_label)

        # School items table
        school_table_label = QLabel("School Items")
        school_table_font = QFont()
        school_table_font.setPointSize(14)
        school_table_font.setBold(True)
        school_table_label.setFont(school_table_font)
        school_table_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(school_table_label)

        school_table = QTableWidget()
        school_table.setRowCount(len(low_stock_school_items))
        school_table.setColumnCount(4)
        school_table.setHorizontalHeaderLabels(["ID", "Item Name", "Units Quantity", "Boxes Quantity"])
        school_table.setEditTriggers(QTableWidget.NoEditTriggers)
        school_table.setSelectionMode(QTableWidget.SingleSelection)
        school_table.setSortingEnabled(True)
        school_table.setFocusPolicy(Qt.NoFocus)
        school_table.horizontalHeader().setStretchLastSection(True)
        school_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        school_table.verticalHeader().setVisible(False)

        for row_idx, item in enumerate(low_stock_school_items):
            school_table.setItem(row_idx, 0, QTableWidgetItem(item[0]))
            school_table.setItem(row_idx, 1, QTableWidgetItem(item[1]))
            school_table.setItem(row_idx, 2, QTableWidgetItem(str(item[2]) if item[2] < 15 else ""))
            school_table.setItem(row_idx, 3, QTableWidgetItem(str(item[3]) if item[3] < 10 else ""))

        for row in range(school_table.rowCount()):
            for column in range(school_table.columnCount()):
                item = school_table.item(row, column)
                if item:
                    item.setToolTip(item.text())

        school_table.cellEntered.connect(self.show_tooltip)

        school_scroll_area = QScrollArea()
        school_scroll_area.setWidgetResizable(True)
        school_scroll_area.setWidget(school_table)

        layout.addWidget(school_scroll_area)

        # Office items table
        office_table_label = QLabel("Office Items")
        office_table_font = QFont()
        office_table_font.setPointSize(14)
        office_table_font.setBold(True)
        office_table_label.setFont(office_table_font)
        office_table_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(office_table_label)

        office_table = QTableWidget()
        office_table.setRowCount(len(low_stock_office_items))
        office_table.setColumnCount(4)
        office_table.setHorizontalHeaderLabels(["ID", "Item Name", "Units Quantity", "Boxes Quantity"])
        office_table.setEditTriggers(QTableWidget.NoEditTriggers)
        office_table.setSelectionMode(QTableWidget.SingleSelection)
        office_table.setSortingEnabled(True)
        office_table.setFocusPolicy(Qt.NoFocus)
        office_table.horizontalHeader().setStretchLastSection(True)
        office_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        office_table.verticalHeader().setVisible(False)

        for row_idx, item in enumerate(low_stock_office_items):
            office_table.setItem(row_idx, 0, QTableWidgetItem(item[0]))
            office_table.setItem(row_idx, 1, QTableWidgetItem(item[1]))
            office_table.setItem(row_idx, 2, QTableWidgetItem(str(item[2]) if item[2] < 15 else ""))
            office_table.setItem(row_idx, 3, QTableWidgetItem(str(item[3]) if item[3] < 10 else ""))

        for row in range(office_table.rowCount()):
            for column in range(office_table.columnCount()):
                item = office_table.item(row, column)
                if item:
                    item.setToolTip(item.text())

        office_table.cellEntered.connect(self.show_tooltip)

        office_scroll_area = QScrollArea()
        office_scroll_area.setWidgetResizable(True)
        office_scroll_area.setWidget(office_table)

        layout.addWidget(office_scroll_area)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_tooltip(self, row, column):
        item = self.sender().item(row, column)
        if item:
            QToolTip.showText(QCursor.pos(), item.text())

def main():
    app = QApplication(sys.argv)
    if os.path.isfile(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
