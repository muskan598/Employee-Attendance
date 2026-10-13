"""
Sample data seeder for Employee Attendance & Analytics API
Loads sample employees and attendance logs from sample_data/ into MongoDB
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "attendance_db")


def load_json_file(filepath):
    """Load and parse MongoDB Extended JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def parse_extended_json(data):
    """Convert MongoDB Extended JSON $date to Python datetime"""
    from datetime import datetime
    
    def convert_dates(obj):
        if isinstance(obj, dict):
            if "$date" in obj:
                # Parse ISO 8601 date string
                date_str = obj["$date"]
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                return {k: convert_dates(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_dates(item) for item in obj]
        else:
            return obj
    
    return convert_dates(data)


def seed_database():
    """Seed the database with sample data"""
    print(f"Connecting to MongoDB: {MONGO_URI}")
    print(f"Database: {MONGO_DB}")
    
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("\nClearing existing data...")
    db.employees.delete_many({})
    db.attendance_logs.delete_many({})
    
    # Load and insert employees
    print("\nLoading employees...")
    employees_data = load_json_file("sample_data/employees.json")
    employees_data = parse_extended_json(employees_data)
    
    if employees_data:
        result = db.employees.insert_many(employees_data)
        print(f"Inserted {len(result.inserted_ids)} employees")
    
    # Load and insert attendance logs
    print("\nLoading attendance logs...")
    attendance_data = load_json_file("sample_data/attendance_logs.json")
    attendance_data = parse_extended_json(attendance_data)
    
    if attendance_data:
        result = db.attendance_logs.insert_many(attendance_data)
        print(f"Inserted {len(result.inserted_ids)} attendance records")
    
    # Verify data
    print("\n=== Verification ===")
    print(f"Total employees: {db.employees.count_documents({})}")
    print(f"Total attendance records: {db.attendance_logs.count_documents({})}")
    
    # Show sample employee
    sample_emp = db.employees.find_one()
    if sample_emp:
        print(f"\nSample employee: {sample_emp['emp_code']} - {sample_emp['name']}")
    
    # Show sample attendance
    sample_att = db.attendance_logs.find_one()
    if sample_att:
        print(f"Sample attendance: {sample_att['emp_code']} on {sample_att['date']} - {sample_att['status']}")
    
    print("\n✓ Seeding completed successfully!")
    print("\nYou can now start the API with:")
    print("  uvicorn app.main:app --port 8000 --reload")
    
    client.close()


if __name__ == "__main__":
    seed_database()
