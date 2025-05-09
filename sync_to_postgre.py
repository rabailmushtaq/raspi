import os
import csv
import glob
import psycopg2
from dotenv import load_dotenv

load_dotenv("local/.env")

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

os.makedirs("data", exist_ok=True)
os.system("rclone copy gdrive:nextbike-data ./data")

for filepath in glob.glob("data/*.csv"):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute(
                "INSERT INTO bike_data (timestamp, bike_count) VALUES (%s, %s)",
                (row["timestamp"], int(row["bike_count"]))
            )
    os.remove(filepath)

conn.commit()
cursor.close()
conn.close()
