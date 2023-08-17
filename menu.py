import customtkinter
import os
import sqlite3


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x520")

# Funções para os botões
def open_entrada():
    os.system("python entry.py")

def open_saida():
    os.system("python exit.py")

def open_patio():
    os.system("python lot.py")

def open_relatorio():
    os.system("python report.py")

def open_config():
    os.system("python config.py")

def logout():
    rt.destroy()
    os.system("python login.py")


fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="Main Menu", font=("Roboto", 24))
label.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=fr, width=240, height=32, text="DAR ENTRADA", command=open_entrada)
button1.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=fr, width=240, height=32, text="DAR SAÍDA", command=open_saida)
button2.pack(pady=12, padx=10)

button3 = customtkinter.CTkButton(master=fr, width=240, height=32, text="PÁTIO", command=open_patio)
button3.pack(pady=12, padx=10)

button4 = customtkinter.CTkButton(master=fr, width=240, height=32, text="RELATÓRIO", command=open_relatorio)
button4.pack(pady=12, padx=10)

button5 = customtkinter.CTkButton(master=fr, width=240, height=32, text="CONFIGURAÇÃO", command=open_config)
button5.pack(pady=12, padx=10)

button6 = customtkinter.CTkButton(master=fr, width=240, height=32, text="LOGOUT",fg_color='#91403d', command=logout)
button6.pack(pady=12, padx=10)



# Inicia a aplicação
rt.mainloop()
