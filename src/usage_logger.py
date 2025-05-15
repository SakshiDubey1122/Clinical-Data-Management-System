import csv
from datetime import datetime
import os

class UsageLogger:
    def __init__(self, log_file='usage_log.csv'):
        self.log_file = log_file
        self.ensure_log_file()

    def ensure_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Username', 'Role', 'Action'])

    def log(self, username, role, action):
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                username,
                role,
                action
            ])
