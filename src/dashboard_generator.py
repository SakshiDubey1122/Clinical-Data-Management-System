# dashboard_generator.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_full_dashboard():
    # Load data
    patient_df = pd.read_csv('data/Patient_data.csv')

    # Create output folder if not exists
    os.makedirs('output', exist_ok=True)

    # Set up 2x3 grid of subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Patient Data Dashboard (Management Only)', fontsize=16)

    # Gender Distribution
    sns.countplot(data=patient_df, x='Gender', ax=axes[0, 0])
    axes[0, 0].set_title('Gender Distribution')

    # Age Distribution
    sns.histplot(data=patient_df, x='Age', bins=10, kde=True, ax=axes[0, 1])
    axes[0, 1].set_title('Age Distribution')

    # Insurance Distribution
    sns.countplot(data=patient_df, x='Insurance', order=patient_df['Insurance'].value_counts().index, ax=axes[0, 2])
    axes[0, 2].set_title('Insurance by Company')
    axes[0, 2].tick_params(axis='x', rotation=45)

    # Visit Over Time
    if 'Visit_time' in patient_df.columns:
        patient_df['Visit_time'] = pd.to_datetime(patient_df['Visit_time'], errors='coerce')
        visits_by_date = patient_df['Visit_time'].dt.date.value_counts().sort_index()
        axes[1, 0].plot(visits_by_date.index, visits_by_date.values, marker='o')
        axes[1, 0].set_title('Visits Over Time')
        axes[1, 0].tick_params(axis='x', rotation=45)

    # Department of Visit
    sns.countplot(data=patient_df, y='Visit_department', order=patient_df['Visit_department'].value_counts().index, ax=axes[1, 1])
    axes[1, 1].set_title('Department of Visit')

    # Empty plot for layout balance
    fig.delaxes(axes[1, 2])  # remove unused subplot

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = os.path.join("output", "dashboard.png")
    plt.savefig(output_path)
    plt.close()
