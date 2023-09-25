import customtkinter
import os
import sqlite3
from tkinter import messagebox
import tkinter as tk


class Emails(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()
        self.mainloop()

    def setup_ui(self):

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=40, fill="both", expand=True)
        self.title("Email Para Relatório")

        def insert_or_update_price():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        # Verifique se já existe um registro para o veículo
                        cursor.execute("SELECT email FROM email")
                        existing_record = cursor.fetchone()

                        # Obtenha os valores dos campos de entrada
                        emails = carencia_entry.get()

                        if existing_record:
                            # Atualize o registro existente
                            cursor.execute(
                                "UPDATE email SET email=?",
                                (emails,))
                        else:
                            # Insira um novo registro
                            cursor.execute(
                                "INSERT INTO email (email) VALUES (?)",
                                (emails,))

                        conn.commit()
                        conn.close()

                        messagebox.showinfo(
                            "Sucesso", f"Email de envio cadastrado com sucesso")

                    except sqlite3.Error as e:
                        print("aqui")
                        print("SQLite error:", e)

        def populate_entries():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM email ")
                        row = cursor.fetchone()
                        cursor.close()

                        if row:
                            carencia_entry.insert(0, row[1])

                    except sqlite3.Error as e:
                        cursor.close()
                        print("SQLite error:", e)

        label = customtkinter.CTkLabel(master=fr, width=300, height=40, font=("Roboto", 36),
                                               text="EMAIL DESTINO RELATÓRIOS")
        label.pack(pady=12, padx=10)

        carencia_label = customtkinter.CTkLabel(
        master=fr, width=240, height=1, text="Email:")
        carencia_label.pack(pady=6, padx=10)

        carencia_entry = customtkinter.CTkEntry(master=fr, width=240)
        carencia_entry.pack(pady=6, padx=10)

        insert_button = customtkinter.CTkButton(
                    master=fr, width=240, height=32, text="Inserir", command= insert_or_update_price)
        insert_button.pack(pady=12, padx=10)

        populate_entries()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = Emails()
    app.run()