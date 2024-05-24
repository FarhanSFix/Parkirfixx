import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from subprocess import call
import os

app = customtkinter.CTk()
app.title('Login Karyawan')

lebarapp = 450
tinggiapp = 360
lebarlayar = app.winfo_screenwidth()
tinggilayar = app.winfo_screenheight()
posisiatas = int(tinggilayar/2 - tinggiapp/2)
posisikanan = int((lebarlayar/2) - (lebarapp/2) + 195 )

app.geometry(f'{lebarapp}x{tinggiapp}+{posisikanan}+{posisiatas}')
app.config(bg='#906126')
app.resizable(False,False)

font1= ('Helvetica',25,'bold')
font2= ('Arial',17,'bold')
font3= ('Arial',13,'bold')
font2= ('Arial',13,'bold','underline')
        
konek = sqlite3.connect('dataparkir.db')
cursor = konek.cursor()

cursor.execute ('''
               CREATE TABLE IF NOT EXISTS karyawan (
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')

frame = customtkinter.CTkFrame(app, bg_color='#906126', fg_color='#906126', width=470,height=360)
frame.place(x=0,y=0)

gambar = PhotoImage(file="loginfix.png")
gambar_label = Label(frame,image=gambar,bg='#906126')
gambar_label.place(x=5,y=70)

login_label = customtkinter.CTkLabel(frame, font=font1, text='LOGIN KARYAWAN', text_color='#121111',bg_color='#906126')
login_label.place(x=110, y=20)

username_entry = customtkinter.CTkEntry(frame, font=font2,text_color='#fff', fg_color='#001A2E', bg_color='#906126', border_color='#004780', border_width=3, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
username_entry.place(x=240, y=100)

password_entry = customtkinter.CTkEntry(frame, font=font2,show='*',text_color='#fff', fg_color='#001A2E', bg_color='#906126', border_color='#004780', border_width=3, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
password_entry.place(x=240, y=170)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM karyawan WHERE username = ?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Succes', 'Berhasil Masuk')
                app.destroy()
                os.system('python index.py')
                return TRUE
            else:
                messagebox.showerror('Error', 'Password Salah!')
        else:
            messagebox.showerror('Error', 'Username tidak terdaftar')
    else:
        messagebox.showerror('Error', 'Masukan data')

login_button = customtkinter.CTkButton(frame,command=login, text_color='#fff', text='LOGIN', fg_color='#004780', hover_color='#002090', bg_color='#906126', cursor='hand2', corner_radius=15, width=120)
login_button.place(x=280, y=250)

def tambahkaryawan():
    username = username_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM karyawan WHERE username = ?', [username])
        result = cursor.fetchone()
        if result:
            if username == 'admin':
                app.destroy()
                os.system('python inputkaryawan.py')
                return True
            else:
                messagebox.showerror('Error', 'Anda tidak punya akses')
        else:
            messagebox.showerror('Error', 'password atau username tidak valid')
    else:
        messagebox.showerror('Error', 'Anda tidak punya akses')

tambahkaryawan_button = customtkinter.CTkButton(frame,command=tambahkaryawan, text_color='#fff', text='Tambah Karyawan', fg_color='#004780', hover_color='#002090', bg_color='#906126', cursor='hand2', corner_radius=15, width=120)
tambahkaryawan_button.place(x=270, y=290)

app.mainloop()