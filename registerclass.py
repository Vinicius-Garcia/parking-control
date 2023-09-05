import customtkinter
import os
import sqlite3
from tkinter import messagebox


class UserRegistrationApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()

    def setup_ui(self):

        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        # Criar a tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')

        # Verificar se existe um usuário com o papel "gerente"
        cursor.execute("SELECT * FROM users WHERE role = 'GERENTE'")
        self.existe_gerente = cursor.fetchone() is not None
        print(self.existe_gerente)
        # Fechar a conexão com o banco de dados
        conn.close()
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=30, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=480, height=40, font=("Roboto", 36), text="Cadastrar Usuário")
        label.pack(pady=(200, 20), padx=10)

        self.firstname = customtkinter.CTkEntry(master=fr, width=480, height=40, placeholder_text="Nome Completo")
        self.firstname.pack(pady=12, padx=10)

        self.entry1 = customtkinter.CTkEntry(master=fr, width=480, height=40, placeholder_text="Usuário")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=fr, width=480, height=40, placeholder_text="Senha", show="*")
        self.entry2.pack(pady=12, padx=10)

        if self.existe_gerente:
            self.combo = customtkinter.CTkComboBox(master=fr, width=480, height=40, values=["OPERADOR"])
        else:
            self.combo = customtkinter.CTkComboBox(master=fr, width=480, height=40, values=["OPERADOR", "GERENTE"])

        self.combo.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=fr, width=480, height=40, text="CADASTRAR", command=self.reg)
        button.pack(pady=12, padx=24)

        button1 = customtkinter.CTkButton(master=fr, width=480, height=40, text="CANCELAR", fg_color='#91403d',
                                          command=self.switch_to_login_screen)
        button1.pack(pady=12, padx=10)

    def add_to_database(self):
        full_name = self.firstname.get()
        username = self.entry1.get()
        password = self.entry2.get()
        role = self.combo.get()

        # Check for empty fields
        if not full_name or not username or not password or not role:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
            return

        # Check for duplicate username
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

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_username = cursor.fetchone()

        if existing_username:
            conn.close()
            messagebox.showwarning("Erro", "O nome de usuário já está em uso.")
            return



        cursor.execute('INSERT INTO users (full_name, username, password, role) VALUES (?, ?, ?, ?)',
                       (full_name, username, password, role))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.destroy()

    def reg(self):
        self.add_to_database()


    def switch_to_login_screen(self):
        self.destroy()


    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = UserRegistrationApp()
    app.run()
