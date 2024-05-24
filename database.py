import sqlite3

def create_table():
    try:
        # Membuat koneksi
        konek = sqlite3.connect('dataparkir.db')
        cursor = konek.cursor()

        # Membuat tabel 'kendaraan'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kendaraan (
                dataplatnomor TEXT PRIMARY KEY,
                datajeniskendaraan TEXT,
                datawaktumasuk TEXT
            )
        ''')

        # Membuat tabel 'arsip_kendaraan'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arsip_kendaraan (
                platnomor TEXT PRIMARY KEY,
                datajeniskendaraan TEXT,
                datawaktumasuk TEXT,
                datawaktukeluar TEXT,
                biaya INTEGER
            )
        ''')

        # Melakukan commit dan menutup koneksi
        konek.commit()
    finally:
        # Menutup koneksi setelah operasi selesai
        if konek:
            konek.close()


def create_arsip_table():
    conn = sqlite3.connect('dataparkir.db')  
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arsip_kendaraan (
            platnomor TEXT PRIMARY KEY,
            datajeniskendaraan TEXT,
            datawaktumasuk TEXT,
            datawaktukeluar TEXT,
            biaya INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def masukan_kearsip(dataplatnomor, datajeniskendaraan, datawaktumasuk, datawaktukeluar,biaya):
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('INSERT INTO arsip_kendaraan (dataplatnomor, datajeniskendaraan, datawaktumasuk, datawaktukeluar, biaya) VALUES (?,?,?,?,?)',
                   (dataplatnomor,datajeniskendaraan,datawaktumasuk,datawaktukeluar,biaya))
    konek.commit()
    konek.close
def fetch_arsipkendaraan():
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('SELECT * FROM arsip_kendaraan')
    kendaraan = cursor.fetchall()
    konek.close()
    return kendaraan

def fetch_kendaraan():
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('SELECT * FROM kendaraan')
    kendaraan = cursor.fetchall()
    konek.close()
    return kendaraan

def insert_kendaraan(dataplatnomor,datajeniskendaraan,datawaktumasuk):
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('INSERT INTO kendaraan (dataplatnomor, datajeniskendaraan, datawaktumasuk) VALUES (?,?,?)',
                   (dataplatnomor,datajeniskendaraan,datawaktumasuk))
    konek.commit()
    konek.close

def update_kendaraan(plat_nomor_lama, jenis_kendaraan_lama, waktu_masuk_lama, plat_nomor_baru, jenis_kendaraan_baru):
    try:
        connection = sqlite3.connect('dataparkir.db')
        cursor = connection.cursor()

        # Check if the existing data with given plat_nomor exists
        cursor.execute('SELECT * FROM kendaraan WHERE dataplatnomor = ?', (plat_nomor_lama,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Update the data with new values
            cursor.execute('UPDATE kendaraan SET dataplatnomor=?, datajeniskendaraan=?, datawaktumasuk=? WHERE dataplatnomor=?',
                           (plat_nomor_baru, jenis_kendaraan_baru, waktu_masuk_lama, plat_nomor_lama))
            connection.commit()
            print(f"Data for platnomor {plat_nomor_lama} updated successfully.")
        else:
            print(f"Data for platnomor {plat_nomor_lama} not found.")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        if connection:
            connection.close()

# def update_kendaraan(dataplatnomor, new_dataplatnomor, new_datajeniskendaraan):
#     try:
#         connection = sqlite3.connect('dataparkir.db')
#         cursor = connection.cursor()

#         # Check if the existing data with given platnomor exists
#         cursor.execute('SELECT * FROM kendaraan WHERE dataplatnomor = ?', (dataplatnomor,))
#         existing_data = cursor.fetchone()

#         if existing_data:
#             # Update the data with new values
#             cursor.execute('UPDATE kendaraan SET dataplatnomor=?, datajeniskendaraan=? WHERE dataplatnomor=?',
#                            (new_dataplatnomor, new_datajeniskendaraan, dataplatnomor))
#             connection.commit()
#             print(f"Data for platnomor {dataplatnomor} updated successfully.")
#         else:
#             print(f"Data for platnomor {dataplatnomor} not found.")

#     except sqlite3.Error as e:
#         print("Error:", e)

#     finally:
#         if connection:
#             connection.close()

def keluarkan_kendaraan(dataplatnomor):
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('DELETE FROM kendaraan WHERE dataplatnomor = ?', (dataplatnomor,))
    konek.commit()
    konek.close()


def plat_exist(dataplatnomor):
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('SELECT COUNT(*) FROM kendaraan where dataplatnomor = ?', (dataplatnomor,))
    result = cursor.fetchone()
    konek.close()
    return result[0] > 0

def cari_kendaraan(dataplatnomor):
    konek = sqlite3.connect('dataparkir.db')
    cursor = konek.cursor()
    cursor.execute('SELECT * FROM kendaraan WHERE dataplatnomor = ?', (dataplatnomor,))
    data_kendaraan = cursor.fetchone()
    konek.close()
    return data_kendaraan

def get_kendaraan_keluar():
    try:
        connection = sqlite3.connect("nama_database.db")
        cursor = connection.cursor()

        # Gantilah "nama_tabel" dengan nama tabel sesuai dengan struktur database Anda
        query = "SELECT plat_nomor, jenis_kendaraan, waktu_masuk, waktu_keluar, biaya_parkir FROM nama_tabel WHERE waktu_keluar IS NOT NULL"

        cursor.execute(query)
        data_kendaraan_keluar = cursor.fetchall()

        return data_kendaraan_keluar

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        if connection:
            connection.close()
            
create_table()


