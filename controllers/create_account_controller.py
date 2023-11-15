from PySide6 import QtWidgets, QtCore, QtGui

class CreateAccountController(QtWidgets.QWidget):
    def __init__(self, screen_manager, sql_connector):
        super().__init__(screen_manager)
        self.screen_manager = screen_manager
        self.sql_connector = sql_connector
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Create Account Page")
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

        self.createAccountTitle = QtWidgets.QLabel(self)
        self.createAccountTitle.setText("Create Account")
        self.createAccountTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.createAccountTitle.setStyleSheet(
            "background-color: lightgray; color: black; font-size: 22pt; font-weight: bold; font-family: Futura;")
        self.createAccountTitle.setGeometry(150, 160, 200, 50)

        self.subloginTitle = QtWidgets.QLabel(self)
        self.subloginTitle.setText("Create an Account to get started")
        self.subloginTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.subloginTitle.setStyleSheet(
            "background-color: lightgray; color: black; font-size: 13pt; font-weight: bold; font-family: Futura;")
        self.subloginTitle.setGeometry(120, 200, 250, 30)

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

        # Submit button
        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setText("Submit")
        self.submitButton.setStyleSheet("background-color: #1a6cf0; color: white; border-radius: 10px")
        self.submitButton.setGeometry(290, 500, 120, 50)
        self.submitButton.clicked.connect(self.submitClicked)

        # Create account button
        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setText("Create Account")
        self.loginButton.setStyleSheet("background-color: lightgray; color: #1a6cf0; border-radius: 10px")
        self.loginButton.clicked.connect(self.loginToAccount)
        self.loginButton.setGeometry(100, 500, 120, 50)

    def loginToAccount(self):
        print("Login clicked.")
        self.screen_manager.setCurrentWidget(self.screen_manager.login_screen)

    def submitClicked(self):
        print("Submit clicked.")
        username = self.usernameBox.text()
        password = self.passwordBox.text()
        self.sql_connector.insert_user_credentials(username, password)
        self.sql_connector.disconnect()
        # Optionally, display a message to the user that the account has been created.
        QtWidgets.QMessageBox.information(self, "Account Created", "Your account has been created successfully.")
        self.screen_manager.setCurrentWidget(self.screen_manager.main_gui_screen)

    def blurPassword(self):
        if self.showPasswordButton.isChecked():
            self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
