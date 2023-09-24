import customtkinter
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib import colors
from openpyxl import Workbook
from tkcalendar import Calendar, DateEntry
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import configparser


class EmailSender(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()


        config = configparser.ConfigParser()
        config.read('config.ini')
        self.to_email = config['EMAIL_CONFIG']['to_email']


    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="ENVIAR EMAIL", font=("Roboto", 24))
        label.pack(pady=(300,0), padx=10)

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

        self.generate_button = customtkinter.CTkButton(self.datesFrame, width=140, height=40, text="ENVIAR E-MAIL",
                                                  command=self.generate_report)
        self.generate_button.pack(pady=10, padx=10, anchor="e", side="left")

        self.tree = tk.ttk.Treeview(master=fr,
                               columns=(
                               "Placa", "Data de Entrada", "Data de Saída", "Tempo de Permanência", "Valor Pago",
                               "Pagamento","Veículo" ,"Operador Entrada", "Operador Saída"))
        self.tree['show'] = 'headings'
        self.tree.heading("#1", text="Placa")
        self.tree.heading("#2", text="Data de Entrada")
        self.tree.heading("#3", text="Data de Saída")
        self.tree.heading("#4", text="Tempo de Permanência")
        self.tree.heading("#5", text="Valor Pago")
        self.tree.heading("#6", text="Pagamento")
        self.tree.heading("#7", text="Veículo")
        self.tree.heading("#8", text="Operador Entrada")
        self.tree.heading("#9", text="Operador Saída")

        self.tree.column("#1", width=50)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=100)
        self.tree.column("#6", width=100)
        self.tree.column("#7", width=50)
        self.tree.column("#8", width=100)
        self.tree.column("#9", width=100)

        self.treeScroll = tk.Scrollbar(master=fr)
        self.treeScroll.configure(command=self.tree.yview)
        self.treeScroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=10)
        self.tree.pack_forget()
        self.treeScroll.pack_forget()

        self.tree2_frame = customtkinter.CTkFrame(master=fr)
        self.tree2_frame.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        self.tree2 = tk.ttk.Treeview(self.tree2_frame,
                                     columns=(
                                         "Operação", "Valor", "Usuário", "Data da Operação", "Observação"))
        self.tree2['show'] = 'headings'
        self.tree2.heading("#1", text="Operação")
        self.tree2.heading("#2", text="Valor")
        self.tree2.heading("#3", text="Usuário")
        self.tree2.heading("#4", text="Data da Operação")
        self.tree2.heading("#5", text="Observação")

        self.tree2.column("#1", width=50)
        self.tree2.column("#2", width=50)
        self.tree2.column("#3", width=100)
        self.tree2.column("#4", width=100)
        self.tree2.column("#5", width=200)

        self.treeScroll2 = tk.Scrollbar(self.tree2_frame)
        self.treeScroll2.configure(command=self.tree2.yview)
        self.treeScroll2.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree2.pack(fill="both", expand=True, padx=(10, 0), pady=10)
        self.tree2.pack_forget()
        self.treeScroll2.pack_forget()



    def update_entry_list(self, start_date, end_date):
        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            start_datetime = f"{start_date} 00:00:00"
            end_datetime = f"{end_date} 23:59:59"

            cursor.execute(
                "SELECT placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada, operador_saida FROM history WHERE data_saida >= ? AND data_saida <= ?",
                (start_datetime, end_datetime))
            entries = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for item in self.tree.get_children():
                self.tree.delete(item)

            for entry in entries:
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada, operador_saida = entry
                self.tree.insert('', tk.END, values=(
                placa, data_entrada, data_saida, tempo_estadia, valor_total, pagamento, veiculo, operador_entrada,
                operador_saida))

            cursor.execute(
                "SELECT operacao, valor, usuario, data_operacao, observacao FROM caixa WHERE data_operacao >= ? AND data_operacao <= ?",
                (start_datetime, end_datetime))
            valores = cursor.fetchall()
            self.tree2.delete(*self.tree2.get_children())

            self.total_deposito = 0.0
            self.total_retirada = 0.0

            for entry in valores:
                operacao, valor, usuario, data_operacao, observacao = entry
                self.tree2.insert('', tk.END, values=(operacao, valor, usuario, data_operacao, observacao))

                valor = float(valor)
                # Calcule os totais com base na operação
                if operacao == 'DEPÓSITO':
                    self.total_deposito += valor
                elif operacao == 'RETIRADA':
                    self.total_retirada += valor

            self.total_geral = self.total_deposito - self.total_retirada

            cursor.close()
            self.send_email()


        except sqlite3.Error as e:
            print("SQLite error:", e)

    def generate_report(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        self.update_entry_list(start_datetime, end_datetime)


    def run(self):
        self.mainloop()

    def send_email(self):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'relatoriostatus@gmail.com'
        smtp_password = 'lzxfdgaxxlujxykx'

        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM email")
        existing_record = cursor.fetchone()
        cursor.close()

        if existing_record[0]:
            to_email = existing_record[0]
        else:
            to_email = self.to_email

        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        subject = f'Relatório de Pagamentos - {start_datetime} - {end_datetime}'

        total_pix = 0
        total_cash = 0
        total_card = 0
        count_pix = 0
        count_cash = 0
        count_card = 0

        total_cars = 0  # Inicializa o total de carros
        total_motorcycles = 0  # Inicializa o total de motos

        total_deposito = 0
        total_saque = 0

        for entry in self.tree.get_children():
            values = self.tree.item(entry)['values']
            valor_total = float(values[4])
            pagamento = values[5]
            veiculo = values[6]  # Veículo está no índice 6

            if pagamento == "PIX":
                total_pix += valor_total
                count_pix += 1
            elif pagamento == "DINHEIRO":
                total_cash += valor_total
                count_cash += 1
            elif pagamento == "CARTÃO":
                total_card += valor_total
                count_card += 1

            # Verifica se o veículo é carro ou moto e incrementa o total correspondente
            if veiculo == "CARRO":
                total_cars += 1
            elif veiculo == "MOTO":
                total_motorcycles += 1

        for entry in self.tree2.get_children():
            values = self.tree2.item(entry)['values']
            operacao = values[0]

            if operacao == "RETIRADA":
                total_saque += float(values[1])
            else:
                total_deposito += float(values[1])

        # Cria a string para o corpo do email com os totais de carros e motos
        body = f"Relatório de Pagamentos do Período de {start_datetime} - {end_datetime}\n" \
               f"Pix: R${total_pix:.2f} (Quantidade: {count_pix})\n" \
               f"Dinheiro: R${total_cash:.2f} (Quantidade: {count_cash})\n" \
               f"Cartão: R${total_card:.2f} (Quantidade: {count_card})\n" \
               f"Total Arrecadado em Ticket: R${(total_card + total_cash + total_pix):.2f} (Quantidade: {(count_card + count_pix + count_cash)})\n" \
               f"Total de Pagamentos de Carros: {total_cars}\n" \
               f"Total de Pagamentos de Motos: {total_motorcycles}\n" \
               f"Total de Saque do Caixa:  R$ {total_saque}\n" \
               f"Total de Depósito no Caixa:  R$ {total_deposito}\n" \
               f"Total do Caixa:  R$ {total_deposito - total_saque}\n" \
               f"Total Geral:  R$ {((total_deposito - total_saque) + (total_card + total_pix + total_cash))}\n"

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
    app = EmailSender()
    app.run()