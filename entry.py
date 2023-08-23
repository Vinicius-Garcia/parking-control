import customtkinter
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import locale
import qrcode
from PIL import Image as pil_image, ImageWin as pil_image_win, ImageTk
import win32print
import win32ui
from escpos.printer import Serial, Usb
import configparser
import sys
import usb.core
import win32con as wcon
import win32con
import win32print as wprn


config = configparser.ConfigParser()
config.read("config.ini")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Create the main tkinter window
rt = customtkinter.CTk()
rt.after(0, lambda:rt.state('zoomed'))




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
    # Connect to the database
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Create the 'entry' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                      (placa TEXT, data TEXT)''')



        if plate_exists(placa):
            messagebox.showwarning("Plate Exists", "Plate already exists in the database.")
            return

        # Save placa and data in the table
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        cursor.execute("INSERT INTO entry (placa, data) VALUES (?, ?)", (placa, data_atual))

        conn.commit()
        conn.close()

        # Update the Listbox with the new entry
        update_entry_list()
    except sqlite3.Error as e:
        print("SQLite error:", e)

# Function to open a new window and display selected entry details
def open_entry_details(event):
        selected_item = tree.selection()[0]  # Get the selected item's ID
        selected_entry = tree.item(selected_item, "values")
        details_window = tk.Toplevel(rt)
        details_window.title("Entry Details")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")

        placa = selected_entry[0]  # Assuming the first value is the "Placa"
        data = selected_entry[1]
        # Get the selected entry details
        selected_entry = placa
        selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

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
            border=0,
        )
        qr.add_data(selected_entry)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="white", back_color="#212121")
        qr_photo = ImageTk.PhotoImage(qr_img)


        qr_label = tk.Label(details_frame, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(pady=6, padx=10)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET", command=lambda: print_entry(selected_entry, formatted_time))
        button.pack(pady=12, padx=10)


def print_entry_teste(placa, data):
    getAllPrinters()
    try:
        # Encontre o dispositivo USB com os IDs de fornecedor e produto
        device = usb.core.find(idVendor=0xFFF0, idProduct=0x0062)

        if device is None:
            raise Exception("Dispositivo USB não encontrado.")

        # Detach do driver do kernel (se necessário)
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        # Configuração do dispositivo
        device.set_configuration()

        # Crie uma instância da impressora USB
        printer = Usb(0x1ABD, 0x0010)

        # Imprima o ticket
        printer.text("TICKET\n")
        printer.qr(placa, size=4)
        printer.text(f"Placa: {placa}\n")
        printer.text(f"Data: {data}\n")
        printer.cut()

        # Feche a instância da impressora
        printer.close()

        print("Ticket impresso com sucesso!")
    except Exception as e:
        print(e)
        print("Erro ao imprimir o ticket.")

def draw_img(hdc, dib, maxh, maxw):
    w, h = dib.size
    print("Image HW: ({:d}, {:d}), Max HW: ({:d}, {:d})".format(h, w, maxh, maxw))
    h = min(h, maxh)
    w = min(w, maxw)
    l = (maxw - w) // 2
    t = 200
    dib.draw(hdc, (l, t, l + w, t + h))

def add_img(hdc, file_name, new_page=False):
    if new_page:
        hdc.StartPage()
    maxw = hdc.GetDeviceCaps(wcon.HORZRES)
    maxh = hdc.GetDeviceCaps(wcon.VERTRES)
    img = pil_image.open(file_name)
    dib = pil_image_win.Dib(img)
    draw_img(hdc.GetHandleOutput(), dib, maxh, maxw)
    if new_page:
        hdc.EndPage()

def print_entry(placa, data):
    PHYSICALWIDTH = 100
    PHYSICALHEIGHT = 400
    printer_name = win32print.GetDefaultPrinter()
    print(printer_name)
    hprinter = win32print.OpenPrinter(printer_name)
    printer_info = win32print.GetPrinter(hprinter, 2)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(printer_name)
    pdc.StartDoc('Ticket')
    pdc.StartPage()

    # Calculate center position for the text
    page_width = pdc.GetDeviceCaps(win32con.PHYSICALWIDTH)
    text_width = pdc.GetTextExtent("TICKET")[0]
    text_x = (page_width - text_width) // 2

    ticket_font = win32ui.CreateFont({
        "name": "Arial",
        "height": 100
    })
    pdc.SelectObject(ticket_font)
    # Draw centered "TICKET" text
    pdc.TextOut(text_x, 100, "TICKET")

    # Draw QR code centered
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )
    qr.add_data(placa)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    temp_qr_image_path = "temp_qr_image.png"
    img.save(temp_qr_image_path)
    add_img(pdc, temp_qr_image_path)

    # Draw plate and date text
    pdc.TextOut(text_x - 400 , 800, "PLACA: " )
    pdc.TextOut(text_x +400, 800,  placa)
    pdc.TextOut(text_x - 400, 950, "DATA/HORA: " )
    pdc.TextOut(text_x + 400, 950, data)

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()
    win32print.ClosePrinter(hprinter)


def update_entry_list():
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT placa, data FROM entry")
        entries = cursor.fetchall()
        tree.delete(*tree.get_children())
        #listbox.delete(0, tk.END)  # Clear the current list

        for entry in entries:
            entry_str = f"Placa: {entry[0]} - Data: {entry[1]}"
            tree.insert('', tk.END, values=(entry[0], entry[1]))

        conn.close()

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

search = customtkinter.CTkFrame(master=fr)
search.pack(pady=40, padx=120)

entry1 = customtkinter.CTkEntry(search, width=240, height=32, placeholder_text="PLACA", validate="key", validatecommand=(rt.register(validate_length), '%P'))
entry1.pack(pady=12, padx=10, side="left")

button = customtkinter.CTkButton(search, width=240, height=32, text="DAR ENTRADA", command=send_entry)
button.pack(pady=12, padx=10, side="left")


tree = tk.ttk.Treeview(master=fr,
                       columns=("Placa", "Data de Entrada"),selectmode="browse")


tree['show'] = 'headings'
tree.heading("#1", text="Placa")
tree.heading("#2", text="Data de Entrada")

# Set column widths
tree.column("#1", width=100)
tree.column("#2", width=150)


treeScroll = tk.Scrollbar(master=fr)
treeScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeScroll.set)
treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)








# Call the function to update the Listbox with existing entries
update_entry_list()

tree.bind("<Double-1>", open_entry_details)

# Start the tkinter main loop
rt.mainloop()