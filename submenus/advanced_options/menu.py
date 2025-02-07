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
DATA_PATH = os.path.join(PROGRAM_PATH, 'data')
CATS_SCHOOL_PATH = os.path.join(DATA_PATH, 'cats_school.pystk')
CATS_OFFICE_PATH = os.path.join(DATA_PATH, 'cats_office.pystk')
BRANDS_SCHOOL_PATH = os.path.join(DATA_PATH, 'brands_school.pystk')
BRANDS_OFFICE_PATH = os.path.join(DATA_PATH, 'brands_office.pystk')
EDITORIALS_PATH = os.path.join(DATA_PATH, 'editorials.pystk')

MOTIVATIONAL_QUOTES = {
    1: "The only way to do great work is to love what you do. - Steve Jobs",
    2: "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    3: "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    4: "The best way to predict the future is to invent it. - Alan Kay",
    5: "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    6: "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    7: "It does not matter how slowly you go as long as you do not stop. - Confucius",
    8: "Everything you've ever wanted is on the other side of fear. - George Addair",
    9: "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    10: "The way to get started is to quit talking and begin doing. - Walt Disney",
    11: "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty. - Winston Churchill",
    12: "Don't let yesterday take up too much of today. - Will Rogers",
    13: "You learn more from failure than from success. Don't let it stop you. Failure builds character. - Unknown",
    14: "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
    15: "If you are working on something that you really care about, you don't have to be pushed. The vision pulls you. - Steve Jobs",
    16: "People who are crazy enough to think they can change the world, are the ones who do. - Rob Siltanen",
    17: "Failure will never overtake me if my determination to succeed is strong enough. - Og Mandino",
    18: "We may encounter many defeats but we must not be defeated. - Maya Angelou",
    19: "Knowing is not enough; we must apply. Wishing is not enough; we must do. - Johann Wolfgang Von Goethe",
    20: "Imagine your life is perfect in every respect; what would it look like? - Brian Tracy"
}

class AdvancedOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Options")
        self.setGeometry(100, 100, 860, 460)

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

        self.subtitle_label = QLabel("Be careful, these options are dangerous and you could delete something you don't want to.")
        self.subtitle_label_font = QFont()
        self.subtitle_label_font.setPointSize(16)
        self.subtitle_label.setFont(self.subtitle_label_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setToolTip("I'm being serious, don't mess with these options unless you know what you're doing.")
        self.layout.addWidget(self.subtitle_label)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.open_folder_button = QPushButton("Open Backups Folder")
        self.open_folder_button.setFont(self.font)
        self.open_folder_button.setFixedHeight(60)
        self.open_folder_button.setFixedWidth(self.title_label.sizeHint().width())
        self.open_folder_button.clicked.connect(self.open_saved_files_folder)
        self.open_folder_button.setToolTip("Open the folder where all your backups are stored.")
        self.button_layout.addWidget(self.open_folder_button)

        self.clear_unused_categories_button = QPushButton("Clear Unused Categories")
        self.clear_unused_categories_button.setFont(self.font)
        self.clear_unused_categories_button.setFixedHeight(60)
        self.clear_unused_categories_button.setFixedWidth(self.title_label.sizeHint().width())
        self.clear_unused_categories_button.clicked.connect(self.clear_unused_categories)
        self.clear_unused_categories_button.setToolTip("Clear all the categories that are not being used by any item.")
        self.button_layout.addWidget(self.clear_unused_categories_button)

        self.clear_unused_brands_button = QPushButton("Clear Unused Brands")
        self.clear_unused_brands_button.setFont(self.font)
        self.clear_unused_brands_button.setFixedHeight(60)
        self.clear_unused_brands_button.setFixedWidth(self.title_label.sizeHint().width())
        self.clear_unused_brands_button.clicked.connect(self.clear_unused_brands)
        self.clear_unused_brands_button.setToolTip("Clear all the brands that are not being used by any item.")
        self.button_layout.addWidget(self.clear_unused_brands_button)

        self.clear_unused_editorials_button = QPushButton("Clear Unused Editorials")
        self.clear_unused_editorials_button.setFont(self.font)
        self.clear_unused_editorials_button.setFixedHeight(60)
        self.clear_unused_editorials_button.setFixedWidth(self.title_label.sizeHint().width())
        self.clear_unused_editorials_button.clicked.connect(self.clear_unused_editorials)
        self.clear_unused_editorials_button.setToolTip("Clear all the editorials that are not being used by any item.")
        self.button_layout.addWidget(self.clear_unused_editorials_button)

        self.clear_data_button = QPushButton("Clear All App Data")
        self.clear_data_button.setFont(self.font)
        self.clear_data_button.setFixedHeight(60)
        self.clear_data_button.setFixedWidth(self.title_label.sizeHint().width())
        self.clear_data_button.clicked.connect(self.clear_all_app_data)
        self.clear_data_button.setToolTip("DANGEROUS!!! Clear all the backups, categories, brands and items in the stock.")
        self.button_layout.addWidget(self.clear_data_button)

        self.about_button = QPushButton("About This Program")
        self.about_button.setFont(self.font)
        self.about_button.setFixedHeight(60)
        self.about_button.setFixedWidth(self.title_label.sizeHint().width())
        self.about_button.clicked.connect(self.about_this_program)
        self.about_button.setToolTip("Info about this program.")
        self.button_layout.addWidget(self.about_button)

        self.layout.addLayout(self.button_layout)

    def open_saved_files_folder(self):
        if not os.path.exists(SAVES_PATH):
            os.makedirs(SAVES_PATH)
        os.startfile(SAVES_PATH) if sys.platform == "win32" else os.system(f'xdg-open "{SAVES_PATH}"')

    def clear_unused_categories(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "This will clear all the categories that are not being used by any item. Do you want to proceed?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                school_cleared = False
                office_cleared = False
                if os.path.isfile(CATS_SCHOOL_PATH):
                    os.remove(CATS_SCHOOL_PATH)
                    school_cleared = True
                if os.path.isfile(CATS_OFFICE_PATH):
                    os.remove(CATS_OFFICE_PATH)
                    office_cleared = True
                if school_cleared and not office_cleared:
                    QMessageBox.information(self, "Success", "Unused categories from school items have been deleted.")
                elif not school_cleared and office_cleared:
                    QMessageBox.information(self, "Success", "Unused categories from office items have been deleted.")
                elif school_cleared and office_cleared:
                    QMessageBox.information(self, "Success", "Unused categories from school and office items have been deleted.")
                else:
                    QMessageBox.information(self, "Info", "There are no categories to delete :)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete categories file: {e}")

    def clear_unused_brands(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "This will clear all the brands that are not being used by any item. Do you want to proceed?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                school_cleared = False
                office_cleared = False
                if os.path.isfile(BRANDS_SCHOOL_PATH):
                    os.remove(BRANDS_SCHOOL_PATH)
                    school_cleared = True
                if os.path.isfile(BRANDS_OFFICE_PATH):
                    os.remove(BRANDS_OFFICE_PATH)
                    office_cleared = True
                if school_cleared and not office_cleared:
                    QMessageBox.information(self, "Success", "Unused brands from school items have been deleted.")
                elif not school_cleared and office_cleared:
                    QMessageBox.information(self, "Success", "Unused brands from office items have been deleted.")
                elif school_cleared and office_cleared:
                    QMessageBox.information(self, "Success", "Unused brands from school and office items have been deleted.")
                else:
                    QMessageBox.information(self, "Info", "There are no brands to delete :)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete brands file: {e}")

    def clear_unused_editorials(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "This will clear all the editorials that are not being used by any item. Do you want to proceed?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if os.path.isfile(EDITORIALS_PATH):
                    os.remove(EDITORIALS_PATH)
                    QMessageBox.information(self, "Success", "Unused editorials have been deleted.")
                else:
                    QMessageBox.information(self, "Info", "There are no editorials to delete :)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete editorials file: {e}")

    def clear_all_app_data(self):
        reply = QMessageBox.question(self, 'Warning', 
                                     "This will erase all backups and items in the stock. This action CANNOT BE UNDONE. Do you want to proceed anyways?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            password, ok = QInputDialog.getText(self, 'Password Required', 'Enter password:', QLineEdit.Password)
            if ok:
                if password == "pystockingnuke":
                    shutil.rmtree(SAVES_PATH, ignore_errors=True)
                    shutil.rmtree(DATA_PATH, ignore_errors=True)
                    QMessageBox.information(self, "Success", "All app data has been cleared.")
                else:
                    QMessageBox.critical(self, "Error", "Wrong password")

    def about_this_program(self):
        quote = random.choice(list(MOTIVATIONAL_QUOTES.values()))
        about_text = (f"<b>PyStocking</b><br>"
                        f"Version: 1.0<br>"
                        f"Developer: Nico (<a href='https://github.com/ngdplnk'>@ngdplnk</a>)<br>"
                        f"© 2025 ngdplnk<br><br>"
                        f"Licensed under <a href='https://github.com/ngdplnk/PyStocking/blob/main/LICENSE'>Elastic License 2.0</a><br><br>"
                        f"\"{quote}\"")
        QMessageBox.information(self, "About This Program", about_text)

def open_advanced_options_menu(parent):
    dialog = AdvancedOptionsDialog(parent)
    dialog.exec_()
