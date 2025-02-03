import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from submenus.add_items.menu import open_add_menu
from submenus.manage_items.menu import open_manage_menu
from submenus.advanced_options.menu import open_advanced_options_menu

# Get PATHS
if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.pystk')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.pystk')
ICON_PATH = os.path.join(PROGRAM_PATH, 'launcher', 'icon.ico')

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window icon
        if os.path.isfile(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        # Window title
        self.setWindowTitle("PyStocking - Main Menu")

        # Set window size
        self.setGeometry(100, 100, 800, 450)

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
        add_button.clicked.connect(lambda: (open_add_menu(self), line_count_label.setText(self.update_line_count(self.get_line_count()))))
        manage_button.clicked.connect(lambda: (open_manage_menu(self), line_count_label.setText(self.update_line_count(self.get_line_count()))))
        advanced_options_button.clicked.connect(lambda: (open_advanced_options_menu(self), line_count_label.setText(self.update_line_count(self.get_line_count()))))
        exit_button.clicked.connect(self.close)

    def adjust_button_widths(self, reference_label, buttons):
        reference_width = reference_label.sizeHint().width()
        for button in buttons:
            button.setFixedWidth(reference_width)

    # Get line count - Create file
    def get_line_count(self):
        try:
            line_count = {
                'books': 0,
                'office': 0
            }
            # Ensure the directory exists
            os.makedirs(os.path.dirname(LATEST_BOOKS_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(LATEST_OFFICE_PATH), exist_ok=True)

            # Ensure the file exists
            if not os.path.isfile(LATEST_BOOKS_PATH):
                with open(LATEST_BOOKS_PATH, 'w') as file:
                    pass  # Create an empty file if it doesn't exist
            if not os.path.isfile(LATEST_OFFICE_PATH):
                with open(LATEST_OFFICE_PATH, 'w') as file:
                    pass  # Create an empty file if it doesn't exist

            with open(LATEST_BOOKS_PATH, 'r') as file:
                line_count['books'] = sum(1 for _ in file)
            with open(LATEST_OFFICE_PATH, 'r') as file:
                line_count['office'] = sum(1 for _ in file)
            return line_count
        except Exception as e:
            return f"Error: {e}"

    def update_line_count(self, line_count):
        if line_count['books'] == 0 and line_count['office'] == 0:
            line_count_label = "No items in stock"
        elif line_count['books'] == 0:
            line_count_label = f"There are {line_count['office']} office item(s) in stock"
        elif line_count['office'] == 0:
            line_count_label = f"There are {line_count['books']} book(s) in stock"
        else:
            line_count_label = f"There are {line_count['books']} book(s) and {line_count['office']} office item(s) in stock"
        return line_count_label
    
def main():
    app = QApplication(sys.argv)
    if os.path.isfile(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()