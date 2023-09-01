import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import locale
import math
import win32print
import win32ui
import win32con as wcon



def validate_length(P):
    if len(P) <= 7:
        return True
    else:
        return False


class Exit(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()
        self.mainloop()
    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="DAR SAIDA", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.search = customtkinter.CTkFrame(master=fr)
        self.search.pack(pady=40, padx=120)

        self.label = customtkinter.CTkLabel(self.search, width=120, height=32, text="PLACA", font=("Roboto", 20))
        self.label.pack(pady=12, padx=10, side="left")

        self.entry1 = customtkinter.CTkEntry(self.search, width=240, height=32, placeholder_text="PLACA", validate="key",
                                        validatecommand=(self.register(validate_length), '%P'))
        self.entry1.pack(pady=12, padx=10, side="left")

        self.button = customtkinter.CTkButton(self.search, width=240, height=32, text="DAR SAIDA", command=self.dar_saida)
        self.button.pack(pady=12, padx=10, side="left")

        self.entry1.bind("<Return>", self.enter_pressed)
        self.after(100, self.set_focus)

        self.tree = tk.ttk.Treeview(master=fr,
                               columns=("Placa", "Data de Entrada", "Veiculo"))
        self.tree.pack(side='left')

        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Veiculo")

        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=50)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        self.treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.update_entry_list()

        self.tree.bind("<Double-1>", self.open_entry_details)


    def open_entry_details(self,selected_item):
        selected_item = self.tree.selection()[0]
        selected_entry = self.tree.item(selected_item, "values")
        details_window = tk.Toplevel(self)
        details_window.title("Entry Details")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")

        placa = selected_entry[0]
        data = selected_entry[1]
        veiculo = selected_entry[2]
        selected_entry = placa
        selected_time = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

        # Calculate the time difference
        current_time = datetime.now()
        time_difference = current_time - selected_time
        print("Time Difference1:", time_difference)
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

        details_label = customtkinter.CTkLabel(
            details_frame, width=120, height=1, text=f"Placa: {selected_entry}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

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

        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min,segunda_faixa, segunda_faixa_min FROM price LIMIT 1")
            price_row = cursor.fetchone()
            cursor.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            price_row = None

        tempo_str = str(time_difference)

        carencia = int(price_row[0]) if price_row else 0
        primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
        demais_faixas = int(price_row[2]) if price_row else 0
        tempo_primeira_faixa = int(price_row[3]) if price_row else 0
        tempo_demais_faixas = int(price_row[4]) if price_row else 0
        segunda_faixa = float(price_row[5]) if price_row else 0.0  # Use float instead of int
        tempo_segunda_faixa = int(price_row[6]) if price_row else 0
        print("Valor Segunda " )
        print(segunda_faixa)
        print("Tempo Segunda"  )
        print(tempo_segunda_faixa )
        valor_total = 0.0
        total_minutos = time_difference.total_seconds() / 60
        print("Total Minutos" )
        print(total_minutos)
        if total_minutos <= carencia:
            valor_total = 0.0
        else:
            print(total_minutos)
            if total_minutos <= tempo_primeira_faixa:
                valor_total = primeira_faixa
            elif total_minutos <= tempo_segunda_faixa:
                valor_total = primeira_faixa + segunda_faixa
            else:
                valor_total += primeira_faixa + segunda_faixa

                total_minutos = total_minutos - tempo_primeira_faixa - tempo_segunda_faixa
                print(total_minutos)
                if total_minutos > 0:
                    total_minutos = total_minutos / tempo_demais_faixas
                    total_minutos_ceiled = math.ceil(total_minutos)
                    print(total_minutos_ceiled)
                    print(demais_faixas)
                    print(valor_total)
                    valor_total += total_minutos_ceiled * demais_faixas

        locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
        valor_total_brl = locale.currency(valor_total, grouping=True)

        valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1,
                                                       text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16),
                                                       anchor='w')
        valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

        combo = customtkinter.CTkComboBox(details_frame, width=400, height=40, values=["PIX", "CARTÃO", "DINHEIRO"])
        combo.pack(pady=12, padx=10)

        pagamento = combo.get()
        formatted_saida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        def move_to_history(placa, entrada, saida, tempo, pagamento, veiculo):
            pagamento = combo.get()

            def print_recibo(placa, entrada, saida, tempo_str, valor_total, pagamento, veiculo):
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

                for text in padrão_superior_texts:
                    text_content, _, ordem = text
                    x_position = 0  # Starting x-position for the text
                    y_position += 40  # Calculate y-position based on ordem value

                    print(y_position)
                    print(text_content)

                    # Draw the text
                    pdc.TextOut(x_position, y_position, text_content)

                y_position += 100  # Adjust y-position after PADRÃO SUPERIOR text

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
                y_position += 50
                pdc.TextOut(0, y_position, "VEICULO: ")
                pdc.TextOut((width - pdc.GetTextExtent(veiculo)[0]), y_position, veiculo)
                y_position += 20
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
                                              data_entrada TEXT,
                                              data_saida TEXT,
                                              tempo_estadia TEXT,
                                              veiculo TEXT,
                                              valor_total REAL,
                                              pagamento TEXT
                                            )''')


                tempo_str = str(tempo)

                cursor.execute(
                    "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min,segunda_faixa, segunda_faixa_min FROM price LIMIT 1")
                price_row = cursor.fetchone()

                carencia = int(price_row[0]) if price_row else 0
                primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
                demais_faixas = int(price_row[2]) if price_row else 0
                tempo_primeira_faixa = int(price_row[3]) if price_row else 0
                tempo_demais_faixas = int(price_row[4]) if price_row else 0
                segunda_faixa = float(price_row[5]) if price_row else 0.0  # Use float instead of int
                tempo_segunda_faixa = int(price_row[6]) if price_row else 0
                print(segunda_faixa)
                print(tempo_segunda_faixa)
                cursor.close()
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
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo) VALUES (?, ?, ?, ?,?, ?, ?)",
                    (placa, entrada, saida, tempo_str, valor_total, pagamento, veiculo))

                cursor.execute("DELETE FROM entry WHERE placa = ?", (placa,))
                conn.commit()
                cursor.close()
                print_recibo(placa, entrada, saida, tempo_str, valor_total, pagamento, veiculo)
                self.update_entry_list()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA",
                                         command=lambda: move_to_history(selected_entry, formatted_time,
                                                                         formatted_saida, time_difference, pagamento, veiculo))
        button.pack(pady=12, padx=10)

    def update_entry_list(self):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT placa, data, veiculo FROM entry")
            entries = cursor.fetchall()
            cursor.close()
            self.tree.delete(*self.tree.get_children())

            for entry in entries:
                self.tree.insert('', tk.END, values=(entry[0], entry[1], entry[2]))

        except sqlite3.Error as e:
            print("SQLite error:", e)

    def open_entry_details_button(self,selected_item):
        print("Received selected item:", selected_item)
        print(self.tree.selection())
        details_window = tk.Toplevel(self)
        details_window.title("Entry Details")
        details_window.geometry("400x450")
        details_window.configure(bg="#212121")

        placa = selected_item[0]
        data = selected_item[1]
        veiculo = selected_item[2]
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
            details_frame, width=120, height=1, text="RECIBO", font=("Roboto", 24))
        details_label.pack(pady=6, padx=10)

        details_label = customtkinter.CTkLabel(
            details_frame, width=120, height=1, text=f"Placa: {selected_entry}", font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

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

        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min,segunda_faixa, segunda_faixa_min FROM price LIMIT 1")
            price_row = cursor.fetchone()
            cursor.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)
            price_row = None

        tempo_str = str(time_difference)

        carencia = int(price_row[0]) if price_row else 0
        primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
        demais_faixas = int(price_row[2]) if price_row else 0
        tempo_primeira_faixa = int(price_row[3]) if price_row else 0
        tempo_demais_faixas = int(price_row[4]) if price_row else 0
        segunda_faixa = float(price_row[5]) if price_row else 0.0  # Use float instead of int
        tempo_segunda_faixa = int(price_row[6]) if price_row else 0
        print("SEGUNDA FAIXA:" + segunda_faixa)
        print("SEGUNDA FAIXA:" + tempo_segunda_faixa)
        cursor.close()

        valor_total = 0.0
        total_minutos = time_difference.total_seconds() / 60
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

        valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1,
                                                       text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16),
                                                       anchor='w')
        valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

        combo = customtkinter.CTkComboBox(details_frame, width=400, height=40, values=["PIX", "CARTÃO", "DINHEIRO"])
        combo.pack(pady=12, padx=10)

        pagamento = combo.get()
        formatted_saida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        def move_to_history(placa, entrada, saida, tempo, pagamento):
            pagamento = combo.get()

            def print_recibo(placa, entrada, saida, tempo_str, valor_total, pagamento):

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

                for text in padrão_superior_texts:
                    text_content, _, ordem = text
                    x_position = 0  # Starting x-position for the text
                    y_position += 40  # Calculate y-position based on ordem value

                    print(y_position)
                    print(text_content)

                    # Draw the text
                    pdc.TextOut(x_position, y_position, text_content)

                y_position += 100  # Adjust y-position after PADRÃO SUPERIOR text

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
                                              data_entrada TEXT,
                                              data_saida TEXT,
                                              tempo_estadia TEXT,
                                              valor_total REAL,
                                              pagamento TEXT,
                                              veiculo TEXT,
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
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (placa, entrada, saida, tempo_str, valor_total, pagamento))

                cursor.execute("DELETE FROM entry WHERE placa = ?", (placa,))
                cursor.commit()
                cursor.close()
                print_recibo(placa, entrada, saida, tempo_str, valor_total, pagamento)
                self.update_entry_list()

            except sqlite3.Error as e:
                print("SQLite error:", e)

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA",
                                         command=lambda: move_to_history(selected_entry, formatted_time,
                                                                         formatted_saida, time_difference, pagamento))
        button.pack(pady=12, padx=10)

    def handle_listbox_click(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_item = self.listbox.get(selected_index)
            print("Selected item:", selected_item)
            self.open_entry_details(selected_item)

    def dar_saida(self):
        plate = self.entry1.get()  # Get the entered license plate
        print("Plate:", plate)
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT placa, data, veiculo FROM entry WHERE placa=?", (plate,))
        entry = cursor.fetchone()
        cursor.close()
        print(entry)

        if entry:
            self.open_entry_details_button(entry)
        else:
            messagebox.showinfo("Placa não encontrada", f"A placa {plate} não foi encontrada no banco de dados.")

    def enter_pressed(self,event):
        self.dar_saida()

    def set_focus(self):
        self.entry1.focus_set()
        self.after(100, self.set_focus)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Exit()
    app.run()