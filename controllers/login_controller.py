from PySide6 import QtWidgets, QtCore, QtGui

class LoginController(QtWidgets.QWidget):
    def __init__(self, screen_manager, sql_connector):
        super().__init__(screen_manager)
        self.screen_manager = screen_manager
        self.sql_connector = sql_connector
        self.setup_ui()
    def setup_ui(self):
        self.setWindowTitle("Login Page")
        self.setStyleSheet("background-color: white;")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.titleLabel = QtWidgets.QLabel(self)
        image = QtGui.QPixmap("72.png")
        self.titleLabel.setPixmap(image)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet(
            "background-color: white; font-size: 22pt; font-weight: bold; font-family: Helvetica; color: black; border-radius: 50px;")
        self.titleLabel.setGeometry(200, 60, 100, 100)

        self.loginTitle = QtWidgets.QLabel(self)
        self.loginTitle.setText("Login")
        self.loginTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.loginTitle.setStyleSheet(
            "background-color: lightgray; color: black; font-size: 22pt; font-weight: bold; font-family: Futura;")
        self.loginTitle.setGeometry(200, 160, 100, 50)

        self.subloginTitle = QtWidgets.QLabel(self)
        self.subloginTitle.setText("Login to your account")
        self.subloginTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.subloginTitle.setStyleSheet(
            "background-color: lightgray; color: black; font-size: 13pt; font-weight: bold; font-family: Futura;")
        self.subloginTitle.setGeometry(175, 200, 150, 30)

        self.usernameBox = QtWidgets.QLineEdit(self)
        self.usernameBox.setPlaceholderText("Enter Username")
        self.usernameBox.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameBox.setStyleSheet("color: black; background-color: white;")
        self.usernameBox.setGeometry(100, 270, 300, 50)

        self.passwordBox = QtWidgets.QLineEdit(self)
        self.passwordBox.setPlaceholderText("Enter Password")
        self.passwordBox.setStyleSheet("background-color: white; color: black;")
        self.passwordBox.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordBox.setGeometry(100, 340, 300, 50)

        # Show password button
        self.showPasswordButton = QtWidgets.QCheckBox(self)
        self.showPasswordButton.setText("Show Password")
        self.showPasswordButton.setStyleSheet("background-color: lightgray; color: black; font-size: 12pt;")
        self.showPasswordButton.clicked.connect(self.blurPassword)
        self.showPasswordButton.setGeometry(290, 400, 150, 30)

        # Show password button
        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setText("Login")
        self.submitButton.setStyleSheet("background-color: #1a6cf0; color: white; border-radius: 10px")
        self.submitButton.clicked.connect(self.submitClicked)
        self.submitButton.setGeometry(290, 500, 120, 50)

        # self.createAccountLabel = QtWidgets.QLabel(self)
        # self.createAccountLabel.setText("Don't have an account?")
        # self.createAccountLabel.setStyleSheet(
        #     "background-color: lightgray; color: black; font-size: 12pt; font-family: Apple Braille")
        # self.createAccountLabel.move(50, 570)

        # Create account button
        self.createAccountButton = QtWidgets.QPushButton(self)
        self.createAccountButton.setText("Create Account")
        self.createAccountButton.setStyleSheet("background-color: lightgray; color: #1a6cf0; border-radius: 10px")
        self.createAccountButton.clicked.connect(self.createAccount)
        self.createAccountButton.setGeometry(100, 500, 120, 50)

        self.usernameBox.clearFocus()
        self.passwordBox.clearFocus()

        # Connect signals to focus in and focus out events for the input fields
        self.usernameBox.installEventFilter(self)
        self.passwordBox.installEventFilter(self)

    def eventFilter(self, source, event):
        if (source == self.usernameBox or source == self.passwordBox) and event.type() == QtCore.QEvent.FocusIn:
            source.clear()
        if (source == self.usernameBox or source == self.passwordBox) and event.type() == QtCore.QEvent.FocusOut:
            if not source.text():
                source.setPlaceholderText("Enter Username" if source == self.usernameBox else "Enter Password")
        return super().eventFilter(source, event)

    def createAccount(self):
        print("Create account clicked.")
        self.screen_manager.setCurrentWidget(self.screen_manager.create_account_screen)

    def main_gui(self):
        self.screen_manager.setCurrentWidget(self.screen_manager.main_gui_screen)

    def submitClicked(self):
        print("Login clicked.")

        username = self.usernameBox.text()
        password = self.passwordBox.text()
        try:
            if self.check_user_credentials(username, password):
                print("username and password inserted successfully.")
                QtWidgets.QMessageBox.information(self, "Success!", "Logged in successfully.")
                self.main_gui()
            else:
                QtWidgets.QMessageBox.critical(self, "Error!", "Invalid username or password.")
        except Exception as e:
            print(f"Error inserting credentials {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Error!", "An error has occurred")

    def check_user_credentials(self, username, password):
        cursor = self.sql_connector.connection.cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def blurPassword(self):
        if self.showPasswordButton.isChecked():
            self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
