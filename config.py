import customtkinter
import tkinter as tk
from tkinter import messagebox
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x300")

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)


def users():
    def add_user():
        adddetails_window = tk.Toplevel(rt)
        adddetails_window.title("Adicionar Usuário")
        adddetails_window.geometry("400x450")
        adddetails_window.configure(bg="#212121")

        def cancel():
            adddetails_window.destroy()

        def adicionar_user():
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                full_name TEXT,
                                username TEXT,
                                password TEXT,
                                role TEXT
                            )''')

                full_name = firstname.get()
                username = entry1.get()
                password = entry2.get()
                role = combo.get()

                cursor.execute('INSERT INTO users (full_name, username, password, role) VALUES (?, ?, ?, ?)',
                               (full_name, username, password, role))

                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Sucesso", "Usuário cadastrado com sucesso!")
                adddetails_window.destroy()
                update_user_list()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        label = customtkinter.CTkLabel(adddetails_window, width=300, height=40, font=("Roboto", 36),
                                       text="Adicionar Usuário")
        label.pack(pady=12, padx=10)

        firstname = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Nome Completo")
        firstname.pack(pady=12, padx=10)

        entry1 = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Usuário")
        entry1.pack(pady=12, padx=10)

        entry2 = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Senha", show="*")
        entry2.pack(pady=12, padx=10)

        combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40, values=["OPERADOR", "GERENTE"])
        combo.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CADASTRAR", command=adicionar_user)
        button.pack(pady=12, padx=24)

        button1 = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                          command=cancel)
        button1.pack(pady=12, padx=10)

    def update_user_list():
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT id, full_name, username, password, role FROM users")
            users = cursor.fetchall()

            listbox.delete(0, tk.END)  # Clear the current list

            for user in users:
                user_str = f"ID: {user[0]} - Nome: {user[1]} - Usuário: {user[2]} - Senha: {user[3]} - Permissão: {user[4]}"
                listbox.insert(tk.END, user_str)

            conn.close()

            # Unbind the previous event bindings
            listbox.unbind("<ButtonRelease-1>")

            # Bind a new event handler to open details for the clicked item
            listbox.bind("<ButtonRelease-1>", lambda event: open_users_details(listbox.get(listbox.curselection())))
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_users_details(selected_item):
        details_window = tk.Toplevel(rt)
        details_window.title("Users Detail")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")
        print(selected_item)
        # Get the selected entry details
        selected_id = selected_item.split(" - ")[0].split(": ")[1]
        print(selected_id)
        selected_full_name = selected_item.split(" - ")[1].split(": ")[1]
        print(selected_full_name)
        selected_username = selected_item.split(" - ")[2].split(": ")[1]
        print(selected_username)
        selected_password = selected_item.split(" - ")[3].split(": ")[1]
        print(selected_password)
        selected_role = selected_item.split(" - ")[4].split(": ")[1]
        print(selected_role)

        def cancel():
            details_window.destroy()

        def update_user():
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE users SET full_name=?, username=?, password=?, role=? WHERE id=?",
                    (firstname.get(), entry1.get(), entry2.get(), combo.get(), selected_id))
                messagebox.showinfo(
                    "Sucesso", "Usuário atualizado com sucesso!")
                details_window.destroy()
                update_user_list()

                conn.commit()
                conn.close()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                       text="Alterar Usuário")
        label.pack(pady=12, padx=10)

        firstname = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Nome Completo")
        firstname.pack(pady=12, padx=10)

        entry1 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Usuário")
        entry1.pack(pady=12, padx=10)

        entry2 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Senha", show="*")
        entry2.pack(pady=12, padx=10)

        combo = customtkinter.CTkComboBox(details_window, width=300, height=40, values=["OPERADOR", "GERENTE"])
        combo.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(details_window, width=300, height=40, text="CADASTRAR", command=update_user)
        button.pack(pady=12, padx=24)

        button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                          command=cancel)
        button1.pack(pady=12, padx=10)

        entry1.insert(0, selected_username)
        entry2.insert(0, selected_password)
        firstname.insert(0, selected_full_name)
        combo.set(selected_role)

    user_window = tk.Toplevel(rt)
    user_window.title("Lista de Usuários")
    user_window.geometry("600x450")
    user_window.configure(bg="#212121")

    button_add = customtkinter.CTkButton(
        user_window, width=240, height=32, text="ADICIONAR USUÁRIO", command=add_user)
    button_add.pack(pady=12, padx=10)

    listbox = tk.Listbox(user_window, width=300, height=200)
    listbox.pack(pady=12, padx=10)

    update_user_list()


def price():
    def insert_price():
        try:
            carencia_val = carencia_entry.get()
            primeira_faixa_val = primeira_faixa_entry.get()
            demais_faixas_val = demais_faixas_entry.get()
            primeira_faixa_min_val = primeira_faixa_min_entry.get()
            demais_faixas_min_val = demais_faixas_min_entry.get()
            print(carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val, demais_faixas_val)

            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS price (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                carencia TEXT,
                                primeira_faixa TEXT,
                                primeira_faixa_min TEXT,
                                demais_faixas TEXT,
                                demais_faixas_min TEXT
                            )''')

            cursor.execute("SELECT * FROM price LIMIT 1")
            row = cursor.fetchone()

            if row:
                cursor.execute(
                    "UPDATE price SET carencia=?, primeira_faixa=?, primeira_faixa_min=?,demais_faixas_min=?, demais_faixas=? WHERE id=?",
                    (carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val, demais_faixas_val,
                     row[0]))
                messagebox.showinfo(
                    "Sucesso", "Valores da tabela de preço atualizados com sucesso!")
                price_window.destroy()
            else:
                cursor.execute(
                    "INSERT INTO price (carencia, primeira_faixa,primeira_faixa_min,demais_faixas_min,  demais_faixas) VALUES (?, ?, ?, ? , ?)",
                    (
                        carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,
                        demais_faixas_val))
                messagebox.showinfo(
                    "Sucesso", "Valores inseridos na tabela de preço com sucesso!")
                price_window.destroy()

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print("aqui")
            print("SQLite error:", e)

    def populate_entries():
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM price LIMIT 1")
            row = cursor.fetchone()

            if row:
                carencia_entry.insert(0, row[1])
                primeira_faixa_entry.insert(0, row[2])
                primeira_faixa_min_entry.insert(0, row[3])
                demais_faixas_entry.insert(0, row[4])
                demais_faixas_min_entry.insert(0, row[5])

            conn.close()

        except sqlite3.Error as e:

            print("SQLite error:", e)

    price_window = tk.Toplevel(rt)
    price_window.title("Tabela de Preço")
    price_window.geometry("400x500")
    price_window.configure(bg="#212121")

    carencia_label = customtkinter.CTkLabel(
        price_window, width=240, height=1, text="Carência:")
    carencia_label.pack(pady=6, padx=10)

    carencia_entry = customtkinter.CTkEntry(price_window, width=240)
    carencia_entry.pack(pady=6, padx=10)

    primeira_faixa_min_label = customtkinter.CTkLabel(
        price_window, width=240, height=1, text="Tempo da Primeira Faixa(em minutos):")
    primeira_faixa_min_label.pack(pady=6, padx=10)

    primeira_faixa_min_entry = customtkinter.CTkEntry(price_window, width=240)
    primeira_faixa_min_entry.pack(pady=6, padx=10)

    primeira_faixa_label = customtkinter.CTkLabel(
        price_window, width=240, height=1, text="Valor da Primeira Faixa:")
    primeira_faixa_label.pack(pady=6, padx=10)

    primeira_faixa_entry = customtkinter.CTkEntry(price_window, width=240)
    primeira_faixa_entry.pack(pady=6, padx=10)

    demais_faixas_min_label = customtkinter.CTkLabel(
        price_window, width=240, height=1, text="Tempo das Demais Faixa(em minutos):")
    demais_faixas_min_label.pack(pady=6, padx=10)

    demais_faixas_min_entry = customtkinter.CTkEntry(price_window, width=240)
    demais_faixas_min_entry.pack(pady=6, padx=10)

    demais_faixas_label = customtkinter.CTkLabel(
        price_window, width=240, height=1, text="Valor das Demais Faixas:")
    demais_faixas_label.pack(pady=6, padx=10)

    demais_faixas_entry = customtkinter.CTkEntry(price_window, width=240)
    demais_faixas_entry.pack(pady=6, padx=10)

    insert_button = customtkinter.CTkButton(
        price_window, width=240, height=32, text="Inserir", command=insert_price)
    insert_button.pack(pady=12, padx=10)

    populate_entries()


def texts():
    def add_user():
        adddetails_window = tk.Toplevel(rt)
        adddetails_window.title("Adicionar Usuário")
        adddetails_window.geometry("400x450")
        adddetails_window.configure(bg="#212121")

        def cancel():
            adddetails_window.destroy()

        def adicionar_user():
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS texts (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   text TEXT,
                                   type TEXT
                               )''')

                text_value = text_entry.get()
                type_value = combo.get()

                cursor.execute('INSERT INTO texts (text, type) VALUES (?, ?)',
                               (text_value, type_value))

                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Sucesso", "Texto cadastrado com sucesso!")
                adddetails_window.destroy()
                update_user_list()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        label = customtkinter.CTkLabel(adddetails_window, width=300, height=40, font=("Roboto", 36),
                                       text="Adicionar Frase")
        label.pack(pady=12, padx=10)

        text_entry = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Texto")
        text_entry.pack(pady=12, padx=10)

        combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40, values=["TICKET", "RECIBO"])
        combo.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CADASTRAR",
                                         command=adicionar_user)
        button.pack(pady=12, padx=24)

        button1 = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                          command=cancel)
        button1.pack(pady=12, padx=10)

    def update_user_list():
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT id, text, type FROM texts")
            texts = cursor.fetchall()

            listbox.delete(0, tk.END)  # Clear the current list

            for text in texts:
                text_str = f"ID: {text[0]} - Text: {text[1]} - Type: {text[2]}"
                listbox.insert(tk.END, text_str)

            conn.close()

            # Unbind the previous event bindings
            listbox.unbind("<ButtonRelease-1>")

            # Bind a new event handler to open details for the clicked item
            listbox.bind("<ButtonRelease-1>", lambda event: open_texts_details(listbox.get(listbox.curselection())))
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_texts_details(selected_item):
        details_window = tk.Toplevel(rt)
        details_window.title("Texts Detail")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")
        print(selected_item)
        # Get the selected entry details
        selected_id = selected_item.split(" - ")[0].split(": ")[1]
        selected_text = selected_item.split(" - ")[1].split(": ")[1]
        selected_type = selected_item.split(" - ")[2].split(": ")[1]


        def cancel():
            details_window.destroy()

        def update_user():
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE texts SET text=?, type=? WHERE id=?",
                    (text.get(), combo.get(), selected_id))
                messagebox.showinfo(
                    "Sucesso", "Frase atualizada com sucesso!")
                details_window.destroy()
                update_user_list()

                conn.commit()
                conn.close()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                       text="Alterar Frase")
        label.pack(pady=12, padx=10)

        text = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Texto")
        text.pack(pady=12, padx=10)

        combo = customtkinter.CTkComboBox(details_window, width=300, height=40, values=["TICKET", "RECIBO"])
        combo.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(details_window, width=300, height=40, text="ATUALIZAR", command=update_user)
        button.pack(pady=12, padx=24)

        button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                          command=cancel)
        button1.pack(pady=12, padx=10)

        text.insert(0, selected_text)
        combo.set(selected_type)

    user_window = tk.Toplevel(rt)
    user_window.title("Lista de Frases")
    user_window.geometry("600x450")
    user_window.configure(bg="#212121")

    button_add = customtkinter.CTkButton(
        user_window, width=240, height=32, text="ADICIONAR FRASES", command=add_user)
    button_add.pack(pady=12, padx=10)

    listbox = tk.Listbox(user_window, width=300, height=200)
    listbox.pack(pady=12, padx=10)

    update_user_list()

button_users = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="USUÁRIOS", command=users)
button_users.pack(pady=12, padx=10)

button_price = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="TABELA DE PREÇO", command=price)
button_price.pack(pady=12, padx=10)

button_price = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="FRASES TICKET", command=texts)
button_price.pack(pady=12, padx=10)

rt.mainloop()
