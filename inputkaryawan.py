import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox

app = customtkinter.CTk()
app.title('Login Karyawan')
lebarapp = 600
tinggiapp = 540
lebarlayar = app.winfo_screenwidth()
tinggilayar = app.winfo_screenheight()
posisiatas = int(tinggilayar/2 - tinggiapp/2)
posisikanan = int((lebarlayar/2) - (lebarapp/2) + 195)

app.geometry(f'{lebarapp}x{tinggiapp}+{posisikanan}+{posisiatas}')
app.config(bg='#001220')
app.resizable(True, True)

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font2_underline = ('Arial', 13, 'bold', 'underline')

konek = sqlite3.connect('dataparkir.db')
cursor = konek.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS karyawan (
               username TEXT NOT NULL,
               alamat TEXT,
               password TEXT NOT NULL,
               nomortelepon INT NOT NULL
               )''')

frame = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=600, height=500)
frame.place(x=0, y=0)

login_label = customtkinter.CTkLabel(frame, font=font1, text='MASUKAN KARYAWAN', text_color='#fff', bg_color='#001220')
login_label.place(x=180, y=30)

global username_entry, alamat_entry, password_entry, confirm_password_entry

username_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
username_entry.place(x=220, y=90)

alamat_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Alamat', placeholder_text_color='#a3a3a3', width=200, height=50)
alamat_entry.place(x=220, y=170)

nomortelepon_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Nomor Telepon', placeholder_text_color='#a3a3a3', width=200, height=50)
nomortelepon_entry.place(x=220, y=250)

password_entry = customtkinter.CTkEntry(frame, font=font2, show='*', text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
password_entry.place(x=220, y=330)

confirm_password_entry = customtkinter.CTkEntry(frame, font=font2, show='*', text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Confirm Password', placeholder_text_color='#a3a3a3', width=200, height=50)
confirm_password_entry.place(x=220, y=410)

def masukankaryawan():
    username = username_entry.get()
    alamat = alamat_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    nomortelepon = nomortelepon_entry.get()

    if username != '' and alamat != '' and password != '':
        if password == confirm_password:
            cursor.execute('SELECT username FROM karyawan WHERE username = ?', [username])
            if cursor.fetchone() is not None:
                messagebox.showerror('Error', 'Username sudah ada.')
            else:
                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                cursor.execute('INSERT INTO karyawan VALUES (?, ?, ?, ?)', [username,alamat, nomortelepon, hashed_password ])
                konek.commit()
                messagebox.showinfo('Succes', 'Karyawan berhasil dimasukan.')
        else:
            messagebox.showerror('Error', 'Password tidak cocok.')
    else:
        messagebox.showerror('Error', 'Masukan data')

login_button = customtkinter.CTkButton(frame, command=masukankaryawan, text_color='#fff', text='Masukan', fg_color='#004780', hover_color='#002090', bg_color='#121111', cursor='hand2', corner_radius=5, width=120)
login_button.place(x=160, y=473)

def close_application():
    app.destroy()

close_button = customtkinter.CTkButton(frame, command=close_application, text_color='#fff', text='Close', fg_color='#004780', hover_color='#002090', bg_color='#121111', cursor='hand2', corner_radius=5, width=120)
close_button.place(x=340, y=473)

app.mainloop()