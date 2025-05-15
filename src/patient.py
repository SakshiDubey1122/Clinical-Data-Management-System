import csv
import os
import pandas as pd

class PatientManager:
    def __init__(self, patient_file='data/Patient_data.csv'):
        self.patient_file = patient_file
        self.headers = [
            "Patient_ID", "Visit_ID", "Visit_time", "Visit_department",
            "Race", "Gender", "Ethnicity", "Age", "Zip_code",
            "Insurance", "Chief_complaint", "Note_ID", "Note_type"
        ]

    def load_data(self):
        if not os.path.exists(self.patient_file):
            return pd.DataFrame(columns=self.headers)
        try:
            df = pd.read_csv(self.patient_file, encoding='utf-8-sig')
            df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
            return df
        except Exception as e:
            print(f"Error reading patient file: {e}")
            return pd.DataFrame(columns=self.headers)

    def save_data(self, df):
        try:
            df.to_csv(self.patient_file, index=False)
        except Exception as e:
            print(f"Error saving patient file: {e}")

    def add_patient(self, patient_id, visit_info):
        df = self.load_data()
        visit_info_cleaned = {col: visit_info.get(col, '') for col in self.headers}
        df = pd.concat([df, pd.DataFrame([visit_info_cleaned])], ignore_index=True)
        self.save_data(df)

    def remove_patient(self, patient_id):
        df = self.load_data()
        patient_id = str(patient_id).strip()
        df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
        initial_count = len(df)
        df = df[df["Patient_ID"] != patient_id]
        self.save_data(df)
        removed_count = initial_count - len(df)
        return f"Removed {removed_count} record(s) for Patient_ID: {patient_id}"

    def retrieve_patient(self, patient_id):
        df = self.load_data()
        patient_id = str(patient_id).strip()
        df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
        patient_df = df[df["Patient_ID"] == patient_id]
        if patient_df.empty:
            return f"No records found for Patient_ID: {patient_id}"
        return patient_df.to_string(index=False)
