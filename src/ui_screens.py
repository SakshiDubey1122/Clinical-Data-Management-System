import tkinter as tk
from tkinter import messagebox
from stats import StatisticsGenerator
from patient import PatientManager
from notes import NotesHandler
from usage_logger import UsageLogger
from dashboard_generator import generate_full_dashboard
from PIL import Image, ImageTk
import os

class UIScreens:
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.pm = PatientManager()
        self.nh = NotesHandler()
        self.logger = UsageLogger()
        self.stats = StatisticsGenerator()
        self.root = tk.Tk()
        self.root.title(f"Welcome {self.username} - Role: {self.role}")
        self.build_menu()

    def build_menu(self):
        if self.role in ['nurse', 'clinician', 'admin']:
            tk.Button(self.root, text="Count Visits", command=self.ask_date_and_show_visits).pack(pady=5)

        if self.role in ['nurse', 'clinician']:
            tk.Button(self.root, text="Add Patient", command=self.add_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Remove Patient", command=self.remove_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Retrieve Patient", command=self.retrieve_patient_ui).pack(pady=5)
            tk.Button(self.root, text="View Note", command=self.view_note_ui).pack(pady=5)

        if self.role == 'management':
            tk.Button(self.root, text="View Stats", command=self.show_stats_ui).pack(pady=5)

        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)
        self.root.mainloop()

    def ask_date_and_show_visits(self):
        date_win = tk.Toplevel(self.root)
        date_win.title("Enter Date")

        tk.Label(date_win, text="Date (MM/DD/YYYY):").grid(row=0, column=0)
        date_entry = tk.Entry(date_win)
        date_entry.grid(row=0, column=1)

        def submit():
            date_value = date_entry.get()
            count = self.stats.count_visits_on_date(date_value)
            messagebox.showinfo("Visit Count", f"Visits on {date_value}: {count}")
            self.logger.log(self.username, self.role, f"count_visits on {date_value}")
            date_win.destroy()

        tk.Button(date_win, text="Submit", command=submit).grid(row=1, columnspan=2)

    def add_patient_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Add Patient")

        fields = [
            "Patient_ID", "Visit_ID", "Visit_time", "Visit_department",
            "Race", "Gender", "Ethnicity", "Age", "Zip_code",
            "Insurance", "Chief_complaint", "Note_ID", "Note_type"
        ]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(win, text=field).grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[field] = entry

        def submit():
            data = {key: val.get() for key, val in entries.items()}
            self.pm.add_patient(data["Patient_ID"], data)
            messagebox.showinfo("Success", f"Patient {data['Patient_ID']} added.")
            self.logger.log(self.username, self.role, f"add_patient {data['Patient_ID']}")
            win.destroy()

        tk.Button(win, text="Add", command=submit).grid(row=len(fields), columnspan=2)

    def remove_patient_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Remove Patient")

        tk.Label(win, text="Patient_ID:").grid(row=0, column=0)
        entry = tk.Entry(win)
        entry.grid(row=0, column=1)

        def submit():
            pid = entry.get()
            msg = self.pm.remove_patient(pid)
            messagebox.showinfo("Removed", msg)
            self.logger.log(self.username, self.role, f"remove_patient {pid}")
            win.destroy()

        tk.Button(win, text="Remove", command=submit).grid(row=1, columnspan=2)

    def retrieve_patient_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Retrieve Patient")

        tk.Label(win, text="Patient_ID:").grid(row=0, column=0)
        entry = tk.Entry(win)
        entry.grid(row=0, column=1)

        def submit():
            pid = entry.get()
            result = self.pm.retrieve_patient(pid)
            messagebox.showinfo("Patient Info", result)
            self.logger.log(self.username, self.role, f"retrieve_patient {pid}")

        tk.Button(win, text="Retrieve", command=submit).grid(row=1, columnspan=2)

    def view_note_ui(self):
        win = tk.Toplevel(self.root)
        win.title("View Note")

        tk.Label(win, text="Patient_ID:").grid(row=0, column=0)
        pid_entry = tk.Entry(win)
        pid_entry.grid(row=0, column=1)

        tk.Label(win, text="Visit_ID:").grid(row=1, column=0)
        vid_entry = tk.Entry(win)
        vid_entry.grid(row=1, column=1)

        def submit():
            note = self.nh.view_note(pid_entry.get(), vid_entry.get())
            messagebox.showinfo("Note", note)
            self.logger.log(self.username, self.role, f"view_note {pid_entry.get()} {vid_entry.get()}")
            win.destroy()

        tk.Button(win, text="View", command=submit).grid(row=2, columnspan=2)

    def show_stats_ui(self):
        try:
            generate_full_dashboard()

        #dashboard_path = "output/dashboard.png"
        
        #if not os.path.exists(dashboard_path):
            messagebox.showinfo("Dashboard Generated", "Dashboard saved to output/dashboard.png")
            self.logger.log(self.username, self.role, "generated_dashboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dashboard image: {e}")
        
        #dashboard_win = tk.Toplevel(self.root)
        #dashboard_win.title("Visual Stats Dashboard")
        #try:
            #img = Image.open(dashboard_path)
           # img = img.resize((1000, 600), Image.LANCZOS)
            #self.dashboard_img_tk = ImageTk.PhotoImage(img)

            #label = tk.Label(dashboard_win, image= self.dashboard_img_tk)  # keep reference to avoid garbage collection
            #label.pack()
        #except Exception as e:
           
           #messagebox.showerror("Error", f"Failed to load dashboard image: {e}")

def show_menu_for_role(username, role):
    print(f"Launching UI for role: {role}")
    app = UIScreens(username, role)
    app.root.mainloop()
