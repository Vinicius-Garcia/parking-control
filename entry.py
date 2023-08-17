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

# Validation function for entry length
def validate_length(P):
    if len(P) <= 7:
        return True
    else:
        return False

def plate_exists(placa):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT placa FROM entry WHERE placa = ?", (placa,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to insert an entry into the database
def send_entry():
    placa = entry1.get()
    
    if plate_exists(placa):
        messagebox.showwarning("Plate Exists", "Plate already exists in the database.")
        return
    # Connect to the database
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        # Create the 'entry' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                      (placa TEXT, data TEXT)''')
        
        # Save placa and data in the table
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO entry (placa, data) VALUES (?, ?)", (placa, data_atual))
        
        conn.commit()
        conn.close()
        
        # Update the Listbox with the new entry
        update_entry_list()
    except sqlite3.Error as e:
        print("SQLite error:", e)

# Function to open a new window and display selected entry details
def open_entry_details(selected_item):
        details_window = tk.Toplevel(rt)
        details_window.title("Entry Details")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")

    # Get the selected entry details
        selected_entry = selected_item.split(" - ")[0].split(": ")[1]
        selected_time = datetime.strptime(selected_item.split(" - ")[1].split(": ")[1], '%Y-%m-%d %H:%M:%S')

        # Format the selected time in Brazilian Portuguese (pt-br) format
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        formatted_time = selected_time.strftime('%d/%m/%Y %H:%M:%S')

        details_frame = tk.Frame(details_window, bg="#212121")
        details_frame.pack(pady=20, padx=10, fill="both", expand=True)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text="TICKET", font=("Roboto", 24))
        details_label.pack(pady=6, padx=10)

        # Generate and display QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(selected_entry)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_photo = ImageTk.PhotoImage(qr_img)

        qr_label = tk.Label(details_frame, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(pady=6, padx=10)
        
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET", command=print_entry)
        button.pack(pady=12, padx=10)


# Function to print the selected entry details
def print_entry():
    print('teste')
    try:
        font = {
             "height": 8,
        }
        with Printer(linegap=1) as printer:
            printer.text('placa', font_config=font)
            printer.text('data', font_config=font)

        messagebox.showinfo("Print", "Entry details printed successfully!")
    except Exception as e:
        print("Printing error:", e)

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

# Create the tkinter frame and widgets
fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="DAR ENTRADA", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="PLACA", validate="key", validatecommand=(rt.register(validate_length), '%P'))
entry1.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=240, height=32, text="DAR ENTRADA", command=send_entry)
button.pack(pady=12, padx=10)

# Add a Listbox widget to display entries
listbox = tk.Listbox(master=fr, width=480, height=200)
listbox.pack(pady=12, padx=10)

# Call the function to update the Listbox with existing entries
update_entry_list()

# Start the tkinter main loop
rt.mainloop()
