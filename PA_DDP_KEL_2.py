import csv
import os
from prettytable import PrettyTable
import pwinput
from datetime import datetime

USERS_FILE = "users.csv"
SERVICES_FILE = "layanan.csv"
RIWAYAT_MEDIS_FILE = "riwayat_medis.csv"

def initialize_data():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "role", "full_name", "age", "address", "phone", "e_money"])
            writer.writerow(["admin", "admin123", "admin", "Administrator", "", "", "", "0"])
    
    if not os.path.exists(SERVICES_FILE):
        with open(SERVICES_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "price", "availability"])
            initial_services = [
                ["1", "Konsultasi Umum", "150000", "True"],
                ["2", "Pemeriksaan Gigi", "200000", "True"],
                ["3", "Tes Laboratorium", "500000", "True"],
                ["4", "Vaksinasi", "300000", "True"],
                ["5", "Medical Check-up", "750000", "True"]
            ]
            writer.writerows(initial_services)
    
    if not os.path.exists(RIWAYAT_MEDIS_FILE):
        with open(RIWAYAT_MEDIS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "username", "patient_name", "service_id", "service_name", "price", "symptoms", "status", "balance_before", "balance_after"])

def load_data():
    users = {}
    layanans = {}
    riwayat_medis = []
    
    with open(USERS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"],
                "full_name": row["full_name"],
                "age": row["age"],
                "address": row["address"],
                "phone": row["phone"],
                "e_money": int(row.get("e_money", 0))
            }
    
    with open(SERVICES_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            layanans[row["id"]] = {
                "name": row["name"],
                "price": int(row["price"]),
                "availability": row["availability"].lower() == "true"
            }
    
    with open(RIWAYAT_MEDIS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        riwayat_medis = [
            {
                "date": row["date"],
                "username": row["username"],
                "patient_name": row["patient_name"],
                "service_id": row["service_id"],
                "service_name": row["service_name"],
                "price": int(row["price"]),
                "symptoms": row["symptoms"],
                "status": row["status"],
                "balance_before": int(row.get("balance_before", 0)),
                "balance_after": int(row.get("balance_after", 0))
            }
            for row in reader
        ]
    
    return users, layanans, riwayat_medis

def save_data(users, layanans, riwayat_medis):
    with open(USERS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "role", "full_name", "age", "address", "phone", "e_money"])
        for username, data in users.items():
            writer.writerow([
                username,
                data["password"],
                data["role"],
                data["full_name"],
                data["age"],
                data["address"],
                data["phone"],
                data["e_money"]
            ])
    
    with open(SERVICES_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "price", "availability"])
        for layanan_id, data in layanans.items():
            writer.writerow([
                layanan_id,
                data["name"],
                data["price"],
                str(data["availability"])
            ])
    
    with open(RIWAYAT_MEDIS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "username", "patient_name", "service_id", "service_name", "price", "symptoms", "status", "balance_before", "balance_after"])
        for record in riwayat_medis:
            writer.writerow([
                record["date"],
                record["username"],
                record["patient_name"],
                record["service_id"],
                record["service_name"],
                record["price"],
                record["symptoms"],
                record["status"],
                record.get("balance_before", 0),
                record.get("balance_after", 0)
            ])

def register(users):
    global layanans, riwayat_medis
    print("\n=== Register Pasien Baru ===")
    while True:
        username = input("Masukkan username (3-20 karakter, alfanumerik): ")
        if not username.isalnum() or not (3 <= len(username) <= 20):
            print("Username harus alfanumerik dan 3-20 karakter!")
            continue
        if username in users:
            print("Username sudah terdaftar!")
            continue
        break

    password = pwinput.pwinput(prompt="Masukkan password: ")
    full_name = input("Nama Lengkap: ")
    while True:
        age = input("Usia (angka): ")
        if not age.isdigit():
            print("Usia harus angka!")
            continue
        age = int(age)
        break
    address = input("Alamat: ")
    while True:
        phone = input("No. Telepon (maks 15 digit): ")
        if not phone.isdigit() or len(phone) > 15:
            print("No. Telepon harus angka dan maksimal 15 digit!")
            continue
        break

    while True:
        try:
            initial_balance = int(input("Saldo awal E-Money (Rp): "))
            if initial_balance < 0:
                print("Saldo awal tidak boleh negatif!")
                continue
            break
        except ValueError:
            print("Masukkan angka yang valid!")

    users[username] = {
        "password": password,
        "role": "patient",
        "full_name": full_name,
        "age": age,
        "address": address,
        "phone": phone,
        "e_money": initial_balance
    }
    save_data(users, layanans, riwayat_medis)
    print("Registrasi berhasil!")
    return username

def login(users):
    print("\n=== Login ===")
    username = input("Masukkan username: ")
    password = pwinput.pwinput(prompt="Masukkan password: ")
    
    if username in users and users[username]["password"] == password:
        print(f"Selamat datang, {users[username].get('full_name', username)}!")
        return username
    else:
        print("Username atau password salah!")
        return None

def display_layanans(layanans):
    if not layanans:
        print("Tidak ada layanan tersedia.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Nama Layanan", "Biaya", "Status"]
    for sid, layanan in layanans.items():
        status = "Tersedia" if layanan["availability"] else "Tidak Tersedia"
        table.add_row([sid, layanan["name"], f"Rp {layanan['price']:,}", status])
    print("\n=== Daftar Layanan Klinik ===")
    print(table)

def add_service(layanans):
    global users, riwayat_medis
    print("\n=== Tambah Layanan Baru ===")
    name = input("Nama layanan: ")
    while True:
        try:
            price = int(input("Biaya layanan (Rp): "))
            break
        except ValueError:
            print("Masukkan angka yang valid!")
    
    sid = str(max(map(int, layanans.keys())) + 1) if layanans else "1"
    layanans[sid] = {
        "name": name,
        "price": price,
        "availability": True
    }
    save_data(users, layanans, riwayat_medis)
    print("Layanan berhasil ditambahkan!")

def edit_service(layanans):
    global users, riwayat_medis
    display_layanans(layanans)
    sid = input("\nMasukkan ID layanan yang akan diedit: ")
    if sid not in layanans:
        print("Layanan tidak ditemukan!")
        return
    
    print(f"\nMengedit {layanans[sid]['name']}")
    name = input("Nama layanan baru (Enter untuk tidak mengubah): ")
    price_str = input("Biaya baru (Enter untuk tidak mengubah): ")
    avail_str = input("Status (1: Tersedia, 0: Tidak Tersedia, Enter untuk tidak mengubah): ")
    
    if name:
        layanans[sid]["name"] = name
    if price_str:
        try:
            layanans[sid]["price"] = int(price_str)
        except ValueError:
            print("Biaya tidak valid! Menggunakan biaya lama.")
    if avail_str in ['0', '1']:
        layanans[sid]["availability"] = bool(int(avail_str))
    
    save_data(users, layanans, riwayat_medis)
    print("Layanan berhasil diperbarui!")

def delete_service(layanans):
    global users, riwayat_medis
    display_layanans(layanans)
    sid = input("\nMasukkan ID layanan yang akan dihapus: ")
    if sid not in layanans:
        print("Layanan tidak ditemukan!")
        return
    
    confirm = input(f"Anda yakin ingin menghapus layanan {layanans[sid]['name']}? (y/n): ")
    if confirm.lower() == 'y':
        del layanans[sid]
        save_data(users, layanans, riwayat_medis)
        print("Layanan berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")

def book_service(username, layanans, riwayat_medis):
    global users
    display_layanans(layanans)
    sid = input("\nMasukkan ID layanan yang diinginkan: ")
    if sid not in layanans:
        print("Layanan tidak ditemukan!")
        return

    service = layanans[sid]
    if not service["availability"]:
        print("Layanan tidak tersedia saat ini!")
        return

    print(f"\nBiaya layanan: Rp {service['price']:,}")
    print(f"Saldo E-money Anda: Rp {users[username]['e_money']:,}")
    symptoms = input("Keluhan/Gejala: ")
    confirm = input("Konfirmasi pemesanan? (y/n): ")

    if confirm.lower() == 'y':
        if users[username]["e_money"] >= service["price"]:
            users[username]["e_money"] -= service["price"]
            status = "Selesai"
            print("Transaksi berhasil!")
        else:
            print("Saldo E-money tidak cukup!")
            return

        balance_before = users[username]["e_money"] + service["price"]
        balance_after = users[username]["e_money"]

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "patient_name": users[username]["full_name"],
            "service_id": sid,
            "service_name": service["name"],
            "price": service["price"],
            "symptoms": symptoms,
            "status": status,
            "balance_before": balance_before,
            "balance_after": balance_after
        }
        riwayat_medis.append(record)
        save_data(users, layanans, riwayat_medis)

        # Display invoice
        print("\n" + "="*50)
        print("               INVOICE PEMBAYARAN")
        print("="*50)
        print(f"Tanggal: {record['date']}")
        print(f"Pasien: {record['patient_name']}")
        print(f"Layanan: {record['service_name']}")
        print(f"Biaya: Rp {record['price']:,}")
        print(f"Saldo E-money sebelum: Rp {users[username]['e_money'] + service['price']:,}")
        print(f"Dibayar: Rp {service['price']:,}")
        print(f"Saldo E-money setelah: Rp {users[username]['e_money']:,}")
        print("="*50)
        print("Terima kasih telah menggunakan layanan kami!")
        print("="*50)

def view_invoices(username, riwayat_medis):
    filtered_records = [r for r in riwayat_medis if r["username"] == username and r["status"] == "Selesai"]

    if not filtered_records:
        print("Tidak ada invoice yang tersedia.")
        return

    print("\n=== Daftar Invoice ===")
    for i, r in enumerate(filtered_records, 1):
        print(f"\n{i}. Tanggal: {r['date']} - Layanan: {r['service_name']} - Biaya: Rp {r['price']:,}")

    choice = input("\nMasukkan nomor invoice yang ingin dilihat (atau Enter untuk kembali): ")
    if choice == "":
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(filtered_records):
            record = filtered_records[idx]
            print("\n" + "="*50)
            print("               INVOICE PEMBAYARAN")
            print("="*50)
            print(f"Tanggal: {record['date']}")
            print(f"Pasien: {record['patient_name']}")
            print(f"Layanan: {record['service_name']}")
            print(f"Biaya: Rp {record['price']:,}")
            print(f"Saldo E-money sebelum: Rp {record['balance_before']:,}")
            print(f"Dibayar: Rp {record['price']:,}")
            print(f"Saldo E-money setelah: Rp {record['balance_after']:,}")
            print("="*50)
            print("Terima kasih telah menggunakan layanan kami!")
            print("="*50)
        else:
            print("Nomor invoice tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")

def top_up_balance(username, users):
    global layanans, riwayat_medis
    print("\n=== Top Up E-Money ===")
    print(f"Saldo E-money Anda saat ini: Rp {users[username]['e_money']:,}")
    while True:
        try:
            amount = int(input("Masukkan jumlah top up (Rp): "))
            if amount <= 0:
                print("Jumlah harus positif!")
                continue
            if amount > 5000000:
                print("Top up maksimal 5 juta!")
                continue
            break
        except ValueError:
            print("Masukkan angka yang valid!")

    users[username]["e_money"] += amount
    save_data(users, layanans, riwayat_medis)
    print(f"Top up berhasil! Saldo E-money Anda sekarang: Rp {users[username]['e_money']:,}")

def view_medical_records(username, riwayat_medis, is_admin=False):
    table = PrettyTable()
    table.field_names = ["Tanggal", "Pasien", "Layanan", "Keluhan", "Biaya", "Status"]
    
    filtered_records = riwayat_medis if is_admin else [r for r in riwayat_medis if r["username"] == username]
    
    if not filtered_records:
        print("Tidak ada riwayat medis.")
        return
    
    for r in filtered_records:
        table.add_row([
            r["date"],
            r["patient_name"],
            r["service_name"],
            r["symptoms"],
            f"Rp {r['price']:,}",
            r["status"]
        ])
    
    print("\n=== Riwayat Medis ===")
    print(table)

def update_record_status(riwayat_medis):
    global users, layanans
    if not riwayat_medis:
        print("Tidak ada riwayat medis untuk diperbarui.")
        return

    print("\n=== Daftar Riwayat Medis ===")
    for i, r in enumerate(riwayat_medis, 1):
        print(f"{i}. Tanggal: {r['date']} - Pasien: {r['patient_name']} - Layanan: {r['service_name']} - Status: {r['status']}")

    while True:
        try:
            choice = int(input("\nMasukkan nomor record yang ingin diperbarui (atau 0 untuk kembali): "))
            if choice == 0:
                return
            if 1 <= choice <= len(riwayat_medis):
                record = riwayat_medis[choice - 1]
                break
            else:
                print("Nomor record tidak valid! Masukkan angka antara 1 dan", len(riwayat_medis))
        except ValueError:
            print("Input harus berupa angka! Silakan coba lagi.")

    print("\nStatus saat ini:", record["status"])
    new_status = input("Status baru (Selesai/Batal/Menunggu): ")

    if new_status in ["Selesai", "Batal", "Menunggu"]:
        record["status"] = new_status
        save_data(users, layanans, riwayat_medis)
        print("Status berhasil diperbarui!")
    else:
        print("Status tidak valid!")

def admin_menu(username):
    global layanans, riwayat_medis, users
    try:
        while True:
            print("\n=== Menu Admin ===")
            print("1. Lihat Daftar Layanan")
            print("2. Tambah Layanan")
            print("3. Edit Layanan")
            print("4. Hapus Layanan")
            print("5. Lihat Semua Riwayat Medis")
            print("6. Update Status Pemeriksaan")
            print("7. Logout")
            
            choice = input("Pilihan Anda: ")
            
            if choice == "1":
                display_layanans(layanans)
            elif choice == "2":
                add_service(layanans)
            elif choice == "3":
                edit_service(layanans)
            elif choice == "4":
                delete_service(layanans)
            elif choice == "5":
                view_medical_records(username, riwayat_medis, True)
            elif choice == "6":
                update_record_status(riwayat_medis)
            elif choice == "7":
                print("Logging out...")
                break
            else:
                print("Pilihan tidak valid!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
        exit(0)
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")
        print("Program akan keluar.")
        exit(1)

def patient_menu(username):
    global layanans, riwayat_medis, users
    try:
        while True:
            print("\n=== Menu Pasien ===")
            print("1. Lihat Daftar Layanan")
            print("2. Pesan Layanan")
            print("3. Lihat Riwayat Medis")
            print("4. Lihat Invoice")
            print("5. Top Up E-Money")
            print("6. Logout")

            choice = input("Pilihan Anda: ")

            if choice == "1":
                display_layanans(layanans)
            elif choice == "2":
                book_service(username, layanans, riwayat_medis)
            elif choice == "3":
                view_medical_records(username, riwayat_medis)
            elif choice == "4":
                view_invoices(username, riwayat_medis)
            elif choice == "5":
                top_up_balance(username, users)
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Pilihan tidak valid!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
        exit(0)
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")
        print("Program akan keluar.")
        exit(1)

if __name__ == "__main__":
    initialize_data()
    users, layanans, riwayat_medis = load_data()
    
    while True:
        print("\n=== Sistem Administrasi Klinik ===")
        print("1. Login")
        print("2. Registrasi Pasien Baru")
        print("3. Keluar")
        
        choice = input("Pilihan Anda: ")
        
        if choice == "1":
            username = login(users)
            if username:
                if users[username]["role"] == "admin":
                    admin_menu(username)
                else:
                    patient_menu(username)
        elif choice == "2":
            register(users)
        elif choice == "3":
            print("Terima kasih telah menggunakan sistem kami!")
            break
        else:
            print("Pilihan tidak valid!")
