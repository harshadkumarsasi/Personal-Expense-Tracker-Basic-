import sys
from PySide6 import QtWidgets, QtCore, QtGui
import sqlite3
from database.sql_connector import SqlConnection
from controllers.login_controller import LoginController
from controllers.create_account_controller import CreateAccountController
from controllers.main_gui_controller import MainGui

class ScreenManager(QtWidgets.QStackedWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setStyleSheet("background-color: lightgray;")
        self.db_connection = db_connection

        self.login_screen = LoginController(self, db_connection)
        self.create_account_screen = CreateAccountController(self, db_connection)
        self.main_gui_screen = MainGui(self, db_connection)

        self.addWidget(self.login_screen)
        self.addWidget(self.create_account_screen)
        self.addWidget(self.main_gui_screen)

        self.setCurrentWidget(self.login_screen)

        self.main_gui_screen.load_saved_expenses()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    db_connection = SqlConnection("expenseTracker.db")
    app_icon = QtGui.QIcon("expenseTrackerIcon.png")
    app.setWindowIcon(app_icon)
    window = ScreenManager(db_connection)
    window.resize(500, 700)
    window.show()
    sys.exit(app.exec_())
