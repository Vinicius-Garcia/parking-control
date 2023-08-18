import customtkinter
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para abrir a janela de lista de usuários
def add_user():
        print('aqui')


def users():
    user_window = tk.Toplevel(rt)
    user_window.title("Lista de Usuários")
    user_window.geometry("400x450")
    user_window.configure(bg="#212121")

    button_add = customtkinter.CTkButton(
    user_window, width=240, height=32, text="ADICIONAR USUÁRIO", command=add_user)
    button_add.pack(pady=12, padx=10)

    listbox = tk.Listbox(user_window, width=480, height=200)
    listbox.pack(pady=12, padx=10)

    user_list()

    def user_list():
     try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT placa, data FROM entry")
        entries = cursor.fetchall()
        
        listbox.delete(0, tk.END)  # Clear the current list
        
        for entry in entries:
            entry_str = f"Placa: {entry[0]} - Data: {entry[1]}"
            listbox.insert(tk.END, entry_str)
        
        conn.close()
        
        # Unbind the previous event bindings
        listbox.unbind("<ButtonRelease-1>")
        
        # Bind a new event handler to open details for the clicked item
        listbox.bind("<ButtonRelease-1>", lambda event: open_entry_details(listbox.get(listbox.curselection())))
    except sqlite3.Error as e:
        print("SQLite error:", e)

    






customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x600")

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

button_users = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="USUÁRIOS", command=users)
button_users.pack(pady=12, padx=10)


def price():
    def insert_price():
        try:
            carencia_val = carencia_entry.get()
            primeira_faixa_val = primeira_faixa_entry.get()
            demais_faixas_val = demais_faixas_entry.get()
            primeira_faixa_min_val = primeira_faixa_min_entry.get()
            demais_faixas_min_val = demais_faixas_min_entry.get()
            print(carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,  demais_faixas_val)

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
                cursor.execute("UPDATE price SET carencia=?, primeira_faixa=?, primeira_faixa_min=?,demais_faixas_min=?, demais_faixas=? WHERE id=?",
                               (carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,  demais_faixas_val, row[0]))
                messagebox.showinfo(
                    "Sucesso", "Valores da tabela de preço atualizados com sucesso!")
                price_window.destroy()    
            else:
                cursor.execute("INSERT INTO price (carencia, primeira_faixa,primeira_faixa_min,demais_faixas_min,  demais_faixas) VALUES (?, ?, ?, ? , ?)",
                               (carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,  demais_faixas_val))
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


# Botão para abrir a janela de tabela de preço
button_price = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="TABELA DE PREÇO", command=price)
button_price.pack(pady=12, padx=10)

# Iniciar o loop principal do Tkinter
rt.mainloop()
