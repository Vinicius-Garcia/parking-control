import customtkinter
import os
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.after(0, lambda: rt.state('zoomed'))


def login():
    username = entry1.get()
    password = entry2.get()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    user_type = user[4]

    if user:
        rt.destroy()  # Fecha a janela de login
        os.system(f'python menu.py {user_type}')
    else:
        label_status.config(text="Login failed. Please try again.")


def switch_to_register_screen():
    os.system('python register.py')


fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=480, height=32, text="Login", font=("Roboto", 48))
label.pack(pady=(250, 20), padx=10)

entry1 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Usuário")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=fr, width=480, height=48, placeholder_text="Senha", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Login", command=login)
button.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(master=fr, width=480, height=48, text="Registre-se",
                                          command=switch_to_register_screen)
register_button.pack(pady=12, padx=10)

rt.mainloop()