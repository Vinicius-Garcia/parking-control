import customtkinter
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import locale
import qrcode
from PIL import Image, ImageTk
from win32printing import Printer


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Create the main tkinter window
rt = customtkinter.CTk()
rt.geometry("600x600")


def open_entry_details(selected_item):
    details_window = tk.Toplevel(rt)
    details_window.title("Entry Details")
    details_window.geometry("400x450")
    details_window.configure(bg="#212121")

    # Get the selected entry details
    selected_entry = selected_item.split(" - ")[0].split(": ")[1]
    selected_time = datetime.strptime(selected_item.split(
        " - ")[1].split(": ")[1], '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference
    current_time = datetime.now()
    time_difference = current_time - selected_time

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
            "SELECT carencia, primeira_faixa, primeira_faixa_min, demais_faixas, demais_faixas_min FROM price LIMIT 1")
        price_row = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        price_row = None

    tempo_carencia = int(price_row[0]) if price_row else 0
    # Use float instead of int
    valor_primeira_faixa = float(price_row[1]) if price_row else 0.0
    tempo_primeira_faixa = int(price_row[2]) if price_row else 0
    valor_demais_faixas = float(price_row[3]) if price_row else 0.0
    tempo_demais_faixas = int(price_row[4]) if price_row else 0

    # Calculate the total value based on time bands and grace period
    valor_total = 0.0

    if time_difference.total_seconds() <= tempo_carencia * 60:
        valor_total = 0.0
        print("Valor total: 0.0 (Carência)")
    elif time_difference.total_seconds() <= tempo_primeira_faixa * 60:
        valor_total = valor_primeira_faixa
        print("Valor total:", valor_total, "(Primeira Faixa)")
    else:
        # Calcula o tempo na primeira faixa
        tempo_primeira_faixa = tempo_primeira_faixa * 60
        valor_total += valor_primeira_faixa

        # Calcula o tempo nas demais faixas (se houver)
        tempo_demais_faixas = time_difference.total_seconds() - tempo_primeira_faixa
        if tempo_demais_faixas > 0:
            num_demais_faixas = int(tempo_demais_faixas / (60 * tempo_demais_faixas))
            valor_total += num_demais_faixas * valor_demais_faixas
            print("Valor total:", valor_total, "(Demais Faixas)")


    # Set the locale to Brazilian Portuguese for currency formatting
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
    valor_total_brl = locale.currency(valor_total, grouping=True)

    # Add a Label to display the calculated value in BRL
    valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16), anchor='w')
    valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

    button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA", command=lambda: move_to_history(selected_entry, formatted_time, datetime.now(), time_difference))
    button.pack(pady=12, padx=10)

def update_entry_list():
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

def handle_listbox_click():
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]  # Get the first selected index
        selected_item = listbox.get(selected_index)
        open_entry_details(selected_item)

def move_to_history(placa, entrada, saida, tempo):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Create the "history" table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            placa TEXT,
                            data_entrada TEXT,
                            data_saida TEXT,
                            tempo_estadia TEXT,
                            valor_total REAL
                          )''')

        # Convert the timedelta to a formatted string for storage
        tempo_str = str(tempo)

        # Get values from the "price" table
        cursor.execute("SELECT carencia, primeira_faixa, demais_faixas FROM price LIMIT 1")
        price_row = cursor.fetchone()

        carencia = int(price_row[0]) if price_row else 0
        primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
        demais_faixas = int(price_row[2]) if price_row else 0

        # Calculate the total value based on time bands and grace period
        valor_total = 0.0

        if tempo.total_seconds() <= carencia * 60:
            valor_total = 0.0
        elif tempo.total_seconds() <= primeira_faixa * 60:
            valor_total = 5.0
        else:
            total_minutos = tempo.total_seconds() / 60
            valor_total = 5.0 + ((total_minutos - primeira_faixa) // demais_faixas) * 2.5

        cursor.execute("INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total) VALUES (?, ?, ?, ?, ?)",
                       (placa, entrada, saida, tempo_str, valor_total))

        cursor.execute("DELETE FROM entry WHERE placa = ?", (placa,))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Veículo retirado com sucesso!")
        update_entry_list()

    except sqlite3.Error as e:
        print("SQLite error:", e)

# Create the tkinter frame and widgets
fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="DAR SAIDA", font=("Roboto", 24))
label.pack(pady=12, padx=10)

# Add a Listbox widget to display entries
listbox = tk.Listbox(master=fr, width=480, height=200)
listbox.pack(pady=12, padx=10)

# Call the function to update the Listbox with existing entries
update_entry_list()

# Start the tkinter main loop
rt.mainloop()
