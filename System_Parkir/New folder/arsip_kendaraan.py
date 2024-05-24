import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import csv

app = customtkinter.CTk()
app.title("Arsip Kendaraan keluar")

lebarapp = 1240
tinggiapp = 420
lebarlayar = app.winfo_screenwidth()
tinggilayar = app.winfo_screenheight()
posisiatas = int(tinggilayar / 2 - tinggiapp / 2)
posisikanan = int((lebarlayar / 2) - (lebarapp / 2) + 90)

app.geometry(f'{lebarapp}x{tinggiapp}+{posisikanan}+{posisiatas}')
app.config(bg='#001220')
app.focus

app.resizable(TRUE, TRUE)

font1 = ('Arial', 18, 'bold')
font2 = ('Arial', 15, 'bold')
font3 = ('Arial', 12, 'bold')

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837', rowheight=27)
style.map('Treeview', background=[('selected', '#ff3625')])

def buka_index():
    try:
        app.destroy()
        os.system('python index.py')
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

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
file_menu.add_command(label="Home", command=buka_index)
file_menu.add_separator()
file_menu.add_command(label="Logout", command=logout)

# Menu "About"
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Kelompok", command=tampilkan_dokumen_kelompok)

listkendaraan = ttk.Treeview(app, height=20)
listkendaraan['columns'] = ('Plat Nomor', 'Jenis Kendaraan', 'Waktu Masuk', 'Waktu Keluar', 'Biaya')

listkendaraan.column('#0', width=0, stretch=tk.NO)
listkendaraan.column('Plat Nomor', anchor=tk.CENTER, width=250)
listkendaraan.column('Jenis Kendaraan', anchor=tk.CENTER, width=250)
listkendaraan.column('Waktu Masuk', anchor=tk.CENTER, width=250)
listkendaraan.column('Waktu Keluar', anchor=tk.CENTER, width=250)
listkendaraan.column('Biaya', anchor=tk.CENTER, width=250)

listkendaraan.heading('Plat Nomor', text='Plat Nomor Kendaraan')
listkendaraan.heading('Jenis Kendaraan', text='Jenis Kendaraan')
listkendaraan.heading('Waktu Masuk', text='Waktu Masuk')
listkendaraan.heading('Waktu Keluar', text='Waktu Keluar')
listkendaraan.heading('Biaya', text='Biaya')

def tampilkan_data():
    try:
        with open('arsip_kendaraan.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            for row in reader:
                listkendaraan.insert("", "end", values=row)
    except FileNotFoundError:
        tk.messagebox.showinfo("Info", "File arsip_kendaraan.csv tidak ditemukan.")

tampilkan_data()
listkendaraan.place(x=570, y=30)

label_cari = customtkinter.CTkLabel(app, font=font1, text='Cari Plat Nomor', text_color='#fff', bg_color='#001220')
label_cari.place(x=20, y=25)

entry_cariplat = customtkinter.CTkEntry(app, font=font2,text_color='#fff', fg_color='#001A2E', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text_color='#a3a3a3', width=180)
entry_cariplat.place(x=180, y=25)

def search_data():
    query = entry_cariplat.get().lower()
    listkendaraan.delete(*listkendaraan.get_children())  # Clear existing data

    try:
        with open('arsip_kendaraan.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            for row in reader:
                if query in row[0].lower():  # Check if the query is in the 'Plat Nomor' column
                    listkendaraan.insert("", "end", values=row)
    except FileNotFoundError:
        tk.messagebox.showinfo("Info", "File arsip_kendaraan.csv tidak ditemukan.")


def cetak_ulang_nota():
    selected_item = listkendaraan.selection()
    if selected_item:
        item = listkendaraan.item(selected_item, "values")
        dataplatnomor = item[0]
        jenis_kendaraan = item[1]
        waktu_masuk = item[2]
        waktu_keluar = item[3]
        biaya = item[4]

        nama_file = f"{jenis_kendaraan}_{dataplatnomor}.txt"

        with open(nama_file, "w") as f:
            f.write("========= Nota Parkir =========\n\n")
            f.write(f"Plat Nomor: {dataplatnomor}\n")
            f.write(f"Jenis Kendaraan: {jenis_kendaraan}\n")
            f.write(f"Waktu Masuk: {waktu_masuk}\n")
            f.write(f"Waktu Keluar: {waktu_keluar}\n")
            f.write("-------------------------------\n")
            f.write(f"Biaya Parkir: Rp.{biaya},00")

        messagebox.showinfo("Info", f"Nota berhasil dicetak ulang: {nama_file}")
    else:
        messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu untuk mencetak ulang nota.")

def hapus_kendaraan():
    selected_item = listkendaraan.selection()
    if selected_item:
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data kendaraan ini?")
        if confirmation:
            listkendaraan.delete(selected_item)
            # You may want to add additional logic to remove the data from your file or database
            messagebox.showinfo("Info", "Data kendaraan berhasil dihapus.")
    else:
        messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu untuk menghapus kendaraan.")



tombol_cari = customtkinter.CTkButton(app, command=search_data, font=font1, text_color='#fff', text='Cari Plat Nomor', fg_color='#054CAE', hover_color='#033582', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombol_cari.place(x=20, y=70)

tombol_cetak_ulang_nota = customtkinter.CTkButton(app, command=cetak_ulang_nota, font=font1, text_color='#fff', text='Cetak Ulang Nota', fg_color='yellow', hover_color='#033582', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombol_cetak_ulang_nota.place(x=20, y=110)

tombol_hapus_kendaraan = customtkinter.CTkButton(app, command=hapus_kendaraan, font=font1, text_color='#fff', text='Hapus Kendaraan', fg_color='red', hover_color='#033582', bg_color='#001220', cursor='hand2', corner_radius=15, width=345)
tombol_hapus_kendaraan.place(x=20, y=149)




app.mainloop()
