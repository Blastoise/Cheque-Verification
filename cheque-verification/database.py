import sqlite3


class Database:
    def __init__(self, pathToDatabase):
        self.conn = sqlite3.connect(pathToDatabase + "/bankdb.sqlite")
        self.cur = self.conn.cursor()

    # Return Account Details of Payer using MICR ID
    def micrToAccountDetails(self, micrId):
        self.cur.execute(
            """
            SELECT * FROM BankAccount WHERE micr_id=?
            """,
            (micrId,),
        )
        return self.cur.fetchone()

    # Return Name of Receiver from Account Number
    def accNumberToName(self, accountNumber):
        self.cur.execute(
            """
            SELECT name FROM BankAccount WHERE account_number=?
            """,
            (accountNumber,),
        )
        return self.cur.fetchone()

    # Update balance of Payer and Receiver using Account Number
    def updateAmount(self, payerAccountNumber, receiverAccountNumber, amount):
        self.cur.execute(
            """
            UPDATE BankAccount SET amount=amount+? WHERE account_number=?
            """,
            (amount, receiverAccountNumber),
        )
        self.cur.execute(
            """
            UPDATE BankAccount SET amount=amount-? WHERE account_number=?
            """,
            (amount, payerAccountNumber),
        )
        self.conn.commit()

    def closeConnection(self):
        self.cur.close()
        self.conn.close()
