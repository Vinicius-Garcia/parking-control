import customtkinter
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import locale
import qrcode
from PIL import Image, ImageTk, ImageWin
import win32print
import win32ui
from escpos.printer import Serial
import configparser
import win32con as wcon
from PIL import Image as pil_image, ImageWin as pil_image_win, ImageTk
from tkcalendar import DateEntry


def validate_length(P):
    if len(P) <= 7:
        return True
    else:
        return False
class Reopen(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()

    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="REABRIR TICKET", font=("Roboto", 24))
        label.pack(pady=12, padx=10)

        self.datesFrame = customtkinter.CTkFrame(master=fr)
        self.datesFrame.pack(pady=10, padx=10, anchor="center")

        start_date_label = customtkinter.CTkLabel(self.datesFrame, text="Data Inicial:")
        start_date_label.pack(padx=(10, 10), pady=5, side="left")

        self.start_date_entry = DateEntry(self.datesFrame, width=16, background="magenta3", foreground="white", bd=2,
                                          locale="pt_br")
        self.start_date_entry.pack(padx=(0, 40), pady=5, anchor="w", side="left")

        end_date_label = customtkinter.CTkLabel(self.datesFrame, text="Data Final:")
        end_date_label.pack(padx=(10, 10), pady=5, anchor="w", side="left")

        self.end_date_entry = DateEntry(self.datesFrame, width=16, background="magenta3", foreground="white", bd=2,
                                        locale="pt_br")
        self.end_date_entry.pack(padx=(0, 40), pady=5, anchor="w", side="left")

        self.generate_button = customtkinter.CTkButton(self.datesFrame, width=140, height=40, text="GERAR",
                                                       command=self.generate_report)
        self.generate_button.pack(pady=10, padx=10, anchor="e", side="left")


        self.tree = tk.ttk.Treeview(master=fr,
                                    columns=(
                                        "Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência",
                                        "Valor Pago",
                                        "Pagamento", "Veículo", "Operador Entrada", "Operador Saída"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Data de Saída")
        self.tree.heading("#4", text="Tempo de Permanência")
        self.tree.heading("#5", text="Valor Pago")
        self.tree.heading("#6", text="Pagamento")
        self.tree.heading("#7", text="Veículo")
        self.tree.heading("#8", text="Operador Entrada")
        self.tree.heading("#9", text="Operador Saída")

        self.tree.column("#1", width=50)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=100)
        self.tree.column("#6", width=100)
        self.tree.column("#7", width=50)
        self.tree.column("#8", width=100)
        self.tree.column("#9", width=100)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        self.tree.bind("<Double-1>", self.open_entry_details)

    def generate_report(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        self.update_entry_list(start_datetime, end_datetime)



    def open_entry_details(self,event):
        selected_item = self.tree.selection()[0]  # Get the selected item's ID
        selected_entry = self.tree.item(selected_item, "values")
        details_window = tk.Toplevel(self)
        details_window.title("Entry Details")
        details_window.geometry("400x350")
        details_window.configure(bg="#212121")
        print(selected_entry)
        placa = selected_entry[0]
        data_entrada = selected_entry[1]
        data_saida = selected_entry[2]
        permanencia = selected_entry[3]
        valor = selected_entry[4]
        operador_entrada = selected_entry[7]
        veiculo = selected_entry[6]
        selected_entry = placa
        selected_time = datetime.strptime(data_entrada, '%d/%m/%Y %H:%M:%S')
        selected_time_exit = datetime.strptime(data_saida, '%d/%m/%Y %H:%M:%S')

        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        formatted_time = selected_time.strftime('%d/%m/%Y %H:%M:%S')
        formatted_time_exit = selected_time_exit.strftime('%d/%m/%Y %H:%M:%S')

        details_frame = tk.Frame(details_window, bg="#212121")
        details_frame.pack(pady=20, padx=10, fill="both", expand=True)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text="TICKET", font=("Roboto", 24))
        details_label.pack(pady=6, padx=10)

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data de Entrada: {formatted_time}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data de Saida: {formatted_time_exit}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Tempo de Permanencia: {permanencia}",font=("Roboto", 16), anchor='w')

        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Valor: {valor}",font=("Roboto", 16), anchor='w')

        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Veiculo: {veiculo}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="REABRIR TICKET",
                                              command=lambda: self.reopen_ticket(placa, data_entrada, operador_entrada, veiculo,details_window))
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


    def reopen_ticket(self, placa, data_entrada, operador_entrada, veiculo,details_window ):
        try:
            # Connect to the database
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            # Delete the ticket from the history table
            cursor.execute(
                "DELETE FROM history WHERE placa = ? AND data_entrada = ? AND operador_entrada = ? AND veiculo = ?",
                (placa, data_entrada, operador_entrada, veiculo))
            conn.commit()

            # Insert the ticket into the entry table
            cursor.execute("INSERT INTO entry (placa, data, veiculo, operador_entrada) VALUES (?, ?, ?, ?)",
                           (placa, data_entrada, veiculo, operador_entrada))
            conn.commit()

            # Close the database connection
            conn.close()

            # Update the entry list
            self.update_entry_list(self.start_date_entry.get(), self.end_date_entry.get())

            messagebox.showinfo("Ticket Reopened", "Ticket has been reopened and added to the entry list.")
            details_window.destroy()

        except sqlite3.Error as e:
            print("SQLite error:", e)
            messagebox.showerror("Error", "An error occurred while reopening the ticket.")
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

    def update_entry_list(self, start_date, end_date):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            start_datetime = f"{start_date} 00:00:00"
            end_datetime = f"{end_date} 23:59:59"

            cursor.execute(
                "SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada, operador_saida FROM history WHERE data_saida >= ? AND data_saida <= ?",
                (start_datetime, end_datetime))
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for item in self.tree.get_children():
                self.tree.delete(item)

            for entry in entries:
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada, operador_saida = entry
                self.tree.insert('', tk.END, values=(
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada,
                operador_saida))

            cursor.close()


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
    app = Reopen()
    app.run()
