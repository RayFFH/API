import sqlite3

connection = sqlite3.connect('grades.db')
# c = connection.cursor()
#
# c.execute("""CREATE TABLE grades (
#        first_name text,
#         last_name text,
#          grade text
#
#  )""")
# # connection.commit()
# connection.close()


def add(first, last, grade):
    connection = sqlite3.connect('grades.db')
    c = connection.cursor()
    c.execute("INSERT INTO grades VALUES (?,?,?)", (first, last, grade))
    connection.commit()
    connection.close()


def show_record():
    connection = sqlite3.connect('grades.db')

    c = connection.cursor()

    c.execute("SELECT rowid, * FROM grades LIMIT 5")
    records = c.fetchall()
    for record in records:
        print(record)

    connection.commit()
    connection.close()


# add('John', 'Smith', 'A')
show_record()