import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic

USERNAME = "admin"
PASSWORD = "admin"
SOURCE_URL = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('window.ui', self)

        self.stackedwidget = self.findChild(QStackedWidget, "stackedWidget")
        self.button_login = self.findChild(QPushButton, "button_login")
        self.lineedit_password = self.findChild(QLineEdit, "lineedit_password")
        self.lineedit_username = self.findChild(QLineEdit, "lineedit_username")
        self.button_convert = self.findChild(QPushButton, "button_convert")
        self.button_logout = self.findChild(QPushButton, "button_logout")
        self.button_reset = self.findChild(QPushButton, "button_reset")
        self.combobox_from = self.findChild(QComboBox, "combobox_from")
        self.combobox_to = self.findChild(QComboBox, "combobox_to")
        self.label_from = self.findChild(QLabel, "label_from")
        self.label_status = self.findChild(QLabel, "label_status")
        self.label_to = self.findChild(QLabel, "label_to")
        self.lineedit_from = self.findChild(QLineEdit, "lineedit_from")
        self.lineedit_to = self.findChild(QLineEdit, "lineedit_to")
        self.error = QErrorMessage()
        self.currency_data = [
            {
                "code": "EUR",
                "quantity": 1,
                "rate": 2.9792,
                "name": "Euro",
            },
            {
                "code": "USD",
                "quantity": 1,
                "rate": 2.6956,
                "name": "US Dollar",
            }
        ]

        self.button_login.clicked.connect(self.on_button_login_clicked)
        self.lineedit_password.returnPressed.connect(self.on_button_login_clicked)
        self.lineedit_username.returnPressed.connect(self.on_button_login_clicked)
        self.button_logout.clicked.connect(self.on_button_logout_clicked)
        self.button_convert.clicked.connect(self.on_button_convert_clicked)
        self.button_reset.clicked.connect(self.on_button_reset_clicked)
        self.lineedit_from.returnPressed.connect(self.on_button_convert_clicked)
        self.combobox_from.currentTextChanged.connect(self.on_combobox_from_clicked)
        self.combobox_to.currentTextChanged.connect(self.on_combobox_to_clicked)

        self.show()

    def on_button_login_clicked(self):
        if self.lineedit_password.text() == PASSWORD and self.lineedit_username.text() == USERNAME:
            self.stackedwidget.setCurrentIndex(1)
            self.button_reset.click()
        else:
            self.lineedit_password.clear()
            self.lineedit_username.clear()
            self.error.showMessage("Username or password incorrect. Please try again.")

    def on_button_logout_clicked(self):
        self.stackedwidget.setCurrentIndex(0)
        self.lineedit_password.clear()
        self.lineedit_username.clear()

    def on_button_convert_clicked(self):
        try:
            from_currency = self.combobox_from.currentText()
            to_currency = self.combobox_to.currentText()
            number = float(self.lineedit_from.text())

            # convert to GEL
            if not from_currency == "GEL":
                for item in self.currency_data:
                    if item["code"] == from_currency:
                        number = number * (item["rate"] / item["quantity"])

            # convert from GEL
            if not to_currency == "GEL":
                for item in self.currency_data:
                    if item["code"] == to_currency:
                        number = number * (item["quantity"] / item["rate"])

            self.lineedit_to.setText(str(number))

            self.label_status.setText("Converted successfully")
        except Exception:
            self.label_status.setText("Something went wrong. Try again.")

    def on_button_reset_clicked(self):
        self.lineedit_from.setText("0")
        self.lineedit_to.setText("0")
        self.currency_info()

        currency_names = ["GEL"] + [item["code"] for item in self.currency_data]

        self.combobox_from.clear()
        self.combobox_from.addItems(currency_names)
        self.combobox_to.clear()
        self.combobox_to.addItems(currency_names)

    def on_combobox_from_clicked(self):
        if self.combobox_from.currentText() == "GEL":
            self.label_from.setText("GEL")
        else:
            for item in self.currency_data:
                if item["code"] == self.combobox_from.currentText():
                    self.label_from.setText(item["name"])
        self.button_convert.click()

    def on_combobox_to_clicked(self):
        if self.combobox_to.currentText() == "GEL":
            self.label_to.setText("GEL")
        else:
            for item in self.currency_data:
                if item["code"] == self.combobox_to.currentText():
                    self.label_to.setText(item["name"])
        self.button_convert.click()

    def currency_info(self):
        try:
            r = requests.get(SOURCE_URL)

            data = r.json()[0]
            data = data["currencies"]

            self.currency_data = data
            self.label_status.setText("Currencies updated successfully")
        except Exception:
            self.label_status.setText("Problem fetching currencies...")


app = QApplication(sys.argv)
window = MainWindow()

sys.exit(app.exec_())
