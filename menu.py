import customtkinter
import os
import sqlite3
import sys

print("User type:", sys.argv[1] )
user_type = sys.argv[1] if len(sys.argv) > 1 else None

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
    if user_type == "GERENTE":
        os.system("python report.py")
    else:
        # Mostrar uma mensagem ou desabilitar o botão de relatório para usuários não autorizados
        button4.configure(state="disabled")  # Desabilita o botão de relatório

def open_config():
    if user_type == "GERENTE":
        os.system("python config.py")
    else:
        # Mostrar uma mensagem ou desabilitar o botão de configuração para usuários não autorizados
        button5.configure(state="disabled")  # Desabilita o botão de configuração

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

if user_type != "GERENTE":
    print(user_type)
    button4.configure(state="disabled")
    button5.configure(state="disabled")

button6 = customtkinter.CTkButton(master=fr, width=240, height=32, text="LOGOUT",fg_color='#91403d', command=logout)
button6.pack(pady=12, padx=10)



# Inicia a aplicação
rt.mainloop()
