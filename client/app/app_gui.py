import customtkinter as ctk

def messaging_app_layout():
    root = ctk.CTk()
    root.title("Messaging App")
    root.geometry("1000x700")

    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(main_frame, width=250, corner_radius=0)
    left_frame.grid(row=0, column=0, sticky="nsw")

    you_frame = ctk.CTkFrame(left_frame, fg_color=("gray85", "gray17"), height=80)
    you_frame.pack(fill="x", padx=10, pady=10)
    you_frame.grid_columnconfigure(0, weight=1)

    you_username_label = ctk.CTkLabel(you_frame, text="Sinan67Tuff", font=ctk.CTkFont(size=16, weight="bold"))
    you_username_label.grid(row=0, column=0, sticky="w", padx=15, pady=20)

    settings_label = ctk.CTkLabel(you_frame, text="⚙", font=ctk.CTkFont(size=24))
    settings_label.grid(row=0, column=1, sticky="e", padx=15, pady=20)

    users_scrollable_frame = ctk.CTkScrollableFrame(left_frame, label_text="Servers")
    users_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for i in range(12):
        user_frame = ctk.CTkFrame(users_scrollable_frame, fg_color="transparent", corner_radius=5)
        user_frame.pack(fill="x", pady=2)

        username_label = ctk.CTkLabel(user_frame, text=f"Server_{i+1}", font=ctk.CTkFont(size=14))
        username_label.pack(side="left", padx=10, pady=10, anchor="w")


    right_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color=("gray92", "gray14"))
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    top_bar = ctk.CTkFrame(right_frame, height=40, corner_radius=0, fg_color=("gray85", "gray17"))
    top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

    domain_label = ctk.CTkLabel(top_bar, text="podbreznik.eu", font=ctk.CTkFont(size=14))
    domain_label.pack(expand=True)

    chat_frame = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
    chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    chat_frame.grid_columnconfigure(0, weight=1)

    messages = [
        ("Yo alo kdaj pišemo OSP?", "them"),
        ("Zaj v ponedeljek.", "you"),
        ("O fak jaz sem cooked.", "them"),
        ("Pa ne stari na easy gre.", "you"),
        ("Veš kako preverjanje je blo.", "you"),
        ("Doro te. Sao da ga nebo Korošec zafuko", "them"),
        ("Eh pa tak mi je vseeno. Faking OSP.", "them"),
        ("Če ti pravim na easy ti bo šlo.", "you"),
        ("Doro te ajde stari se čujemo", "them"),
        ("Ajde", "you"),
        ("Doro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafuko", "them"),
        ("Doro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafukoDoro te. Sao da ga nebo Korošec zafuko", "you"),

    ]

    for message, sender in messages:
        if sender == "them":
            msg_label = ctk.CTkLabel(chat_frame, text=message, fg_color=("#D3D3D3", "#333333"), text_color=("black", "white"), corner_radius=10, justify="left", wraplength=500, font=("Roboto", 15))
            msg_label.pack(anchor="w", pady=8, padx=8)
        else:
            msg_label = ctk.CTkLabel(chat_frame, text=message, fg_color=("#3B8ED0", "#1F6AA5"), text_color="white", corner_radius=10, justify="left", wraplength=500, font=("Roboto", 15))
            msg_label.pack(anchor="w", pady=8, padx=8)

# Opcija za groupchate če dama namesto else - elif sender == "you":

    input_frame = ctk.CTkFrame(right_frame, corner_radius=0, fg_color=("gray85", "gray17"))
    input_frame.grid(row=2, column=0, sticky="ew")

    message_entry = ctk.CTkEntry(input_frame, placeholder_text="Type a message...", font=("Roboto", 18))
    message_entry.pack(side="left", fill="x", expand=True, padx=13, pady=13)

    send_button = ctk.CTkButton(input_frame, text="Send")
    send_button.pack(side="right", padx=10, pady=10)


    root.mainloop()

if __name__ == "__main__":
    messaging_app_layout()