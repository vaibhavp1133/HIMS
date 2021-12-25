from tkinter import *
from tkinter import messagebox
from mysql import connector
from datetime import date
from dateutil.relativedelta import relativedelta
from bill import *

# db_user = os.environ.get('DB_USER')
# db_pass = os.environ.get('DB_PASS')

def main():
    con = connector.connect(host="localhost", user="root", password="vaibhav", database="HIMS")
    cur = con.cursor()

    cur.execute("create table if not exists policy(PID int primary key, PName varchar(20), Sum_Insured double(15,3), Benefits varchar(1000), Duration varchar(50), per_month double(15,3))")


    root = Tk()
    root.title("Welcome to DMNS Insurance company")
    cur.execute("select * from policy")
    policies = cur.fetchall()
    list_policies = {}
    val = []


    def click(value):
        Label(frm1, text="Insurance Name : ").grid(row=0, column=0, sticky=E)
        text = Label(frm1, width=70, height=1, bd=1, relief="sunken", padx=5, pady=5)
        text.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        text.config(text=policies[value - 1][1])

        Label(frm1, text="Sum Insured    : ").grid(row=1, column=0, sticky=E)
        text = Label(frm1, width=70, height=1, bd=1, relief="sunken", padx=5, pady=5)
        text.grid(row=1, column=1, sticky=W, padx=10, pady=10)
        text.config(text=policies[value - 1][2])

        Label(frm1, text="Duration       : ").grid(row=2, column=0, sticky=E)
        text = Label(frm1, width=70, height=1, bd=1, relief="sunken", padx=5, pady=5)
        text.grid(row=2, column=1, sticky=W, padx=10, pady=10)
        text.config(text=policies[value - 1][4])

        Label(frm1, text="Payable amount : ").grid(row=3, column=0, sticky=E)
        text = Label(frm1, width=70, height=1, bd=1, relief="sunken", padx=5, pady=5)
        text.grid(row=3, column=1, sticky=W, padx=10, pady=10)
        text.config(text=str(policies[value - 1][5]) + "Rs./month")

        Label(frm1, text="Benefits       : ").grid(row=4, column=0, sticky=NE)
        text = Text(frm1, width=60, height=13, padx=10, pady=10)
        text.grid(row=4, column=1, padx=10, pady=10)
        text.insert(END, policies[value - 1][3])
        text.config(state="disabled", bg='#%02x%02x%02x' % (240, 240, 240))


    def Buy():
        cur.execute("create table if not exists Buys(P_ID int,PID int,start_Date Date, End_Date Date,Foreign key (P_ID) references person(P_ID),Foreign key (PID) references policy(PID))")
        cur.execute(f"Select P_ID from person order by P_ID")
        p_id = cur.fetchall()[-1][0]#person id
        pid=v.get()#policy id
        today=date.today()
        if pid == 1 or pid == 2:
            afte5yrs=today+relativedelta(years=+5)
            cur.execute(f"Insert into buys values({p_id},{pid},'{today}','{afte5yrs}')")
        else:
            afte3yrs=today+relativedelta(years=+3)
            cur.execute(f"Insert into buys values({p_id},{pid},'{today}','{afte3yrs}')")
        con.commit()
        root.destroy()
        bill()

    for i in range(len(policies)):
            list_policies[policies[i][0]] = [policies[i][1], policies[i][2], policies[i][3], policies[i][4]]

    frm = Frame(root)
    Label(frm, text="Welcome to DMNS Health Insurance company", font=("", 26), bd=1, relief="sunken").pack()
    frm.grid(row=0, columnspan=3)

    v = IntVar(root, 0)

    Label(root, text="Please select a insurance type").grid(row=1, sticky=W)
    frm1 = Frame(root, highlightbackground="grey", highlightthickness=1, padx=10, pady=10)
    for (i, val) in list_policies.items():
        Radiobutton(root, text=f"{i}.{val[0]}", variable=v, value=i, command=lambda: click(v.get()), padx=10, pady=10).grid(
            row=2, column=i - 1, sticky=W)

    frm1.grid(row=3, columnspan=3)
    btn = Button(root, text="Buy", command=Buy).grid(row=4, columnspan=3, padx=10, pady=10)
    root.mainloop()