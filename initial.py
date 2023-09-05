import customtkinter as ctk
from loginscreen import Login
import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                (placa TEXT, data TEXT, operador_entrada TEXT, veiculo TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              placa TEXT,
                                              data_entrada TEXT,
                                              data_saida TEXT,
                                              tempo_estadia TEXT,
                                              veiculo TEXT,
                                              valor_total REAL,
                                              pagamento TEXT,
                                              operador_entrada TEXT,
                                              operador_saida TEXT
                                            )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS texts (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      text TEXT,
                      type TEXT,
                      ordem TEXT
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS price (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       carencia TEXT,
                       primeira_faixa TEXT,
                       primeira_faixa_min TEXT,
                       segunda_faixa TEXT,
                       segunda_faixa_min TEXT,
                       demais_faixas TEXT,
                       demais_faixas_min TEXT
                   )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name TEXT,
                   username TEXT,
                   password TEXT,
                   role TEXT
               )''')

conn.commit()
cursor.close()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    Login(app)
    app.mainloop()


if __name__ == "__main__":
    main()