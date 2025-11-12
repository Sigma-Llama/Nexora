import customtkinter as ctk

DATABASE = {                            # To je zaj zacasno samo da dela pol pride tvoj db
    "user@test.com": "geslo123",
    "test@test.si": "geslo456"
}

def db(email, password):
    if email in DATABASE:
        if DATABASE[email] == password:
            return "SUCCESS"
        else:
            return "WRONG_PASSWORD"
    else:
        return "NOT_FOUND"


def loginSignup():
    """
    Tu bo main aplikacija
    """

    root = ctk.CTk()
    root.title("Login/Signup")
    root.geometry("400x500")

    def final_signup():
        clear_frame(signup_frame)
        success_label = ctk.CTkLabel(signup_frame, text="Registracija Uspesna!", font=("Roboto", 20))
        success_label.pack(expand=True)
        print("Registracija uspesno zakljucena.")

    # --- Preveri email ---
    def process_signup():
        email = email_entry_signup.get()
        signup_error_label.configure(text="")

        if "@" in email:
            print("Sign-up za:", email)
            
            clear_frame(signup_frame)
            
            verification_label = ctk.CTkLabel(signup_frame, text="Vnesi 6 mestno kodo", font=("Roboto", 18))
            verification_label.pack(pady=(40,10), padx=10)

            code_entry = ctk.CTkEntry(signup_frame, placeholder_text="_ _ _ _ _ _", justify="center", width=200)
            code_entry.pack(pady=10, padx=10)
            
            finish_button = ctk.CTkButton(signup_frame, text="Registriraj se", command=final_signup)
            finish_button.pack(pady=20, padx=10)
        else:
            signup_error_label.configure(text="Jebi se. To ni email.", text_color="red")

    # --- Preverjanje login podatkov ---
    def process_login():
        email = email_entry_login.get()
        password = password_entry_login.get()
        
        login_error_label.configure(text="")
        
        result = db(email, password)

        if result == "SUCCESS":
            # Tu bo pol koda, ki odpre glavni del aplikacije.
            print("Login Successful!")
            clear_frame(login_frame)
            success_label = ctk.CTkLabel(login_frame, text=f"Welcome,\n{email}", font=("Roboto", 24))
            success_label.pack(expand=True)

        elif result == "NOT_FOUND":
            login_error_label.configure(text="Account ni najden.")
        elif result == "WRONG_PASSWORD":
            login_error_label.configure(text="Geslo napačno.")


    def show_login_frame():
        signup_frame.pack_forget()
        login_frame.pack(pady=20, padx=60, fill="both", expand=True)

    def show_signup_frame():
        login_frame.pack_forget()
        signup_frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # --- Initial Frame ---
    initial_frame = ctk.CTkFrame(root)
    initial_frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    # --- Initial Frame (Widget) ---
    hello_label = ctk.CTkLabel(initial_frame, text="Dober Dan", font=("Roboto", 24))
    hello_label.pack(pady=12, padx=10)

    login_button_initial = ctk.CTkButton(initial_frame, text="Log In", command=show_login_frame)
    login_button_initial.pack(pady=12, padx=10)

    signin_button_initial = ctk.CTkButton(initial_frame, text="Sign Up", command=show_signup_frame)
    signin_button_initial.pack(pady=12, padx=10)

    # --- Login Frame ---
    login_frame = ctk.CTkFrame(root) # Hidden

    # --- Login Frame (Widget) ---
    email_entry_login = ctk.CTkEntry(login_frame, placeholder_text="E-mail")
    email_entry_login.pack(pady=12, padx=10)

    password_entry_login = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
    password_entry_login.pack(pady=12, padx=10)
    
    forgot_password_button = ctk.CTkButton(login_frame, text="Forgot Password?", fg_color="transparent", border_width=0, text_color=("gray70", "gray30"))
    forgot_password_button.pack(pady=12, padx=10)

    login_button_login = ctk.CTkButton(login_frame, text="Log In", command=process_login)
    login_button_login.pack(pady=(12, 5), padx=10)
    
    # --- Error ---
    login_error_label = ctk.CTkLabel(login_frame, text="", text_color="red")
    login_error_label.pack(pady=5, padx=10)


    # --- Sign up Frame ---
    signup_frame = ctk.CTkFrame(root) # Hidden

    # --- Sign Up Frame (Widget) ---
    username_entry_signup = ctk.CTkEntry(signup_frame, placeholder_text="Username")
    username_entry_signup.pack(pady=12, padx=10)
    
    email_entry_signup = ctk.CTkEntry(signup_frame, placeholder_text="E-mail")
    email_entry_signup.pack(pady=12, padx=10)

    password_entry_signup = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*")
    password_entry_signup.pack(pady=12, padx=10)
    
    signup_button_signup = ctk.CTkButton(signup_frame, text="Sign Up", command=process_signup)
    signup_button_signup.pack(pady=(12, 5), padx=10)

    # ---  Error ---
    signup_error_label = ctk.CTkLabel(signup_frame, text="", text_color="red")
    signup_error_label.pack(pady=5, padx=10)


    login_frame.pack_forget()
    signup_frame.pack_forget()

    root.mainloop()

    
if __name__ == "__main__":
    loginSignup()