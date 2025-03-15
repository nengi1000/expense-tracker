

import sys
from app import expenseApp
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_db


def main():

    app = QApplication(sys.argv)

    if not init_db("spend_chek.db"):
        QMessageBox.critical(None, "SOZ, ERROR!","I COULDN'T LOAD YOUR DATABASE")
        sys.exit(5)

    window = expenseApp()
    window.show()       
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
