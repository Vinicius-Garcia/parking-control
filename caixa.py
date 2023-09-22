import sqlite3
from tkinter import ttk, messagebox, filedialog
import customtkinter
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib import colors
from openpyxl import Workbook
from tkcalendar import Calendar, DateEntry
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class Caixa(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()

        self.total_frame = customtkinter.CTkFrame(master=self.generate2)
        self.total_frame.pack(pady=10, padx=10, anchor="e")

        self.total_label = customtkinter.CTkLabel(self.total_frame, text="Total: R$0.00")
        self.total_label.pack(padx=10, pady=10, side="left")

        self.mainloop()

    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="CAIXA", font=("Roboto", 24))
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

        self.generate_button = customtkinter.CTkButton(self.datesFrame, width=140, height=40, text="BUSCAR OPERAÇOES",
                                                       command=self.generate_report)
        self.generate_button.pack(pady=10, padx=10, anchor="e", side="left")

        self.entry = customtkinter.CTkButton(self.datesFrame, width=140, height=40, text="BUSCAR OPERAÇOES",
                                                       command=self.registrar_entrada)
        self.entry.pack(pady=10, padx=10, anchor="e", side="left")
        self.exit = customtkinter.CTkButton(self.datesFrame, width=140, height=40, text="BUSCAR OPERAÇOES",
                                                       command=self.registrar_saida)
        self.exit.pack(pady=10, padx=10, anchor="e", side="left")

        self.generate = customtkinter.CTkFrame(master=fr)
        self.generate.pack(pady=10, padx=10, fill="both")

        self.generate2 = customtkinter.CTkFrame(self.generate)
        self.generate2.pack(pady=10, padx=10, anchor="w", side="left")

        self.generate1 = customtkinter.CTkFrame(self.generate)
        self.generate1.pack(pady=10, padx=10, anchor="e", side="right")

        self.button = customtkinter.CTkButton(self.generate1, width=120, height=24, text="EXPORTAR PDF",
                                              command=self.export_pdf)
        self.button.pack(padx=10, pady=10, side="left")

        self.button1 = customtkinter.CTkButton(self.generate1, width=120, height=24, text="EXPORTAR EXCEL",
                                               command=self.export_excel)
        self.button1.pack(padx=10, pady=10, side="left")


        self.tree = tk.ttk.Treeview(master=fr,
                                    columns=(
                                        "Operação", "Valor", "Usuário", "Data da Operação"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Operação")
        self.tree.heading("#2", text="Valor")
        self.tree.heading("#3", text="Usuário")
        self.tree.heading("#4", text="Data da Operação")

        self.tree.column("#1", width=50)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=100)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)

    def generate_report(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        self.update_entry_list(start_datetime, end_datetime)

    def update_entry_list(self, start_date, end_date):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            start_datetime = f"{start_date} 00:00:00"
            end_datetime = f"{end_date} 23:59:59"

            cursor.execute(
                "SELECT operacao, valor, usuario, data_operacao FROM caixa WHERE data_operacao >= ? AND data_operacao <= ?",
                (start_datetime, end_datetime))
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for item in self.tree.get_children():
                self.tree.delete(item)

            for entry in entries:
                operacao, valor, usuario, data_operacao= entry
                self.tree.insert('', tk.END, values=(operacao, valor, usuario, data_operacao))

            cursor.close()


        except sqlite3.Error as e:
            print("SQLite error:", e)

    def registrar_entrada(self):
        placa = input("Digite a placa do veículo: ")
        data_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_saida = ""

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO caixa (placa, data_entrada, data_saida) VALUES (?, ?, ?)",
                       (placa, data_entrada, data_saida))
        self.conn.commit()

        self.update_treeview()

    def registrar_saida(self):
        selected_item = self.tree.selection()
        if selected_item:
            placa = self.tree.item(selected_item, "values")[0]
            data_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor = self.conn.cursor()
            cursor.execute("UPDATE caixa SET data_saida = ? WHERE placa = ? AND data_saida = ''",
                           (data_saida, placa))
            self.conn.commit()

            self.update_treeview()

    def export_pdf(self):
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.pdf"
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename,
                                                    filetypes=[("PDF Files", "*.pdf")])
            if not filename:
                return

            doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
            data = []

            header = ("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento", "Veiculo", "Operador Entrada", "Operador Saida")
            data.append(header)

            for entry in self.tree.get_children():
                values = self.tree.item(entry)['values']
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

    def export_excel(self):
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.xlsx"
            filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_filename,
                                                    filetypes=[("Excel Files", "*.xlsx")])
            if not filename:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório"

            header = ["Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento", "Veiculo", "Operador Entrada", "Operador Saida"]
            ws.append(header)

            for entry in self.tree.get_children():
                values = self.tree.item(entry)['values']
                ws.append(values)

            wb.save(filename)
            messagebox.showinfo("Export Excel", "Dados exportados para Excel com sucesso!")

        except Exception as e:
            print("Erro ao exportar para Excel:", e)


if __name__ == "__main__":
    app = Caixa()
