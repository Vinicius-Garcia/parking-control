import customtkinter
from caixa import Caixa
from reportclass import Report


class Financial(customtkinter.CTk):
    def __init__(self, user):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.user = user
        self.setup_ui()
        self.mainloop()

    def setup_ui(self):

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=36, text="FINANCEIRO", font=("Roboto", 36))
        label.pack(pady=(10, 10), padx=10)

        if self.user[4] == 'GERENTE':
            button = customtkinter.CTkButton(master=fr, width=480, height=36, text="RELATÓRIO", command=self.open_relatorio)
            button.pack(pady=12, padx=10)

        button1 = customtkinter.CTkButton(master=fr, width=480, height=36, text="CAIXA", command=self.open_caixa)
        button1.pack(pady=12, padx=10)


    def open_relatorio(self):
        Report()

    def open_caixa(self):
        Caixa(self.user)





if __name__ == "__main__":
    app = Financial()
