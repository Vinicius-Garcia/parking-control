import customtkinter
import os
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x450")

def add_to_database():
    conn = sqlite3.connect("user_data.db")  # Cria ou conecta-se ao banco de dados
    cursor = conn.cursor()

    # Crie a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            password TEXT
        )
    ''')

    # Insira os dados do registro na tabela
    full_name = firstname.get()
    username = entry1.get()
    password = entry2.get()

    cursor.execute('INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)',
                   (full_name, username, password))

    conn.commit()  # Salva as alterações
    conn.close()   # Fecha a conexão com o banco de dados

def reg():
    add_to_database()
    switch_to_login_screen()

def switch_to_login_screen():
    rt.destroy()  # Fecha a janela de registro
    os.system("python login.py")  # Abre a janela de login

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=30, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="Register System", text_font=("Roboto", 24))
label.pack(pady=12, padx=10)

firstname = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Full name")
firstname.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=240, height=32, text="Register", command=reg)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=fr, text="Remember me")
checkbox.pack(pady=12, padx=10)

rt.mainloop()
