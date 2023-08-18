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

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("1200x600")

def update_entry_list():
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total FROM history")
        entries = cursor.fetchall()

        # Clear existing items in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        for entry in entries:
            placa, data_entrada, data_saida, tempo_estadia, valor_total = entry
            tree.insert('', tk.END, values=(placa, data_entrada, data_saida, tempo_estadia,valor_total ))

        conn.close()

    except sqlite3.Error as e:
        print("SQLite error:", e)

def export_pdf():
    try:
        default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.pdf"
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename, filetypes=[("PDF Files", "*.pdf")])
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
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename, filetypes=[("Excel Files", "*.xlsx")])
        if not filename:
            return
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Relatório"
        
        header = ["Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago" ]
        ws.append(header)
        
        for entry in tree.get_children():
            values = tree.item(entry)['values']
            ws.append(values)
        
        wb.save(filename)
        messagebox.showinfo("Export Excel", "Dados exportados para Excel com sucesso!")

    except Exception as e:
        print("Erro ao exportar para Excel:", e)

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="RELATÓRIO", font=("Roboto", 24))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=240, height=32, text="EXPORTAR PDF", command=export_pdf)
button.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=fr, width=240, height=32, text="EXPORTAR EXCEL", command=export_excel)
button1.pack(pady=12, padx=10)

tree = tk.ttk.Treeview(master=fr, columns=("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago"))
tree['show'] = 'headings'
tree.heading("#1", text="Placa")
tree.heading("#2", text="Data de Entrada")
tree.heading("#3", text="Data de Saída")
tree.heading("#4", text="Tempo de Permanência")
tree.heading("#5", text="Valor Pago")

# Set column widths
tree.column("#1", width=40)
tree.column("#2", width=150)
tree.column("#3", width=150)
tree.column("#4", width=150)
tree.column("#5", width=150)

tree.pack(pady=12, padx=10, fill="both", expand=True)

update_entry_list()

rt.mainloop()
