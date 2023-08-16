import customtkinter
import os
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x450")

def add_to_database():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')

    full_name = firstname.get()
    username = entry1.get()
    password = entry2.get()
    role = combo.get()

    cursor.execute('INSERT INTO users (full_name, username, password, role) VALUES (?, ?, ?, ?)',
                   (full_name, username, password, role))

    conn.commit()
    conn.close()

def reg():
    add_to_database()
    switch_to_login_screen()

def switch_to_login_screen():
    rt.destroy()
    os.system("python login.py")

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=30, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=2, text="Register System")
label.pack(pady=12, padx=10)

firstname = customtkinter.CTkEntry(master=fr, width=240, height=2, placeholder_text="Full name")
firstname.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=fr, width=240, height=2, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=fr, width=240, height=2, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

combo = customtkinter.CTkComboBox(master=fr, width=240, height=2, values=["OPERADOR", "GERENTE"])
combo.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=240, height=2, text="Register", command=reg)
button.pack(pady=12, padx=10)


rt.mainloop()
