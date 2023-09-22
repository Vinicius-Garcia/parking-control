import smtplib
import sqlite3
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox

import customtkinter

from exitclass import Exit
from settingclass import Settings
from reportclass import Report
from lotclass import Lot
from entryclass import Entry
from emailsender import EmailSender
class Menu(customtkinter.CTk):
    def __init__(self, type_user, user):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.user = user
        self.setup_ui(type_user, user)
        self.mainloop()

    def setup_ui(self, type_user, user):
        user_type = type_user

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=36, text="GESTÃO DE ESTACIONAMENTO", font=("Roboto", 36))
        label.pack(pady=(10, 10), padx=10)

        button1 = customtkinter.CTkButton(master=fr, width=480, height=36, text="REGISTRAR ENTRADA", command=self.open_entrada)
        button1.pack(pady=12, padx=10)

        button2 = customtkinter.CTkButton(master=fr, width=480, height=36, text="REGISTRAR SAÍDA", command=self.open_saida)
        button2.pack(pady=12, padx=10)

        button3 = customtkinter.CTkButton(master=fr, width=480, height=36, text="PÁTIO", command=self.open_patio)
        button3.pack(pady=12, padx=10)

        button7 = customtkinter.CTkButton(master=fr, width=480, height=36, text="EMAIL", command=self.open_email)
        button7.pack(pady=12, padx=10)

        button8 = customtkinter.CTkButton(master=fr, width=480, height=36, text="BACKUP", command=self.backup)
        button8.pack(pady=12, padx=10)

        if user_type == "GERENTE" or user_type == "MASTER":


            button4 = customtkinter.CTkButton(master=fr, width=480, height=36, text="RELATÓRIO", command=self.open_relatorio)
            button4.pack(pady=12, padx=10)

            button5 = customtkinter.CTkButton(master=fr, width=480, height=36, text="CONFIGURAÇÃO", command=self.open_config)
            button5.pack(pady=12, padx=10)



        button6 = customtkinter.CTkButton(master=fr, width=480, height=36, text="LOGOUT", fg_color='#91403d',
                                          command=self.logout)
        button6.pack(pady=12, padx=10)




    # Funções para os botões
    def open_entrada(self):
        Entry(self.user)

    def open_saida(self):
        Exit(self.user)

    def open_patio(self):
        Lot()

    def open_relatorio(self):
        Report()

    def open_config(self):
        Settings()

    def open_email(self):
        EmailSender()

    def backup(self):
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

        # Create a temporary ZIP file containing the database file
        with zipfile.ZipFile('user_data.zip', 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            backup_zip.write('user_data.db', arcname='user_data.db')

        subject = 'BACKUP BANCO DE DADOS'

        body = 'Backup do banco de dados anexado.'

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the ZIP file to the email
        with open('user_data.zip', 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="user_data.zip"')
            msg.attach(part)

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

    def logout(self):
        self.destroy()




if __name__ == "__main__":
    app = Menu()
