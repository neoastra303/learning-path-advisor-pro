# Command Reference - Quick Commands

## Setup & Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Upgrade dependencies
pip install -r requirements.txt --upgrade

# Install with development dependencies
pip install -r requirements.txt pytest pytest-cov
```

---

## Running the Server

### Development Mode (Default)
```bash
cd learning-path-advisor/backend
python server.py
```
Output:
```
2024-01-15 10:30:45,123 - server - INFO - Starting Learning Path Advisor API on 0.0.0.0:5000
```

### Production Mode
```bash
set FLASK_ENV=production
cd learning-path-advisor/backend
python server.py
```

### Custom Port
```bash
set API_PORT=8000
python server.py
```

### With Configuration File
```bash
cp .env.example .env
# Edit .env with your settings
python server.py
```

---

## Testing

### Run All Tests
```bash
pytest tests/test_api.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_api.py::TestValidation -v
pytest tests/test_api.py::TestAPIEndpoints -v
pytest tests/test_api.py::TestErrorHandling -v
```

### Run Specific Test
```bash
pytest tests/test_api.py::TestValidation::test_validate_input_valid -v
```

### Run with Coverage Report
```bash
pytest tests/test_api.py --cov=server --cov-report=html
```

### Run with Short Output
```bash
pytest tests/test_api.py -q
```

### Stop on First Failure
```bash
pytest tests/test_api.py -x
```

---

## API Testing with curl

### Test Documentation Endpoint
```bash
curl http://localhost:5000/
curl http://localhost:5000/api/docs
```

### Get All Courses
```bash
curl http://localhost:5000/api/all-courses
```

### Get All Categories
```bash
curl http://localhost:5000/api/all-categories
```

### Calculate Learning Path
```bash
curl -X POST http://localhost:5000/api/path \
  -H "Content-Type: application/json" \
  -d "{
    \"start_courses\": [\"Python Basics\"],
    \"goal_course\": \"Machine Learning\",
    \"learning_style\": \"balanced\"
  }"
```

### Get Course Recommendations
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d "{
    \"completed_courses\": [\"Python Basics\"],
    \"strategy\": \"meu\",
    \"risk_tolerance\": 0.5
  }"
```

### Get Course Details
```bash
curl -X POST http://localhost:5000/api/course-details \
  -H "Content-Type: application/json" \
  -d "{
    \"course_name\": \"Python Basics\",
    \"completed_courses\": []
  }"
```

### Plan Career Path
```bash
curl -X POST http://localhost:5000/api/career-path \
  -H "Content-Type: application/json" \
  -d "{
    \"current_skills\": [\"Python Basics\"],
    \"target_career\": \"Data Scientist\",
    \"time_horizon_months\": 12
  }"
```

### Skill Gap Analysis
```bash
curl -X POST http://localhost:5000/api/skill-gap-analysis \
  -H "Content-Type: application/json" \
  -d "{
    \"current_skills\": [\"Python Basics\"],
    \"target_skills\": [\"Machine Learning\", \"Data Visualization\"]
  }"
```

---

## Configuration

### Copy Environment Template
```bash
cp .env.example .env
```

### View Current Configuration
```bash
# Windows
type .env

# Mac/Linux
cat .env
```

### Edit Configuration
```bash
# Windows (Notepad)
notepad .env

# Mac (TextEdit)
open -t .env

# Linux (nano)
nano .env
```

### Validate Configuration
```bash
python -c "from config import config; print(f'Environment: {config.__class__.__name__}')"
```

---

## Logging

### View Server Logs (Running Process)
```bash
# Windows: Use Control+C to see output
# Mac/Linux: Logs appear in terminal

# To save logs to file
python server.py > server.log 2>&1 &
```

### Tail Logs (Linux/Mac)
```bash
tail -f server.log
tail -100 server.log
```

### Search Logs
```bash
# Mac/Linux
grep "ERROR" server.log
grep -i "course" server.log

# Windows PowerShell
Select-String -Path server.log -Pattern "ERROR"
```

---

## Debugging

### Check if Port is in Use
```bash
# Windows
netstat -ano | findstr :5000
tasklist | findstr python

# Mac/Linux
lsof -i :5000
ps aux | grep python
```

### Kill Process on Port
```bash
# Windows (replace PID)
taskkill /PID 1234 /F

# Mac/Linux
kill -9 <PID>
```

### Test Python Installation
```bash
python --version
python -m pip --version
which python  # or 'where python' on Windows
```

### Test Flask Installation
```bash
python -c "import flask; print(flask.__version__)"
python -c "from flask_cors import CORS; print('CORS OK')"
```

---

## Development Workflow

### Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies in Virtual Environment
```bash
pip install -r requirements.txt
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

---

## File Operations

### Check Directory Structure
```bash
# Windows
tree

# Mac/Linux
tree -L 2
find . -type f -name "*.py" | head -20
```

### View File Contents
```bash
# Quick view
cat server.py

# Paged view
more server.py

# Search in files
grep -r "CORS" .
grep -r "def " learning-path-advisor/backend/
```

### Find Files
```bash
# All Python files
find . -name "*.py"

# All test files
find . -name "*test*.py"

# All config files
find . -name "*.env*"
```

---

## Git Commands

### Check Git Status
```bash
git status
git diff
```

### Commit Changes
```bash
git add .
git commit -m "Add improvements: CORS, validation, logging"
git push origin main
```

### View Commit History
```bash
git log --oneline
git log --oneline -10
git show <commit-sha>
```

### Rollback Changes
```bash
git revert HEAD
git checkout .
git reset --hard HEAD~1
```

---

## Documentation Access

### Quick Start
```bash
# View available documentation
ls -la *.md

# Read documentation
cat QUICK_REFERENCE.md
cat IMPLEMENTATION_SUMMARY.md
cat IMPROVEMENT_PLAN.md
```

### In Browser
```
http://localhost:5000/          # Home + API docs
http://localhost:5000/api/docs  # API docs only
```

---

## Performance Testing

### Simple Load Test
```bash
# Test single endpoint 10 times
for i in {1..10}; do
  curl -w "Time: %{time_total}s\n" http://localhost:5000/api/all-courses
done
```

### Measure Response Time
```bash
time curl -X POST http://localhost:5000/api/path \
  -H "Content-Type: application/json" \
  -d '{"start_courses":["Python Basics"],"goal_course":"Machine Learning"}'
```

### Concurrent Requests (requires Apache Bench)
```bash
ab -n 100 -c 10 http://localhost:5000/api/all-courses
```

---

## Database Commands (When Implemented)

```bash
# Initialize database
python manage.py db init

# Create tables
python manage.py db create

# Migrate
python manage.py db migrate

# Seed data
python manage.py db seed

# Backup
python manage.py db backup
```

---

## Troubleshooting Commands

### Check Python Version
```bash
python --version
python -c "import sys; print(f'Python {sys.version}')"
```

### Check Package Versions
```bash
pip list | grep Flask
pip show flask-cors
```

### Verify Imports
```bash
python -c "from server import app; print('Import OK')"
python -c "from enhanced_learning_path_advisor import *; print('Import OK')"
```

### Run Single Test for Debugging
```bash
pytest tests/test_api.py::TestValidation::test_validate_input_valid -vv -s
```

### Generate Test Coverage Report
```bash
pytest tests/ --cov=server --cov-report=term-missing
pytest tests/ --cov=server --cov-report=html
# Then open htmlcov/index.html
```

---

## Cheat Sheet

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Start server | `python server.py` |
| Run tests | `pytest tests/ -v` |
| View API docs | `http://localhost:5000/api/docs` |
| Test endpoint | `curl http://localhost:5000/api/all-courses` |
| Kill process | `taskkill /PID <pid> /F` |
| Check port | `netstat -ano \| findstr :5000` |
| View logs | `tail -f server.log` |
| Edit config | Edit `.env` file |
| Check status | `git status` |

---

## Environment Variables Quick Set

### Windows (Command Prompt)
```batch
set FLASK_ENV=production
set API_PORT=8000
set LOG_LEVEL=WARNING
python server.py
```

### Windows (PowerShell)
```powershell
$env:FLASK_ENV="production"
$env:API_PORT="8000"
$env:LOG_LEVEL="WARNING"
python server.py
```

### Mac/Linux
```bash
export FLASK_ENV=production
export API_PORT=8000
export LOG_LEVEL=WARNING
python server.py
```

---

**Keep this reference for daily development!** 📋
