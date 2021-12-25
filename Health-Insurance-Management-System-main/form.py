import os
from tkinter import *
from mysql import connector
from policy import *
from tkinter import messagebox

# db_user = os.environ.get('DB_USER')
# db_pass = os.environ.get('DB_PASS')

conn = connector.connect(host = "localhost", user = "root", password = "vaibhav")
cur = conn.cursor()

cur.execute("create database if not exists hims")
conn.database = "hims"

cur.execute("create table if not exists person(p_id int auto_increment primary key, "\
            "name varchar(100) not null, email varchar(100) unique not null, ph_no varchar(10) not null, gend varchar(6) not null)")
cur.execute("create table if not exists policy(PID int primary key, PName varchar(20), Sum_Insured double(15,3), Benefits varchar(1000), Duration varchar(50), per_month double(15,3))")
cur.execute("create table if not exists bill(Bill_ID int auto_increment primary key,PID int,Total_Amount double(15,3),foreign key(PID) references policy(PID))")
cur.execute("create table if not exists payment(Payment_ID int auto_increment primary key,mode varchar(30),BankName varchar(10))")
# cur.execute("alter table bill add column Payment_ID int")
cur.execute("alter table bill add foreign key(Payment_ID) references payment(Payment_ID)")
cur.execute("create table if not exists performs(P_ID int,Payment_ID int,foreign key(P_ID) references person(P_ID),foreign key(Payment_ID) references payment(Payment_ID))")


def submit():
    if(uname.get().rstrip() == "" or email.get().rstrip() == "" or phone.get().rstrip() == "" or (seltdGend.get() != 1 and seltdGend.get() != 2)):
        messagebox.showerror(title = "Error", message = "Please enter all the details!")
        return

    gend = "Male"
    if seltdGend.get() == 2:
        gend = "Female"

    cur.execute("insert into person(name, email, ph_no, gend) value(%s, %s, %s, %s)", (uname.get(), email.get(), phone.get(), gend))
    conn.commit()
    wind.destroy()
    main()

wind = Tk(className=" Person Details")
Label(wind, text="DMNS Health Insurance company", font=("", 26), bd=1, relief="sunken").pack()
frm=Frame(wind)
Label(frm, text = "Enter your details here:").grid(row = 0, column = 1, padx = 10, pady = 20)

Label(frm, text = "Name :").grid(row = 1, column = 0)
uname =  Entry(frm)
uname.grid(row = 1, column = 1)

Label(frm, text = "Email :").grid(row = 2, column = 0, pady = 10)
email =  Entry(frm)
email.grid(row = 2, column = 1, pady = 10)

Label(frm, text = "Phone :").grid(row = 3, column = 0)
phone = Entry(frm)
phone.grid(row = 3, column = 1, pady = 10)

seltdGend = IntVar()
Label(frm, text='Gender:').grid(row = 4, column = 0, padx = 10, pady = 10)
male = Radiobutton(frm, text='Male', value = 1, variable = seltdGend)
female = Radiobutton(frm, text='Female', value = 2, variable = seltdGend)
male.grid(row=4, column=1, sticky="w")
female.grid(row=4, column=1, sticky = "e")

contBtn = Button(frm, text = "Continue", command = submit)
contBtn.grid(row = 5, column = 1, pady = 10)
frm.pack()

wind.mainloop()



# insert into policy values(1, "Individual", 200000, "An Individual Health Insurance is a policy which you may buy to cover you, your spouse, children and parents. This type of insurance policy covers your medical expenses for injury & illnesses related hospitalization, surgery costs, room rent, daycare procedures and more.", "3 years", 1000);

# insert into policy values(2, "Family Floater", 300000, "Under a Family Floater Health Insurance, single Sum Insured floats for all the members covered under the policy. A Family Floater Health Insurance Plan is beneficial because the premium is comparatively lower than the Individual Health Insurance policy. This policy can cover yourself, your spouse, children and parents.", "2 years", 2000);

# insert into policy values(3, "Senior Citizen", 500000, "A Senior Citizen Policy will offer coverage for cost of medicines, hospitalization arising out of accident or illness, pre and post hospitalization and treatment. Along with these, some other benefits like Domiciliary Hospitalization and Psychiatric benefits are also covered.", "5 years", 3000);