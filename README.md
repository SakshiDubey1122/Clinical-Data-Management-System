# Clinical-Data-Management-System
This project is a Python-based Clinical Data Management System designed for use in a hospital or clinical environment. It provides role-based access to patient data, clinical notes, and visit statistics using a graphical interface built with the tkinter library.
Key Features

- User Authentication (from Credentials.csv)
- Role-Based Access Control
             Management: View data visualizations and statistics
             Clinician/Nurse: Retrieve/Add/Remove patients and view notes
             Admin: Can count visits
- CRUD Operations on Patient Records
- View Clinical Notes
- View Statistics & Dashboard (for Management)
- Usage Logging
- Visual Stats Dashboard auto-generated in output/
```
Repository Structure
├── data/
│   ├── Patient_data.csv         # Patient demographic & visit data
│   ├── Notes.csv                # Notes by visit/patient
│   └── Credentials.csv          # User credentials and roles
├── output/
│   ├── dashboard.png            # Visual dashboard for management
│   ├── usage_log.csv            # Tracks user actions
│   └── updated_patient_data.csv# Saved after patient modifications
├── auth.py                     # Handles authentication
├── main.py                     # Program entry (Tkinter login window)
├── notes.py                    # Note viewing logic
├── patient.py                  # Add/Remove/Retrieve patient logic
├── stats.py                    # Data analytics and plotting
├── ui_screens.py               # GUI per role
├── usage_logger.py             # Usage tracking
├── dashboard_generator.py      # Generates management-only dashboard
├── UML_Diagram.png             # Class diagram for the project
├── README.md                   # This file
└── requirements.txt            # Python dependencies                 ```

1- How to Run
bash
git clone <your-repository-url>
cd <repository-directory>

2- Set up the Python Environment
python3 -m venv venv
source venv/bin/activate

3- Requirements
Ensure you have Python 3.10+ installed.
Install packages via:
pip install -r requirements.txt

4- How to Use
Login using credentials from data/Credentials.csv
Use available UI buttons based on your role:
Admin/Nurse/Clinician: Add, remove, count, view statistics or view patients
Management: Click "View Stats" to generate a visual dashboard. The dashboard is saved in output/dashboard.png

5- Output Files
output/updated_patient_data.csv: Modified patient records
output/dashboard.png: Stats dashboard for management

6- Additional Notes
If login fails, the attempt is logged in usage_log.csv
Only management users can access the visual dashboard
Data files must be present in the data/ folder with exact headers
Dashboard errors are gracefully handled if image rendering fails

7- See UML_Diagram.png in the project root for class and interaction structure.


