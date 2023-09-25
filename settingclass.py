import customtkinter
import tkinter as tk
from tkinter import messagebox
import sqlite3

from emails import Emails
from prices import Prices

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()


class Settings(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()
        self.mainloop()

    def setup_ui(self):


        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)


        label = customtkinter.CTkLabel(master=fr, text="CONFIGURAÇÕES", font=("Roboto", 32))
        label.pack(padx=(10, 10), pady=20, )

        button_users = customtkinter.CTkButton(
            master=fr, width=480, height=48, text="USUÁRIOS", command=self.users)
        button_users.pack(pady=12, padx=10)

        button_price = customtkinter.CTkButton(
            master=fr, width=480, height=48, text="TABELA DE PREÇO", command=self.price)
        button_price.pack(pady=12, padx=10)

        button_price = customtkinter.CTkButton(
            master=fr, width=480, height=48, text="FRASES TICKET", command=self.texts)
        button_price.pack(pady=12, padx=10)
        button_email = customtkinter.CTkButton(
            master=fr, width=480, height=48, text="EMAIL", command=self.emails)
        button_email.pack(pady=12, padx=10)


    def users(self):
            def add_user():
                adddetails_window = tk.Toplevel(self)
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
                        cursor.close()

                        messagebox.showinfo(
                            "Sucesso", "Usuário cadastrado com sucesso!")
                        adddetails_window.destroy()
                        update_user_list()

                    except sqlite3.Error as e:
                        print("SQLite error:", e)

                label = customtkinter.CTkLabel(adddetails_window, width=300, height=40, font=("Roboto", 36),
                                               text="Adicionar Usuário")
                label.pack(pady=12, padx=10)

                firstname = customtkinter.CTkEntry(adddetails_window, width=300, height=40,
                                                   placeholder_text="Nome Completo")
                firstname.pack(pady=12, padx=10)

                entry1 = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Usuário")
                entry1.pack(pady=12, padx=10)

                entry2 = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Senha",
                                                show="*")
                entry2.pack(pady=12, padx=10)

                combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40,
                                                  values=["OPERADOR", "GERENTE"])
                combo.pack(pady=12, padx=10)

                button = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CADASTRAR",
                                                 command=adicionar_user)
                button.pack(pady=12, padx=24)

                button1 = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CANCELAR",
                                                  fg_color='#91403d',
                                                  command=cancel)
                button1.pack(pady=12, padx=10)

            def update_user_list():
                try:
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT full_name, username, password, role, id FROM users")
                    users = cursor.fetchall()
                    cursor.close()
                    tree.delete(*tree.get_children())
                    for user in users:
                        tree.insert('', tk.END, values=(user[0], user[1], user[2], user[3], user[4]))


                except sqlite3.Error as e:
                    print("SQLite error:", e)

            def open_users_details(event):
                selected_item = tree.selection()[0]
                selected_entry = tree.item(selected_item, "values")
                details_window = tk.Toplevel(self)
                details_window.title("Users Detail")
                details_window.geometry("400x520")
                details_window.configure(bg="#212121")
                selected_full_name = selected_entry[0]
                selected_username = selected_entry[1]
                selected_password = selected_entry[2]
                selected_role = selected_entry[3]
                selected_id = selected_entry[4]

                def cancel():
                    details_window.destroy()

                def update_user():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE users SET full_name=?, username=?, password=?, role=? WHERE id=?",
                            (firstname.get(), entry1.get(), entry2.get(), combo.get(), selected_id))
                        conn.commit()
                        cursor.close()
                        messagebox.showinfo(
                            "Sucesso", "Usuário atualizado com sucesso!")
                        details_window.destroy()
                        update_user_list()


                    except sqlite3.Error as e:
                        print("SQLite error:", e)

                def remove_user():
                    selected_item = tree.selection()[0]
                    if selected_item:
                        confirmation = messagebox.askyesno("Confirmar Remoção",
                                                           "Tem certeza de que deseja remover este usuário?")
                        if confirmation:
                            conn = sqlite3.connect('user_data.db')
                            cursor = conn.cursor()
                            selected_entry = tree.item(selected_item, "values")
                            selected_id = selected_entry[4]
                            cursor.execute("DELETE FROM users WHERE id=?", (selected_id,))
                            conn.commit()
                            cursor.close()
                            update_user_list()
                            details_window.destroy()

                label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                               text="Alterar Usuário")
                label.pack(pady=12, padx=10)

                firstname = customtkinter.CTkEntry(details_window, width=300, height=40,
                                                   placeholder_text="Nome Completo")
                firstname.pack(pady=12, padx=10)

                entry1 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Usuário")
                entry1.pack(pady=12, padx=10)

                entry2 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Senha",
                                                show="*")
                entry2.pack(pady=12, padx=10)

                combo = customtkinter.CTkComboBox(details_window, width=300, height=40, values=["OPERADOR", "GERENTE"])
                combo.pack(pady=12, padx=10)

                button = customtkinter.CTkButton(details_window, width=300, height=40, text="CADASTRAR",
                                                 command=update_user)
                button.pack(pady=12, padx=24)

                button_remove_user = customtkinter.CTkButton(
                    details_window, width=300, height=40, text="REMOVER USUÁRIO",fg_color='#91403d', command=remove_user)
                button_remove_user.pack(pady=12, padx=10)
                button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR",
                                                  fg_color='#a2a2a2',
                                                  command=cancel)
                button1.pack(pady=12, padx=10)

                entry1.insert(0, selected_username)
                entry2.insert(0, selected_password)
                firstname.insert(0, selected_full_name)
                combo.set(selected_role)

            user_window = tk.Toplevel(self)
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
            treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)
            tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)

            update_user_list()

            tree.bind("<Double-1>", open_users_details)

    def emails(self):
        Emails()

    def price(self):
        Prices()
    def texts(self):
            def add_texts():
                adddetails_window = tk.Toplevel(self)
                adddetails_window.title("Adicionar Frases")
                adddetails_window.geometry("400x450")
                adddetails_window.configure(bg="#212121")

                def cancel():
                    adddetails_window.destroy()

                def adicionar_text():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        cursor.execute('''CREATE TABLE IF NOT EXISTS texts (
                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              text TEXT,
                                              type TEXT,
                                              ordem TEXT
                                          )''')

                        text_value = text_entry.get()
                        type_value = combo.get()
                        order_value = order_entry.get()

                        cursor.execute('INSERT INTO texts (text, type, ordem) VALUES (?, ?, ?)',
                                       (text_value, type_value, order_value))
                        conn.commit()
                        cursor.close()
                        messagebox.showinfo(
                            "Sucesso", "Texto cadastrado com sucesso!")
                        adddetails_window.destroy()
                        update_text_list()

                    except sqlite3.Error as e:
                        print("SQLite error:", e)

                label = customtkinter.CTkLabel(adddetails_window, width=300, height=40, font=("Roboto", 36),
                                               text="Adicionar Frase")
                label.pack(pady=12, padx=10)

                text_entry = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Texto")
                text_entry.pack(pady=12, padx=10)

                combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40,
                                                  values=["PADRÃO SUPERIOR", "TICKET INFERIOR", "RECIBO INFERIOR"])
                combo.pack(pady=12, padx=10)

                order_entry = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="ORDEM")
                order_entry.pack(pady=12, padx=10)

                button = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CADASTRAR",
                                                 command=adicionar_text)
                button.pack(pady=12, padx=24)

                button1 = customtkinter.CTkButton(adddetails_window, width=300, height=40, text="CANCELAR",
                                                  fg_color='#91403d',
                                                  command=cancel)
                button1.pack(pady=12, padx=10)

            def update_text_list():
                try:
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT  text, type, ordem, id FROM texts")
                    texts = cursor.fetchall()
                    cursor.close()
                    tree.delete(*tree.get_children())
                    for text in texts:
                        tree.insert('', tk.END, values=(text[0], text[1], text[2], text[3]))




                except sqlite3.Error as e:
                    print("SQLite error:", e)

            def open_texts_details(selected_item):
                selected_item = tree.selection()[0]  # Get the selected item's ID
                selected_entry = tree.item(selected_item, "values")
                details_window = tk.Toplevel(self)
                details_window.title("Texts Detail")
                details_window.geometry("400x520")
                details_window.configure(bg="#212121")
                # Get the selected entry details
                selected_text = selected_entry[0]
                selected_type = selected_entry[1]
                selected_id = selected_entry[3]
                selected_order = selected_entry[2]

                def cancel():
                    details_window.destroy()

                def update_user():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE texts SET text=?, type=?, ordem=? WHERE id=?",
                            (text.get(), combo.get(), selected_id, order_entry.get()))
                        conn.commit()
                        cursor.close()
                        messagebox.showinfo(
                            "Sucesso", "Frase atualizada com sucesso!")
                        details_window.destroy()
                        update_text_list()


                    except sqlite3.Error as e:
                        print("SQLite error:", e)

                def remove_text():
                    selected_item = tree.selection()[0]
                    if selected_item:
                        confirmation = messagebox.askyesno("Confirmar Remoção",
                                                           "Tem certeza de que deseja remover esta frase?")
                        if confirmation:
                            conn = sqlite3.connect('user_data.db')
                            cursor = conn.cursor()
                            selected_entry = tree.item(selected_item, "values")
                            selected_id = selected_entry[3]
                            cursor.execute("DELETE FROM texts WHERE id=?", (selected_id,))
                            conn.commit()
                            cursor.close()
                            update_text_list()
                            details_window.destroy()
                label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                               text="Alterar Frase")
                label.pack(pady=12, padx=10)

                text = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Texto")
                text.pack(pady=12, padx=10)

                combo = customtkinter.CTkComboBox(details_window, width=300, height=40,
                                                  values=["PADRÃO SUPERIOR", "TICKET INFERIOR", "RECIBO INFERIOR"])
                combo.pack(pady=12, padx=10)

                order_entry = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="ORDEM")
                order_entry.pack(pady=12, padx=10)

                button = customtkinter.CTkButton(details_window, width=300, height=40, text="ATUALIZAR",
                                                 command=update_user)
                button.pack(pady=12, padx=24)

                button_remove_text = customtkinter.CTkButton(
                    details_window, width=300, height=40, text="REMOVER FRASE", fg_color='#91403d' ,command=remove_text)
                button_remove_text.pack(pady=12, padx=10)

                button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR",
                                                  fg_color='#a2a2a2',
                                                  command=cancel)


                button1.pack(pady=12, padx=10)

                text.insert(0, selected_text)
                order_entry.insert(0, selected_order)
                combo.set(selected_type)

            user_window = tk.Toplevel(self)
            user_window.title("Lista de Frases")
            user_window.geometry("600x450")
            user_window.configure(bg="#212121")

            button_add = customtkinter.CTkButton(
                user_window, width=240, height=32, text="ADICIONAR FRASES", command=add_texts)
            button_add.pack(pady=12, padx=10)

            tree = tk.ttk.Treeview(user_window,
                                   columns=("TEXTO", "TIPO", "ORDEM"))
            tree['show'] = 'headings'
            tree.heading("#1", text="TEXTO")
            tree.heading("#2", text="TIPO")
            tree.heading("#3", text="ORDEM")

            # Set column widths
            tree.column("#1", width=300)
            tree.column("#2", width=150)
            tree.column("#3", width=50)

            treeScroll = tk.Scrollbar(user_window)
            treeScroll.configure(command=tree.yview)
            tree.configure(yscrollcommand=treeScroll.set)
            treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
            tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
            treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

            update_text_list()

            tree.bind("<Double-1>", open_texts_details)



if __name__ == "__main__":
    app = Settings()