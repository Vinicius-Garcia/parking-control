import customtkinter

from exitclass import Exit
from settingclass import Settings
from reportclass import Report
from entryclass import Entry
from actions import Actions
class Financial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.setup_ui()
        self.mainloop()

    def setup_ui(self):

        fr = customtkinter.CTkFrame(master=self)
        fr.pack(pady=40, padx=120, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=fr, width=120, height=36, text="FINANCEIRO", font=("Roboto", 36))
        label.pack(pady=(10, 10), padx=10)

        button4 = customtkinter.CTkButton(master=fr, width=480, height=36, text="RELATÓRIO", command=self.open_relatorio)
        button4.pack(pady=12, padx=10)


    def open_relatorio(self):
        Report()





if __name__ == "__main__":
    app = Financial()
