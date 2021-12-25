import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from mysql import connector
import os


# db_user = os.environ.get('DB_USER')
# db_pass = os.environ.get('DB_PASS')

con = connector.connect(host = "localhost", user = "root", password = "vaibhav")
cur = con.cursor()

cur.execute("create database if not exists hims")
con.database = "hims"

def payment():
    cur.execute("create table if not exists payment(Payment_ID int auto_increment primary key,mode varchar(30),BankName varchar(10))")
    # cur.execute("alter table bill add column Payment_ID int")
    # cur.execute("alter table bill add foreign key(payment_ID) references payment(Payment_ID)")
    cur.execute("create table if not exists performs(P_ID int,Payment_ID int,foreign key(P_ID) references person(P_ID),foreign key(Payment_ID) references payment(Payment_ID))")

    def click():
        def pay():
            mode=clicked.get()
            if seltdBank.get() == 1:
                Bank="HDFC"
            elif seltdBank.get() == 2:
                Bank = "Axis"
            elif seltdBank.get() == 3:
                Bank="ICICI"
            cur.execute(f"insert into payment(mode,BankName) values ('{mode}','{Bank}')")
            con.commit()
            cur.execute("select payment_ID from payment order by payment_ID")
            Payment_ID=cur.fetchall()[-1][0]
            cur.execute("select Bill_ID from bill order by Bill_ID")
            Bill_ID = cur.fetchall()[-1][0]
            cur.execute(f"UPDATE bill SET Payment_ID = {Payment_ID} where Bill_ID = {Bill_ID}")
            con.commit()
            cur.execute("select P_ID from buys")
            P_ID=cur.fetchall()[-1][0]
            cur.execute(f"insert into performs values({P_ID},{Payment_ID})")
            con.commit()
            messagebox.showinfo(title="payment successful",message="paid successfully")
            root.destroy()

        payment = Frame(root,highlightthickness=1,highlightbackground="grey")
        seltdBank = IntVar()
        if clicked.get() == 'Net Banking':
            Radiobutton(payment, text='HDFC', value=1, variable=seltdBank).pack()
            Radiobutton(payment, text='Axis', value=2, variable=seltdBank).pack()
            Radiobutton(payment, text='ICICI', value=3, variable=seltdBank).pack()
            Label(payment, text="CUSTOMER ID : ").pack(pady=10)
            cust_id = Entry(payment).pack(pady=(0,10),padx=10)
            Label(payment, text="Password : ").pack()
            passwd = Entry(payment).pack(pady=(0,10),padx=10)
        elif clicked.get() == "Credit/Debit/ATM Card":
            Radiobutton(payment, text='HDFC', value=1, variable=seltdBank).pack(pady=5,padx=10)
            Radiobutton(payment, text='Axis', value=2, variable=seltdBank).pack(pady=5,padx=10)
            Radiobutton(payment, text='ICICI', value=3, variable=seltdBank).pack(pady=5,padx=10)
            Label(payment, text="CARD NUMBER : ").pack(pady=15,padx=10)
            card_no = Entry(payment).pack(pady=10,padx=10)

        payment.grid(row=2,columnspan=3,sticky=W+E,padx=10,pady=10)
        btn1 = Button(root, text="Pay",command=pay)
        btn1.grid(row=6,columnspan=3,pady=10)


    root = Tk()
    root.title("Mode of Payment")
    root.geometry("300x400")
    frm=Frame(root)
    paymentOpt=["Credit/Debit/ATM Card","Net Banking"]
    clicked = StringVar()
    paymentMethod = OptionMenu(frm,clicked,*paymentOpt)
    paymentMethod.config(width=30)
    paymentMethod.grid(row=0,column=0,padx=10,pady=10)
    clicked.set("Select payment method")


    btn = Button(frm, text = "select", command=click)
    btn.grid(row=0,column=1,pady=10)

    frm.grid(row=0,sticky=N,pady=10)
    root.mainloop()
