import customtkinter
import os
import sqlite3


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x420")
def login():
    username = entry1.get()
    password = entry2.get()

    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    conn.close()
    user_type  = user[4]

    if user:
        rt.destroy()  # Fecha a janela de login
        os.system(f"python menu.py {user_type} ")  # Abre a tela de controle
    else:
        label_status.config(text="Login failed. Please try again.")

def switch_to_register_screen():
    rt.destroy()  # Fecha a janela atual
    os.system("python register.py")  # Abre a tela de registro

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="Login", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Usuário")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Senha", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=fr, width=240, height=32, text="Login", command=login)
button.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(master=fr, width=240, height=32, text="Registre-se", command=switch_to_register_screen)
register_button.pack(pady=12, padx=10)


rt.mainloop()
