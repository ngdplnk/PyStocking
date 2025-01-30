import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from submenus.add_items.menu import open_add_menu
from submenus.manage_items.menu import open_manage_menu

# Get PATHS
if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')
LATEST_BOOKS_PATH = os.path.join(SAVES_PATH, 'latest_books.csv')
LATEST_OFFICE_PATH = os.path.join(SAVES_PATH, 'latest_office.csv')

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowTitle("PyStocking - Main Menu")

        # Set window size
        self.setFixedSize(800, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title label
        title_label = QLabel("Main Menu")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Line count label
        line_count = self.get_line_count()
        line_count_label = QLabel(self.update_line_count(line_count))
        line_count_font = QFont()
        line_count_font.setPointSize(18)
        line_count_label.setFont(line_count_font)
        line_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(line_count_label)

        # Add items button
        add_button = QPushButton("Add Items")
        add_button.setFixedSize(200, 50)
        add_button.setStyleSheet("font-size: 16px;")
        add_button.setToolTip("Add new items to the stock")
        add_button.clicked.connect(lambda: (open_add_menu(self), line_count_label.setText(self.update_line_count(self.get_line_count()))))
        layout.addWidget(add_button)

        # Manage items button
        manage_button = QPushButton("Manage Items")
        manage_button.setFixedSize(200, 50)
        manage_button.setStyleSheet("font-size: 16px;")
        manage_button.setToolTip("Manage the stock")
        manage_button.clicked.connect(lambda: (open_manage_menu(self), line_count_label.setText(self.update_line_count(self.get_line_count()))))
        layout.addWidget(manage_button)

        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedSize(200, 50)
        exit_button.setStyleSheet("font-size: 16px;")
        exit_button.setToolTip("Exit the program")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        central_widget.setLayout(layout)

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
                line_count[0] = sum(1 for _ in file)
            with open(LATEST_OFFICE_PATH, 'r') as file:
                line_count[1] = sum(1 for _ in file)
            return line_count
        except Exception as e:
            return f"Error: {e}"

    def update_line_count(self, line_count):
        if line_count[0] == 0 and line_count[1] == 0:
            line_count_label = "No items in stock"
        elif line_count[0] == 0:
            line_count_label = f"There are {line_count[1]} office item(s) in stock"
        elif line_count[1] == 0:
            line_count_label = f"There are {line_count[0]} book(s) in stock"
        else:
            line_count_label = f"There are {line_count[0]} book(s) and {line_count[1]} office item(s) in stock"
        return line_count_label
    
def main():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()