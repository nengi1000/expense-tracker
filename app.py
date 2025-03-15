#app desigm here

from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QHBoxLayout, QVBoxLayout, QHeaderView
from PyQt6.QtCore import QDate, Qt
from database import get_expensnses, add_an_expense, delete_an_exoense


class expenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.userface()
        self.load_table_data()

    def settings(self):
        self.setGeometry(100, 100, 580, 550)
        self.setWindowTitle("my expense tracker app!!")

    # UI Setup
    def userface(self):
        self.datebox = QDateEdit()
        self.datebox.setDate(QDate.currentDate())
        self.dropdown =  QComboBox()
        self.description = QLineEdit()
        self.amount = QLineEdit()

        self.buttonadd = QPushButton("Add an expense")
        self.buttondel = QPushButton("Delete an expense")

        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["expense_id", "amount", "category", "description", "date" ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #this fixes tit for when the category date and all stretches

        self.buttonadd.clicked.connect(self.add_expense)
        self.buttondel.clicked.connect(self.delete_expense)

        self.dropdown_thungs()
        self.styling()
        self.setup_layout()

    #my css bit
    def styling(self):
        self.setStyleSheet("""
                            QWidget{
                                background-color: #E1DAE2;
                                font-size : 15px;
                                color: black;
                            }
                            
                            QLabel{ 
                                font-size: 16.5px;
                                font-weight: bold;
                                padding: 5px;
                            }
                            
                            QLineEdit, QDateEdit, QComboBox,QPushButton{
                                background-colour: #C3BDCF;
                                border: 2px solid #767280;
                                border-radius: 6.8px; 
                                padding: 5px;
                            }
                            
                            QComboBox::drop-down {
                                border-radius: 4px; 
                                border: none;
                                padding-right: 5px;
                            }
                            
                             QPushButton:hover {
                                  background-color: #9C27B0;
                             }

                            QPushButton:pressed {
                                 background-color: #4A148C;
                            }
  
                            QTableWidget {
                                background-color: #DEDAE3;
                                alternate-background-color: #9A96A1;
                                gridline-color: #988fb0;
                                selection-color: white;
                                selection-background-color: #cb51e0;
                                font-size: 14.5px;
                                border-radius: 10px;
                                border: 2px solid #988fb0;
                            }     
                            
                            QHeaderView::section {
                                background-color:#E1DAE2;
                                color:  black;
                                font-weight: bold;
                                font-size: 15px;
                                padding: 5px;
                                border: 1px solid #988fb0;
                                border-radius: 5px;
                            }
 
                            """)

    #add widgets
    def setup_layout(self):
        master_layout = QVBoxLayout()
        r1 = QHBoxLayout()
        r2= QHBoxLayout()
        r3 = QVBoxLayout()

        #row 1
        r1.addWidget(QLabel("date"))
        r1.addWidget(self.datebox)
        r1.addWidget(QLabel("category"))
        r1.addWidget(self.dropdown)

        #rown 2
        r2.addWidget(QLabel("amount"))
        r2.addWidget(self.amount)
        r2.addWidget(QLabel("description"))
        r2.addWidget(self.description)

        #row 3
        r3.addWidget(self.buttonadd)
        r3.addWidget(self.buttondel)

        #addong layouts
        master_layout.addLayout(r1)
        master_layout.addLayout(r2)
        master_layout.addLayout(r3)
        master_layout.addWidget(self.table)

        self.setLayout(master_layout)

    def dropdown_thungs(self):
        categories = ["food", "rent", "bills", "family", "frds/entertainmainment", "shopping", "others"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        all_expenses = get_expensnses()
        self.table.setRowCount(0)
        for rw, expense in enumerate(all_expenses):
            self.table.insertRow(rw)

            for column, data in enumerate(expense):
                self.table.setItem(rw, column, QTableWidgetItem ( str (data) ) )

        print(get_expensnses())  # Check if the expense actually exists in the database

    def clear_the_inputs(self):
        self.datebox.setDate(QDate.currentDate())
        self.dropdown.setCurrentText(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.datebox.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        description =self.description.text()

        try:
            amount = float(self.amount.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Amount must be a number. (if theres a comma, remove)")
            return


        print("hi, im trying to add this expense...")

        if not amount or not description:
            QMessageBox.warning(self, "hold on", "amount or description can't be empty")
            return

        if add_an_expense(date, category, amount, description):
            self.load_table_data()
            self.clear_the_inputs()

        else:
            QMessageBox.critical(self, "sorry error","failed to add this expense")

    def delete_expense(self):
        row_selected = self.table.currentRow()

        if row_selected == -1:
            QMessageBox.warning(self, "bruh","pick a row before pressing delete...")
            return

        # getid = self.table.item(row_selected, 0)
        expense_id = int(self.table.item(row_selected, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Do you really want to delete this?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes and delete_an_exoense(expense_id):
            self.load_table_data()