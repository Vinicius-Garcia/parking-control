import customtkinter
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import locale
import qrcode
from PIL import Image, ImageTk, ImageWin
import win32print
import win32ui
from escpos.printer import Serial
import configparser
import win32con as wcon
from PIL import Image as pil_image, ImageWin as pil_image_win, ImageTk


def validate_length(P):
    if len(P) <= 7:
        return True
    else:
        return False
class Lot(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()

    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)
        style = ttk.Style(master=fr)
        style.configure('Treeview', background='white', foreground='black', font=('Roboto', 18, 'normal', 'roman'),
                        rowheight=30)
        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="PÁTIO ATUAL", font=("Roboto", 24))
        label.pack(pady=12, padx=10)

        self.generate = customtkinter.CTkFrame(master=fr)
        self.generate.pack(pady=10, padx=10, fill="both")


        self.generate1 = customtkinter.CTkFrame(self.generate)
        self.generate1.pack(pady=10, padx=10, anchor="e", side="right")

        self.button = customtkinter.CTkButton(self.generate1, width=120, height=24, text="IMPRIMIR",
                                              command=self.imprimir)
        self.button.pack(padx=10, pady=10, side="left")


        self.tree = tk.ttk.Treeview(master=fr,
                               columns=("Placa", "Data de Entrada", "Veículo"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Veículo")

        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        self.treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.update_entry_list()

        self.tree.bind("<Double-1>", self.open_entry_details)

    def imprimir(self):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT placa, data, veiculo FROM entry")
            entries = cursor.fetchall()
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)

            printer_info = win32print.GetPrinter(hprinter, 2)
            pdc = win32ui.CreateDC()
            pdc.CreatePrinterDC(printer_name)
            pdc.StartDoc('Ticket')
            pdc.StartPage()

            y_position = 0
            font = win32ui.CreateFont({
                    "name": "Arial",  # Altere para a fonte desejada
                    "height": 30,  # Altere para o tamanho de fonte desejado
            })
            pdc.SelectObject(font)
            width = pdc.GetDeviceCaps(wcon.HORZRES)
            text_width = pdc.GetTextExtent("OCUPAÇÃO")[0]

            x_position = (width - text_width) // 2

            y_position += 50  # Ajuste a posição vertical conforme necessário
            pdc.TextOut(x_position, y_position, 'OCUPAÇÃO')

            y_position += 50
            total_carros = 0
            total_motos = 0
            for entry in entries:
                    placa = entry[0]
                    data = entry[1]
                    veiculo = entry[2]
                    text_width = pdc.GetTextExtent(veiculo)[0]

                    x_position = (width - text_width) // 2
                    pdc.TextOut(0, y_position, placa)
                    pdc.TextOut(x_position, y_position, veiculo)
                    pdc.TextOut((width - pdc.GetTextExtent(data)[0]), y_position, data)
                    y_position += 50
                    if veiculo.lower() == "carro":
                        total_carros += 1
                    elif veiculo.lower() == "moto":
                        total_motos += 1

            total_geral = len(entries)
            y_position += 50
            pdc.TextOut(0, y_position, f"Total Carros: {total_carros}")
            y_position += 30
            pdc.TextOut(0, y_position, f"Total Motos: {total_motos}")
            y_position += 30
            pdc.TextOut(0, y_position, f"Total Geral: {total_geral}")

            pdc.EndPage()
            pdc.EndDoc()
            pdc.DeleteDC()
            win32print.ClosePrinter(hprinter)

            cursor.close()

        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_entry_details(self,event):
        selected_item = self.tree.selection()[0]  # Get the selected item's ID
        selected_entry = self.tree.item(selected_item, "values")
        details_window = tk.Toplevel(self)
        details_window.title("Entry Details")
        details_window.geometry("400x250")
        details_window.configure(bg="#212121")

        placa = selected_entry[0]
        data = selected_entry[1]
        veiculo = selected_entry[2]
        selected_entry = placa
        selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        formatted_time = selected_time.strftime('%d/%m/%Y %H:%M:%S')

        details_frame = tk.Frame(details_window, bg="#212121")
        details_frame.pack(pady=20, padx=10, fill="both", expand=True)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text="TICKET", font=("Roboto", 24))
        details_label.pack(pady=6, padx=10)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Veiculo: {veiculo}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                              command=lambda: self.print_entry(placa, formatted_time, details_window))
        button.pack(pady=12, padx=10)

    def draw_img(self, hdc, dib, maxh, maxw, y_position):
        w, h = dib.size
        h = min(h, maxh)
        w = min(w, maxw)
        l = (maxw - w) // 2
        t = y_position
        dib.draw(hdc, (l, t, l + w, t + h))

    def add_img(self,hdc, file_name, y_position, new_page=False):
        if new_page:
            hdc.StartPage()
        maxw = hdc.GetDeviceCaps(wcon.HORZRES)
        maxh = hdc.GetDeviceCaps(wcon.VERTRES)
        img = pil_image.open(file_name)
        dib = pil_image_win.Dib(img)
        self.draw_img(hdc.GetHandleOutput(), dib, maxh, maxw, y_position)
        if new_page:
            hdc.EndPage()

    def print_entry(self, placa, data, details_window):
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT text, type, ordem FROM texts")
        texts = cursor.fetchall()
        cursor.close()
        padrão_superior_texts = [text for text in texts if text[1] == 'PADRÃO SUPERIOR']
        qr_code_texts = [text for text in texts if text[1] == 'QR CODE']
        padrão_inferior_texts = [text for text in texts if text[1] == 'TICKET INFERIOR']

        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(hprinter, 2)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)
        pdc.StartDoc('Ticket')
        pdc.StartPage()

        y_position = 0  # Starting y-position for the text

        font = win32ui.CreateFont({
            "name": "Arial",  # Change to the desired font name
            "height": 30,  # Change to the desired font size
        })

        pdc.SelectObject(font)
        if padrão_superior_texts:
            for text in padrão_superior_texts:
                text_content, _, ordem = text
                x_position = 0
                y_position += 40
                pdc.TextOut(x_position, y_position, text_content)

        y_position += 50

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(placa)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        temp_qr_image_path = "temp_qr_image.png"
        img.save(temp_qr_image_path)
        self.add_img(pdc, temp_qr_image_path, y_position)

        width = pdc.GetDeviceCaps(wcon.HORZRES)

        y_position += 250

        pdc.TextOut(0, y_position, "PLACA: ")
        pdc.TextOut((width - pdc.GetTextExtent(placa)[0]), y_position, placa)
        y_position += 50
        pdc.TextOut(0, y_position, "DATA/HORA: ")
        pdc.TextOut((width - pdc.GetTextExtent(data)[0]), y_position, data)
        y_position += 20
        if padrão_inferior_texts:
            for text in padrão_inferior_texts:
                text_content, _, ordem = text
                l = width // 2
                x_position = (width - pdc.GetTextExtent(text_content)[0]) // 2  # Calculate centered x-position

                y_position += 40  # Calculate y-position based on ordem value

                # Draw the text
                pdc.TextOut(x_position, y_position, text_content)

        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

        details_window.destroy()

    def update_entry_list(self):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT placa, data, veiculo FROM entry")
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            cursor.close()
            for entry in entries:
                entry_str = f"Placa: {entry[0]} - Data: {entry[1]} - Veiculo: {entry[2]}"
                self.tree.insert('', tk.END, values=(entry[0], entry[1], entry[2]))


        except sqlite3.Error as e:
            print("SQLite error:", e)

    def handle_listbox_click(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_item = self.listbox.get(selected_index)
            self.open_entry_details(selected_item)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Lot()
    app.run()
