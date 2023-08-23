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
rt.after(0, lambda:rt.state('zoomed'))


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
start_date_label.pack(padx=(10,10), pady=5, side="left")

start_date_entry = DateEntry(datesFrame, width=16, background="magenta3", foreground="white", bd=2, locale="pt_br")
start_date_entry.pack(padx=(0,40), pady=5, anchor="w", side="left" )

end_date_label = customtkinter.CTkLabel(datesFrame, text="Data Final:")
end_date_label.pack(padx=(10,10), pady=5, anchor="w", side="left")

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
                       columns=("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento"))
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
