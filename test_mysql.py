# import mysql.connector
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="1234567890"
# )

# print(mydb)

# from mysql.connector import connect, Error
# try:
#     with connect(
#         host="localhost",
#         user="root",  # input("Enter username: "),
#         password="1234567890",  # getpass("Enter password: "),
#     ) as connection:
#         # create_db_query = "CREATE DATABASE crypto_trans"
#         with connection.cursor() as cursor:
#             for x in cursor:
#                 print(x)

#             # cursor.execute(create_db_query)
# except Error as e:
#     print(e)


import mysql.connector
import csv
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234567890",
  database="sql1624295_1"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT users.bnb_wallet AS bnb_wallet, users.name AS name FROM users")
sql = "SELECT users.bnb_wallet, users.name, payments.* FROM payments LEFT JOIN purchases ON (payments.purchase_id=purchases.id) LEFT JOIN users ON (purchases.user_id = users.id)"


mycursor.execute(sql)

# myresult = mycursor.fetchall()


columns = [col[0] for col in mycursor.description]
rows = [dict(zip(columns, row)) for row in mycursor.fetchall()]

print(rows)
# for x in myresult:
#     print(x[2])
#     print(type(x))
#     print(x)
    


# with open("out.csv", "w", newline='') as csv_file:  # Python 3 version    
# #with open("out.csv", "wb") as csv_file:              # Python 2 version
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow([i[0] for i in cursor.description]) # write headers
#     csv_writer.writerows(cursor)