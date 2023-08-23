import customtkinter
import os
import sqlite3


def login_screen():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    rt = customtkinter.CTk()
    rt.after(0, lambda:rt.state('zoomed'))
    def login():
        username = entry1.get()
        password = entry2.get()

        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()
        print(user)


        if user:
            user_type = user[4]
            rt.destroy()  # Fecha a janela de login
            menu(user_type) # Abre a tela de controle
        else:
            label_status.config(text="Login failed. Please try again.")

    def switch_to_register_screen():
        rt.destroy()  # Fecha a janela atual
        register()  # Abre a tela de registro



    fr = customtkinter.CTkFrame(master=rt)
    fr.pack(pady=40, padx=120, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=fr, width=480, height=32, text="Login", font=("Roboto", 48))
    label.pack(pady=(250,20), padx=10)

    entry1 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Usuário")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Senha", show="*")
    entry2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Login", command=login)
    button.pack(pady=12, padx=10)

    register_button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Registre-se", command=switch_to_register_screen)
    register_button.pack(pady=12, padx=10)


    rt.mainloop()

def register():
    import customtkinter
    import os
    import sqlite3

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

    def add_to_database():
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')

        full_name = firstname.get()
        username = entry1.get()
        password = entry2.get()
        role = combo.get()

        cursor.execute('INSERT INTO users (full_name, username, password, role) VALUES (?, ?, ?, ?)',
                       (full_name, username, password, role))

        conn.commit()
        conn.close()

    def reg():
        add_to_database()
        switch_to_login_screen()

    def switch_to_login_screen():
        rt.destroy()
        login_screen()

    fr = customtkinter.CTkFrame(master=rt)
    fr.pack(pady=30, padx=120, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=fr, width=300, height=40, font=("Roboto", 36), text="Cadastrar Usuário")
    label.pack(pady=12, padx=10)

    firstname = customtkinter.CTkEntry(master=fr, width=300, height=40, placeholder_text="Nome Completo")
    firstname.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=fr, width=300, height=40, placeholder_text="Usuário")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=fr, width=300, height=40, placeholder_text="Senha", show="*")
    entry2.pack(pady=12, padx=10)

    combo = customtkinter.CTkComboBox(master=fr, width=300, height=40, values=["OPERADOR", "GERENTE"])
    combo.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=fr, width=300, height=40, text="CADASTRAR", command=reg)
    button.pack(pady=12, padx=24)

    button1 = customtkinter.CTkButton(master=fr, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                      command=switch_to_login_screen)
    button1.pack(pady=12, padx=10)

    rt.mainloop()

def menu(user_type):
    import customtkinter
    import os
    import sqlite3
    import sys

    print("User type:", user_type)
    user_type = user_type

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

    # Funções para os botões
    def open_entrada():
        entry()

    def open_saida():
        exit()

    def open_patio():
        lot()

    def open_relatorio():
        if user_type == "GERENTE":
            report()
        else:
            # Mostrar uma mensagem ou desabilitar o botão de relatório para usuários não autorizados
            button4.configure(state="disabled")  # Desabilita o botão de relatório

    def open_config():
        if user_type == "GERENTE":
            config()
        else:
            # Mostrar uma mensagem ou desabilitar o botão de configuração para usuários não autorizados
            button5.configure(state="disabled")  # Desabilita o botão de configuração

    def logout():
        rt.destroy()
        login_screen()

    fr = customtkinter.CTkFrame(master=rt)
    fr.pack(pady=40, padx=120, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=fr, width=120, height=48, text="Main Menu", font=("Roboto", 48))
    label.pack(pady=(150, 10), padx=10)

    button1 = customtkinter.CTkButton(master=fr, width=480, height=48, text="DAR ENTRADA", command=open_entrada)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=fr, width=480, height=48, text="DAR SAÍDA", command=open_saida)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=fr, width=480, height=48, text="PÁTIO", command=open_patio)
    button3.pack(pady=12, padx=10)

    button4 = customtkinter.CTkButton(master=fr, width=480, height=48, text="RELATÓRIO", command=open_relatorio)
    button4.pack(pady=12, padx=10)

    button5 = customtkinter.CTkButton(master=fr, width=480, height=48, text="CONFIGURAÇÃO", command=open_config)
    button5.pack(pady=12, padx=10)

    if user_type != "GERENTE":
        print(user_type)
        button4.configure(state="disabled")
        button5.configure(state="disabled")

    button6 = customtkinter.CTkButton(master=fr, width=480, height=48, text="LOGOUT", fg_color='#91403d',
                                      command=logout)
    button6.pack(pady=12, padx=10)

    # Inicia a aplicação
    rt.mainloop()


def exit():
    import customtkinter
    import sqlite3
    from datetime import datetime
    import tkinter as tk
    from tkinter import messagebox
    import locale
    import math

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Create the main tkinter window
    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

    def open_entry_details(selected_item):
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
            details_frame, width=120, height=1, text=f"Tempo desde a entrada: {hours:02d}:{minutes:02d}:{seconds:02d}",
            font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        # Get values from the "price" table
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

        # Calculate the total value based on time bands and grace period
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

        # Set the locale to Brazilian Portuguese for currency formatting
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
        valor_total_brl = locale.currency(valor_total, grouping=True)

        # Add a Label to display the calculated value in BRL
        valor_total_brl_label = customtkinter.CTkLabel(details_frame, width=120, height=1,
                                                       text=f"Valor Total: {valor_total_brl}", font=("Roboto", 16),
                                                       anchor='w')
        valor_total_brl_label.pack(pady=6, padx=10, anchor="w")

        combo = customtkinter.CTkComboBox(details_frame, width=400, height=40, values=["PIX", "CARTÃO", "DINHEIRO"])
        combo.pack(pady=12, padx=10)

        pagamento = combo.get()
        formatted_saida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="DAR SAIDA",
                                         command=lambda: move_to_history(selected_entry, formatted_time,
                                                                         formatted_saida, time_difference, pagamento))
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
            selected_index = selected_indices[0]  # Get the first selected index
            selected_item = listbox.get(selected_index)
            open_entry_details(selected_item)

    def move_to_history(placa, entrada, saida, tempo, pagamento):
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
                                valor_total REAL,
                                pagamento TEXT
                              )''')

            # Convert the timedelta to a formatted string for storage
            tempo_str = str(tempo)

            # Get values from the "price" table
            cursor.execute(
                "SELECT carencia, primeira_faixa, demais_faixas, primeira_faixa_min, demais_faixas_min FROM price LIMIT 1")
            price_row = cursor.fetchone()

            carencia = int(price_row[0]) if price_row else 0
            primeira_faixa = float(price_row[1]) if price_row else 0.0  # Use float instead of int
            demais_faixas = int(price_row[2]) if price_row else 0
            tempo_primeira_faixa = int(price_row[3]) if price_row else 0
            tempo_demais_faixas = int(price_row[4]) if price_row else 0

            # Calculate the total value based on time bands and grace period
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

            cursor.execute(
                "INSERT INTO history (placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento) VALUES (?, ?, ?, ?, ?, ?)",
                (placa, entrada, saida, tempo_str, valor_total, pagamento))

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

    tree = tk.ttk.Treeview(master=fr,
                           columns=("Placa", "Data de Entrada"))
    tree.pack(side='left')

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


def entry():
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


    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Create the main tkinter window
    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

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

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                         command=lambda: print_entry(selected_entry, formatted_time))
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
        pdc.TextOut(text_x - 400, 800, "PLACA: ")
        pdc.TextOut(text_x + 400, 800, placa)
        pdc.TextOut(text_x - 400, 950, "DATA/HORA: ")
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
            # listbox.delete(0, tk.END)  # Clear the current list

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

    entry1 = customtkinter.CTkEntry(search, width=240, height=32, placeholder_text="PLACA", validate="key",
                                    validatecommand=(rt.register(validate_length), '%P'))
    entry1.pack(pady=12, padx=10, side="left")

    button = customtkinter.CTkButton(search, width=240, height=32, text="DAR ENTRADA", command=send_entry)
    button.pack(pady=12, padx=10, side="left")

    tree = tk.ttk.Treeview(master=fr,
                           columns=("Placa", "Data de Entrada"), selectmode="browse")

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
def lot():
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

    config = configparser.ConfigParser()
    config.read("config.ini")

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Create the main tkinter window
    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

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

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Placa: {selected_entry}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        details_label = customtkinter.CTkLabel(details_frame, width=120, height=1, text=f"Data: {formatted_time}",
                                               font=("Roboto", 16), anchor='w')
        details_label.pack(pady=6, padx=10, anchor="w")

        button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                         command=lambda: print_entry(selected_entry, formatted_time))
        button.pack(pady=12, padx=10)

    def print_entry(placa, data):
        try:
            porta = config.get("config", "porta")
            print(porta)
            p = Serial(devfile=porta,
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       timeout=1.00,
                       dsrdtr=True)

            p.text("TICKET\n")
            p.qr(placa, size=4)
            p.text(f"Placa: {placa}\n")
            p.text(f"Data: {data}\n")

            p.cut()

            # Close the details_window after printing
            details_window.destroy()

        except Exception as e:
            print(e)
            messagebox.showerror("Erro", "Erro ao imprimir ticket")
            return

    def update_entry_list():
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT placa, data FROM entry")
            entries = cursor.fetchall()
            tree.delete(*tree.get_children())
            # listbox.delete(0, tk.END)  # Clear the current list

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

    label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="PÁTIO ATUAL", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    tree = tk.ttk.Treeview(master=fr,
                           columns=("Placa", "Data de Entrada"))
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


def config():
    import customtkinter
    import tkinter as tk
    from tkinter import messagebox
    import sqlite3

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

    fr = customtkinter.CTkFrame(master=rt)
    fr.pack(pady=40, padx=120, fill="both", expand=True)

    def users():
        def add_user():
            adddetails_window = tk.Toplevel(rt)
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
                    conn.close()
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

            entry2 = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Senha", show="*")
            entry2.pack(pady=12, padx=10)

            combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40, values=["OPERADOR", "GERENTE"])
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

                cursor.execute("SELECT full_name, username, password, role FROM users")
                users = cursor.fetchall()
                tree.delete(*tree.get_children())
                for user in users:
                    tree.insert('', tk.END, values=(user[0], user[1], user[2], user[3]))

                conn.close()

                # Unbind the previous event bindings
            except sqlite3.Error as e:
                print("SQLite error:", e)

        def open_users_details(event):
            selected_item = tree.selection()[0]  # Get the selected item's ID
            selected_entry = tree.item(selected_item, "values")
            details_window = tk.Toplevel(rt)
            details_window.title("Users Detail")
            details_window.geometry("400x450")
            details_window.configure(bg="#212121")
            print(selected_item)
            # Get the selected entry details
            selected_full_name = selected_entry[0]
            print(selected_full_name)
            selected_username = selected_entry[1]
            print(selected_username)
            selected_password = selected_entry[2]
            print(selected_password)
            selected_role = selected_entry[3]
            print(selected_role)

            def cancel():
                details_window.destroy()

            def update_user():
                try:
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        "UPDATE users SET full_name=?, username=?, password=?, role=? WHERE id=?",
                        (firstname.get(), entry1.get(), entry2.get(), combo.get(), selected_id))
                    messagebox.showinfo(
                        "Sucesso", "Usuário atualizado com sucesso!")
                    details_window.destroy()
                    update_user_list()

                    conn.commit()
                    conn.close()

                except sqlite3.Error as e:
                    print("SQLite error:", e)

            label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                           text="Alterar Usuário")
            label.pack(pady=12, padx=10)

            firstname = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Nome Completo")
            firstname.pack(pady=12, padx=10)

            entry1 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Usuário")
            entry1.pack(pady=12, padx=10)

            entry2 = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Senha", show="*")
            entry2.pack(pady=12, padx=10)

            combo = customtkinter.CTkComboBox(details_window, width=300, height=40, values=["OPERADOR", "GERENTE"])
            combo.pack(pady=12, padx=10)

            button = customtkinter.CTkButton(details_window, width=300, height=40, text="CADASTRAR",
                                             command=update_user)
            button.pack(pady=12, padx=24)

            button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                              command=cancel)
            button1.pack(pady=12, padx=10)

            entry1.insert(0, selected_username)
            entry2.insert(0, selected_password)
            firstname.insert(0, selected_full_name)
            combo.set(selected_role)

        user_window = tk.Toplevel(rt)
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
        treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)  # Change side to 'right' and fill to 'y'
        tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)

        # Call the function to update the Listbox with existing entries
        update_user_list()

        tree.bind("<Double-1>", open_users_details)

    def price():
        def insert_price():
            try:
                carencia_val = carencia_entry.get()
                primeira_faixa_val = primeira_faixa_entry.get()
                demais_faixas_val = demais_faixas_entry.get()
                primeira_faixa_min_val = primeira_faixa_min_entry.get()
                demais_faixas_min_val = demais_faixas_min_entry.get()
                print(carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,
                      demais_faixas_val)

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
                    cursor.execute(
                        "UPDATE price SET carencia=?, primeira_faixa=?, primeira_faixa_min=?,demais_faixas_min=?, demais_faixas=? WHERE id=?",
                        (carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,
                         demais_faixas_val,
                         row[0]))
                    messagebox.showinfo(
                        "Sucesso", "Valores da tabela de preço atualizados com sucesso!")
                    price_window.destroy()
                else:
                    cursor.execute(
                        "INSERT INTO price (carencia, primeira_faixa,primeira_faixa_min,demais_faixas_min,  demais_faixas) VALUES (?, ?, ?, ? , ?)",
                        (
                            carencia_val, primeira_faixa_val, primeira_faixa_min_val, demais_faixas_min_val,
                            demais_faixas_val))
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

    def texts():
        def add_user():
            adddetails_window = tk.Toplevel(rt)
            adddetails_window.title("Adicionar Usuário")
            adddetails_window.geometry("400x450")
            adddetails_window.configure(bg="#212121")

            def cancel():
                adddetails_window.destroy()

            def adicionar_user():
                try:
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS texts (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       text TEXT,
                                       type TEXT
                                   )''')

                    text_value = text_entry.get()
                    type_value = combo.get()

                    cursor.execute('INSERT INTO texts (text, type) VALUES (?, ?)',
                                   (text_value, type_value))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo(
                        "Sucesso", "Texto cadastrado com sucesso!")
                    adddetails_window.destroy()
                    update_user_list()

                except sqlite3.Error as e:
                    print("SQLite error:", e)

            label = customtkinter.CTkLabel(adddetails_window, width=300, height=40, font=("Roboto", 36),
                                           text="Adicionar Frase")
            label.pack(pady=12, padx=10)

            text_entry = customtkinter.CTkEntry(adddetails_window, width=300, height=40, placeholder_text="Texto")
            text_entry.pack(pady=12, padx=10)

            combo = customtkinter.CTkComboBox(adddetails_window, width=300, height=40, values=["TICKET", "RECIBO"])
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

                cursor.execute("SELECT  text, type,id FROM texts")
                texts = cursor.fetchall()

                tree.delete(*tree.get_children())
                for text in texts:
                    tree.insert('', tk.END, values=(text[0], text[1], text[2]))

                conn.close()


            except sqlite3.Error as e:
                print("SQLite error:", e)

        def open_texts_details(selected_item):
            selected_item = tree.selection()[0]  # Get the selected item's ID
            selected_entry = tree.item(selected_item, "values")
            details_window = tk.Toplevel(rt)
            details_window.title("Texts Detail")
            details_window.geometry("400x450")
            details_window.configure(bg="#212121")
            print(selected_item)
            # Get the selected entry details
            selected_text = selected_entry[0]
            selected_type = selected_entry[1]
            selected_id = selected_entry[2]

            def cancel():
                details_window.destroy()

            def update_user():
                try:
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        "UPDATE texts SET text=?, type=? WHERE id=?",
                        (text.get(), combo.get(), selected_id))
                    messagebox.showinfo(
                        "Sucesso", "Frase atualizada com sucesso!")
                    details_window.destroy()
                    update_user_list()

                    conn.commit()
                    conn.close()

                except sqlite3.Error as e:
                    print("SQLite error:", e)

            label = customtkinter.CTkLabel(details_window, width=300, height=40, font=("Roboto", 36),
                                           text="Alterar Frase")
            label.pack(pady=12, padx=10)

            text = customtkinter.CTkEntry(details_window, width=300, height=40, placeholder_text="Texto")
            text.pack(pady=12, padx=10)

            combo = customtkinter.CTkComboBox(details_window, width=300, height=40, values=["TICKET", "RECIBO"])
            combo.pack(pady=12, padx=10)

            button = customtkinter.CTkButton(details_window, width=300, height=40, text="ATUALIZAR",
                                             command=update_user)
            button.pack(pady=12, padx=24)

            button1 = customtkinter.CTkButton(details_window, width=300, height=40, text="CANCELAR", fg_color='#91403d',
                                              command=cancel)
            button1.pack(pady=12, padx=10)

            text.insert(0, selected_text)
            combo.set(selected_type)

        user_window = tk.Toplevel(rt)
        user_window.title("Lista de Frases")
        user_window.geometry("600x450")
        user_window.configure(bg="#212121")

        button_add = customtkinter.CTkButton(
            user_window, width=240, height=32, text="ADICIONAR FRASES", command=add_user)
        button_add.pack(pady=12, padx=10)

        tree = tk.ttk.Treeview(user_window,
                               columns=("TEXTO", "TIPO"))
        tree['show'] = 'headings'
        tree.heading("#1", text="TEXTO")
        tree.heading("#2", text="TIPO")

        # Set column widths
        tree.column("#1", width=400)
        tree.column("#2", width=150)

        treeScroll = tk.Scrollbar(user_window)
        treeScroll.configure(command=tree.yview)
        tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
        tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

        # Call the function to update the Listbox with existing entries
        update_user_list()

        tree.bind("<Double-1>", open_texts_details)

    label = customtkinter.CTkLabel(master=fr, text="CONFIGURAÇÕES", font=("Roboto", 32))
    label.pack(padx=(10, 10), pady=(150, 20), )

    button_users = customtkinter.CTkButton(
        master=fr, width=480, height=48, text="USUÁRIOS", command=users)
    button_users.pack(pady=12, padx=10)

    button_price = customtkinter.CTkButton(
        master=fr, width=480, height=48, text="TABELA DE PREÇO", command=price)
    button_price.pack(pady=12, padx=10)

    button_price = customtkinter.CTkButton(
        master=fr, width=480, height=48, text="FRASES TICKET", command=texts)
    button_price.pack(pady=12, padx=10)

    rt.mainloop()


def report():
    import customtkinter
    import os
    import sqlite3
    from datetime import datetime
    import tkinter as tk
    from tkinter import messagebox, filedialog
    import locale
    import qrcode
    from PIL import Image, ImageTk
    from win32printing import Printer
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from openpyxl import Workbook
    from tkcalendar import Calendar, DateEntry

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    rt = customtkinter.CTk()
    rt.after(0, lambda: rt.state('zoomed'))

    def update_entry_list(start_date, end_date):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total,pagamento  FROM history WHERE data_entrada BETWEEN ? AND ?",
                (start_date, end_date))
            entries = cursor.fetchall()
            print(entries)
            tree.delete(*tree.get_children())
            # Clear existing items in the Treeview
            for item in tree.get_children():
                tree.delete(item)

            for entry in entries:
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento = entry
                tree.insert('', tk.END, values=(placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento))

            conn.close()

        except sqlite3.Error as e:
            print("SQLite error:", e)

    def export_pdf():
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.pdf"
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename,
                                                    filetypes=[("PDF Files", "*.pdf")])
            if not filename:
                return

            doc = SimpleDocTemplate(filename, pagesize=letter)
            data = []

            header = ("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento")
            data.append(header)

            for entry in tree.get_children():
                values = tree.item(entry)['values']
                data.append(values)

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            doc.build([table])

            messagebox.showinfo("Export PDF", "Dados exportados para PDF com sucesso!")

        except Exception as e:
            print("Erro ao exportar para PDF:", e)

    def export_excel():
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.xlsx"
            filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename,
                                                    filetypes=[("Excel Files", "*.xlsx")])
            if not filename:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório"

            header = ["Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento"]
            ws.append(header)

            for entry in tree.get_children():
                values = tree.item(entry)['values']
                ws.append(values)

            wb.save(filename)
            messagebox.showinfo("Export Excel", "Dados exportados para Excel com sucesso!")

        except Exception as e:
            print("Erro ao exportar para Excel:", e)

    def generate_report():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        print(start_datetime)
        print(end_datetime)

        update_entry_list(start_datetime, end_datetime)

    fr = customtkinter.CTkFrame(master=rt)
    fr.pack(pady=40, padx=120, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="RELATÓRIO", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    datesFrame = customtkinter.CTkFrame(master=fr)
    datesFrame.pack(pady=10, padx=10, anchor="center")

    start_date_label = customtkinter.CTkLabel(datesFrame, text="Data Inicial:")
    start_date_label.pack(padx=(10, 10), pady=5, side="left")

    start_date_entry = DateEntry(datesFrame, width=16, background="magenta3", foreground="white", bd=2, locale="pt_br")
    start_date_entry.pack(padx=(0, 40), pady=5, anchor="w", side="left")

    end_date_label = customtkinter.CTkLabel(datesFrame, text="Data Final:")
    end_date_label.pack(padx=(10, 10), pady=5, anchor="w", side="left")

    end_date_entry = DateEntry(datesFrame, width=16, background="magenta3", foreground="white", bd=2, locale="pt_br")
    end_date_entry.pack(padx=(0, 40), pady=5, anchor="w", side="left")

    generate_button = customtkinter.CTkButton(datesFrame, width=140, height=40, text="GERAR", command=generate_report)
    generate_button.pack(pady=10, padx=10, anchor="e", side="left")

    generate = customtkinter.CTkFrame(master=fr)
    generate.pack(pady=10, padx=10, anchor="e")

    button = customtkinter.CTkButton(generate, width=120, height=24, text="EXPORTAR PDF", command=export_pdf)
    button.pack(padx=10, pady=10, side="left")

    button1 = customtkinter.CTkButton(generate, width=120, height=24, text="EXPORTAR EXCEL", command=export_excel)
    button1.pack(padx=10, pady=10, side="left")

    tree = tk.ttk.Treeview(master=fr,
                           columns=("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago",
                                    "Pagamento"))
    tree['show'] = 'headings'
    tree.heading("#1", text="Placa")
    tree.heading("#2", text="Data de Entrada")
    tree.heading("#3", text="Data de Saída")
    tree.heading("#4", text="Tempo de Permanência")
    tree.heading("#5", text="Valor Pago")
    tree.heading("#6", text="Pagamento")

    # Set column widths
    tree.column("#1", width=100)
    tree.column("#2", width=150)
    tree.column("#3", width=150)
    tree.column("#4", width=150)
    tree.column("#5", width=150)
    tree.column("#6", width=150)

    treeScroll = tk.Scrollbar(master=fr)
    treeScroll.configure(command=tree.yview)
    treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

    tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)

    rt.mainloop()


def control():
    import customtkinter
    import os
    from PIL import Image

    class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
        def __init__(self, master, command=None, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_columnconfigure(0, weight=1)

            self.command = command
            self.radiobutton_variable = customtkinter.StringVar()
            self.label_list = []
            self.button_list = []

        def add_item(self, item, image=None):
            label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
            button = customtkinter.CTkButton(self, text="Command", width=100, height=24)
            if self.command is not None:
                button.configure(command=lambda: self.command(item))
            label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
            button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
            self.label_list.append(label)
            self.button_list.append(button)

        def remove_item(self, item):
            for label, button in zip(self.label_list, self.button_list):
                if item == label.cget("text"):
                    label.destroy()
                    button.destroy()
                    self.label_list.remove(label)
                    self.button_list.remove(button)
                    return

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            self.title("CTkScrollableFrame example")
            self.grid_rowconfigure(0, weight=1)
            self.columnconfigure(2, weight=1)

            # create scrollable label and button frame
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300,
                                                                            command=self.label_button_frame_event,
                                                                            corner_radius=0)
            self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
            for i in range(20):  # add items with images
                self.scrollable_label_button_frame.add_item(f"image and item {i}", image=customtkinter.CTkImage(
                    Image.open(os.path.join(current_dir, "test_images", "chat_light.png"))))

        def label_button_frame_event(self, item):
            print(f"label button frame clicked: {item}")

    if __name__ == "__main__":
        customtkinter.set_appearance_mode("dark")
        app = App()
        app.mainloop()

login_screen()
