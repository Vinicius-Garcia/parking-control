import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import locale
import math


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.after(0, lambda:rt.state('zoomed'))


def open_entry_details(selected_item):
    selected_item = tree.selection()[0]
    selected_entry = tree.item(selected_item, "values")
    details_window = tk.Toplevel(rt)
    details_window.title("Entry Details")
    details_window.geometry("400x450")
    details_window.configure(bg="#212121")

    placa = selected_entry[0]
    data = selected_entry[1]
    selected_entry = placa
    selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

    # Calculate the time difference
    current_time = datetime.now()
    time_difference = current_time - selected_time
    print("Time Difference:", time_difference)
    # Calculate hours, minutes, and seconds
    total_seconds = int(time_difference.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the selected time in Brazilian Portuguese (pt-br) format
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    formatted_time = selected_time.strftime('%d/%m/%Y %H:%M:%S')

    details_frame = tk.Frame(details_window, bg="#212121")
    details_frame.pack(pady=20, padx=10, fill="both", expand=True)

    details_label = customtkinter.CTkLabel(
        details_frame, width=120, height=1, text="TICKET", font=("Roboto", 24))
    details_label.pack(pady=6, padx=10)

    details_label = customtkinter.CTkLabel(
        details_frame, width=120, height=1, text=f"Placa: {selected_entry}", font=("Roboto", 16), anchor='w')
    details_label.pack(pady=6, padx=10, anchor="w")

    details_label = customtkinter.CTkLabel(
        details_frame, width=120, height=1, text=f"Data: {formatted_time}", font=("Roboto", 16), anchor='w')
    details_label.pack(pady=6, padx=10, anchor="w")

    details_label = customtkinter.CTkLabel(
        details_frame, width=120, height=1, text=f"Tempo desde a entrada: {hours:02d}:{minutes:02d}:{seconds:02d}", font=("Roboto", 16), anchor='w')
    details_label.pack(pady=6, padx=10, anchor="w")

    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min FROM price LIMIT 1")
        price_row = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        price_row = None

    tempo_str = str(time_difference)

    carencia = int(price_row[0]) if price_row else 0
    primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
    demais_faixas = int(price_row[2]) if price_row else 0
    tempo_primeira_faixa = int(price_row[3]) if price_row else 0
    tempo_demais_faixas = int(price_row[4]) if price_row else 0


    valor_total = 0.0
    total_minutos = time_difference.total_seconds() / 60
    print(total_minutos)
    if total_minutos <= carencia:
        valor_total = 0.0
    else:
        print(total_minutos)
        if total_minutos <= tempo_primeira_faixa:
            valor_total = primeira_faixa
        else:
            valor_total += primeira_faixa

            total_minutos = total_minutos - tempo_primeira_faixa
            if total_minutos > 0:
                total_minutos = total_minutos / tempo_demais_faixas
                total_minutos_ceiled = math.ceil(total_minutos)
                valor_total += total_minutos_ceiled * demais_faixas


    locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
    valor_total_brl = locale.currency(valor_total, grouping=True)

    valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16), anchor='w')
    valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

    combo = customtkinter.CTkComboBox(details_frame, width=400, height=40, values=["PIX", "CARTÃO", "DINHEIRO"])
    combo.pack(pady=12, padx=10)

    pagamento = combo.get()
    formatted_saida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA", command=lambda: move_to_history(selected_entry, formatted_time, formatted_saida, time_difference, pagamento))
    button.pack(pady=12, padx=10)

def update_entry_list():
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT placa, data FROM entry")
        entries = cursor.fetchall()

        tree.delete(*tree.get_children())

        for entry in entries:
            tree.insert('', tk.END, values=(entry[0], entry[1]))
        
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

def handle_listbox_click():
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]
        selected_item = listbox.get(selected_index)
        open_entry_details(selected_item)

def move_to_history(placa, entrada, saida, tempo, pagamento):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            placa TEXT,
                            data_entrada TEXT,
                            data_saida TEXT,
                            tempo_estadia TEXT,
                            valor_total REAL,
                            pagamento TEXT
                          )''')

        tempo_str = str(tempo)

        cursor.execute("SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min FROM price LIMIT 1")
        price_row = cursor.fetchone()

        carencia = int(price_row[0]) if price_row else 0
        primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
        demais_faixas = int(price_row[2]) if price_row else 0
        tempo_primeira_faixa = int(price_row[3]) if price_row else 0
        tempo_demais_faixas = int(price_row[4]) if price_row else 0

        valor_total = 0.0
        total_minutos = tempo.total_seconds() / 60
        if total_minutos <= carencia:
            valor_total = 0.0
        else:
            print(total_minutos)
            if total_minutos <= tempo_primeira_faixa:
                valor_total = primeira_faixa
            else:
                valor_total += primeira_faixa

                total_minutos = total_minutos - tempo_primeira_faixa
                if total_minutos > 0:
                    total_minutos = total_minutos / tempo_demais_faixas
                    total_minutos_ceiled = math.ceil(total_minutos)
                    valor_total += total_minutos_ceiled * demais_faixas


        cursor.execute("INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento) VALUES (?, ?, ?, ?, ?, ?)",
                       (placa, entrada, saida, tempo_str, valor_total, pagamento))

        cursor.execute("DELETE FROM entry WHERE placa = ?", (placa,))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Veículo retirado com sucesso!")
        update_entry_list()

    except sqlite3.Error as e:
        print("SQLite error:", e)

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="DAR SAIDA", font=("Roboto", 24))
label.pack(pady=12, padx=10)

tree = tk.ttk.Treeview(master=fr,
                       columns=("Placa", "Data de Entrada"))
tree.pack(side='left')

tree['show'] = 'headings'
tree.heading("#1", text="Placa")
tree.heading("#2", text="Data de Entrada")

tree.column("#1", width=100)
tree.column("#2", width=150)


treeScroll = tk.Scrollbar(master=fr)
treeScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeScroll.set)
treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

update_entry_list()

tree.bind("<Double-1>", open_entry_details)

rt.mainloop()
