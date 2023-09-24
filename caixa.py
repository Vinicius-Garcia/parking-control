import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    def __init__(self, user):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()
        self.user = user
        self.total_deposito = 0.0
        self.total_retirada = 0.0
        self.total_geral = 0.0




        self.mainloop()

    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="CAIXA", font=("Roboto", 24))
        label.pack(pady=12, padx=10)

        self.search = customtkinter.CTkFrame(master=fr)
        self.search.pack(pady=10, padx=10, fill="both")

        self.search1 = customtkinter.CTkFrame(self.search)
        self.search1.pack(pady=10, padx=10, anchor="w", side="left")

        self.search2 = customtkinter.CTkFrame(self.search)
        self.search2.pack(pady=10, padx=10, anchor="e", side="right")



        self.datesFrame = customtkinter.CTkFrame(self.search1)
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

        self.entry = customtkinter.CTkButton(self.search2, width=140, height=40, text="RETIRADA", fg_color='#91403d',
                                                       command=self.registrar_saida)
        self.entry.pack(pady=10, padx=10, anchor="e", side="left")
        self.exit = customtkinter.CTkButton(self.search2, width=140, height=40, text="DEPÓSITO",fg_color='#3d9b39',
                                                       command=self.registrar_entrada)
        self.exit.pack(pady=10, padx=10, anchor="e", side="left")

        self.generate = customtkinter.CTkFrame(master=fr)
        self.generate.pack(pady=10, padx=10, fill="both")

        self.generate2 = customtkinter.CTkFrame(self.generate)
        self.generate2.pack(pady=10, padx=10, anchor="w", side="left")

        self.generate1 = customtkinter.CTkFrame(self.generate)
        self.generate1.pack(pady=10, padx=10, anchor="e", side="right")

        self.total_frame = customtkinter.CTkFrame(master=self.generate2)
        self.total_frame.pack(pady=10, padx=10, anchor="e")

        self.totaldeposito_label = customtkinter.CTkLabel(self.total_frame, text="Total de Depósito: R$0.00")
        self.totaldeposito_label.pack(padx=10, pady=10, side="left")

        self.totalsaque_label = customtkinter.CTkLabel(self.total_frame, text="Total de Depósito: R$0.00")
        self.totalsaque_label.pack(padx=10, pady=10, side="left")

        self.total_label = customtkinter.CTkLabel(self.total_frame, text="Total de Depósito: R$0.00")
        self.total_label.pack(padx=10, pady=10, side="left")




        self.button = customtkinter.CTkButton(self.generate1, width=120, height=24, text="EXPORTAR PDF",
                                              command=self.export_pdf)
        self.button.pack(padx=10, pady=10, side="left")

        self.button1 = customtkinter.CTkButton(self.generate1, width=120, height=24, text="EXPORTAR EXCEL",
                                               command=self.export_excel)
        self.button1.pack(padx=10, pady=10, side="left")

        self.button2 = customtkinter.CTkButton(self.generate1, width=120, height=24, text="ENVIAR EMAIL",
                                               command=self.send_email)
        self.button2.pack(padx=10, pady=10, side="left")




        self.tree = tk.ttk.Treeview(master=fr,
                                    columns=(
                                        "Operação", "Valor", "Usuário", "Data da Operação", "Observação"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Operação")
        self.tree.heading("#2", text="Valor")
        self.tree.heading("#3", text="Usuário")
        self.tree.heading("#4", text="Data da Operação")
        self.tree.heading("#5", text="Observação")

        self.tree.column("#1", width=50)
        self.tree.column("#2", width=50)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=200)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)


        self.generate_report()

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
                "SELECT operacao, valor, usuario, data_operacao, observacao FROM caixa WHERE data_operacao >= ? AND data_operacao <= ?",
                (start_datetime, end_datetime))
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())

            self.total_deposito = 0.0
            self.total_retirada = 0.0

            for entry in entries:
                operacao, valor, usuario, data_operacao, observacao = entry
                self.tree.insert('', tk.END, values=(operacao, valor, usuario, data_operacao, observacao))

                valor = float(valor)
                # Calcule os totais com base na operação
                if operacao == 'DEPÓSITO':
                    self.total_deposito += valor
                elif operacao == 'RETIRADA':
                    self.total_retirada += valor

            self.total_geral = self.total_deposito - self.total_retirada
            self.update_total_labels()  # Chame esta função para atualizar os rótulos dos totais

            cursor.close()

        except sqlite3.Error as e:
            print("SQLite error:", e)

    def update_total_labels(self):
        self.totaldeposito_label.configure(text=f"Total de Depósito: R${self.total_deposito:.2f}")
        self.totalsaque_label.configure(text=f"Total de Retirada: R${self.total_retirada:.2f}")
        self.total_label.configure(text=f"Total: R${self.total_geral:.2f}")

    def registrar_saida(self):
        def insert_value(operation):
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                valor = value_entry.get()
                observacao = obs_entry.get()
                data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                usuario = self.user[1]
                operacao = operation

                cursor.execute(
                    "INSERT INTO caixa (operacao, valor, usuario, data_operacao, observacao) VALUES (?, ?, ?, ?, ?)",
                    (operacao, valor, usuario, data_atual, observacao))

                conn.commit()
                conn.close()

                start_datetime = self.start_date_entry.get()
                end_datetime = self.end_date_entry.get()
                self.update_entry_list(start_datetime, end_datetime)

                # Feche a janela após a inserção
                price_window.destroy()
            except sqlite3.Error as e:
                print("SQLite error:", e)

        price_window = tk.Toplevel(self)
        price_window.title("SAQUE")
        price_window.geometry("400x700")
        price_window.configure(bg="#212121")

        label = customtkinter.CTkLabel(price_window, width=300, height=40, font=("Roboto", 36),
                                       text="REGISTRAR RETIRADA")
        label.pack(pady=12, padx=10)

        value = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Valor:")
        value.pack(pady=6, padx=10)

        value_entry = customtkinter.CTkEntry(price_window, width=240)
        value_entry.pack(pady=6, padx=10)

        obs_label = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Observação :")
        obs_label.pack(pady=6, padx=10)

        obs_entry = customtkinter.CTkEntry(price_window, width=240)
        obs_entry.pack(pady=6, padx=10)


        insert_button = customtkinter.CTkButton(
            price_window, width=240, height=32, text="Inserir", command=lambda: insert_value('RETIRADA'))
        insert_button.pack(pady=12, padx=10)




    def registrar_entrada(self):
        def insert_value(operation):
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()

                valor = value_entry.get()  # Obtenha o valor do Entry onde o usuário insere o valor
                observacao = obs_entry.get()  # Obtenha a observação do Entry onde o usuário insere a observação
                data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')  # Obtenha a data atual no formato desejado
                usuario = self.user[1]  # Obtenha o usuário do atributo 'user'
                operacao = operation  # Use o parâmetro 'operation'

                cursor.execute(
                    "INSERT INTO caixa (operacao, valor, usuario, data_operacao, observacao) VALUES (?, ?, ?, ?, ?)",
                    (operacao, valor, usuario, data_atual, observacao))

                conn.commit()
                conn.close()

                start_datetime = self.start_date_entry.get()
                end_datetime = self.end_date_entry.get()
                self.update_entry_list(start_datetime, end_datetime)

                price_window.destroy()
            except sqlite3.Error as e:
                print("SQLite error:", e)

        price_window = tk.Toplevel(self)
        price_window.title("DEPÓSITO")
        price_window.geometry("400x700")
        price_window.configure(bg="#212121")

        label = customtkinter.CTkLabel(price_window, width=300, height=40, font=("Roboto", 36),
                                       text="REGISTRAR DEPÓSITO")
        label.pack(pady=12, padx=10)

        value = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Valor:")
        value.pack(pady=6, padx=10)

        value_entry = customtkinter.CTkEntry(price_window, width=240)
        value_entry.pack(pady=6, padx=10)

        obs_label = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Observação :")
        obs_label.pack(pady=6, padx=10)

        obs_entry = customtkinter.CTkEntry(price_window, width=240)
        obs_entry.pack(pady=6, padx=10)

        insert_button = customtkinter.CTkButton(
            price_window, width=240, height=32, text="Inserir", command=lambda: insert_value('DEPÓSITO'))
        insert_button.pack(pady=12, padx=10)

    def export_pdf(self):
        try:
            default_filename = f"RELATÓRIO - {datetime.now().strftime('%Y-%m-%d')}.pdf"
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename,
                                                    filetypes=[("PDF Files", "*.pdf")])
            if not filename:
                return

            doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
            data = []

            header = ("Operação", "Valor", "Usuário", "Data da Operação", "Observação")
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

            header = ["Operação", "Valor", "Usuário", "Data da Operação", "Observação"]
            ws.append(header)

            for entry in self.tree.get_children():
                values = self.tree.item(entry)['values']
                ws.append(values)

            wb.save(filename)
            messagebox.showinfo("Export Excel", "Dados exportados para Excel com sucesso!")

        except Exception as e:
            print("Erro ao exportar para Excel:", e)

    def send_email(self):
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM email")
        existing_record = cursor.fetchone()
        cursor.close()
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'relatoriostatus@gmail.com'
        smtp_password = 'lzxfdgaxxlujxykx'

        if existing_record[0]:
            to_email = existing_record[0]
        else:
            to_email = self.to_email

        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        subject = f'Relatório de Caixa - {start_datetime} - {end_datetime}'

        data = []
        self.total_deposito = 0.0
        self.total_retirada = 0.0

        for entry in self.tree.get_children():
            values = self.tree.item(entry)['values']
            operacao, valor, _, data_operacao, observacao = values
            data.append((operacao, valor, data_operacao, observacao))

            valor = float(valor)
            # Calcule os totais com base na operação
            if operacao == 'DEPÓSITO':
                self.total_deposito += valor
            elif operacao == 'RETIRADA':
                self.total_retirada += valor



        self.total_geral = self.total_deposito - self.total_retirada
        self.update_total_labels()  # Chame esta função para atualizar os rótulos dos totais

        # Cria a string para o corpo do email com os dados e totais
        body = f"Relatório de Pagamentos do Período de {start_datetime} - {end_datetime}\n\n"

        for operacao, valor, data_operacao, observacao in data:
            body += f"Operação: {operacao}\n"
            body += f"Valor: R${valor:.2f}\n"
            body += f"Data da Operação: {data_operacao}\n"
            body += f"Observação: {observacao}\n\n"

        body += f"Total de Depósito: R${self.total_deposito:.2f}\n"
        body += f"Total de Retirada: R${self.total_retirada:.2f}\n"
        body += f"Total: R${self.total_geral:.2f}\n"

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
    app = Caixa()
