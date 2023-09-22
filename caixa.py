import customtkinter
class Caixa(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()
        self.mainloop()

    def setup_ui(self):

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=36, text="CAIXA", font=("Roboto", 36))
        label.pack(pady=(10, 10), padx=10)





if __name__ == "__main__":
    app = Caixa()
