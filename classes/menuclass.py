import customtkinter
import os
import sqlite3
import sys

from classes.exitclass import Exit
from settingclass import Settings
from reportclass import Report
from lotclass import Lot
from entryclass import Entry
class Menu(customtkinter.CTk):
    def __init__(self, type_user):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui(type_user)
        self.mainloop()

    def setup_ui(self, type_user):
        print("User type:", type_user)
        user_type = type_user

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=48, text="MENU", font=("Roboto", 48))
        label.pack(pady=(150, 10), padx=10)

        button1 = customtkinter.CTkButton(master=fr, width=480, height=48, text="DAR ENTRADA", command=self.open_entrada)
        button1.pack(pady=12, padx=10)

        button2 = customtkinter.CTkButton(master=fr, width=480, height=48, text="DAR SAÍDA", command=self.open_saida)
        button2.pack(pady=12, padx=10)

        if user_type == "GERENTE" or user_type == "MASTER":
            button3 = customtkinter.CTkButton(master=fr, width=480, height=48, text="PÁTIO", command=self.open_patio)
            button3.pack(pady=12, padx=10)

            button4 = customtkinter.CTkButton(master=fr, width=480, height=48, text="RELATÓRIO", command=self.open_relatorio)
            button4.pack(pady=12, padx=10)

        button5 = customtkinter.CTkButton(master=fr, width=480, height=48, text="CONFIGURAÇÃO", command=self.open_config)
        button5.pack(pady=12, padx=10)

        button6 = customtkinter.CTkButton(master=fr, width=480, height=48, text="LOGOUT", fg_color='#91403d',
                                          command=self.logout)
        button6.pack(pady=12, padx=10)




    # Funções para os botões
    def open_entrada(self):
        Entry()

    def open_saida(self):
        Exit()

    def open_patio(self):
        Lot()

    def open_relatorio(self):
        Report()

    def open_config(self):
        Settings()

    def logout(self):
        self.destroy()




if __name__ == "__main__":
    app = Menu()
    app.run()
