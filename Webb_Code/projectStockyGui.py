import sys
import random
import mariadb
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtGui import QPixmap
from createDiagrams import createDiagramsFunc
import hashlib

# Connector to the stock data base REMINDER USING MARIADB.
try:
    conn = mariadb.connect(
        user="illusion173",
        password="P@K3M0n123",
        host="localhost",
        port=3306,
        database="stockDataBase",
        autocommit=True
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB server: {e}")
    sys.exit(1)

# Get the Cursor
cursor = conn.cursor()
# Some global variables I need for spacing issues.
iconLimit = 0
X_LOCATION = 175
Y_LOCATION = 150

# Lists I need for again, spacing issues and keeping count of what needs to be created.
nameList = []
buttonList = []
user = ""
# So for some reason MariaDB is not committing when I use LOAD DATA.
# So I am doing it here.
sqlstockDataQuery = """LOAD DATA LOCAL INFILE '/home/illusion/Desktop/CS317_Project/webbCode/stockData.csv' INTO TABLE stockDataBase.stockData FIELDS TERMINATED by ',' LINES TERMINATED by '\n'IGNORE 1 LINES (stockDate, stockTicker, stockName, RSI, MACD, stochasticOperator, Volume, Price, PriceChange)"""
# sqlstockDataQueryCHECK = """SELECT * FROM stockData"""

cursor.execute(sqlstockDataQuery, ())

# Debugging - DO NOT TOUCH
# cursor.execute(sqlstockDataQueryCHECK, ())
# account = cursor.fetchone()
# print(account)


class signUpPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Project Stocky - Sign Up')
        self.resize(480, 100)
        pageLayout = QGridLayout()
        # First Name Box
        firstName = QLabel('<font size="4"> First Name </font>')
        self.placeHolderfirstName = QLineEdit()
        self.placeHolderfirstName.setPlaceholderText('Enter First Name')
        pageLayout.addWidget(firstName, 0, 0)
        pageLayout.addWidget(self.placeHolderfirstName, 0, 1)

        # Last Name Box
        lastName = QLabel('<font size="4"> Last Name </font>')
        self.placeHolderlastName = QLineEdit()
        self.placeHolderlastName.setPlaceholderText('Enter Last Name')
        pageLayout.addWidget(lastName, 1, 0)
        pageLayout.addWidget(self.placeHolderlastName, 1, 1)

        # Email Address Box
        emailAddress = QLabel('<font size="4"> Email Address </font>')
        self.placeHolderemailAddress = QLineEdit()
        self.placeHolderemailAddress.setPlaceholderText('Enter Email Address')
        pageLayout.addWidget(emailAddress, 2, 0)
        pageLayout.addWidget(self.placeHolderemailAddress, 2, 1)

        # Password Box
        phoneNumber = QLabel('<font size="4"> Phone Number </font>')
        self.placeHolderphoneNumber = QLineEdit()
        self.placeHolderphoneNumber.setPlaceholderText('Enter Phone Number')
        pageLayout.addWidget(phoneNumber, 3, 0)
        pageLayout.addWidget(self.placeHolderphoneNumber, 3, 1)

        # Username Box
        userName = QLabel('<font size="4"> New Username </font>')
        self.placeHolderUsername = QLineEdit()
        self.placeHolderUsername.setPlaceholderText('Enter Username')
        pageLayout.addWidget(userName, 4, 0)
        pageLayout.addWidget(self.placeHolderUsername, 4, 1)

        # Password Box
        password = QLabel('<font size="4"> New Password </font>')
        self.placeHolderPassword = QLineEdit()
        self.placeHolderPassword.setPlaceholderText('Enter password')
        self.placeHolderPassword.setEchoMode(QLineEdit.EchoMode.Password)
        pageLayout.addWidget(password, 5, 0)
        pageLayout.addWidget(self.placeHolderPassword, 5, 1)

        # Show Password Button
        self.showBox = QPushButton('Show', self)
        self.showBox.clicked.connect(self.showPass)
        pageLayout.addWidget(self.showBox, 5, 3, 1, 2)
        pageLayout.setRowMinimumHeight(2, 75)

        # Login Button
        self.button_SignUp = QPushButton('Confirm Sign Up', self)
        self.button_SignUp.clicked.connect(self.signUp)
        pageLayout.addWidget(self.button_SignUp, 2, 3, 1, 2)
        pageLayout.setRowMinimumHeight(2, 75)

        self.setLayout(pageLayout)

    # Show Password Function
    def showPass(self):
        # print("Password has been shown")
        self.placeHolderPassword.setEchoMode(QLineEdit.EchoMode.Normal)

    def doesUserExist(self, username):
        # print("Checking if user exists...")
        # Actual Login Query to avoid SQL injections
        sqlLoginQuery = """SELECT * FROM LoginTable WHERE LoginUsername = %s"""

        cursor.execute(sqlLoginQuery, (username, ))

        account = cursor.fetchone()

        if(account):
            return True
        else:
            return False

    def signUp(self):
        if(self.doesUserExist(self.placeHolderUsername.text())):
            self.errormsg = QMessageBox()
            self.errormsg.setIcon(QMessageBox.Critical)
            self.errormsg.setText(
                "Username Already Exists!")
            self.errormsg.exec_()
            return
        else:
            # print("Attempting to Sign up!")
            sqlSignUpQueryLoginTable = """INSERT INTO LoginTable VALUES(%s, %s, %d)"""
            sqlSignUpQueryuserTable = """INSERT INTO userTable VALUES(%s, %s, %s, %s, %d)"""
            # Grabbing user Inputted data
            usernameInput = self.placeHolderUsername.text()

            passwordInput = hashlib.sha512(str.encode(
                self.placeHolderPassword.text())).hexdigest()
            print(passwordInput)
            firstname = self.placeHolderfirstName.text()

            lastname = self.placeHolderlastName.text()

            emailAddress = self.placeHolderemailAddress.text()

            phoneNumber = self.placeHolderphoneNumber.text()

            # Create USERID
            userID = random.randint(1, 9999)
            # we need to update both tables
            cursor.execute(sqlSignUpQueryLoginTable,
                           (usernameInput, passwordInput, userID,))

            cursor.execute(sqlSignUpQueryuserTable, (phoneNumber,
                                                     emailAddress, firstname, lastname, userID,))

            sqlSignUpCheckQuery = """SELECT * FROM LoginTable WHERE userID = %s"""

            cursor.execute(sqlSignUpCheckQuery, (userID,))

            account = cursor.fetchone()
            # If account exists
            if account:
                successmsg = QMessageBox()
                successmsg.setWindowTitle("Success - Sign Up")
                successmsg.setText("Sucess in Signing up")
                x = successmsg.exec_()
                # print("Success in signing up!")
            else:
                # If account for any reason cant sign up.
                failuremsg = QMessageBox()
                failuremsg.setIcon(QMessageBox.Critical)
                failuremsg.setWindowTitle("Failure - Sign Up")
                failuremsg.setText("Failure in Signing up - Retry")
                y = failuremsg.exec_()

# Base class for importing a dashboard into Project Stocky.
# Essentially queries and asks the database for all elements of the stockDashboard Table and returns the list and pyqt5 puts it in a viewable table.
# From here the user MUST enter a Name for Project Stocky to continue to function.


class importDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Import Dashboard")
        self.setGeometry(0, 0, 700, 700)
        pageLayout = QGridLayout()
        self.myTableWidget = QTableWidget()
        dashboardNameLabel = QLabel(
            '<font size="3">Enter a Configuration Name </font>')
        self.dashboardName = QLineEdit()
        self.dashboardName.setPlaceholderText('Dashboard Name')
        pageLayout.addWidget(dashboardNameLabel, 0, 0)
        pageLayout.addWidget(self.dashboardName, 0, 1)

        self.submitName = QPushButton("Submit Name", self)
        self.submitName.clicked.connect(self.submitNameFunction)
        pageLayout.addWidget(self.submitName, 0, 2)

        sqlImportDashboard = """Select * FROM StockDashboard"""

        cursor.execute(sqlImportDashboard)

        dashboardData = cursor.fetchall()
        # print(type(dashboardData))
        # print(dashboardData)
        self.myTableWidget.setColumnCount(3)
        y = len(dashboardData)

        self.myTableWidget.setRowCount(y)
        self.myTableWidget.setHorizontalHeaderLabels(
            ['Dashboard Name', 'Stock Ticker', 'ID'])
        self.myTableWidget.horizontalHeader().setDefaultSectionSize(125)

        for x in range(len(dashboardData)):
            self.myTableWidget.setItem(
                x, 0, QTableWidgetItem(dashboardData[x][0]))
            self.myTableWidget.setItem(
                x, 1, QTableWidgetItem(dashboardData[x][1]))
            self.myTableWidget.setItem(
                x, 2, QTableWidgetItem(str(dashboardData[x][2])))

        pageLayout.addWidget(self.myTableWidget, 1, 1)
        self.setLayout(pageLayout)

    def convertTuple(self, tup):
        # initialize an empty string
        str = ''
        for item in tup:
            str = str + item
        return str

    def submitNameFunction(self):
        submittedText = self.dashboardName.text()

        sqlImportDashboard = """SELECT DashboardItemTicker FROM StockDashboard WHERE DashboardName = %s"""

        cursor.execute(sqlImportDashboard, (submittedText, ))

        account = cursor.fetchall()
        nameList.clear()
        nameList.append(account)
        for x in range(len(nameList[0])):
            self.newWidget = StockButton(self.convertTuple(nameList[0][x]))
            buttonList.append(self.newWidget)

        self.newDashboard = dashboard()
        self.newDashboard.show()
        self.close()

# Base class for Saving a dashboard into Project Stocky.
# Asks the user for a name to save the dashboard
# Additionally asks the user for six stock tickers to save to that dashboard configuration.
# From here the user can load another dashboard configuration.


class saveDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Dashboard")
        self.setGeometry(0, 0, 500, 500)
        pageLayout = QGridLayout()

        dashboardNameLabel = QLabel(
            '<font size="3"> Dashboard Configuration Name </font>')
        self.dashboardName = QLineEdit()
        self.dashboardName.setPlaceholderText('Dashboard Name')
        pageLayout.addWidget(dashboardNameLabel, 0, 0)
        pageLayout.addWidget(self.dashboardName, 0, 1)

        stockTickerTitle = QLabel('<font size="3">Stock Tickers Max 6 </font>')
        self.stockTickerone = QLineEdit()
        self.stockTickerone.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(stockTickerTitle, 1, 0)
        pageLayout.addWidget(self.stockTickerone, 1, 1)

        self.stockTickertwo = QLineEdit()
        self.stockTickertwo.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(self.stockTickertwo, 2, 1)

        self.stockTickerthree = QLineEdit()
        self.stockTickerthree.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(self.stockTickerthree, 3, 1)

        self.stockTickerfour = QLineEdit()
        self.stockTickerfour.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(self.stockTickerfour, 4, 1)

        self.stockTickerfive = QLineEdit()
        self.stockTickerfive.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(self.stockTickerfive, 5, 1)

        self.stockTickerSix = QLineEdit()
        self.stockTickerSix.setPlaceholderText('Stock Ticker')
        pageLayout.addWidget(self.stockTickerSix, 6, 1)

        self.button_SignUp = QPushButton('Save Configuration', self)
        self.button_SignUp.clicked.connect(self.savingDashboard)
        pageLayout.addWidget(self.button_SignUp, 7, 1)
        pageLayout.setRowMinimumHeight(2, 75)

        self.setLayout(pageLayout)

    def savingDashboard(self):
        # print("SAVING!")
        sqlSaveDashboardQuery = """INSERT INTO StockDashboard VALUES(%s, %s, %d)"""

        # Grabbing data
        dashboardName = self.dashboardName.text()
        dashboardID = random.randint(1, 9999)
        # Really janky way to save the names, but it works, since they are all Qline Edits this is the most efficient way
        stockTickerone = self.stockTickerone.text()
        stockTickertwo = self.stockTickertwo.text()
        stockTickerthree = self.stockTickerthree.text()
        stockTickerfour = self.stockTickerfour.text()
        stockTickerfive = self.stockTickerfive.text()
        stockTickersix = self.stockTickerSix.text()

        nameList.clear()
        # Creation of List
        if stockTickerone != "":
            nameList.append(stockTickerone)
        if stockTickertwo != "":
            nameList.append(stockTickertwo)
        if stockTickerthree != "":
            nameList.append(stockTickerthree)
        if stockTickerfour != "":
            nameList.append(stockTickerfour)
        if stockTickerfive != "":
            nameList.append(stockTickerfive)
        if stockTickersix != "":
            nameList.append(stockTickersix)
        x = 0
        if dashboardName == "":
            failuremsg = QMessageBox()
            failuremsg.setIcon(QMessageBox.Critical)
            failuremsg.setWindowTitle("Failure")
            failuremsg.setText(
                "Failure in Saving - Dashboard Name cannot be empty.")
            y = failuremsg.exec_()
            return

        for x in range(len(nameList)):
            cursor.execute(sqlSaveDashboardQuery,
                           (dashboardName, nameList[x], dashboardID))

        successmsg = QMessageBox()
        successmsg.setWindowTitle("Success - Saving")
        successmsg.setText("Sucess in Saving stock tickers.")
        x = successmsg.exec_()

# This is the stockpage class, used for the presentation of a tile.
# This class will handle the creation of the diagrams that are created by creatediagrams.py
# With a query based on the user's input to the tile in the dashboard class, the user will be able to see the data the program pulls from the database.


class stockPage(QWidget):
    def __init__(self, userInput):
        super().__init__()

        self.setWindowTitle('Project Stocky - Data - ' + userInput)
        self.setGeometry(0, 0, 1200, 900)
        createDiagramsFunc(userInput)
        pageLayout = QGridLayout()
        self.VerticalBoxLayoutStock = QVBoxLayout()

        # print("Latest data Tuple")
        sqlBullishorBearishSetterQuery = """SELECT stockDate, RSI, MACD, stochasticOperator FROM stockData WHERE stockTicker = %s ORDER by stockDate DESC LIMIT 1"""

        cursor.execute(sqlBullishorBearishSetterQuery, (userInput, ))

        account = cursor.fetchone()

        # print("Date")
        # print(type(account[0]))
        self.date = str(account[0])
        # print("RSI")
        # print(account[1])
        self.RSI = account[1]
        # print("MACD")
        # print(account[2])
        self.MACD = account[2]
        # print("stochasticOperator")
        # print(account[3])
        self.stochasticOperator = account[3]

        self.Title = QLabel(self)
        self.Title.setText(
            "Stock Data for: {}\nLatest Record Date: {}".format(userInput, self.date))
        self.Title.setStyleSheet(
            "font: bold;color: #0BD964;font-size:20px;text-align: center;")

        self.RSILabeL = QLabel(self)
        self.RSILabeL.setText("RSI: {}".format(self.RSI))
        self.RSILabeL.setStyleSheet(
            "font: bold;color: #0BD964;font-size:20px;text-align: center;")

        self.MACDLabel = QLabel(self)
        self.MACDLabel.setText("MACD:  {}".format(self.MACD))
        self.MACDLabel.setStyleSheet(
            "font: bold;color: #0BD964;font-size:20px;text-align: center;")

        self.stochasticOperatorLabel = QLabel(self)
        self.stochasticOperatorLabel.setText(
            "Stochastic Operator: {}\n\n".format(self.stochasticOperator))
        self.stochasticOperatorLabel.setStyleSheet(
            "font: bold;color: #0BD964;font-size:20px;text-align: center;")

        self.VerticalBoxLayoutStock.addWidget(self.Title)
        self.VerticalBoxLayoutStock.addWidget(self.RSILabeL)
        self.VerticalBoxLayoutStock.addWidget(self.MACDLabel)
        self.VerticalBoxLayoutStock.addWidget(self.stochasticOperatorLabel)

        pageLayout.addLayout(self.VerticalBoxLayoutStock, 1, 1)

        self.labelbar = QLabel(self)
        self.pixmap = QPixmap('stockImageDataFor{}.png'.format(userInput))
        self.labelbar.setPixmap(self.pixmap)
        pageLayout.addWidget(self.labelbar, 2, 1)
        sqlBullishorBearishSetterQuery = """SELECT stockDate, RSI, MACD, stochasticOperator, Volume, Price, PriceChange FROM stockData WHERE stockTicker = %s"""

        cursor.execute(sqlBullishorBearishSetterQuery, (userInput, ))

        stockData = cursor.fetchall()
        print(stockData)
        # Creation of Table
        self.stockDataTable = QTableWidget()

        self.stockDataTable.setColumnCount(7)
        rowLength = len(stockData)

        self.stockDataTable.setRowCount(rowLength)
        self.stockDataTable.setHorizontalHeaderLabels(
            ['Date', 'RSI', 'MACD', 'Stochastic Operator', 'Volume', 'Closing Price', 'Price Change'])
        self.stockDataTable.horizontalHeader().setDefaultSectionSize(130)
        # Really gross way to organize this table, but it works.
        for x in range(len(stockData)):
            self.stockDataTable.setItem(
                x, 0, QTableWidgetItem(str(stockData[x][0])))
            self.stockDataTable.setItem(
                x, 1, QTableWidgetItem(str(stockData[x][1])))
            self.stockDataTable.setItem(
                x, 2, QTableWidgetItem(str(stockData[x][2])))
            self.stockDataTable.setItem(
                x, 3, QTableWidgetItem(str((stockData[x][3]))))
            self.stockDataTable.setItem(
                x, 4, QTableWidgetItem(str(stockData[x][4])))
            self.stockDataTable.setItem(
                x, 5, QTableWidgetItem(str(stockData[x][5])))
            self.stockDataTable.setItem(
                x, 6, QTableWidgetItem(str(stockData[x][6])))

        pageLayout.addWidget(self.stockDataTable, 3, 1)
        self.setLayout(pageLayout)

# This is the base stockbutton class, used for transition between stockPage and the dashboard.
# When a user enters a ticker, this handles all looks for the button too.
# This additionally checks the status of the stock, if the stock is bullish or bearish, this automatically queries back to the database to save it.


class StockButton(QWidget):
    def __init__(self, userInput):
        super().__init__()

        self.greenFlag = True

        self.stockTickerPresent = userInput

        sqlBullishorBearishSetterQuery = """SELECT stockName FROM stockData WHERE stockTicker = %s ORDER by stockDate DESC LIMIT 1"""

        cursor.execute(sqlBullishorBearishSetterQuery,
                       (self.stockTickerPresent, ))

        account = cursor.fetchone()

        self.BullishOrBearishString = self.BullishOrBearishMATH(
            self.stockTickerPresent)
        # setting layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.iconbutton = QPushButton(account[0] + "\n" +
                                      self.stockTickerPresent + "\n" + self.BullishOrBearishString, self)
        if(self.greenFlag):
            self.iconbutton.setStyleSheet(
                "border-style: solid; border-color: #000000; border-width: 3px; color: #00CC0E;border-color: black;")
        else:
            self.iconbutton.setStyleSheet(
                "border-style: solid; border-color: #000000; border-width: 3px; color: #FA1F0C;border-color: black;")

        self.iconbutton.clicked.connect(self.presentStockPage)
        # creating a delete button
        self.deleteButton = QPushButton("X", self)
        # setting radius and border
        self.deleteButton.setStyleSheet(
            "border-radius : 19; border : 2px solid black")
        self.iconbutton.setGeometry(0, 0, 200, 200)
        self.deleteButton.setGeometry(150, 0, 50, 50)
        self.deleteButton.clicked.connect(self.deleteself)
        global iconLimit
        iconLimit = iconLimit + 1

    # classic getter
    def getname(self):
        return self.stockTickerPresent

    # Delete Button Functionality
    def deleteself(self):
        global iconLimit
        iconLimit = iconLimit - 1
        self.hide()

    def presentStockPage(self):
        self.newStockPage = stockPage(self.stockTickerPresent)
        self.newStockPage.show()

        print("Going Stock Page!")

    def BullishOrBearishMATH(self, stockTicker):
        self.counter = 0

        # First we have to retrieve data from the database

        # print("Latest data Tuple")
        sqlBullishorBearishSetterQuery = """SELECT stockDate, RSI, MACD, stochasticOperator FROM stockData WHERE stockTicker = %s ORDER by stockDate DESC LIMIT 1"""

        cursor.execute(sqlBullishorBearishSetterQuery, (stockTicker, ))

        account = cursor.fetchone()

        # print("Date")
        # print(type(account[0]))
        self.date = account[0]
        # print("RSI")
        # print(account[1])
        self.RSI = account[1]
        # print("MACD")
        # print(account[2])
        self.MACD = account[2]
        # print("stochasticOperator")
        # print(account[3])
        self.stochasticOperator = account[3]

       # print("Doing math for setter...")
        if(self.RSI > 70):
            # Overbought so Bullish
            self.counter = self.counter + 1
        elif self.RSI < 30:
            self.counter = self.counter - 1

        if(self.MACD > 0):
            self.counter = self.counter + 1
        elif(self.counter < 0):
            self.counter = self.counter - 1

        if(self.stochasticOperator > 80):
            self.counter = self.counter + 1
        elif(self.counter < 20):
            self.counter = self.counter - 1

        sqlBullishorBearishSetterQuery = """INSERT INTO StockPreview VALUES (%s, %s)"""
        sqlCheck = """SELECT * FROM StockPreview WHERE stockTicker = %s"""

        cursor.execute(sqlCheck, (stockTicker, ))
        account = cursor.fetchone()

        match self.counter:
            case 0:
                return("Neutral")
            case 1:
                if(account):
                    return("Slightly Bullish")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, True))
                    return("Slightly Bullish")

            case 2:
                if(account):
                    return("Bullish")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, True))
                    return("Bullish")

            case 3:
                if(account):
                    return("Bullish+")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, True))
                    return("Bullish+")

            case -1:
                self.greenFlag = False

                if(account):
                    return("Slightly Bearish")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, False))
                    return("Slightly Bearish")
            case -2:
                self.greenFlag = False
                if(account):
                    return("Bearish")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, False))
                    return("Bearish")
            case -3:
                self.greenFlag = False
                if(account):
                    return("Bearish-")
                else:
                    cursor.execute(sqlBullishorBearishSetterQuery,
                                   (stockTicker, False))
                    return("Bearish-")

    def BullishOrBearishGetter(self):
        return self.BullishOrBearishString

# The beginning of it all, the login System class.
# The user will have to first sign up, but the login system has an inherent encryption sha512 to ensure the user's password is secret and correct.
# The class has inherent error handling too.


class LoginSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Stocky - Login')
        self.resize(480, 100)
        pageLayout = QGridLayout()
        sqlstockDataQuery = """LOAD DATA LOCAL INFILE '/home/illusion/Desktop/CS317_Project/webbCode/stockData.csv' INTO TABLE stockDataBase.stockData FIELDS TERMINATED by ',' LINES TERMINATED by '\n'IGNORE 1 LINES (stockDate, stockTicker, stockName, RSI, MACD, stochasticOperator, Volume, Price, PriceChange)"""

        cursor.execute(sqlstockDataQuery, ())

        # Username Box
        userName = QLabel('<font size="4"> Username </font>')
        self.placeHolderUsername = QLineEdit()
        self.placeHolderUsername.setPlaceholderText('Enter Username')
        pageLayout.addWidget(userName, 0, 0)
        pageLayout.addWidget(self.placeHolderUsername, 0, 1)

        # Password Box
        password = QLabel('<font size="4"> Password </font>')
        self.placeHolderPassword = QLineEdit()
        self.placeHolderPassword.setPlaceholderText('Enter password')
        self.placeHolderPassword.setEchoMode(QLineEdit.EchoMode.Password)
        pageLayout.addWidget(password, 1, 0)
        pageLayout.addWidget(self.placeHolderPassword, 1, 1)

        # Show Password Button
        self.showBox = QPushButton('Show', self)
        self.showBox.clicked.connect(self.showPass)
        pageLayout.addWidget(self.showBox, 1, 3, 1, 2)
        pageLayout.setRowMinimumHeight(2, 75)

        # Login Button
        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.login)
        pageLayout.addWidget(self.button_login, 4, 0, 1, 5)
        pageLayout.setRowMinimumHeight(2, 75)

        # sign up button
        self.button_signup = QPushButton('New Account - Sign Up', self)
        pageLayout.addWidget(self.button_signup, 5, 0, 1, 5)
        pageLayout.setRowMinimumHeight(2, 75)
        # Create Page
        self.signUpPage = signUpPage()
        # on Click show page
        self.button_signup.clicked.connect(self.signUpPage.show)
        self.setLayout(pageLayout)

    # Show Password Function
    def showPass(self):
        # print("Password has been shown")
        self.placeHolderPassword.setEchoMode(QLineEdit.EchoMode.Normal)

    def login(self):
        # print("Attempting to Login...")
        global user
        # Actual Login Query to avoid SQL injections
        sqlLoginQuery = """SELECT * FROM LoginTable WHERE LoginUsername = %s AND LoginPassword = %s"""

        # Grabbing data
        usernameInput = self.placeHolderUsername.text()
        passwordInput = hashlib.sha512(str.encode(
            self.placeHolderPassword.text())).hexdigest()

        cursor.execute(sqlLoginQuery, (usernameInput, passwordInput, ))

        account = cursor.fetchone()
        print(account)
        if account:
            successmsg = QMessageBox()
            successmsg.setWindowTitle("Success - Login In")
            successmsg.setText("Welcome")
            x = successmsg.exec_()
            self.newDashboard = dashboard()
            self.newDashboard.show()
            self.close()
        else:
            failuremsg = QMessageBox()
            failuremsg.setIcon(QMessageBox.Critical)
            failuremsg.setWindowTitle("Failure - Login In")
            failuremsg.setText(
                "Failure in Logging In\nUsername/Password Incorrect")
            y = failuremsg.exec_()

# This shows all the data that is saved by Project Stocky when the user signs up.
# Additionally, the user can change their phone number and email for contact information purposes.


class aboutUserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)
        self.setWindowTitle("About User")

        sqlLoginQuery = """SELECT phoneNumber, EmailAddress, FirstName, LastName, USERID FROM userTable NATURAL JOIN LoginTable WHERE LoginUsername = %s"""

        cursor.execute(sqlLoginQuery, (user, ))

        account = cursor.fetchone()

        pageLayout = QGridLayout()

        self.setWindowTitle('Project Stocky - User Info')
        firstName = QLabel(
            '<font size="4"> First Name: {} </font>'.format(account[2]))

        pageLayout.addWidget(firstName, 0, 0)

        # Last Name Box
        lastName = QLabel(
            '<font size="4"> Last Name: {} </font>'.format(account[3]))
        pageLayout.addWidget(lastName, 1, 0)

        # Email Address Box
        emailAddress = QLabel(
            '<font size="4"> Email Address: {}</font>'.format(account[1]))
        pageLayout.addWidget(emailAddress, 2, 0)

        # Password Box
        phoneNumber = QLabel(
            '<font size="4"> Phone Number: {} </font>'.format(account[0]))
        pageLayout.addWidget(phoneNumber, 3, 0)

        self.changePhoneNumber = QPushButton('Change Phone Number')
        self.changePhoneNumber.clicked.connect(self.changePhoneNumberFunc)
        pageLayout.addWidget(self.changePhoneNumber, 4, 0)

        self.changeEmail = QPushButton('Change Email')
        self.changeEmail.clicked.connect(self.ChangeEmailFunc)
        pageLayout.addWidget(self.changeEmail, 5, 0)

        self.setLayout(pageLayout)

    def ChangeEmailFunc(self):
        print("I am Changing an email!")
        changedEmail, doneone = QtWidgets.QInputDialog.getText(
            self, "Change Email", "Enter Email Address: ")
        if(changedEmail != ""):
            print("Finally changing!")
            sqlLoginQuery = """UPDATE userTable NATURAL JOIN LoginTable SET EmailAddress = %s WHERE LoginUsername = %s"""
            cursor.execute(sqlLoginQuery, (changedEmail, user, ))

    def changePhoneNumberFunc(self):
        print("I am Changing a phone number!")
        changedPhoneNumber, donetwo = QtWidgets.QInputDialog.getText(
            self, "Change Phone Number", "Enter Phone Number: ")
        if(changedPhoneNumber != ""):
            print("Finally changing! Phone")
            sqlLoginQuery = """UPDATE userTable NATURAL JOIN LoginTable SET phoneNumber = %s WHERE LoginUsername = %s"""

            cursor.execute(sqlLoginQuery, (changedPhoneNumber, user, ))

# This main dashboard class is needed for everything and essentially is a connector betwen the classes of the program.
# From here the user can enter a stock ticker, and this class handles with the mariadb to ensure that the stock ticker is both valid and has data to present.
# If the stock ticker entered valid, the system outputs a stock tile, aka a StuckButton object.
# The user will be able to view if the stock is currently bearish or bullish.
# Furthermore the user can save and import a new dashboard with buttons from this window.


class dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # TESTING
        test = "NULL"
        global buttonList
        global nameList

        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        self.setCentralWidget(self.window)
        self.layout.setContentsMargins(5, 200, 0, 0)
        self.window.setLayout(self.layout)

        self.setWindowTitle('Project Stocky - Dashboard')
        self.setFixedSize(1280, 720)

        self.dashboardTitle = QLabel("Project Stocky", self)
        self.dashboardTitle.setGeometry(520, 0, 225, 45)
        self.dashboardTitle.setStyleSheet("font-size: 33px;")
        self.dashboardTitle.setAlignment(QtCore.Qt.AlignCenter)

        # stock Look Up
        self.stockLookUpLabel = QLabel("Stock Lookup", self)
        self.stockLookUpLabel.setStyleSheet("font-size: 20px;")
        self.stockLookUpLabel.setGeometry(33, 0, 175, 30)

        # Stock Look up
        self.stockLookUpEdit = QLineEdit(self)
        self.stockLookUpEdit.setPlaceholderText("Enter Stock Ticker")
        self.stockLookUpEdit.setGeometry(33, 30, 133, 30)

        self.stockSubmitted = QLabel("", self)

        # Submit Stock Ticker Button
        self.stockLookUpButton = QPushButton("Submit", self)
        self.stockLookUpButton.setGeometry(175, 30, 75, 30)
        # When Clicked, run function to check input.
        self.stockLookUpButton.clicked.connect(self.checkInput)

        # Help Button
        self.helpButton = QPushButton("Help", self)
        self.helpButton.setGeometry(900, 30, 75, 30)
        # execute if clicked
        self.helpButton.clicked.connect(self.showHelpMessage)

        # User Information
        self.createDashboard = QPushButton("User\nInfo", self)
        self.createDashboard.setGeometry(1000, 30, 75, 60)
        self.createDashboard.clicked.connect(self.AboutUserButtonFunc)

        self.createDashboard = QPushButton("Save\nDashboard\nConfig", self)
        self.createDashboard.setGeometry(1100, 30, 75, 60)
        self.createDashboard.clicked.connect(self.saveDashboardFunc)

        # Current Config Label
        self.createDashboard = QPushButton("Import\nDashboard\nConfig", self)
        self.createDashboard.setGeometry(1200, 30, 75, 60)
        self.createDashboard.clicked.connect(self.importDashboard)

        if(buttonList != None):
            self.showButtons()

    def saveDashboardFunc(self):
        self.newSaveDashboard = saveDashboard()
        self.newSaveDashboard.show()

    def importDashboard(self):
        self.newImportDashboard = importDashboard()
        self.newImportDashboard.show()
        self.hide()

    def checkInput(self):
        # make labels
        userInput = ""
        userInput = self.stockLookUpEdit.text()
        self.errormsg = QMessageBox()
        self.errormsg.setWindowTitle("Error")
        self.errormsg.setText("")

        # If input is empty
        if userInput == "":
            self.errormsg.setIcon(QMessageBox.Critical)
            self.errormsg.setText(
                "Stock Ticker cannot be empty")
            self.errormsg.exec_()
        # if stock input is not empty check
        else:
            # so if the user input ISNT empty, check it with mySql see if it exists

            if self.SQLCheckInput(userInput):

                # Check if theres too many
                # if there isnt too many, create the Icon
                if self.isIconLimitReached():
                    self.errormsg.setIcon(QMessageBox.Critical)
                    self.errormsg.setText(
                        "Too many Icons! Max is 6.")
                    self.errormsg.exec_()
                else:
                    self.newWidget = StockButton(userInput)
                    buttonList.append(self.newWidget)
                    self.showButtons()
                    nameList.append(self.newWidget.getname())

                    # buttonList.append(self.newButton)
            else:
                self.errormsg.setIcon(QMessageBox.Critical)
                self.errormsg.setText(
                    "Error when Entering Ticker!\nEnter A valid Ticker and Try Again.")
                self.errormsg.exec_()

    def SQLCheckInput(self, userInput):
        # Actual Login Query to avoid SQL injections
        sqlLoginQuery = """SELECT * FROM stockData WHERE stockTicker = %s"""

        cursor.execute(sqlLoginQuery, (userInput, ))

        account = cursor.fetchone()

        if(account):
            return True
        else:
            return False

    def isIconLimitReached(self):
        global iconLimit
        if(iconLimit == 6):
            return True
        else:
            return False

    def showHelpMessage(self):
        helpMessage = QMessageBox(self)
        helpMessage.setIcon(QMessageBox.Information)
        helpMessage.setWindowTitle("Help")
        helpMessage.setText("To begin Project Stocky, first enter a stock ticker into the stock lookup. After pressing the Submit button, a tile will be made. After clicking on said tile, the Stock page will be shown, and graphs will be presented. ")
        helpMessage.setFixedSize(150, 150)
        helpMessage.show()

    def showButtons(self):
        for button in buttonList:
            self.layout.addWidget(button)

    def AboutUserButtonFunc(self):
        self.newAboutPage = aboutUserPage()
        self.newAboutPage.show()


# begin Project Stocky!
if __name__ == "__main__":
    # create pyqt5 app
    app = QApplication(sys.argv)
    # create the instance of our Window
    form = LoginSystem()
    form.show()
    # start the app
    sys.exit(app.exec())
