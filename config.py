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

            cursor.execute("SELECT full_name, username, password, role FROM users")
            users = cursor.fetchall()
            tree.delete(*tree.get_children())
            for user in users:
                tree.insert('', tk.END, values=(user[0], user[1], user[2], user[3]))

            conn.close()

            # Unbind the previous event bindings
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_users_details(event):
        selected_item = tree.selection()[0]  # Get the selected item's ID
        selected_entry = tree.item(selected_item, "values")
        details_window = tk.Toplevel(rt)
        details_window.title("Users Detail")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")
        print(selected_item)
        # Get the selected entry details
        selected_full_name = selected_entry[0]
        print(selected_full_name)
        selected_username = selected_entry[1]
        print(selected_username)
        selected_password = selected_entry[2]
        print(selected_password)
        selected_role =selected_entry[3]
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

    tree = tk.ttk.Treeview(user_window,
                           columns=("Nome", "Usuário", "Senha", "Permissão"))
    tree['show'] = 'headings'
    tree.heading("#1", text="Nome")
    tree.heading("#2", text="Usuário")
    tree.heading("#3", text="Senha")
    tree.heading("#4", text="Permissão")

    # Set column widths
    tree.column("#1", width=100)
    tree.column("#2", width=150)
    tree.column("#3", width=100)
    tree.column("#4", width=100)

    treeScroll = tk.Scrollbar(user_window)
    treeScroll.configure(command=tree.yview)
    tree.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side='right', fill='y',padx=(0, 10), pady=10)  # Change side to 'right' and fill to 'y'
    tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)

    # Call the function to update the Listbox with existing entries
    update_user_list()

    tree.bind("<Double-1>", open_users_details)


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

            cursor.execute("SELECT  text, type,id FROM texts")
            texts = cursor.fetchall()

            tree.delete(*tree.get_children())
            for text in texts:

                tree.insert('', tk.END, values=(text[0], text[1], text[2]))

            conn.close()


        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_texts_details(selected_item):
        selected_item = tree.selection()[0]  # Get the selected item's ID
        selected_entry = tree.item(selected_item, "values")
        details_window = tk.Toplevel(rt)
        details_window.title("Texts Detail")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")
        print(selected_item)
        # Get the selected entry details
        selected_text = selected_entry[0]
        selected_type = selected_entry[1]
        selected_id = selected_entry[2]


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

    tree = tk.ttk.Treeview(user_window,
                           columns=("TEXTO", "TIPO"))
    tree['show'] = 'headings'
    tree.heading("#1", text="TEXTO")
    tree.heading("#2", text="TIPO")

    # Set column widths
    tree.column("#1", width=400)
    tree.column("#2", width=150)

    treeScroll = tk.Scrollbar(user_window)
    treeScroll.configure(command=tree.yview)
    tree.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
    tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
    treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

    # Call the function to update the Listbox with existing entries
    update_user_list()

    tree.bind("<Double-1>", open_texts_details)



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
