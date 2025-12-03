import customtkinter as ctk
from tkinter import ttk
import threading
import time
from client.app import api_client


def run_discord_like():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Nexora — Chat")
    root.geometry("1000x700")

    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # Left sidebar: servers
    left_frame = ctk.CTkFrame(main_frame, width=90, corner_radius=0)
    left_frame.grid(row=0, column=0, sticky="nsw")

    servers = [f"SV{i+1}" for i in range(10)]
    server_buttons = []
    for s in servers:
        btn = ctk.CTkButton(left_frame, text=s, width=60, height=60, corner_radius=10)
        btn.pack(pady=6, padx=6)
        server_buttons.append(btn)

    # Center: guild/channel list
    center_frame = ctk.CTkFrame(main_frame, width=200, corner_radius=0)
    center_frame.grid(row=0, column=1, sticky="nsw")
    center_frame.grid_rowconfigure(1, weight=1)

    guild_label = ctk.CTkLabel(center_frame, text="Servers", font=ctk.CTkFont(size=16, weight="bold"))
    guild_label.pack(pady=(10, 6))

    channels_frame = ctk.CTkScrollableFrame(center_frame, label_text="Channels")
    channels_frame.pack(fill="both", expand=True, padx=8, pady=8)

    channels = ["general", "random", "projects", "osp-help"]
    channel_buttons = []
    for ch in channels:
        b = ctk.CTkButton(channels_frame, text="# " + ch, anchor="w")
        b.pack(fill="x", pady=4, padx=6)
        channel_buttons.append(b)

    # Right: chat area
    right_frame = ctk.CTkFrame(main_frame, corner_radius=0)
    right_frame.grid(row=0, column=2, sticky="nsew")
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    top_bar = ctk.CTkFrame(right_frame, height=50, corner_radius=0)
    top_bar.grid(row=0, column=0, sticky="ew")
    channel_label = ctk.CTkLabel(top_bar, text="# general", font=ctk.CTkFont(size=18, weight="bold"))
    channel_label.pack(side="left", padx=12)

    # Scrollable chat area using a canvas inside a frame for better message placement
    chat_outer = ctk.CTkFrame(right_frame)
    chat_outer.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
    chat_outer.grid_rowconfigure(0, weight=1)
    chat_outer.grid_columnconfigure(0, weight=1)

    canvas = ctk.CTkCanvas(chat_outer, bg=chat_outer.cget('fg_color'))
    scrollbar = ctk.CTkScrollbar(chat_outer, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    messages_frame = ctk.CTkFrame(canvas)
    messages_frame.grid_columnconfigure(0, weight=1)
    canvas.create_window((0, 0), window=messages_frame, anchor='nw')

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox('all'))

    messages_frame.bind('<Configure>', lambda e: on_frame_configure())

    # Sample messages
    initial_messages = [
        ("Yo alo kdaj pišemo OSP?", "them"),
        ("Zaj v ponedeljek.", "you"),
        ("O fak jaz sem cooked.", "them"),
        ("Pa ne stari na easy gre.", "you"),
    ]

    displayed = set()

    def add_message(text, sender='you', ts=None):
        bubble = ctk.CTkFrame(messages_frame, fg_color=("#3B8ED0" if sender=='you' else "#D3D3D3"), corner_radius=10)
        lbl = ctk.CTkLabel(bubble, text=text, wraplength=500, text_color=("white" if sender=='you' else "black"))
        lbl.pack(padx=10, pady=8)
        key = (ts or text)
        if key in displayed:
            return
        displayed.add(key)
        if sender == 'you':
            bubble.pack(anchor='e', pady=6, padx=10, fill='none')
        else:
            bubble.pack(anchor='w', pady=6, padx=10, fill='none')
        root.update_idletasks()
        canvas.yview_moveto(1.0)

    for m, s in initial_messages:
        add_message(m, s)

    # Input area
    input_bar = ctk.CTkFrame(right_frame, height=60)
    input_bar.grid(row=2, column=0, sticky="ew", padx=8, pady=(0,8))
    input_entry = ctk.CTkEntry(input_bar, placeholder_text="Message #general")
    input_entry.pack(side='left', fill='x', expand=True, padx=(10,6), pady=10)

    # API settings
    BASE_URL = 'https://127.0.0.1:5000'
    VERIFY = False

    def send():
        text = input_entry.get().strip()
        if not text:
            return
        # Optimistically show message locally
        add_message(text, 'you', ts=str(time.time()))
        input_entry.delete(0, 'end')
        # Send to server in background
        def _send_bg(t=text):
            try:
                api_client.send_message(t, sender='gui-user', room='general', base_url=BASE_URL, verify=VERIFY)
            except Exception:
                pass
        threading.Thread(target=_send_bg, daemon=True).start()

    def poll_loop():
        while True:
            try:
                msgs = api_client.get_messages(room='general', base_url=BASE_URL, verify=VERIFY)
                # schedule UI update on main thread
                def _update():
                    for m in msgs:
                        text = m.get('text') or m.get('MSG') or ''
                        sender = m.get('sender') or m.get('UserName') or 'them'
                        ts = m.get('ts') or m.get('DateInf') or text
                        add_message(text, sender if sender else 'them', ts=ts)
                root.after(0, _update)
            except Exception as e:
                # ignore transient errors (server down, etc.)
                pass
            time.sleep(2)

    # start poller thread
    threading.Thread(target=poll_loop, daemon=True).start()

    send_btn = ctk.CTkButton(input_bar, text="Send", width=100, command=send)
    send_btn.pack(side='right', padx=(6,10), pady=10)

    # Enter binding
    input_entry.bind('<Return>', lambda e: send())

    root.mainloop()


if __name__ == '__main__':
    run_discord_like()
