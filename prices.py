import customtkinter
import os
import sqlite3
from tkinter import messagebox
import tkinter as tk


class Prices(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()
        self.mainloop()

    def setup_ui(self):

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=40, fill="both", expand=True)
        self.title("Tabela de Preço")
        def insert_car():
            price_window = tk.Toplevel(self)
            price_window.title("Tabela de Preço Carro")
            price_window.geometry("400x700")
            price_window.configure(bg="#212121")

            def insert_or_update_price(veiculo):
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        # Verifique se já existe um registro para o veículo
                        cursor.execute("SELECT * FROM price WHERE veiculo=?", (veiculo,))
                        existing_record = cursor.fetchone()

                        # Obtenha os valores dos campos de entrada
                        carencia_val = carencia_entry.get()
                        primeira_faixa_val = primeira_faixa_entry.get()
                        primeira_faixa_min_val = primeira_faixa_min_entry.get()
                        segunda_faixa_val = segunda_faixa_entry.get()
                        segunda_faixa_min_val = segunda_faixa_min_entry.get()
                        demais_faixas_val = demais_faixas_entry.get()
                        demais_faixas_min_val = demais_faixas_min_entry.get()

                        if existing_record:
                            # Atualize o registro existente
                            cursor.execute(
                                "UPDATE price SET carencia=?, primeira_faixa=?, primeira_faixa_min=?, segunda_faixa=?, segunda_faixa_min=?, demais_faixas=?, demais_faixas_min=? WHERE veiculo=?",
                                (carencia_val, primeira_faixa_val, primeira_faixa_min_val, segunda_faixa_val,
                                 segunda_faixa_min_val, demais_faixas_val, demais_faixas_min_val, veiculo))
                        else:
                            # Insira um novo registro
                            cursor.execute(
                                "INSERT INTO price (veiculo, carencia, primeira_faixa, primeira_faixa_min, segunda_faixa, segunda_faixa_min, demais_faixas, demais_faixas_min) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (veiculo, carencia_val, primeira_faixa_val, primeira_faixa_min_val, segunda_faixa_val,
                                 segunda_faixa_min_val, demais_faixas_val, demais_faixas_min_val))

                        conn.commit()
                        conn.close()

                        messagebox.showinfo(
                            "Sucesso", f"Valores da tabela de preço para {veiculo} atualizados com sucesso!")

                        price_window.destroy()

                    except sqlite3.Error as e:
                        print("SQLite error:", e)

            def populate_entries():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM price WHERE veiculo= ?", ('CARRO',))
                        row = cursor.fetchone()
                        cursor.close()

                        if row:
                            carencia_entry.insert(0, row[1])
                            primeira_faixa_entry.insert(0, row[2])
                            primeira_faixa_min_entry.insert(0, row[3])
                            demais_faixas_entry.insert(0, row[4])
                            demais_faixas_min_entry.insert(0, row[5])
                            segunda_faixa_entry.insert(0, row[6])
                            segunda_faixa_min_entry.insert(0, row[7])



                    except sqlite3.Error as e:
                        cursor.close()
                        print("SQLite error:", e)

            label = customtkinter.CTkLabel(price_window, width=300, height=40, font=("Roboto", 36),
                                               text="Tabela de Preços")
            label.pack(pady=12, padx=10)

            carencia_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Carência:")
            carencia_label.pack(pady=6, padx=10)

            carencia_entry = customtkinter.CTkEntry(price_window, width=240)
            carencia_entry.pack(pady=6, padx=10)

            primeira_faixa_min_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Tempo da Primeira Faixa(em minutos):")
            primeira_faixa_min_label.pack(pady=6, padx=10)

            primeira_faixa_min_entry = customtkinter.CTkEntry(price_window, width=240)
            primeira_faixa_min_entry.pack(pady=6, padx=10)

            primeira_faixa_label = customtkinter.CTkLabel(
                 price_window, width=240, height=1, text="Valor da Primeira Faixa:")
            primeira_faixa_label.pack(pady=6, padx=10)

            primeira_faixa_entry = customtkinter.CTkEntry(price_window, width=240)
            primeira_faixa_entry.pack(pady=6, padx=10)
            segunda_faixa_min_label = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Tempo da Segunda Faixa(em minutos):")
            segunda_faixa_min_label.pack(pady=6, padx=10)

            segunda_faixa_min_entry = customtkinter.CTkEntry(price_window, width=240)
            segunda_faixa_min_entry.pack(pady=6, padx=10)

            segunda_faixa_label = customtkinter.CTkLabel(
            price_window, width=240, height=1, text="Valor da Segunda Faixa:")
            segunda_faixa_label.pack(pady=6, padx=10)

            segunda_faixa_entry = customtkinter.CTkEntry(price_window, width=240)
            segunda_faixa_entry.pack(pady=6, padx=10)

            demais_faixas_min_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Tempo das Demais Faixa(em minutos):")
            demais_faixas_min_label.pack(pady=6, padx=10)

            demais_faixas_min_entry = customtkinter.CTkEntry(price_window, width=240)
            demais_faixas_min_entry.pack(pady=6, padx=10)

            demais_faixas_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Valor das Demais Faixas:")
            demais_faixas_label.pack(pady=6, padx=10)

            demais_faixas_entry = customtkinter.CTkEntry(price_window, width=240)
            demais_faixas_entry.pack(pady=6, padx=10)

            insert_button = customtkinter.CTkButton(
                    price_window, width=240, height=32, text="Inserir", command=lambda: insert_or_update_price('CARRO'))
            insert_button.pack(pady=12, padx=10)

            populate_entries()

        def insert_moto():
                price_window = tk.Toplevel(self)
                price_window.title("Tabela de Preço Moto")
                price_window.geometry("400x700")
                price_window.configure(bg="#212121")

                def insert_or_update_price(veiculo):
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        # Verifique se já existe um registro para o veículo
                        cursor.execute("SELECT * FROM price WHERE veiculo=?", (veiculo,))
                        existing_record = cursor.fetchone()

                        # Obtenha os valores dos campos de entrada
                        carencia_val = carencia_entry.get()
                        primeira_faixa_val = primeira_faixa_entry.get()
                        primeira_faixa_min_val = primeira_faixa_min_entry.get()
                        segunda_faixa_val = segunda_faixa_entry.get()
                        segunda_faixa_min_val = segunda_faixa_min_entry.get()
                        demais_faixas_val = demais_faixas_entry.get()
                        demais_faixas_min_val = demais_faixas_min_entry.get()

                        if existing_record:
                            # Atualize o registro existente
                            cursor.execute(
                                "UPDATE price SET carencia=?, primeira_faixa=?, primeira_faixa_min=?, segunda_faixa=?, segunda_faixa_min=?, demais_faixas=?, demais_faixas_min=? WHERE veiculo=?",
                                (carencia_val, primeira_faixa_val, primeira_faixa_min_val, segunda_faixa_val,
                                 segunda_faixa_min_val, demais_faixas_val, demais_faixas_min_val, veiculo))
                        else:
                            # Insira um novo registro
                            cursor.execute(
                                "INSERT INTO price (veiculo, carencia, primeira_faixa, primeira_faixa_min, segunda_faixa, segunda_faixa_min, demais_faixas, demais_faixas_min) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (veiculo, carencia_val, primeira_faixa_val, primeira_faixa_min_val, segunda_faixa_val,
                                 segunda_faixa_min_val, demais_faixas_val, demais_faixas_min_val))

                        conn.commit()
                        conn.close()

                        messagebox.showinfo(
                            "Sucesso", f"Valores da tabela de preço para {veiculo} atualizados com sucesso!")
                        price_window.destroy()

                    except sqlite3.Error as e:
                        print("SQLite error:", e)

                def populate_entries():
                    try:
                        conn = sqlite3.connect('user_data.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM price WHERE veiculo= ?", ('MOTO',))
                        row = cursor.fetchone()
                        cursor.close()

                        if row:
                            carencia_entry.insert(0, row[1])
                            primeira_faixa_entry.insert(0, row[2])
                            primeira_faixa_min_entry.insert(0, row[3])
                            demais_faixas_entry.insert(0, row[4])
                            demais_faixas_min_entry.insert(0, row[5])
                            segunda_faixa_entry.insert(0, row[6])
                            segunda_faixa_min_entry.insert(0, row[7])



                    except sqlite3.Error as e:
                        cursor.close()
                        print("SQLite error:", e)

                label = customtkinter.CTkLabel(price_window, width=300, height=40, font=("Roboto", 36),
                                               text="Tabela de Preços")
                label.pack(pady=12, padx=10)

                carencia_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Carência:")
                carencia_label.pack(pady=6, padx=10)

                carencia_entry = customtkinter.CTkEntry(price_window, width=240)
                carencia_entry.pack(pady=6, padx=10)

                primeira_faixa_min_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Tempo da Primeira Faixa(em minutos):")
                primeira_faixa_min_label.pack(pady=6, padx=10)

                primeira_faixa_min_entry = customtkinter.CTkEntry(price_window, width=240)
                primeira_faixa_min_entry.pack(pady=6, padx=10)

                primeira_faixa_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Valor da Primeira Faixa:")
                primeira_faixa_label.pack(pady=6, padx=10)

                primeira_faixa_entry = customtkinter.CTkEntry(price_window, width=240)
                primeira_faixa_entry.pack(pady=6, padx=10)
                segunda_faixa_min_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Tempo da Segunda Faixa(em minutos):")
                segunda_faixa_min_label.pack(pady=6, padx=10)

                segunda_faixa_min_entry = customtkinter.CTkEntry(price_window, width=240)
                segunda_faixa_min_entry.pack(pady=6, padx=10)

                segunda_faixa_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Valor da Segunda Faixa:")
                segunda_faixa_label.pack(pady=6, padx=10)

                segunda_faixa_entry = customtkinter.CTkEntry(price_window, width=240)
                segunda_faixa_entry.pack(pady=6, padx=10)

                demais_faixas_min_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Tempo das Demais Faixa(em minutos):")
                demais_faixas_min_label.pack(pady=6, padx=10)

                demais_faixas_min_entry = customtkinter.CTkEntry(price_window, width=240)
                demais_faixas_min_entry.pack(pady=6, padx=10)

                demais_faixas_label = customtkinter.CTkLabel(
                    price_window, width=240, height=1, text="Valor das Demais Faixas:")
                demais_faixas_label.pack(pady=6, padx=10)

                demais_faixas_entry = customtkinter.CTkEntry(price_window, width=240)
                demais_faixas_entry.pack(pady=6, padx=10)

                insert_button = customtkinter.CTkButton(
                    price_window, width=240, height=32, text="Inserir", command=lambda: insert_or_update_price('MOTO'))
                insert_button.pack(pady=12, padx=10)

                populate_entries()

        insert_button_car = customtkinter.CTkButton(master=fr, width=240, height=32, text="CARRO", command=insert_car)
        insert_button_car.pack(pady=12, padx=10)

        insert_button_moto = customtkinter.CTkButton( master=fr, width=240, height=32, text="MOTO", command=insert_moto)
        insert_button_moto.pack(pady=12, padx=10)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = Prices()
    app.run()