import csv
from datetime import datetime
import os

# Simulated data
data = [{"timestamp": datetime.now().isoformat(), "bike_count": 12}]

# File path
filename = f"/home/pi/exports/data_{datetime.now().strftime('%Y-%m-%dT%H:%M')}.csv"

os.makedirs("/home/pi/exports", exist_ok=True)

# Write CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["timestamp", "bike_count"])
    writer.writeheader()
    writer.writerows(data)

# Upload to Google Drive
os.system(f"rclone copy {filename} gdrive:nextbike-data")
