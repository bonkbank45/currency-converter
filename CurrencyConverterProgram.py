import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox

root = tk.Tk()
root.title("Currency_Converter_Program")

#กำหนดขนาดและสี
root.configure(bg="#FFE4E1")
root.geometry("800x450")#กว้างxสูง
root.minsize(800,450)
root.maxsize(800,450)

left_frame = Frame(root, width=200, height=50)
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=200, height=50)
right_frame.grid(row=0, column=1, padx=10, pady=5)

tool_bar = Frame(left_frame, width=185, height=50)
tool_bar.grid(row=0, column=0, padx=20, pady=5)

English = {"S_Currency":"Select Currency",
           "Amount_Error":"----Please enter an amount----",
            "Change_Currency":"Convert",
            "sentence_1":"Amount  :",
            "sentence_2":"From Currency :",
            "sentence_3":"To Currency :",
            "sentence_4":"Total  :",
            "sentence_5":" Select Currency :"
            }
Thai    =   {"S_Currency":"เลือกสกุลเงิน",
            "Amount_Error":"----โปรดใส่จำนวนเงิน----",
            "Change_Currency":"แปลง",
            "sentence_1":"จำนวนเงิน  :",
            "sentence_2":"จากสกุลเงิน  :",
            "sentence_3":"เป็นสกุลเงิน  :",
            "sentence_4":"จำนวนเงินที่ได้  :"
            }

#ฟังก์ชั่นแปลภาษา
def set_language(lang_code):
    if lang_code == "en":
        translations = English
        vocabulary1.set("Select Currency")
        vocabulary2.set("Select Currency")
    elif lang_code == "th":
        translations = Thai
        vocabulary1.set("เลือกสกุลเงิน")
        vocabulary2.set("เลือกสกุลเงิน")
    else:
        raise ValueError("Unsupported language code")
    convert.config(text=translations["Change_Currency"])
    uname1.config(text=translations["sentence_1"])
    uname2.config(text=translations["sentence_2"])
    uname3.config(text=translations["sentence_3"])
    uname4.config(text=translations["sentence_4"])

#ฟังก์ชั่นให้พิมพ์เลขได้อย่างเดียว
def NumOnly(S):
    if S.isdigit():
        return True
    root.bell()
    return False

#แปลงเงินเรียลไทม์ API
def RealTimeCyrren():
    import requests # pip install requests  #นำข้อมูลจากเว็ป
    import json     
    url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"

    channel1.delete(0, tk.END) #ลบค่าที่ช่องแปลงเงิน

    currency_to_1 = Curreny_Code1.get()
    currency_to_2 = Curreny_Code2.get()
    amount        = channel.get()
  
    querystring = {"from":currency_to_1,"to": currency_to_2,"amount":amount }

    headers = {
	"X-RapidAPI-Key": "your_rapid_api_key",
	"X-RapidAPI-Host": "currency-converter18.p.rapidapi.com"
    }
    #ถ้าไม่ใส่จำนวนเงิน
    if (channel.get() == ""):
     tkinter.messagebox.showinfo("Error !!", "----โปรดใส่จำนวนเงิน----")
    #ถ้าไม่เลือกสกุลเงิน
    elif  (currency_to_1 == "เลือกสกุลเงิน" or currency_to_2== "เลือกสกุลเงิน"):
     tkinter.messagebox.showinfo("Error !!","----โปรดเลือกสกุลเงิน----.")

    else:
        response = requests.request("GET", url, headers=headers, params=querystring)
        data1 = json.loads(response.text) 
        converted_Amount = data1["result"]["convertedAmount"]
        format_money = "{:,.3f}".format(converted_Amount)
        channel1.config(state=NORMAL)
        channel1.delete(0, END)
        channel1.insert(0, str(format_money))
        channel1.config(state=DISABLED)
        
#เวลาเรียลไทม์
def localtim(uname6):
   import time
   time1 = time.localtime()
   a = time.strftime('%A %d %B %Y ', time1)
   uname6.config(text=str(a))
   uname6.after(0,localtim)

#สกุลเงินใน Txt
File = open('currency.txt',encoding="utf8")
currency_txt = File.read()

#ใส่ข้อความ
uname1 = Label(root,text = "จำนวนเงิน  :",font=('TH Sarabun New', 18, 'bold'),width=20,anchor=E,bg="#FFE4E1")
uname1.grid(row=1, column=0 ,pady=10)
uname2 = Label(root,text = "จากสกุลเงิน  :",font=('TH Sarabun New', 18, 'bold'),width=20,anchor=E,bg="#FFE4E1")
uname2.grid(row=2, column=0,pady=10)
uname3 = Label(root,text = "เป็นสกุลเงิน  :",font=('TH Sarabun New', 18, 'bold'),width=20,anchor=E,bg="#FFE4E1")
uname3.grid(row=3, column=0,pady=10)
uname4 = Label(root,text = "จำนวนเงินที่ได้  :",font=('TH Sarabun New', 18, 'bold'),width=20,anchor=E,bg="#FFE4E1")
uname4.grid(row=5, column=0,pady=10)

# #เว้นว่าง
uname5  = Label(root,text="\t",bg="#FFE4E1")
uname5.grid(row=7,  column=2,pady=10)

#โชว์วันที่กดใช้งาน
uname6 = Label(right_frame,width=21,anchor=E ,font=('TH Sarabun New', 16, 'bold'),bg="#FFE4E1")
uname6.grid(row=0,column=7, ipadx=2)
localtim(uname6)


#กล่องรับจำนวนเงินที่ต้องการแปลง
Number = (root.register(NumOnly), '%S')
channel  = Entry(root,font = 6, validate='key', vcmd = Number)
channel.grid(row=1,  column=1,padx=20)

#ช่องเงินที่แปลงแล้ว
channel1 = Entry(root,font = 6, state=DISABLED)
channel1.grid(row=5, column=1,padx=20)

#ใส่ข้อความสกุลเงิน
vocabulary1 = StringVar(root)
vocabulary1.set("เลือกสกุลเงิน")
vocabulary2 = StringVar(root)
vocabulary2.set("เลือกสกุลเงิน")

#ช่องเลือกสกุลเงิน  state="readonly"เลือกได้อย่างเดียวแก้ไขไม่ได้
Curreny_Code1 = ttk.Combobox(root, width = 18, textvariable = vocabulary1,state="readonly",font=1)
Curreny_Code1['values'] = (currency_txt)
Curreny_Code1.grid(row=2, column=1)
Curreny_Code1.current()
Curreny_Code2 = ttk.Combobox(root, width = 18, textvariable = vocabulary2,state="readonly",font=1)
Curreny_Code2['values'] = (currency_txt)
Curreny_Code2.grid(row=3, column=1)
Curreny_Code2.current()

#ใส่ปุ่มแปลงเงิน
Label(tool_bar, font=('Nueva Std Cond',10, 'bold'), text="Language").grid(row=0, column=0, padx=5, pady=5)
change = Button(tool_bar, font=('TH Sarabun New', 10, 'bold'), text=" ไทย ", bd=5, bg="#FFFF00", fg="black", relief=RAISED, cursor="hand2", width=5, height=1,
                command=lambda: set_language("th"))
change.grid(row=0, column=4, padx=5, pady=3, ipadx=10)

change = Button(tool_bar, font=('TH Sarabun New', 10, 'bold'), text=" English ", bd=5, bg="#FFFF00", fg="black", relief=RAISED, cursor="hand2", width=5, height=1,
                command=lambda: set_language("en"))
change.grid(row=0, column=5, padx=5, pady=3, ipadx=10)

convert = Button(root, font=('TH Sarabun New', 18, 'bold'), text="แปลง", bd=5, bg="#FFFF00", fg="black", relief=RAISED, cursor="hand2",
                command=RealTimeCyrren)
convert.grid(row=4, column=1, pady=10,ipadx=10 )

root.mainloop()
