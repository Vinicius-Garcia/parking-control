import customtkinter as ctk
from loginscreen import Login


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    Login(app)
    app.mainloop()


if __name__ == "__main__":
    main()