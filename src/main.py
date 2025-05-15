from auth import Authenticator
from usage_logger import UsageLogger
from ui_screens import show_menu_for_role
from dashboard_generator import generate_full_dashboard
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class UIApp:
    def __init__(self):
        self.authenticator = Authenticator()
        self.logger = UsageLogger()
        self.root = tk.Tk()
        self.root.title("Clinical Data - Login")
        self.root.geometry("400x200")
        self.build_login_screen()
        self.root.mainloop()

    def build_login_screen(self):
        tk.Label(self.root, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)

        self.entry_user = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_pw = tk.Entry(self.root, show="*", width=30, font=("Arial", 12))

        self.entry_user.grid(row=0, column=1, padx=10, pady=10)
        self.entry_pw.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Login", width=15, command=self.attempt_login).grid(row=2, columnspan=2, pady=10)
        tk.Button(self.root, text="Exit", width=15, command=self.log_exit).grid(row=3, columnspan=2)

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pw.get()
        username, role = self.authenticator.authenticate(username, password)  

        if role:
            self.logger.log(username, role, "login_success")
            self.root.withdraw()
            show_menu_for_role(username, role)
            self.logger.log(username, role, "logout")
            self.root.destroy()
        else:
            self.logger.log(username, "unknown", "login_failed")
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def display_dashboard_image(self):
        dashboard_path = "output/dashboard.png"
        if not os.path.exists(dashboard_path):
            messagebox.showerror("Dashboard Missing", f"Dashboard image not found at: {dashboard_path}")
            return

        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Management Dashboard")

        img = Image.open(dashboard_path)
        img = img.resize((1000, 600))
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(dashboard_window, image=img_tk)
        label.image = img_tk  # Keep reference
        label.pack()
        
        dashboard_window.mainloop()

    def log_exit(self):
        self.logger.log("system", "system", "application_exit")
        self.root.destroy()

if __name__ == "__main__":
    UIApp()
