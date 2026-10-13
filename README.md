# Employee Attendance & Analytics API

Complete FastAPI + MongoDB backend for HR attendance management.

## Quick Start

### 1. Install MongoDB

**Option A - MongoDB Atlas (Recommended - Free Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free M0 cluster
3. Get connection string
4. Update `.env` file

**Option B - Local MongoDB**
```bash
# Download from: https://www.mongodb.com/try/download/community
# Or use Docker:
docker run -d -p 27017:27017 mongo:7
```

### 2. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure MongoDB
copy .env.example .env
# Edit .env with your MongoDB connection string
```

### 3. Run

```bash
# Load sample data (optional)
python sample_seed.py

# Start API
uvicorn app.main:app --port 8000 --reload
```

### 4. Access

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Project Structure

```
├── app/
│   └── main.py              # Complete API (1100+ lines)
├── sample_data/             # Sample employees & attendance
├── REVIEW.md                # Part A: Code review
├── DECISIONS.md             # Part C: Technical decisions
├── openapi.yaml             # API specification
└── requirements.txt         # Dependencies
```

## Features

✅ **11 API Endpoints** - Complete CRUD + Analytics  
✅ **Business Rules R1-R10** - IST timezone, overtime, grace period  
✅ **MongoDB Aggregations** - Employee summaries, leaderboards, trends  
✅ **Race-Safe** - Atomic operations, no duplicate punch-ins  
✅ **8 Optimized Indexes** - Fast queries on 100k+ records  
✅ **Complete Documentation** - OpenAPI spec, code review, decisions  

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/employees` | Create employee |
| GET | `/employees` | List employees |
| POST | `/attendance/punch-in` | Punch in |
| POST | `/attendance/punch-out` | Punch out |
| GET | `/attendance` | List attendance |
| PATCH | `/attendance/{emp_code}/{date}` | Regularize record |
| GET | `/analytics/employees/{emp_code}/monthly` | Monthly summary |
| GET | `/analytics/departments/summary` | Department summary |
| GET | `/analytics/leaderboard/late` | Late comers |
| GET | `/analytics/departments/{dept}/trend` | Daily trend |

## Assignment Completion

- ✅ **Part A (Review):** REVIEW.md - 15 defects documented
- ✅ **Part B (Build):** All endpoints implemented with MongoDB aggregations
- ✅ **Part C (Explain):** DECISIONS.md - 5 technical questions answered

## Submission Ready

All requirements met:
- All code in `app/main.py` (single file as required)
- Complete documentation
- Sample data included
- Ready to test with evaluator's MongoDB

---

**HROne Software Engineer Trainee Assignment**  
FastAPI + MongoDB + Python 3.11+
