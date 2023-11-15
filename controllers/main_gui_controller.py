from PySide6 import QtWidgets, QtCore, QtGui

class CustomListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, date, name, amount):
        super().__init__()
        self.date = date
        self.name = name
        self.amount = amount
class CustomItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if isinstance(index, CustomListWidgetItem):
            rect = option.rect
            rect.setWidth(400)  # Adjust the width as needed

            painter.setPen(QtGui.QPen(QtCore.Qt.white))
            painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
            painter.drawRect(rect)

            date_rect = rect.adjusted(5, 5, 0, 0)
            name_rect = rect.adjusted(110, 5, 0, 0)
            amount_rect = rect.adjusted(260, 5, 0, 0)

            painter.drawText(date_rect, index.date)
            painter.drawText(name_rect, index.name)
            painter.drawText(amount_rect, index.amount)
        else:
            super().paint(painter, option, index)

class MainGui(QtWidgets.QWidget):
    def __init__(self, screen_manager, sql_connector):
        super().__init__()
        self.screen_manager = screen_manager
        self.sql_connector = sql_connector
        self.expenses_by_month = {}  # Dictionary to store expenses by month
        self.current_month = None
        self.setup_ui()

    def setup_ui(self):
        self.resize(100, 700)
        self.setStyleSheet("background-color: grey;")
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Personal Expense Tracker")
        self.label1.setStyleSheet("background-color: black; color: white; font-size: 19pt; font-weight: bold;")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setGeometry(0,0,500,70)

        self.logoutButton = QtWidgets.QPushButton(self)
        self.logoutButton.setText("Log Out")
        self.logoutButton.setStyleSheet(
            "background-color: black; color: red; font-size: 13pt; font-family: Helvetica; border-radius: 10px;")
        self.logoutButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.logoutButton.setGeometry(20, 650, 460, 40)
        self.logoutButton.clicked.connect(self.logout)

        self.expenseSheetLabel = QtWidgets.QLabel(self)
        self.expenseSheetLabel.setText("Expense Chart")
        self.expenseSheetLabel.setStyleSheet("background-color: black; color: white; font-size: 22pt; font-weight: bold; font-family: Helvetica; border-radius: 10px;")
        self.expenseSheetLabel.setGeometry(50, 120, 400, 50)
        self.expenseSheetLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.date_label = QtWidgets.QLabel(self)
        self.date_label.setText("Date")
        self.date_label.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; font-size: 14pt; font-family: Helvetica;")
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setGeometry(5, 220, 150, 30)

        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setGeometry(10, 250, 150, 30)

        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setText("Name of Purchase")
        self.name_label.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; font-size: 14pt; font-family: Helvetica;")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setGeometry(180, 220, 150, 30)

        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name of Purchase")
        self.name_input.setAlignment(QtCore.Qt.AlignCenter)
        self.name_input.setGeometry(180, 250, 150, 30)

        self.amount_label = QtWidgets.QLabel(self)
        self.amount_label.setText("Amount")
        self.amount_label.setStyleSheet("background-color: lightgray; color: black; font-weight: bold; font-size: 14pt; font-family: Helvetica;")
        self.amount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_label.setGeometry(350, 220, 130, 30)

        self.amount_input = QtWidgets.QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter Amount")
        self.amount_input.setAlignment(QtCore.Qt.AlignCenter)
        self.amount_input.setGeometry(350, 250, 130, 30)
        self.amount_input.returnPressed.connect(self.add_expense)

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setText("Add Purchase")
        self.addButton.setStyleSheet("background-color: black; color: white; font-size: 14pt; font-weight: bold; border-radius: 10px;")
        self.addButton.setGeometry(180, 310, 150, 30)
        self.addButton.setCursor(QtGui.Qt.PointingHandCursor)
        self.addButton.clicked.connect(self.add_expense)

        self.expense_list = QtWidgets.QListWidget(self)
        self.expense_list.setGeometry(50, 370, 400, 250)
        self.expense_list.setStyleSheet("background-color: black; color: white; font-size: 12pt;")

        self.item_delegate = CustomItemDelegate()
        self.expense_list.setItemDelegate(self.item_delegate)

        # Style the input fields
        self.date_input.setStyleSheet("background-color: black; color: white; font-size: 12pt;")
        self.name_input.setStyleSheet("background-color: black; color: white; font-size: 10pt;")
        self.amount_input.setStyleSheet("background-color: black; color: white; font-size: 10pt;")

        self.load_saved_expenses()

    def load_saved_expenses(self):
        if self.current_month:
            saved_expenses = self.sql_connector.get_expenses_by_month(self.current_month)
            for expense in saved_expenses:
                date, name, amount = expense
                self.add_expense_to_list(date, name, amount)

    def add_expense(self):
        date = self.date_input.date().toString(QtCore.Qt.ISODate)
        name = self.name_input.text()
        amount = self.amount_input.text()

        if not date or not name or not amount:
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return

        if self.current_month not in self.expenses_by_month:
            self.expenses_by_month[self.current_month] = []

        expense_text = f"{date}{' ' * 35}{name}{' ' * 35}₹{amount}"
        self.expense_list.addItem(expense_text)

        self.expenses_by_month[self.current_month].append({
            "date": date,
            "name": name,
            "amount": amount
        })
        self.name_input.clear()
        self.amount_input.clear()

        self.sql_connector.insert_expense(self.current_month, date, name, amount)

    def update_expense_list(self):
        self.expense_list.clear()
        if self.current_month in self.expenses_by_month:
            expenses = self.expenses_by_month[self.current_month]
            for expense in expenses:
                item = QtWidgets.QListWidgetItem(f"{expense['date']} - {expense['name']} - ${expense['amount']}")
                self.expense_list.addItem(item)

    def logout(self):
        self.screen_manager.setCurrentWidget(self.screen_manager.login_screen)