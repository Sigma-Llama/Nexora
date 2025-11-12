import customtkinter as ctk

def domain():
    root = ctk.CTk()
    root.title("Domena")
    root.geometry("400x150")

    main_frame = ctk.CTkFrame(root)

    naslov = ctk.CTkLabel(root, text="Vpiši Domeno Strežnika", font=("Roboto", 19))
    naslov.pack(pady=12, padx=10)

    domena = ctk.CTkEntry(root, placeholder_text="Domena", width=340, height=9)
    domena.pack(pady=12, padx=10)

    poslji = ctk.CTkButton(root, text="Connect", font=("Roboto", 15), command=loginSignup())
    poslji.pack(pady=12, padx=10)

    root.mainloop()


if __name__ == "__main__":
    domain()