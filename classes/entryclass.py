import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
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
        return False

class Entry(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.vehicle_type = tk.StringVar()
        self.vehicle_type.set("CARRO")
        self.setup_ui()
        self.mainloop()
    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="DAR ENTRADA", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.search = customtkinter.CTkFrame(master=fr)
        self.search.pack(pady=40, padx=120)

        self.labelplaca = customtkinter.CTkLabel(self.search, width=120, height=32, text="PLACA:", font=("Roboto", 18))
        self.labelplaca.pack(pady=12, padx=10, side="left")

        self.entry1 = customtkinter.CTkEntry(self.search, width=240, height=32, placeholder_text="PLACA",
                                             validate="key",
                                             validatecommand=(self.register(validate_length), '%P'))
        self.entry1.pack(pady=12, padx=10, side="left")
        self.entry1.focus()  # Set the focus to the license plate input field
        self.entry1.bind("<Return>", self.send_entry_and_open_print)  # Bind Enter key to send entry and open print

        self.vehicle_checkbox = customtkinter.CTkCheckBox(self.search, text="MOTO", variable=self.vehicle_type,
                                                          onvalue="MOTO", offvalue="CARRO")
        self.vehicle_checkbox.pack(pady=12, padx=10, side="left")

        self.button = customtkinter.CTkButton(self.search, width=240, height=32, text="DAR ENTRADA",
                                              command=self.send_entry)
        self.button.pack(pady=12, padx=10, side="left")

        self.tree = tk.ttk.Treeview(master=fr,
                               columns=("Placa", "Data de Entrada", "Veiculo"), selectmode="browse")

        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Veiculo")

        # Set column widths
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=50)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='y')  # Change side to 'right' and fill to 'y'
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        self.treeScroll.pack(side='right', fill='y', padx=(0, 10), pady=10)

        # Call the function to update the Listbox with existing entries
        self.update_entry_list()

        self.tree.bind("<Double-1>", self.open_entry_details)
    def plate_exists(self,placa):
            conn = sqlite3.connect('../user_data.db')
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

    def send_entry(self):
        placa = self.entry1.get()
        veiculo = self.vehicle_type.get()

        try:
            conn = sqlite3.connect('../user_data.db')
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                             (placa TEXT, data TEXT, veiculo TEXT)''')

            if self.plate_exists(placa):
                cursor.close()
                messagebox.showwarning("Plate Exists", "Plate already exists in the database.")
                return

            data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            cursor.execute("INSERT INTO entry (placa, data, veiculo) VALUES (?, ?, ?)", (placa, data_atual, veiculo))

            conn.commit()  # Commit the changes to the database

            self.update_entry_list()  # Update the UI
            cursor.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)


        # Function to open a new window and display selected entry details
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

            self.button = customtkinter.CTkButton(details_frame, width=240, height=32, text="IMPRIMIR TICKET",
                                             command=lambda: self.print_entry(selected_entry, formatted_time))
            self.button.pack(pady=12, padx=10)


    def draw_img(self,hdc, dib, maxh, maxw, y_position):
            w, h = dib.size
            print("Image HW: ({:d}, {:d}), Max HW: ({:d}, {:d})".format(h, w, maxh, maxw))
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


    def print_entry(self,placa, data):
            conn = sqlite3.connect('../user_data.db')
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

            for text in padrão_superior_texts:
                text_content, _, ordem = text
                x_position = 0  # Starting x-position for the text
                y_position += 40  # Calculate y-position based on ordem value

                print(y_position)
                print(text_content)

                # Draw the text
                pdc.TextOut(x_position, y_position, text_content)

            y_position += 50  # Adjust y-position after PADRÃO SUPERIOR text

            # Draw QR code centered
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

            print(width)

            y_position += 250  # Adjust y-position after QR code

            pdc.TextOut(0, y_position, "PLACA: ")
            pdc.TextOut((width - pdc.GetTextExtent(placa)[0]), y_position, placa)
            y_position += 50  # Adjust y-position after PLACA text
            pdc.TextOut(0, y_position, "DATA/HORA: ")
            pdc.TextOut((width - pdc.GetTextExtent(data)[0]), y_position, data)
            y_position += 20
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


    def update_entry_list(self):
            try:
                conn = sqlite3.connect('../user_data.db')
                cursor = conn.cursor()
                cursor.execute("SELECT placa, data, veiculo FROM entry")
                entries = cursor.fetchall()
                self.tree.delete(*self.tree.get_children())
                # listbox.delete(0, tk.END)  # Clear the current list
                cursor.close()
                for entry in entries:
                    entry_str = f"Placa: {entry[0]} - Data: {entry[1]} - Veiculo: {entry[2]}"
                    self.tree.insert('', tk.END, values=(entry[0], entry[1], entry[2]))


            except sqlite3.Error as e:
                print("SQLite error:", e)


    def handle_listbox_click(self):
            selected_indices = self.listbox.curselection()
            if selected_indices:
                selected_index = selected_indices[0]  # Get the first selected index
                selected_item = self.listbox.get(selected_index)
                self.open_entry_details(selected_item)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = Entry()
    app.run()

