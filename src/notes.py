import pandas as pd
import os

class NotesHandler:
    def __init__(self, notes_file='data/Notes.csv'):
        self.notes_file = notes_file
        self.default_columns = ["Patient_ID", "Visit_ID", "Note_ID", "Note_text"]

    def load_data(self):
        if not os.path.exists(self.notes_file):
            print("Notes file not found. Returning empty DataFrame.")
            return pd.DataFrame(columns=self.default_columns)
        try:
            df = pd.read_csv(self.notes_file, encoding='utf-8-sig')
            df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
            return df
        except Exception as e:
            print(f"Error reading notes file: {e}")
            return pd.DataFrame(columns=self.default_columns)

    def view_note(self, patient_id, visit_id):
        df = self.load_data()
        try:
            patient_id = str(patient_id).strip()
            visit_id = str(visit_id).strip()

            df["Patient_ID"] = df["Patient_ID"].astype(str).str.strip()
            df["Visit_ID"] = df["Visit_ID"].astype(str).str.strip()

            result = df[
                (df["Patient_ID"] == patient_id) &
                (df["Visit_ID"] == visit_id)
            ]

            if result.empty:
                return f"No note found for Patient_ID {patient_id}, Visit_ID {visit_id}."
            return result[["Note_ID", "Note_text"]].to_string(index=False)
        except Exception as e:
            return f"Error processing note: {e}"

    def add_note(self, patient_id, visit_id, note_id, note_text):
        df = self.load_data()
        new_entry = pd.DataFrame([{
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Note_ID": note_id,
            "Note_text": note_text
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        try:
            df.to_csv(self.notes_file, index=False, encoding='utf-8-sig')
            print(f"Note added for Patient_ID {patient_id}, Visit_ID {visit_id}")
        except Exception as e:
            print(f"Error saving notes: {e}")
