

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    database =QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False

    query = QSqlQuery()

    query.exec("""
                CREATE TABLE IF NOT EXISTS spendings(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT
                )
                """)

    return True

def get_expensnses():
    query = QSqlQuery("SELECT * FROM spendings ORDER BY date DESC")
    spendings = []
    while query.next():
        # spendings.append( [[query.value(n)] for n in range(5)] )
        spendings.append([query.value(n) for n in range(5)])
    return spendings

def add_an_expense(date, category, amount, description):
    print("accunt never empty.. need to add an expense??..")
    query = QSqlQuery()
    query.prepare("""
                    INSERT INTO spendings (date, category, amount, description)
                    VALUES (?, ?, ?, ?)
                    """)

    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    print("i don add o")
    return query.exec()

def delete_an_exoense(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM spendings WHERE id = ? ")
    query.addBindValue(expense_id)
    return query.exec()
