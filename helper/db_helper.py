import sqlite3


class db_helper:

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS entry
                    (placa TEXT, data DATE, operador_entrada TEXT, veiculo TEXT)''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  placa TEXT,
                                                  data_entrada DATE,
                                                  data_saida DATE,
                                                  tempo_estadia TEXT,
                                                  veiculo TEXT,
                                                  valor_total REAL,
                                                  pagamento TEXT,
                                                  operador_entrada TEXT,
                                                  operador_saida TEXT
                                                )''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS email (
                                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  email TEXT
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
                           demais_faixas_min TEXT,
                           veiculo TEXT
                       )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       full_name TEXT,
                       username TEXT,
                       password TEXT,
                       role TEXT
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS caixa (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       operacao TEXT,
                        valor TEXT,
                       usuario TEXT,
                        data_operacao DATE,
                        observacao TEXT
                   )''')

    conn.commit()
    cursor.close()

if __name__ == "__main__":
    app = db_helper()
    app.run()
