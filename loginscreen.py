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
        label.pack(pady=(250, 20), padx=10)

        self.entry1 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Usuário")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Senha", show="*")
        self.entry2.pack(pady=12, padx=10)

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

        user_type = user[4]

        if user:
            Menu(user_type)
           # self.destroy()  # Fecha a janela de login
        else:
            self.label_status.config(text="Login failed. Please try again.")


if __name__ == "__main__":
    app = Login()
