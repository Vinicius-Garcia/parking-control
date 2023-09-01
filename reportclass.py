import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
from tkcalendar import Calendar, DateEntry
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Report(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()
        self.total_frame = customtkinter.CTkFrame(master=self.generate2)
        self.total_frame.pack(pady=10, padx=10, anchor="e")

        self.total_pix_label = customtkinter.CTkLabel(self.total_frame, text="Pix: R$0.00")
        self.total_pix_label.pack(padx=10, pady=10, side="left")

        self.total_cash_label = customtkinter.CTkLabel(self.total_frame, text="Dinheiro: R$0.00")
        self.total_cash_label.pack(padx=10, pady=10, side="left")

        self.total_card_label = customtkinter.CTkLabel(self.total_frame, text="Cartão: R$0.00")
        self.total_card_label.pack(padx=10, pady=10, side="left")


    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="RELATÓRIO", font=("Roboto", 24))
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

        self.send_email_button = customtkinter.CTkButton(self.generate1, width=120, height=24, text="ENVIAR E-MAIL",
                                                         command=self.send_email)
        self.send_email_button.pack(padx=10, pady=10, side="left")

        self.tree = tk.ttk.Treeview(master=fr,
                               columns=(
                               "Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago",
                               "Pagamento"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Data de Saída")
        self.tree.heading("#4", text="Tempo de Permanência")
        self.tree.heading("#5", text="Valor Pago")
        self.tree.heading("#6", text="Pagamento")

        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)
        self.tree.column("#4", width=150)
        self.tree.column("#5", width=150)
        self.tree.column("#6", width=150)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)



    def update_entry_list(self, start_date, end_date):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total,pagamento, veiculo  FROM history WHERE data_saida BETWEEN ? AND ?",
                (start_date, end_date))
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for item in self.tree.get_children():
                self.tree.delete(item)

            for entry in entries:
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo = entry
                self.tree.insert('', tk.END, values=(placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo))

            cursor.close()


        except sqlite3.Error as e:
            print("SQLite error:", e)

    def export_pdf(self):
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.pdf"
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename,
                                                    filetypes=[("PDF Files", "*.pdf")])
            if not filename:
                return

            doc = SimpleDocTemplate(filename, pagesize=letter)
            data = []

            header = ("Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento", "Veiculo")
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

            header = ["Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago", "Pagamento", "Veiculos"]
            ws.append(header)

            for entry in self.tree.get_children():
                values = self.tree.item(entry)['values']
                ws.append(values)

            wb.save(filename)
            messagebox.showinfo("Export Excel", "Dados exportados para Excel com sucesso!")

        except Exception as e:
            print("Erro ao exportar para Excel:", e)

    def generate_report(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        self.update_entry_list(start_datetime, end_datetime)

        # Initialize instance variables to store totals and counts for each payment method
        self.total_pix = 0
        self.total_cash = 0
        self.total_card = 0
        self.count_pix = 0
        self.count_cash = 0
        self.count_card = 0

        for entry in self.tree.get_children():
            values = self.tree.item(entry)['values']
            valor_total = float(values[4])  # Valor total está no índice 4
            pagamento = values[5]  # Tipo de pagamento está no índice 5

            if pagamento == "PIX":
                self.total_pix += valor_total
                self.count_pix += 1
            elif pagamento == "DINHEIRO":
                self.total_cash += valor_total
                self.count_cash += 1
            elif pagamento == "CARTÃO":
                self.total_card += valor_total
                self.count_card += 1

        self.total_pix_label.configure(text=f"Pix: R${self.total_pix:.2f} (Quantidade: {self.count_pix})")
        self.total_cash_label.configure(text=f"Dinheiro: R${self.total_cash:.2f} (Quantidade: {self.count_cash})")
        self.total_card_label.configure(text=f"Cartão: R${self.total_card:.2f} (Quantidade: {self.count_card})")

    def run(self):
        self.mainloop()

    def send_email(self):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'viniciusgarcia130@gmail.com'
        smtp_password = '@Qwertyuiop0'

        to_email = 'viniciusgarcia1300@gmail.com'

        subject = 'Relatório de Vendas'

        total_pix = 0
        total_cash = 0
        total_card = 0
        count_pix = 0
        count_cash = 0
        count_card = 0

        for entry in self.tree.get_children():
            values = self.tree.item(entry)['values']
            valor_total = float(values[4])
            pagamento = values[5]

            if pagamento == "PIX":
                total_pix += valor_total
                count_pix += 1
            elif pagamento == "DINHEIRO":
                total_cash += valor_total
                count_cash += 1
            elif pagamento == "CARTÃO":
                total_card += valor_total
                count_card += 1

        body = f"Total Pix: R${total_pix:.2f} (Quantidade: {count_pix})\n" \
               f"Total Dinheiro: R${total_cash:.2f} (Quantidade: {count_cash})\n" \
               f"Total Cartão: R${total_card:.2f} (Quantidade: {count_card})\n"


        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.sendmail(smtp_username, to_email, msg.as_string())

            server.quit()

            messagebox.showinfo("Envio de E-mail", "E-mail enviado com sucesso!")

        except Exception as e:
            print("Erro ao enviar o e-mail:", e)
            messagebox.showerror("Erro ao enviar E-mail", "Ocorreu um erro ao enviar o e-mail.")


if __name__ == "__main__":
    app = Report()
    app.run()