import tkinter as tk

class TicketWindow:
    def __init__(self, parent, placa, data_atual):
        self.parent = parent
        self.placa = placa
        self.data_atual = data_atual

        self.ticket_window = parent
        self.ticket_window.geometry("400x300")
        
        ticket_label = tk.Label(master=self.ticket_window, text="TICKET", font=("Roboto", 18))
        ticket_label.pack(pady=10)
        
        placa_label = tk.Label(master=self.ticket_window, text=f"PLACA: {self.placa}")
        placa_label.pack()
        
        data_label = tk.Label(master=self.ticket_window, text=f"DATA E HORA DE ENTRADA: {self.data_atual}")
        data_label.pack()
        
        print_button = tk.Button(master=self.ticket_window, text="Imprimir", command=self.imprimir_ticket)
        print_button.pack(pady=10)
        
        cancel_button = tk.Button(master=self.ticket_window, text="Cancelar", command=self.ticket_window.destroy)
        cancel_button.pack(pady=5)

    def imprimir_ticket(self):
        # Lógica para imprimir o ticket (aqui você pode adicionar sua própria lógica de impressão)
        print("Imprimir ticket")
        self.ticket_window.destroy()
