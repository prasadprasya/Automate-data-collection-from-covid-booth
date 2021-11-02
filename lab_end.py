import tkinter  as tk
from tkinter import *
import sqlite3
from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)
my_conn = sqlite3.connect('db1.sqlite')
cur = my_conn.cursor()

###### end of connection ####

##### tkinter window ######



my_w = tk.Tk()
my_w.geometry("400x350")


def my_show():
    r_set = my_conn.execute('''SELECT * from covid_testing_booth ''')
    i = 0  # row value inside the loop
    for student in r_set:
        for j in range(len(student)):
            e = Entry(my_w, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(tk.END, student[j])

        b1 =tk.Button(my_w, width='8', text='positive', fg='red', anchor='w', command=lambda k=student[0]:positive(k))
        b1.grid(row=i, column=7)
        b2 =tk.Button(my_w, text='negative', fg='green', anchor='w', command=lambda j=student[0]:negative(j))
        b2.grid(row=i, column=8)
        i = i + 1



def positive(id):
    num = my_conn.execute("SELECT mobile FROM covid_testing_booth WHERE id=?", (id,))
    number_id=num.fetchone()
    number = number_id[0]


    client.messages.create(
        body="you tested 'POSITIVE', so u have to be home quarantine or approach to doctor for treatment ",
        from_=keys.twilio_number,
        to=number
    )



def negative(id):
    num= my_conn.execute("SELECT mobile FROM covid_testing_booth WHERE id=?",(id,))
    number_id=num.fetchone()
    number = number_id[0]

    client.messages.create(
        body="you tested 'NEGATIVE', Wear mask and carry hand sanitizer and follow some precautions",
        from_=keys.twilio_number,
        to=number
    )


my_show()  # open the window with record at the starting

my_w.mainloop()