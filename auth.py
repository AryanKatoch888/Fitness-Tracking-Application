import tkinter as tk
from tkinter import ttk, messagebox
from db_setup import connect_db, setup_database  


class AuthApp:
    def __init__(self, root, navigation_manager):
        self.root = root
        self.navigation_manager = navigation_manager
        self.root.title("Login & Signup")
        self.root.geometry("400x300")

        # Frames for Login and Signup
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(expand=True)

        # Add Login widgets
        self.login_widgets()

    def login_widgets(self):
        """Widgets for the Login page."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        ttk.Label(self.frame, text="Login", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.frame, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame, width=15)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=15)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Login", command=self.login).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self.frame, text="Signup", command=self.signup_widgets).grid(row=3, column=1, padx=5, pady=10)

    def signup_widgets(self):
        """Widgets for the Signup page."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        ttk.Label(self.frame, text="Signup", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.frame, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame, width=15)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=15)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Signup", command=self.signup).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self.frame, text="Back to Login", command=self.login_widgets).grid(row=3, column=1, padx=5, pady=10)

    def login(self):
        """Handle the login process."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                messagebox.showinfo("Success", f"Welcome, {username}!")
                self.root.destroy()
                self.navigation_manager.show_fitness_app()
                
                
            else:
                messagebox.showerror("Error", "Invalid credentials!")

    def signup(self):
        """Handle the signup process."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Signup successful! Please login.")
                self.login_widgets()
            except Error as e:
                messagebox.showerror("Error")
