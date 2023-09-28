from tkinter import messagebox

import customtkinter
import os
import sqlite3
from registerclass import UserRegistrationApp
from menuclass import Menu

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()


class Login(customtkinter.CTk):
    def __init__(self, root):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))

        self.setup_ui()
        self.mainloop()

    def setup_ui(self):
        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=480, height=32, text="Login", font=("Roboto", 48))
        label.pack(pady=(20, 20), padx=10)

        self.entry1 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Usuário")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Senha", show="*")
        self.entry2.pack(pady=12, padx=10)

        self.entry2.bind("<Return>", self.enter_pressed)


        self.button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Login", command=self.loginfunction)
        self.button.pack(pady=12, padx=10)

        self.register_button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Registre-se",
                                                  command=self.switch_to_register_screen)
        self.register_button.pack(pady=12, padx=10)

    def switch_to_register_screen(self):
        UserRegistrationApp()

    def loginfunction(self):
        username = self.entry1.get()
        password = self.entry2.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()



        if user:
            user_type = user[4]
            self.entry1.delete(0, 'end')  # Limpa o campo de usuário
            self.entry2.delete(0, 'end')  # Limpa o campo de senha
            Menu(user_type, user)

        else:
            messagebox.showerror("Erro no Login",
                                 "Usuário ou Senha incorreto.")

    def enter_pressed(self,event):
        self.loginfunction()


if __name__ == "__main__":
    app = Login()

