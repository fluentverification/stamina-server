import sqlite3
import getpass

from admin import *

connection = sqlite3.connect("database.db")

with open("schema.sql") as schema:
	connection.executescript(schema.read())

cur = connection.cursor()

if __name__=="__main__":
	num_admin_accounts = int(input("Please put the number of admin accounts to add: "))
	for n in range(num_admin_accounts):
		username = input("Username: ")
		password = getpass.getpass()
		if len(password) < AdminSettings.MIN_PASSWORD_LENGTH:
			print(f"Password is too short! (Must be at least {AdminSettings.MIN_PASSWORD_LENGTH} characters)")
			exit(1)
		cur.execute("insert into users (username, passwd, admin) values (? ? ?)", (username, password, 1,))
