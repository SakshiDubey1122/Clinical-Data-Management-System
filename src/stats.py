import pandas as pd
import matplotlib.pyplot as plt
import os

class StatisticsGenerator:
    def __init__(self, patient_file='data/Patient_data.csv'):
        self.patient_file = patient_file
        self.df = self.load_data()

    def load_data(self):
        if not os.path.exists(self.patient_file):
            return pd.DataFrame()
        try:
            df = pd.read_csv(self.patient_file, encoding='utf-8-sig')
            df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
            print("DEBUG HEAD:\n", df.head())
            print("COLUMNS:", df.columns.tolist())
        except Exception as e:
            print(f"Error reading file: {e}")
            return pd.DataFrame()

        if "Visit_time" in df.columns:
            df["Visit_time"] = pd.to_datetime(df["Visit_time"], errors='coerce', infer_datetime_format=True)
        else:
            print("'Visit_time' column is missing in Patient_data.csv")
            df["Visit_time"] = pd.NaT

        return df

    def visits_over_time(self):
        if self.df.empty or "Visit_time" not in self.df.columns:
            print("No data for visits_over_time")
            return

        visits_by_date = self.df["Visit_time"].dt.date.value_counts().sort_index()
        print("Visit counts by date:\n", visits_by_date)

        try:
            plt.figure(figsize=(10, 5))
            visits_by_date.plot(kind='line', title='Visits Over Time', marker='o')
            plt.xlabel("Date")
            plt.ylabel("Number of Visits")
            plt.xticks(rotation=45)
            plt.tight_layout()
            os.makedirs("output", exist_ok=True)
            plt.savefig("output/visits_over_time.png")
            plt.close()
            print("visits_over_time.png saved in output/")
        except Exception as e:
            print("Error creating visits_over_time.png:", e)

    def insurance_distribution(self):
        if self.df.empty or "Insurance" not in self.df.columns:
            print("No data for insurance_distribution")
            return

        counts = self.df["Insurance"].value_counts()
        print("Insurance counts:\n", counts)

        try:
            plt.figure(figsize=(8, 5))
            counts.plot(kind='bar', title='Insurance Distribution', color='skyblue')
            plt.xlabel("Insurance Type")
            plt.ylabel("Patient Count")
            plt.tight_layout()
            os.makedirs("output", exist_ok=True)
            plt.savefig("output/insurance_distribution.png")
            plt.close()
            print("insurance_distribution.png saved in output/")
        except Exception as e:
            print("Error creating insurance_distribution.png:", e)

    def demographics_summary(self):
        if self.df.empty:
            return "No data available."

        summary = {}
        for field in ["Gender", "Race", "Ethnicity"]:
            if field in self.df.columns:
                summary[field] = self.df[field].value_counts().to_dict()
        return summary

    def count_visits_on_date(self, date_str):
        if self.df.empty or "Visit_time" not in self.df.columns:
            print("Dataframe is empty or missing Visit_time")
            return 0

        date_check = pd.to_datetime(date_str, errors='coerce').date()
        matched = self.df[self.df["Visit_time"].dt.date == date_check]
        print(f"🔍 Count for {date_str}: {matched.shape[0]}")
        return matched.shape[0]

    def show_stats(self):
        if self.df.empty or 'Patient_ID' not in self.df.columns:
            return "No data to show. (Missing 'Patient_ID' column)"

        os.makedirs("output", exist_ok=True)
        visuals = []

        try:
            self.visits_over_time()
            visuals.append("output/visits_over_time.png")
        except Exception as e:
            print("Failed to generate visits_over_time:", e)

        try:
            self.insurance_distribution()
            visuals.append("output/insurance_distribution.png")
        except Exception as e:
            print("Failed to generate insurance_distribution:", e)

        try:
            summary = self.demographics_summary()
            with open("output/demographics_summary.txt", "w") as f:
                for k, v in summary.items():
                    f.write(f"{k}:\n")
                    for label, count in v.items():
                        f.write(f"  {label}: {count}\n")
                    f.write("\n")
            visuals.append("output/demographics_summary.txt")
        except Exception as e:
            print("Failed demographics summary:", e)

        return f"Stats loaded. Visits: {len(self.df)}, Unique Patients: {self.df['Patient_ID'].nunique()}\n\nVisuals generated: {', '.join(visuals)}"
