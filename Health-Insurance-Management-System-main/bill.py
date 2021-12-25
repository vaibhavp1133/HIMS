import os
from tkinter import *
from mysql import connector
from tkinter import messagebox
from payment import *
def bill():
    def cont():
        wind.destroy()
        payment()

    # db_user = os.environ.get('DB_USER')
    # db_pass = os.environ.get('DB_PASS')

    conn = connector.connect(host = "localhost", user = "root", password = "vaibhav")
    cur = conn.cursor()
    conn.database = "hims"

    cur.execute("create table if not exists bill(Bill_ID int auto_increment primary key,PID int,Total_Amount double(15,3),foreign key(PID) references policy(PID))")

    wind = Tk(className=" Bill")
    wind.geometry("400x300")

    Label(wind, text = "Summary", font = ("",12, "bold"))
    cur.execute("select * from buys")
    buys=cur.fetchall()[-1]
    p_id=buys[0]
    pid=buys[1]
    start_date=buys[2]
    end_date=buys[3]
    cur.execute(f"select name from person where P_ID = {p_id}")
    per_name = cur.fetchone()[0]
    cur.execute(f"select pname,sum_insured,per_month from policy where PID = {pid}")
    policy = cur.fetchone()
    pol_name = policy[0]
    sum_insured = policy[1]
    payable = policy[2]
    Label(wind, text="DMNS Health Insurance company", font=("", 26), bd=1, relief="sunken").pack()
    Label(wind,text="Summary",font=("",12,"bold")).pack()

    frm=Frame(wind, highlightbackground="grey", highlightthickness=1, padx=10, pady=10)

    Label(frm, text = "Customer Name   : ").grid(row=0,column=0,sticky=E)
    Label(frm, text = "Customer ID   : ").grid(row=1,column=0,sticky=E)
    Label(frm, text = "Insurance Name   : ").grid(row=2,column=0,sticky=E)
    Label(frm, text = "Start date   : ").grid(row=3,column=0,sticky=E)
    Label(frm, text = "End date   : ").grid(row=4,column=0,sticky=E)
    Label(frm, text = "Sum Insured   : ").grid(row=5,column=0,sticky=E)
    Label(frm, text = "Payable amount   : ").grid(row=6,column=0,sticky=E)
    Label(frm, text = "Total amount   : ").grid(row=7,column=0,sticky=E)

    Label(frm, text=per_name).grid(row=0,column=1,sticky=W)
    Label(frm, text=p_id).grid(row=1,column=1,sticky=W)
    Label(frm, text=pol_name).grid(row=2,column=1,sticky=W)
    Label(frm, text=str(start_date)).grid(row=3,column=1,sticky=W)
    Label(frm, text=str(end_date)).grid(row=4,column=1,sticky=W)
    Label(frm, text="₹ "+str(sum_insured)).grid(row=5,column=1,sticky=W)
    Label(frm, text="₹ "+str(payable *12) + "/ Year").grid(row=6,column=1,sticky=W)
    if pid == 3:
        Label(frm, text="₹ "+str(payable *12 *3)).grid(row=7,column=1,sticky=W)
        cur.execute(f"insert into bill(pid,total_amount) values({pid},{payable * 12 * 3})")
        conn.commit()
    else:
        Label(frm, text="₹ " + str(payable * 12 * 5)).grid(row=7, column=1, sticky=W)
        cur.execute(f"insert into bill (pid,total_amount) values ({pid},{payable * 12 * 5})")
        conn.commit()

    frm.pack()
    contBtn = Button(wind, text = "Go to payment", command=cont)
    contBtn.pack(pady=10)

    wind.mainloop()