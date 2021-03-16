import random
import sqlite3


class Bank:

    def __init__(self):
        self.card_number = self.card_number_func()
        self.card_pin = self.card_pin_func()
        self.money = 0

    @staticmethod
    def card_number_func():
        random.seed()
        card_no = "400000"
        double_a = 8
        for _ in range(0, 9):
            a = str(random.randint(0, 9))
            card_no += a
        for i in range(6, 15):
            b = int(card_no[i])
            if i % 2 == 0:
                b *= 2
                if b > 9:
                    b -= 9
            double_a += b
        if double_a % 10 == 0:
            a = 0
        else:
            a = 10 - (double_a % 10)

        return card_no + str(a)

    @staticmethod
    def card_pin_func():
        random.seed()
        pin = ""
        for _ in range(4):
            pin += str(random.randint(0, 9))
        return pin

    @staticmethod
    def login():
        user_card = input("Enter your card number:\n")
        user_pin = input("Enter your PIN:\n")
        cur.execute("Select * from card;")
        records = cur.fetchall()
        for i in range(len(records)):
            if records[i][1] == user_card and records[i][2] == user_pin:
                print("You have successfully logged in!")
                while True:
                    choose2 = input("1. Balance\n2. Add income\n3. Do Transfer\n4. Close account\n5. Log out\n0. Exit\n")
                    if choose2 == '1':
                        Bank.balance(i)
                    if choose2 == '2':
                        Bank.income(i)
                    if choose2 == '3':
                        Bank.transfer(i)
                    if choose2 == '4':
                        Bank.close_account(i)
                    if choose2 == '5':
                        print("You have successfully logged out!")
                        return
                    if choose2 == '0':
                        exit("Bye!")
        else:
            print("Wrong card number or PIN!")

    @staticmethod
    def create_database():
        cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        conn.commit()

    @staticmethod
    def balance(counter):
        cur.execute("Select * from card;")
        records = cur.fetchall()
        print("Balance: ", records[counter][3])

    @staticmethod
    def income(counter):
        cur.execute("Select * from card;")
        records = cur.fetchall()
        income = int(input("Enter income:\n"))
        temp = records[counter][3] + income
        cur.execute("Update card set balance =  (?) where number = (?);", (temp, records[counter][1]))
        conn.commit()
        print("Income was added!")

    @staticmethod
    def transfer(counter):
        cur.execute("Select * from card;")
        records = cur.fetchall()
        print("Transfer")
        card_transfer = input("Enter card number:\n")
        if not(Bank.lunh_check(card_transfer)):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not(any(card_transfer in sl for sl in records)):
            print("Such a card does not exist.")
        else:
            how_much = int(input("Enter how much money you want to transfer: "))
            if how_much > records[counter][3]:
                print("Not enough money!")
            else:
                cur.execute("Select * from card where number = (?);", (card_transfer,))
                records2 = cur.fetchall()
                temp = records[counter][3] - how_much
                temp2 = records2[0][3] + how_much
                cur.execute("Update card set balance =  (?) where number = (?);", (temp, records[counter][1]))
                conn.commit()
                cur.execute("Update card set balance =  (?) where number = (?);", (temp2, card_transfer))
                conn.commit()
                print("Success!")

    @staticmethod
    def lunh_check(card_number):
        result = 0
        i = 0
        for _ in card_number:
            a = int(card_number[i])
            if i % 2 == 0:
                a *= 2
                if a > 9:
                    a -= 9
            result += a
            i += 1
        if result % 10 == 0:
            return True
        else:
            return False

    @staticmethod
    def close_account(counter):
        cur.execute("Select * from card;")
        records = cur.fetchall()
        cur.execute("Delete from card where number = (?);", (records[counter][1],))
        conn.commit()


while True:

    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    Bank.create_database()

    choose = input("1. Create an account\n2. Log into account\n0. Exit\n")

    if choose == '1':
        new_account = Bank()
        print("Your card has been created")
        print("Your card number:")
        print(new_account.card_number)
        print("Your card PIN:")
        print(new_account.card_pin)
        cur.execute("INSERT into card (number, pin, balance) values (?, ?, ?);", (new_account.card_number, new_account.card_pin, new_account.money))
        conn.commit()
    elif choose == '2':
        Bank.login()
    elif choose == '0':
        exit("Bye!")
