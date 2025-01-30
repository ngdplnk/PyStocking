import os
import sys
import shutil
import random
from PyQt5.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')
SAVES_PATH = os.path.join(PROGRAM_PATH, 'saves')

MOTIVATIONAL_QUOTES = {
    1: "The only way to do great work is to love what you do. - Steve Jobs",
    2: "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    3: "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    4: "The best way to predict the future is to invent it. - Alan Kay",
    5: "Don't watch the clock; do what it does. Keep going. - Sam Levenson"
}

class AdvancedOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Options")
        self.setGeometry(100, 100, 700, 380)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.font = QFont()
        self.font.setPointSize(14)

        self.title_label = QLabel("Advanced Options")
        self.title_label_font = QFont()
        self.title_label_font.setPointSize(24)
        self.title_label_font.setBold(True)
        self.title_label.setFont(self.title_label_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Be careful, these options are dangerous and\nyou could delete something you don't want to.\nContinue at your own risk.")
        self.subtitle_label_font = QFont()
        self.subtitle_label_font.setPointSize(18)
        self.subtitle_label.setFont(self.subtitle_label_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.subtitle_label)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.open_folder_button = QPushButton("Open Saved Files Folder")
        self.open_folder_button.setFont(self.font)
        self.open_folder_button.setFixedHeight(60)
        self.open_folder_button.setFixedWidth(self.title_label.sizeHint().width())
        self.open_folder_button.clicked.connect(self.open_saved_files_folder)
        self.button_layout.addWidget(self.open_folder_button)

        self.clear_data_button = QPushButton("Clear All App Data")
        self.clear_data_button.setFont(self.font)
        self.clear_data_button.setFixedHeight(60)
        self.clear_data_button.setFixedWidth(self.title_label.sizeHint().width())
        self.clear_data_button.clicked.connect(self.clear_all_app_data)
        self.button_layout.addWidget(self.clear_data_button)

        self.about_button = QPushButton("About This Program")
        self.about_button.setFont(self.font)
        self.about_button.setFixedHeight(60)
        self.about_button.setFixedWidth(self.title_label.sizeHint().width())
        self.about_button.clicked.connect(self.about_this_program)
        self.button_layout.addWidget(self.about_button)

        self.layout.addLayout(self.button_layout)

    def open_saved_files_folder(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "It's not recommended to enter this folder unless you want to restore an old export you did in the past. "
                                     "DO NOT TOUCH latest_books.csv nor latest_office.csv. Do you want to proceed anyways?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if not os.path.exists(SAVES_PATH):
                os.makedirs(SAVES_PATH)
            os.startfile(SAVES_PATH) if sys.platform == "win32" else os.system(f'xdg-open "{SAVES_PATH}"')

    def clear_all_app_data(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "This will erase all backups and items in the stock. This action CANNOT BE UNDONE. Do you want to proceed anyways?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            password, ok = QInputDialog.getText(self, 'Password Required', 'Enter password:', QLineEdit.Password)
            if ok:
                if password == "pystockingnuke":
                    shutil.rmtree(SAVES_PATH, ignore_errors=True)
                    QMessageBox.information(self, "Success", "All app data has been cleared.")
                else:
                    QMessageBox.critical(self, "Error", "Wrong password")

    def about_this_program(self):
        quote = random.choice(list(MOTIVATIONAL_QUOTES.values()))
        about_text = (f"PyStocking\n"
                      f"Version: 1.0\n"
                      f"Developer: Your Name\n"
                      f"License: MIT\n"
                      f"© 2023 Your Company\n\n"
                      f"Motivational Quote: \"{quote}\"")
        QMessageBox.information(self, "About This Program", about_text)

def open_advanced_options_menu(parent):
    dialog = AdvancedOptionsDialog(parent)
    dialog.exec_()