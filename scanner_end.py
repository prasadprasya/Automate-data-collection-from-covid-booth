import cv2
import sqlite3
from tkinter import ttk
import tkinter as tk

conn = sqlite3.connect('db1.sqlite')
cur = conn.cursor()
# Make some fresh tables using executescript()

cur.execute('''
    CREATE TABLE IF NOT EXISTS"covid_testing_booth" (
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name" varchar(200) NOT NULL,
	"aadhar" INTEGER(16) NOT NULL,
	"address" varchar(500) NOT NULL,
	"mobile" varchar(13) NOT NULL)
''')
my_w=tk.Tk()
my_w.geometry('400x500')
my_w.title("www.plus2net.com")
trv = ttk.Treeview(my_w, selectmode='browse')
trv.grid(row=1, column=1, columnspan=4, padx=20, pady=20)
trv["columns"] = ("1", "2", "3", "4", "5")
trv['show'] = 'headings'
trv.column("1", width=30, anchor='c')
trv.column("2", width=255, anchor='c')
trv.column("3", width=255, anchor='c')
trv.column("4", width=255, anchor='c')
trv.column("5", width=255, anchor='c')

trv.heading("1", text="id")
trv.heading("2", text="Name")
trv.heading("3", text="aadhar")
trv.heading("4", text="address")
trv.heading("5", text="mobile")

i=0

l0 = tk.Label(my_w, text='To scan qrcode click below',
              font=('Helvetica', 16), width=30, anchor="c")
l0.grid(row=2, column=1, columnspan=4)
b1 = tk.Button(my_w, text='scan', width=10,
               command=lambda: scan())
b1.grid(row=3, column=2)

my_str = tk.StringVar()
l1 = tk.Label(my_w, textvariable=my_str, width=10)
l1.grid(row=4, column=2)
def scan():
    # set up camera object
    cap = cv2.VideoCapture(0)
    # QR code detection object
    detector = cv2.QRCodeDetector()
    flag=True
    while flag:
        # get the image
        _, img = cap.read()
        # get bounding box coords and data

        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            mystring = list()
            mystring = str(data)

            x = mystring.split("&")
            name=x[0]
            aadhar=x[1]
            address=x[2]
            mobile=x[3]
            global i
            i = i + 1
            cur.execute('''INSERT OR IGNORE INTO "covid_testing_booth"
                (id, name, aadhar, address, mobile) 
                VALUES ( ?, ?, ?, ?, ?)''',
                        (i, name, aadhar, address, mobile))

            trv.insert("", 'end',
                       values=(i, name, aadhar, address, mobile,))

            my_str.set("Data added ")
            l1.after(30, lambda: my_str.set(''))  # remove the message

            conn.commit()
            flag=False


        # display the image preview
        cv2.imshow("code detector", img)
        if cv2.waitKey(1) == ord("q"):
            break

    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()
my_w.mainloop()


