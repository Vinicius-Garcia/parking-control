import tkinter as tk
import os

# Funções para os botões
def open_entrada():
    os.system("python entrada.py")

def open_saida():
    os.system("python saida.py")

def open_patio():
    os.system("python patio.py")

def open_relatorio():
    os.system("python relatorio.py")

def open_config():
    os.system("python config.py")

# Cria a janela principal
root = tk.Tk()
root.geometry("800x600")
root.title("Sistema de Estacionamento")

# Criação do título
title_label = tk.Label(master=root, text="Menu", font=("Roboto", 24))
title_label.pack(pady=20)

# Criação dos botões com tamanho maior
button_entrada = tk.Button(master=root, text="Entrada", width=20, height=3, command=open_entrada)
button_saida = tk.Button(master=root, text="Saída", width=20, height=3, command=open_saida)
button_patio = tk.Button(master=root, text="Pátio", width=20, height=3, command=open_patio)
button_relatorio = tk.Button(master=root, text="Relatório", width=20, height=3, command=open_relatorio)
button_config = tk.Button(master=root, text="Configurações", width=20, height=3, command=open_config)

# Posicionamento dos botões
button_entrada.pack(pady=10)
button_saida.pack(pady=10)
button_patio.pack(pady=10)
button_relatorio.pack(pady=10)
button_config.pack(pady=10)

# Inicia a aplicação
root.mainloop()
