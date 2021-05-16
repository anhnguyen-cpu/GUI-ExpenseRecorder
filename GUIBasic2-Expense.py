from tkinter import *
from tkinter import ttk, messagebox #ttk istheme of tk
import csv
from datetime import datetime
from typing import Collection

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Anh Nguyen')
GUI.geometry('600x600+500+100') #chieucao-rong cua GUI // vitri cua GUI









###################menu bar################

menubar = Menu(GUI)
GUI.config(menu=menubar)

#####file menu
filemenu = Menu(menubar)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
#####help
def About():
    messagebox.showinfo('About','Hello This is My Program for input information expense.')


helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

#########################################

Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

expenseicon = PhotoImage(file='expense.png')
listicon = PhotoImage(file='list.png')

Tab.add(T1,text=f'{"Add Expense": ^50s}', image=expenseicon,compound='top')
Tab.add(T2,text=f'{"Expense List": ^50s}', image=listicon,compound='top')

F1 = Frame(T1)
# F1.place(x=100,y=50)
F1.pack()

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พูธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()
    if expense =='' or price =='' or  quantity=='':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลให้ครบ')
        return
    try:
        total = int(price) * int(quantity)
        print('รายการ: {} ราคา: {} บาท จำนวน {} ชิ้น รวมเป็นเงิน {} บาท'.format(expense,price,quantity,total))
        text= 'รายการ: {} ราคา: {} บาท\n จำนวน {} ชิ้น รวมเป็นเงิน {} บาท'.format(expense,price,quantity,total)
        v_result.set(text)
        #clear ข้อมูลเก่า
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        #บันทึกข้อมูลลงcsv อย่าลื่ม import csv ด้วย
        today = datetime.now().strftime('%a')
        dt=datetime.now().strftime('%Y/%m/%d-{}, %H:%M:%S'.format(days[today]))
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
            #newline=''ทำให้ข้อมูลไม่มีบรรทัดว่าง
            #with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลจากข้อมูลเก่า
            fw = csv.writer(f) #สร้างฟังซันสำหรับเขียนข้อมูล
            data = [dt,expense,price,quantity,total]
            fw.writerow(data)

        #ทำให้เคอเชอร์กลับไปตำแหน่ง E1
        E1.focus()
        update_table()
    except Exception as e:
        print('ERROR:',e)
        messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        # messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')
#ทำให้สามารถกด Enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None)

FONT1 = (None,20)

centerimg = PhotoImage(file='wallet.png')
logo = ttk.Label(F1,image=centerimg)
logo.pack()


#-----TEXT 1------------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() la bien dac biet de luu du lieu trong GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

#---------------------end------------
#-----TEXT 2------------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() la bien dac biet de luu du lieu trong GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

#---------------------end------------

#-----TEXT 2------------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() la bien dac biet de luu du lieu trong GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()

#---------------------end------------

buttonimg = PhotoImage(file='save.png')
B2 = ttk.Button(F1,text='Save',command=Save, image=buttonimg,compound='left')
B2.pack(ipadx=30,ipady=10,pady=20)

v_result = StringVar()
v_result.set('============ผลหัพธ์============')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)



######################tab2#########################

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

############table#############
L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)


header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable  = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()

# for i in range(len(header)):

#     resulttable.heading(header[i],text=header[i])

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

def update_table():
    resulttable.delete(*resulttable.get_children())
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()
print('GET CHILD:',resulttable.get_children())

        # print(data)
        # print(data[0])
        # for d in data:
        #     print(d)


# read_csv()

GUI.mainloop() #runeverytime #finish
