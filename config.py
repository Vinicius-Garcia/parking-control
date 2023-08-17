import customtkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Função para abrir a janela de usuários


def users():
    user_window = tk.Toplevel(rt)
    user_window.title("Lista de Usuários")
    user_window.geometry("400x450")
    user_window.configure(bg="#212121")

    # Coloque o código aqui para exibir a lista de usuários na nova janela

# Função para abrir a janela de tabela de preços


def price():
    price_window = tk.Toplevel(rt)
    price_window.title("Tabela de Preço")
    price_window.geometry("400x450")
    price_window.configure(bg="#212121")

    # Coloque o código aqui para permitir ao usuário escolher os parâmetros de preço


# Configurações da janela principal
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

rt = customtkinter.CTk()
rt.geometry("600x600")

fr = customtkinter.CTkFrame(master=rt)
fr.pack(pady=40, padx=120, fill="both", expand=True)

# Botão para abrir a janela de usuários
button_users = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="USUÁRIOS", command=users)
button_users.pack(pady=12, padx=10)

# Botão para abrir a janela de tabela de preço
button_price = customtkinter.CTkButton(
    master=fr, width=240, height=32, text="TABELA DE PREÇO", command=price)
button_price.pack(pady=12, padx=10)

rt.mainloop()
