import pandas as pd
import os

class Authenticator:
    def __init__(self, credential_file='data/Credentials.csv'):
        self.credential_file = credential_file

    def authenticate(self, username, password):
        if not os.path.exists(self.credential_file):
            print("Credential file not found.")
            return None, None

        try:
            df = pd.read_csv(self.credential_file, encoding='utf-8-sig')
            df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]

            # Print for debug
            print("Loaded credentials:\n", df.head())

            # Clean up input and DataFrame
            username = str(username).strip()
            password = str(password).strip()
            df['username'] = df['username'].astype(str).str.strip()
            df['password'] = df['password'].astype(str).str.strip()
            df['role'] = df['role'].astype(str).str.strip()

            match = df[
                (df['username'] == username) &
                (df['password'] == password)
            ]

            if not match.empty:
                role = match.iloc[0]['role']
                return username, role
            else:
                print("Invalid username or password.")
                return None, None
        except Exception as e:
            print("Error during authentication:", e)
            return None, None
