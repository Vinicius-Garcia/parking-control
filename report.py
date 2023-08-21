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
rt.geometry("900x600")


def update_entry_list(start_date, end_date):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total FROM history WHERE data_entrada BETWEEN ? AND ?",
            (start_date, end_date))
        entries = cursor.fetchall()
        print(entries)
        # Clear existing items in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        for entry in entries:
            placa, data_entrada, data_saida, tempo_estadia, valor_total = entry
            tree.insert('', tk.END, values=(placa, data_entrada, data_saida, tempo_estadia, valor_total))

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

        header = ("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago")
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

        header = ["Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago"]
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
fr.grid(row=0, column=0, padx=120, pady=40, sticky="nsew")

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="RELATÓRIO", font=("Roboto", 24))
label.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

start_date_label = customtkinter.CTkLabel(master=fr, text="Data Inicial:")
start_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")  # Place in row 4, column 0

start_date_entry = DateEntry(master=fr, width=16, background="magenta3", foreground="white", bd=2, locale="pt_br")
start_date_entry.grid(row=2, column=0, padx=(80, 0), pady=5, sticky="w")  # Place in row 4, column 1

end_date_label = customtkinter.CTkLabel(master=fr, text="Data Final:")
end_date_label.grid(row=2, column=1, padx=0, pady=5, sticky="w")  # Place in row 4, column 2

end_date_entry = DateEntry(master=fr, width=16, background="magenta3", foreground="white", bd=2, locale="pt_br")
end_date_entry.grid(row=2, column=1, padx=(80, 0), pady=5, sticky="w")  # Place in row 4, column 3

generate_button = customtkinter.CTkButton(master=fr, width=240, height=40, text="GERAR", command=generate_report)
generate_button.grid(row=3, column=0, pady=10)  # Place in row 4, starting from column 4

tree = tk.ttk.Treeview(master=fr,
                       columns=("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago"))
tree['show'] = 'headings'
tree.heading("#1", text="Placa")
tree.heading("#2", text="Data de Entrada")
tree.heading("#3", text="Data de Saída")
tree.heading("#4", text="Tempo de Permanência")
tree.heading("#5", text="Valor Pago")

# Set column widths
tree.column("#1", width=100)
tree.column("#2", width=150)
tree.column("#3", width=150)
tree.column("#4", width=150)
tree.column("#5", width=150)

tree.grid(row=6, column=0, columnspan=2, padx=10, pady=12, sticky="nsew")

button = customtkinter.CTkButton(master=fr, width=240, height=40, text="EXPORTAR PDF", command=export_pdf)
button.grid(row=7, column=0, padx=10, pady=10)

button1 = customtkinter.CTkButton(master=fr, width=240, height=40, text="EXPORTAR EXCEL", command=export_excel)
button1.grid(row=7, column=1, padx=10, pady=10)

rt.mainloop()
