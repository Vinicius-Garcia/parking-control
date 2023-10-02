import math

import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import locale
import qrcode
from PIL import Image as pil_image, ImageWin as pil_image_win, ImageTk
import win32print
import win32ui
import win32con as wcon


def validate_length(P):
    if len(P) <= 7:
        return True
    else:
        messagebox.showerror("Erro de entrada", "A placa deve conter 7 caracteres.")
        return False


class Entry(customtkinter.CTk):
    def __init__(self, user):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.user = user
        self.vehicle_type = tk.StringVar()
        self.vehicle_type.set("CARRO")
        self.details_window = None
        self.details_window_open = False
        self.setup_ui()
        self.mainloop()
    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="CONTROLE DE ACESSO", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.search = customtkinter.CTkFrame(master=fr)
        self.search.pack(pady=40, padx=120)

        self.labelplaca = customtkinter.CTkLabel(self.search, width=120, height=32, text="PLACA:", font=("Roboto", 18))
        self.labelplaca.pack(pady=12, padx=(10,1), side="left")

        self.entry1 = customtkinter.CTkEntry(self.search, width=240, height=32, placeholder_text="PLACA",
                                             validate="key",
                                             validatecommand=(self.register(validate_length), '%P'))
        self.entry1.pack(pady=12, padx=10, side="left")
        self.entry1.bind("<Return>", self.enter_pressed)
        self.after(200, lambda: self.entry1.focus())

        self.vehicle_checkbox = customtkinter.CTkCheckBox(self.search, text="MOTO", variable=self.vehicle_type,
                                                          onvalue="MOTO", offvalue="CARRO")
        self.vehicle_checkbox.pack(pady=12, padx=10, side="left")

        self.button = customtkinter.CTkButton(self.search, width=240, height=32, text="REGISTRAR ENTRADA / SAIDA",
                                              command=self.send_entry)
        self.button.pack(pady=12, padx=10, side="left")

        style = ttk.Style()
        style.configure("Treeview", rowheight=150)

        self.tree = tk.ttk.Treeview(master=fr,
                               columns=("Placa", "Data de Entrada", "Veículo"), selectmode="browse", style="Treeview")

        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Veículo")

        # Set column widths
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=50)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        self.treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)
        self.tree.tag_configure("custom_font", font=("Roboto", 18))


        self.update_entry_list()

        self.tree.bind("<Double-1>", self.open_entry_details_list)


    def plate_exists(self,placa):
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT placa FROM entry WHERE placa = ?", (placa,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None

    def send_entry_and_open_print(self, event=None):
        if self.tree.selection():
            selected_item = self.tree.selection()[0]  # Get the selected item's ID
            self.send_entry()  # Trigger the entry process
            self.open_entry_details(selected_item)  # Open the print ticket screen

    def send_entry(self, placa=None, frame=None):

        if placa:
            frame.destroy()
            placa = placa
        else:
            placa = self.entry1.get()

        veiculo = self.vehicle_type.get()


        if len(placa) < 7:  # Use len(placa) to check the length
            messagebox.showerror("Erro de Registro",
                                 "Ocorreu um erro ao registrar a entrada, placa deve conter 7 dígitos.")
            return

        self.entry1.delete(0,tk.END )

        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                             (placa TEXT, data DATE, operador_entrada TEXT, veiculo TEXT)''')

            if self.plate_exists(placa): # Get the entered license plate
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute("SELECT placa, data, veiculo, operador_entrada FROM entry WHERE placa=?", (placa,))
                entry = cursor.fetchone()
                cursor.close()

                if entry:
                    self.open_entry_details_button(entry)

                return

            data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            cursor.execute("INSERT INTO entry (placa, data, veiculo, operador_entrada) VALUES (?, ?, ?, ?)", (placa, data_atual, veiculo, self.user[1]))

            conn.commit()  # Commit the changes to the database
            cursor.close()
            self.update_entry_list()  # Update the UI

            self.open_entry_details('',placa, data_atual, veiculo,)

        except sqlite3.Error as e:
            print("SQLite error:", e)
            messagebox.showerror("Erro de Registro", "Ocorreu um erro ao registrar a entrada.")

        # Function to open a new window and display selected entry details


    def open_entry_details_button(self,selected_item):
        details_window = tk.Toplevel(self)
        details_window.title("RECIBO DE PAGAMENTO")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")
        print(selected_item)
        placa = selected_item[0]
        data = selected_item[1]
        veiculo = selected_item[2]
        operador_entrada = selected_item[3]
        selected_entry = placa
        selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

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
            details_frame, width=120, height=1, text="RECIBO", font=("Roboto", 24))
        details_label.pack(pady=6, padx=10)

        frame_plate = tk.Frame(details_frame, bg="#212121")
        frame_plate.pack(fill="x")

        labelplaca = customtkinter.CTkLabel(frame_plate, width=120, height=1, text="PLACA:",
                                                 font=("Roboto", 16))
        labelplaca.pack(side="left")

        plate_entry = customtkinter.CTkEntry(
            frame_plate, width=120, height=1, font=("Roboto", 16))
        plate_entry.pack( side="left")

        details_label = customtkinter.CTkLabel(
            details_frame, width=120, height=1, text=f"Data: {formatted_time}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")
        details_label = customtkinter.CTkLabel(
            details_frame, width=120, height=1, text=f"Veiculo: {veiculo}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(
            details_frame, width=120, height=1, text=f"Tempo desde a entrada: {hours:02d}:{minutes:02d}:{seconds:02d}",
            font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        plate_entry.insert(0, selected_entry)
        print(veiculo)
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min,segunda_faixa, segunda_faixa_min FROM price WHERE veiculo=?",(veiculo,))
            price_row = cursor.fetchone()
            cursor.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            price_row = None

        tempo_str = str(time_difference)
        carencia = int(price_row[0]) if price_row else 0
        primeira_faixa = float(price_row[1]) if price_row else 0.0
        demais_faixas = int(price_row[2]) if price_row else 0
        tempo_primeira_faixa = int(price_row[3]) if price_row else 0
        tempo_demais_faixas = int(price_row[4]) if price_row else 0
        segunda_faixa = float(price_row[5]) if price_row else 0.0
        tempo_segunda_faixa = int(price_row[6]) if price_row else 0

        cursor.close()

        valor_total = 0.0
        total_minutos = time_difference.total_seconds() / 60
        if total_minutos <= carencia:
            valor_total = 0.0
        else:
            if total_minutos <= tempo_primeira_faixa:
                valor_total = primeira_faixa
            elif total_minutos <= tempo_segunda_faixa:
                valor_total = primeira_faixa + segunda_faixa
            else:
                valor_total += primeira_faixa + segunda_faixa

                total_minutos = total_minutos - tempo_primeira_faixa - tempo_segunda_faixa
                if total_minutos > 0:
                    total_minutos = total_minutos / tempo_demais_faixas
                    total_minutos_ceiled = math.ceil(total_minutos)
                    valor_total += total_minutos_ceiled * demais_faixas

        locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
        valor_total_brl = locale.currency(valor_total, grouping=True)

        valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1,
                                                       text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16),
                                                       anchor='w')
        valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

        combo = customtkinter.CTkComboBox(details_frame, width=400, height=40, values=["--", "PIX", "CARTÃO", "DINHEIRO"])
        combo.pack(pady=12, padx=10)

        pagamento = combo.get()
        formatted_saida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        def move_to_history(placa, entrada, saida, tempo, pagamento, operador_entrada):
            pagamento = combo.get()
            print(pagamento)
            if pagamento == '--':
                messagebox.showerror("ERRO", "ESCOLHA UMA FORMA DE PAGAMENTO")
                return
            placa_editada=plate_entry.get()

            def print_recibo(placa, entrada, saida, tempo_str, valor_total, pagamento, operador_entrada):

                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute("SELECT text, type, ordem FROM texts")
                texts = cursor.fetchall()
                cursor.close()
                padrão_superior_texts = [text for text in texts if text[1] == 'PADRÃO SUPERIOR']
                recibo_inferior = [text for text in texts if text[1] == 'RECIBO INFERIOR']
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
                width = pdc.GetDeviceCaps(wcon.HORZRES)

                pdc.TextOut(((width - pdc.GetTextExtent("RECIBO")[0]) // 2), y_position, "RECIBO")

                if padrão_superior_texts:
                    for text in padrão_superior_texts:
                        text_content, _, ordem = text
                        x_position = 0
                        y_position += 40

                        pdc.TextOut(x_position, y_position, text_content)

                y_position += 100
                pdc.TextOut(0, y_position, "PLACA: ")
                pdc.TextOut((width - pdc.GetTextExtent(placa)[0]), y_position, placa)
                y_position += 50  # Adjust y-position after PLACA text
                pdc.TextOut(0, y_position, "DATA DE ENTRADA: ")
                pdc.TextOut((width - pdc.GetTextExtent(entrada)[0]), y_position, entrada)
                y_position += 50  # Adjust y-position after PLACA text
                pdc.TextOut(0, y_position, "SAIDA: ")
                pdc.TextOut((width - pdc.GetTextExtent(saida)[0]), y_position, saida)
                y_position += 50  # Adjust y-position after PLACA text
                pdc.TextOut(0, y_position, "VALOR TOTAL: ")
                pdc.TextOut((width - pdc.GetTextExtent(str(valor_total))[0]), y_position, str(valor_total))
                y_position += 50  # Adjust y-position after PLACA text
                pdc.TextOut(0, y_position, "PAGAMENTO: ")
                pdc.TextOut((width - pdc.GetTextExtent(pagamento)[0]), y_position, pagamento)
                y_position += 20
                if recibo_inferior:
                    for text in recibo_inferior:
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

            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              placa TEXT,
                                              data_entrada DATE,
                                              data_saida DATE,
                                              tempo_estadia TEXT,
                                              valor_total REAL,
                                              pagamento TEXT,
                                              veiculo TEXT,
                                              operador_entrada TEXT,
                                              operador_saida TEXT
                                            )''')


                tempo_str = str(tempo)

                cursor.execute(
                    "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min FROM price LIMIT 1")
                price_row = cursor.fetchone()
                cursor.close()
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
                    if total_minutos <= tempo_primeira_faixa:
                        valor_total = primeira_faixa
                    elif total_minutos <= tempo_segunda_faixa:
                        valor_total = primeira_faixa + segunda_faixa
                    else:
                        valor_total += primeira_faixa + segunda_faixa

                        total_minutos = total_minutos - tempo_primeira_faixa - tempo_segunda_faixa
                        if total_minutos > 0:
                            total_minutos = total_minutos / tempo_demais_faixas
                            total_minutos_ceiled = math.ceil(total_minutos)
                            valor_total += total_minutos_ceiled * demais_faixas
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada, operador_saida) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (placa, entrada, saida, tempo_str, valor_total, pagamento, veiculo, operador_entrada, self.user[2]))

                cursor.execute("DELETE FROM entry WHERE placa = ?", (placa,))
                conn.commit()
                cursor.close()
                print_recibo(placa_editada, entrada, saida, tempo_str, valor_total, pagamento, operador_entrada)
                self.update_entry_list()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA",
                                         command=lambda: move_to_history(selected_entry, formatted_time,
                                                                         formatted_saida, time_difference, pagamento,operador_entrada))
        button.pack(pady=12, padx=10)

    def open_entry_details(self,event, plate, date, veiculo):
            details_window = tk.Toplevel(self)
            details_window.title("Ticket")
            details_window.geometry("400x250")
            details_window.configure(bg="#212121")

            self.after(200, lambda: details_window.focus())
            if plate and date and veiculo:
                placa = plate
                data = date
                veiculo = veiculo
            else:
                selected_item = self.tree.selection()[0]  # Get the selected item's ID
                selected_entry = self.tree.item(selected_item, "values")
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

            self.button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                             command=lambda: self.print_entry(selected_entry, formatted_time, details_window))
            self.button.pack(pady=12, padx=10)

            details_window.bind("<Return>",
                                lambda event, p=placa, d=formatted_time, w=details_window: self.print_entry(p, d, w))


    def open_entry_details_list(self, event=None):
        details_window = tk.Toplevel(self)
        details_window.title("TICKET")
        details_window.geometry("400x300")
        details_window.configure(bg="#212121")

        self.after(200, lambda: details_window.focus())

        selected_item = self.tree.selection()[0] if self.tree.selection() else None
        if selected_item:
            selected_entry = self.tree.item(selected_item, "values")
            placa = selected_entry[0]
            data = selected_entry[1]
            veiculo = selected_entry[2]

            selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
            formatted_time = selected_time.strftime('%d/%m/%Y %H:%M:%S')

            details_frame = tk.Frame(details_window, bg="#212121")
            details_frame.pack(pady=20, padx=10, fill="both", expand=True)

            details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text="TICKET",
                                                   font=("Roboto", 24))
            details_label.pack(pady=6, padx=10)

            details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {placa}",
                                                   font=("Roboto", 16), anchor='w')
            details_label.pack(pady=6, padx=10, anchor="w")

            details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}",
                                                   font=("Roboto", 16), anchor='w')
            details_label.pack(pady=6, padx=10, anchor="w")
            details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Veiculo: {veiculo}",
                                                   font=("Roboto", 16), anchor='w')
            details_label.pack(pady=6, padx=10, anchor="w")

            self.button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                                  command=lambda: self.print_entry(placa, formatted_time, details_window))
            self.button.pack(pady=12, padx=10)

            self.button1 = customtkinter.CTkButton(details_frame, width=240, height=32,fg_color='#91403d', text="DAR SAIDA",
                                                  command=lambda: self.send_entry(placa, details_window))
            self.button1.pack(pady=12, padx=10)



    def draw_img(self,hdc, dib, maxh, maxw, y_position):
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


    def print_entry(self,placa, data, details_window):
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
                # listbox.delete(0, tk.END)  # Clear the current list
                cursor.close()
                for entry in entries:
                    entry_str = f"Placa: {entry[0]} - Data: {entry[1]} - Veiculo: {entry[2]}"
                    self.tree.insert('', tk.END, values=(entry[0], entry[1], entry[2]), tags=("custom_font",))


            except sqlite3.Error as e:
                print("SQLite error:", e)

    def enter_pressed(self,event):
        self.send_entry()

    def enter_pressed_ticket(self, selected_entry, formatted_time, details_window):
        self.print_entry(selected_entry, formatted_time, details_window)

    def set_focus(self):
        self.entry1.focus_set()
        self.after(100, self.set_focus)
    def handle_listbox_click(self):
            selected_indices = self.listbox.curselection()
            if selected_indices:
                selected_index = selected_indices[0]  # Get the first selected index
                selected_item = self.listbox.get(selected_index)
                self.open_entry_details(selected_item)

    def run(self):
        self.mainloop()

    def on_details_window_close(self):
        self.details_window_open = False  # Marque a janela de detalhes como fechada
        if self.details_window is not None:
            self.details_window.destroy()

if __name__ == "__main__":
    app = Entry()
    app.run()

