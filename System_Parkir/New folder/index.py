#file index.py
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox,filedialog
import sqlite3
import datetime
import time
import database
from datetime import datetime, timedelta
import os
from subprocess import call
import csv


app=customtkinter.CTk()
app.title("Halaman Utama Sistem parkir")

lebarapp = 900
tinggiapp = 420
lebarlayar = app.winfo_screenwidth()
tinggilayar = app.winfo_screenheight()
posisiatas = int(tinggilayar/2 - tinggiapp/2)
posisikanan = int((lebarlayar/2) - (lebarapp/2) + 90 )

app.geometry(f'{lebarapp}x{tinggiapp}+{posisikanan}+{posisiatas}')
app.config(bg='#001220')
app.focus

app.resizable(False, False)

font1 =('Arial',18,'bold')
font2 =('Arial',15,'bold')
font3 =('Arial',12,'bold')

def buka_arsip_kendaraan():
    try:
        app.destroy()
        os.system('python arsip_kendaraan.py')
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi untuk menampilkan isi dokumen kelompok.txt
def tampilkan_dokumen_kelompok():
    try:
        # Memeriksa apakah file "kelompok.txt" ada dalam direktori yang sama
        file_path = "kelompok.txt"
        try:
            with open(file_path, 'r') as file:
                isi_dokumen = file.read()

            # Membuat jendela baru untuk menampilkan isi dokumen
            popup = tk.Toplevel()
            popup.title("Isi Dokumen Kelompok")

            # Widget Text untuk menampilkan isi dokumen
            text_widget = tk.Text(popup, wrap="word", width=60, height=20)
            text_widget.insert("1.0", isi_dokumen)
            text_widget.config(state="disabled")
            text_widget.pack(padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File 'kelompok.txt' tidak ditemukan.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")


# ... (fungsi dan definisi lainnya)
def logout():
    messagebox.showinfo('Succes', 'Berhasil Keluar.')
    app.destroy()
    os.system('python loginkaryawan.py')
    #call(["python", "loginkaryawan.py"])
    return TRUE
# Menambahkan menu bar
menu_bar = Menu(app)
app.config(menu=menu_bar)

# Menu "File"
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu Halaman", menu=file_menu)
file_menu.add_command(label="Arsip Kendaraan", command=buka_arsip_kendaraan)
file_menu.add_separator()
file_menu.add_command(label="Logout", command=logout)

# Menu "About"
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Kelompok", command=tampilkan_dokumen_kelompok)


#fungsi untuk mengupdate treeview pada kendaraan
def updatekendaraan():
    kendaraans = database.fetch_kendaraan()
    listkendaraan.delete(*listkendaraan.get_children())
    for kendaraann in kendaraans:
        listkendaraan.insert('', END, values=kendaraann)

#fungsi untuk memasukan data kendaraan
def masukan():
    dataplatnomor = entry_platnomor.get()
    datajeniskendaraan = pkendaraan.get()
    datawaktumasuk = iwaktu.get()
    if not (dataplatnomor and datajeniskendaraan and datawaktumasuk):
        messagebox.showerror('Error','Masukan semua data.')
    elif database.plat_exist(dataplatnomor):
        messagebox.showerror('Error','Kendaraan ini sudah masuk')
    else :
        database.insert_kendaraan(dataplatnomor,datajeniskendaraan,datawaktumasuk)
        updatekendaraan()
        clear()
        messagebox.showinfo('Succes', 'Kendaraan berhasil dimasukan')


def masukan():
    # Mendapatkan input pengguna dari entry_platnomor
    dataplatnomor = entry_platnomor.get()

    # Menghilangkan spasi dari plat nomor
    dataplatnomor = dataplatnomor.replace(" ", "")

    # Memeriksa apakah data yang dimasukkan sesuai dengan ketentuan
    if not (dataplatnomor and pkendaraan.get() and iwaktu.get()):
        messagebox.showerror('Error', 'Masukkan semua data.')
    elif database.plat_exist(dataplatnomor):
        messagebox.showerror('Error', 'Kendaraan ini sudah masuk')
    else:
        database.insert_kendaraan(dataplatnomor, pkendaraan.get(), iwaktu.get())
        updatekendaraan()
        clear()
        messagebox.showinfo('Success', 'Kendaraan berhasil dimasukkan')



#fungsi untuk membersihkan kolom entry
def clear(*klik):
    if klik:
        listkendaraan.selection_remove(listkendaraan.focus())
    entry_platnomor.delete(0, END)
    pkendaraan.set('')
    iwaktu.set('')

#fungsi untuk menghitung biaya parkir
def hitung_biaya_parkir(waktu_masuk, waktu_keluar, tarif_pertama_motor, tarif_perjam_selanjutnya_motor, tarif_pertama_mobil, tarif_perjam_selanjutnya_mobil):
    
    kendaraan_dipilih = listkendaraan.focus()

    waktu_masuk = datetime.strptime(waktu_masuk, '%H:%M:%S')
    waktu_keluar = datetime.strptime(waktu_keluar, '%H:%M:%S')
    jenis_kendaraan = listkendaraan.item(kendaraan_dipilih)['values'][1]

    durasi_parkir = waktu_keluar - waktu_masuk

    total_jam = int(durasi_parkir.total_seconds() // 3600)

    total_jam = max(1, total_jam)

    # Menghitung biaya parkir
    if jenis_kendaraan == "Motor":
        biaya_pertama = tarif_pertama_motor
        biaya_selanjutnya = tarif_perjam_selanjutnya_motor
    elif jenis_kendaraan == "Mobil":
        biaya_pertama = tarif_pertama_mobil
        biaya_selanjutnya = tarif_perjam_selanjutnya_mobil
    
    biaya_parkir = biaya_pertama + biaya_selanjutnya * (total_jam - 1)
    return int(biaya_parkir)

#fungsi untuk mengeluarkan kendaraan
def keluarkan():
    kendaraan_dipilih = listkendaraan.focus()
    if not kendaraan_dipilih:
        messagebox.showerror('Error', 'Pilih kendaraan untuk dikeluarkan.')
    else:
        dataplatnomor = listkendaraan.item(kendaraan_dipilih)['values'][0]
        jenis_kendaraan = listkendaraan.item(kendaraan_dipilih)['values'][1]
        waktu_masuk = listkendaraan.item(kendaraan_dipilih)['values'][2]
        waktu_keluar = iwaktu.get()
        
        #tarif kendaraan
        tarif_pertama_motor = 2000
        tarif_perjam_selanjutnya_motor = 1000
        tarif_pertama_mobil = 5000
        tarif_perjam_selanjutnya_mobil = 2000

        biaya = hitung_biaya_parkir(waktu_masuk, waktu_keluar, tarif_pertama_motor, tarif_perjam_selanjutnya_motor, tarif_pertama_mobil, tarif_perjam_selanjutnya_mobil)

        with open('arsip_kendaraan.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dataplatnomor, jenis_kendaraan, waktu_masuk, waktu_keluar, biaya])
        
        nama_file = f"{jenis_kendaraan}_{dataplatnomor}.txt"

        with open(nama_file, "w") as f:
            f.write(f"========= Nota Parkir =========\n\n")
            f.write(f"Plat Nomor: {dataplatnomor}\n")
            f.write(f"Jenis Kendaraan: {jenis_kendaraan}\n")
            f.write(f"Waktu Masuk: {waktu_masuk}\n")
            f.write(f"Waktu Keluar: {waktu_keluar}\n")
            f.write(f"-------------------------------\n")
            f.write(f"Biaya Parkir: Rp.{biaya},00")

        database.keluarkan_kendaraan(dataplatnomor)
        updatekendaraan()
        clear()
        messagebox.showinfo('Success', f'Kendaraan dengan plat nomor {dataplatnomor} berhasil dikeluarkan pada pukul {waktu_keluar} \nBiaya parkir : Rp.{biaya},00 \nNota telah dicetak! File disimpan sebagai: {nama_file}')

# Fungsi untuk mencari data plat nomor
def cari_data_plat_nomor():
    dataplatnomor = entry_cariplat.get()
    if not dataplatnomor:
        messagebox.showerror('Error', 'Masukkan plat nomor untuk pencarian.')
    else:
        data_kendaraan = database.cari_kendaraan(dataplatnomor)
        if data_kendaraan:
            for item in listkendaraan.get_children():
                if listkendaraan.item(item, 'values')[0] == dataplatnomor:
                    listkendaraan.selection_set(item)
                    listkendaraan.focus(item)
                    break
        else:
            messagebox.showerror('Info', f'Data kendaraan dengan plat nomor {dataplatnomor} tidak ditemukan.')

#fungsi untuk logout


edit_popup = None 

platnomor = customtkinter.CTkLabel(app, font=font1, text='Plat Nomor', text_color='#fff',bg_color='#001220')
platnomor.place(x=20, y=20)
entry_platnomor = customtkinter.CTkEntry(app, font=font2,text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text_color='#a3a3a3', width=180)
entry_platnomor.place(x=180, y=20)

jeniskendaraan = customtkinter.CTkLabel(app, font=font1, text='Jenis Kendaraan', text_color='#fff', bg_color='#001220')
jeniskendaraan.place(x=20, y=60)
pilihankendaraan = ['Motor', 'Mobil']
pkendaraan = StringVar()
entry_jeniskendaraan = customtkinter.CTkComboBox(app, font=font2, text_color='#fff', fg_color='#001A2E',bg_color='#121111', dropdown_hover_color='#004780', button_color='#004780',border_color='#004780', button_hover_color='#004780', width=180, variable=pkendaraan, values=pilihankendaraan, state='readonly')
entry_jeniskendaraan.place(x= 180, y=60)

waktumasuk = customtkinter.CTkLabel(app, font=font1, text='Waktu Masuk', text_color='#fff', bg_color='#001220')
waktumasuk.place(x=20, y=100)
inpwaktu = []
iwaktu = StringVar()
entry_waktumasuk = customtkinter.CTkComboBox(app, font=font2, text_color='#fff', fg_color='#001A2E', bg_color='#121111', dropdown_hover_color='#004780', button_color='#004780', border_color='#004780', button_hover_color='#004780', width=180, variable=iwaktu, values=inpwaktu, state='readonly')
def times():
    entry_waktumasuk.set(time.strftime("%H:%M:%S"))
    entry_waktumasuk.after(2, times)
times()
entry_waktumasuk.place(x= 180, y=100)

def edit_data():
    # Mendapatkan data kendaraan yang dipilih
    kendaraan_dipilih = listkendaraan.focus()
    
    if not kendaraan_dipilih:
        messagebox.showerror('Error', 'Pilih kendaraan untuk diedit.')
        return
    
    # Mendapatkan data saat ini
    plat_nomor_sekarang = listkendaraan.item(kendaraan_dipilih)['values'][0]
    jenis_kendaraan_sekarang = listkendaraan.item(kendaraan_dipilih)['values'][1]
    waktu_masuk_sekarang = listkendaraan.item(kendaraan_dipilih)['values'][2]
    
    # Membuat jendela pop-up untuk mengedit data
    global edit_popup
    edit_popup = tk.Toplevel()
    edit_popup.title("Edit Data Kendaraan")
    
    # Label dan Entry untuk plat nomor baru
    label_plat_nomor = tk.Label(edit_popup, text="Plat Nomor Baru:")
    label_plat_nomor.grid(row=0, column=0, padx=10, pady=10)
    
    entry_plat_nomor_baru = ttk.Entry(edit_popup)
    entry_plat_nomor_baru.grid(row=0, column=1, padx=10, pady=10)
    entry_plat_nomor_baru.insert(0, plat_nomor_sekarang)
    
    # Label dan Combobox untuk jenis kendaraan baru
    label_jenis_kendaraan = tk.Label(edit_popup, text="Jenis Kendaraan Baru:")
    label_jenis_kendaraan.grid(row=1, column=0, padx=10, pady=10)
    
    pilihan_kendaraan = ['Motor', 'Mobil']
    jenis_kendaraan_baru = ttk.Combobox(edit_popup, values=pilihan_kendaraan)
    jenis_kendaraan_baru.grid(row=1, column=1, padx=10, pady=10)
    jenis_kendaraan_baru.set(jenis_kendaraan_sekarang)
    
    # Tombol untuk menyimpan perubahan
    tombol_simpan = ttk.Button(edit_popup, text="Simpan", command=lambda: simpan_perubahan(plat_nomor_sekarang, jenis_kendaraan_sekarang, waktu_masuk_sekarang, entry_plat_nomor_baru.get(), jenis_kendaraan_baru.get()))
    tombol_simpan.grid(row=2, column=0, columnspan=2, pady=10)

def simpan_perubahan(plat_nomor_lama, jenis_kendaraan_lama, waktu_masuk_lama, plat_nomor_baru, jenis_kendaraan_baru):
    if not (plat_nomor_baru and jenis_kendaraan_baru):
        messagebox.showerror('Error', 'Masukkan data yang valid.')
        return
    messagebox.showinfo('Success', 'Kendaraan berhasil diedit')
    
    # Memanggil fungsi dari database atau sumber data lainnya untuk menyimpan perubahan
    # (Anda perlu mengganti ini dengan cara yang sesuai dengan implementasi Anda)
    database.update_kendaraan(plat_nomor_lama, jenis_kendaraan_lama, waktu_masuk_lama, plat_nomor_baru, jenis_kendaraan_baru)
    
    # Menutup jendela pop-up
    edit_popup.destroy()
    
    updatekendaraan()

# Menambahkan tombol untuk memulai proses edit
tombol_edit = customtkinter.CTkButton(app, command=edit_data, font=font1, text_color='#fff', text='Edit Data', fg_color='#FFD700', hover_color='#FFA500', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombol_edit.place(x=20, y=330)


tombolmasuk = customtkinter.CTkButton(app, command=masukan, font=font1, text_color='#fff', text='Kendaraan Masuk', fg_color='#05A312', hover_color='#00850B', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombolmasuk.place(x=20, y=150)

tombolkeluar = customtkinter.CTkButton(app, command=keluarkan, font=font1, text_color='#fff', text='Kendaraan Keluar', fg_color='#E40404', hover_color='#AE0000', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombolkeluar.place(x=20, y=185)

label_cari = customtkinter.CTkLabel(app, font=font1, text='Cari Plat Nomor', text_color='#fff', bg_color='#001220')
label_cari.place(x=20, y=245)

entry_cariplat = customtkinter.CTkEntry(app, font=font2,text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text_color='#a3a3a3', width=180)
entry_cariplat.place(x=180, y=245)

tombol_cari = customtkinter.CTkButton(app, command=cari_data_plat_nomor, font=font1, text_color='#fff', text='Cari Plat Nomor', fg_color='#054CAE', hover_color='#033582', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombol_cari.place(x=20, y=295)


style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837', rowheight=27)
style.map('Treeview', background=[('selected', '#ff3625')])

listkendaraan = ttk.Treeview(app,height=20)
listkendaraan['columns'] = ('Plat Nomor', 'Jenis Kendaraan', 'Waktu Masuk')

listkendaraan.column('#0', width=0, stretch=tk.NO)
listkendaraan.column('Plat Nomor', anchor=tk.CENTER, width=250)
listkendaraan.column('Jenis Kendaraan', anchor=tk.CENTER, width=250)
listkendaraan.column('Waktu Masuk', anchor=tk.CENTER, width=250)

listkendaraan.heading('Plat Nomor', text='Plat Nomor Kendaraan')
listkendaraan.heading('Jenis Kendaraan', text='Jenis Kendaraan')
listkendaraan.heading('Waktu Masuk', text='Waktu Masuk')

listkendaraan.place(x=570, y=30)

updatekendaraan()

app.mainloop()
