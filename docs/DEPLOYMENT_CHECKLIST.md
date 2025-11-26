# Deployment & Setup Checklist

## Pre-Deployment Setup

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (optional but recommended)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created from `.env.example` template
- [ ] Database initialized (if applicable)

### Configuration
- [ ] `FLASK_ENV` set appropriately (development/production)
- [ ] `API_PORT` configured
- [ ] `CORS_ORIGINS` configured for your deployment
- [ ] `LOG_LEVEL` set for environment
- [ ] Path configuration verified

---

## Testing Before Deployment

### Unit Tests
- [ ] Run full test suite: `pytest tests/test_api.py -v`
- [ ] All tests passing: Expected 20+ tests ✅
- [ ] No warnings in test output
- [ ] Coverage > 80% on critical paths

### Manual API Tests
```bash
# Test documentation endpoint
curl http://localhost:5000/api/docs

# Test all courses endpoint
curl http://localhost:5000/api/all-courses

# Test path calculation
curl -X POST http://localhost:5000/api/path \
  -H "Content-Type: application/json" \
  -d '{"start_courses":["Python Basics"],"goal_course":"Data Structures"}'

# Test error handling
curl -X POST http://localhost:5000/api/path \
  -H "Content-Type: application/json" \
  -d '{"start_courses":[],"goal_course":"Data Structures"}'
```

- [ ] All manual tests pass
- [ ] Error messages clear and helpful
- [ ] CORS headers present in responses

### Performance Tests
- [ ] API response time < 500ms
- [ ] No memory leaks (monitor for 5 minutes)
- [ ] Logging performance acceptable

---

## Pre-Production Checks

### Security
- [ ] No hardcoded credentials in code
- [ ] `.env` file added to `.gitignore`
- [ ] Debug mode disabled in production
- [ ] CORS origins properly configured (not `*`)
- [ ] Input validation active
- [ ] Error messages don't leak sensitive info

### Code Quality
- [ ] No TODO or FIXME comments left
- [ ] Type hints present on all functions
- [ ] Documentation complete
- [ ] Docstrings accurate
- [ ] No unused imports

### Logging
- [ ] Structured logging configured
- [ ] Log file rotation setup
- [ ] Log level appropriate for environment
- [ ] Sensitive data not logged
- [ ] Timestamps correct

---

## Deployment Steps

### 1. Code Deployment
```bash
# Clone or pull latest code
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run tests
pytest tests/test_api.py -v --tb=short
```
- [ ] Code deployed
- [ ] Tests passing
- [ ] No merge conflicts

### 2. Environment Setup
```bash
# Copy and configure environment file
cp .env.example .env
# Edit .env with production settings
```
- [ ] `.env` file configured
- [ ] All required variables set
- [ ] Database path correct (if applicable)
- [ ] Log file path writable

### 3. Start Service
```bash
cd learning-path-advisor/backend
python server.py
```
- [ ] Server starts without errors
- [ ] Initial log messages appear
- [ ] API responds to requests

### 4. Verify Deployment
```bash
# Check API is responding
curl -v http://localhost:5000/api/all-courses

# Check documentation
curl http://localhost:5000/api/docs
```
- [ ] API responding correctly
- [ ] Documentation accessible
- [ ] No errors in logs
- [ ] CORS headers correct

---

## Post-Deployment Verification

### Health Checks (First Hour)
- [ ] Server running without crashes
- [ ] API endpoints responding
- [ ] Database queries successful
- [ ] No error spikes in logs
- [ ] Performance metrics normal

### Extended Monitoring (First Day)
- [ ] All endpoints working correctly
- [ ] Error rate < 0.1%
- [ ] Response times consistent
- [ ] Memory usage stable
- [ ] No unhandled exceptions

### Load Testing (Optional)
```bash
# Simple load test with curl
for i in {1..100}; do
  curl http://localhost:5000/api/all-courses
done
```
- [ ] Server handles concurrent requests
- [ ] No performance degradation
- [ ] Memory usage acceptable

---

## Configuration Checklist

### Development Environment
```
FLASK_ENV=development
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=*
LOG_LEVEL=DEBUG
```
- [ ] Configuration set correctly

### Production Environment
```
FLASK_ENV=production
API_HOST=0.0.0.0  # or specific IP
API_PORT=5000     # or 80/443 with reverse proxy
CORS_ORIGINS=yourdomain.com
LOG_LEVEL=WARNING
```
- [ ] Configuration set correctly
- [ ] Security settings enabled
- [ ] All secrets in .env, not in code

---

## Troubleshooting Checklist

### Server Won't Start
- [ ] Python version check: `python --version` (must be 3.8+)
- [ ] Port available: `netstat -ano | findstr :5000` (Windows)
- [ ] Dependencies installed: `pip list | grep Flask`
- [ ] .env file readable
- [ ] No syntax errors in config.py

### API Returns 500 Errors
- [ ] Check logs for actual error message
- [ ] Run tests to identify issue: `pytest tests/test_api.py -v`
- [ ] Check .env configuration
- [ ] Verify database/data files exist
- [ ] Check permissions on log directory

### CORS Errors in Frontend
- [ ] Check CORS_ORIGINS in .env
- [ ] Verify origin matches frontend domain
- [ ] Check server is actually running
- [ ] Look for CORS headers in response: `curl -v`
- [ ] Check browser console for detailed error

### Performance Issues
- [ ] Check memory usage: `top` or Task Manager
- [ ] Monitor log file for slow operations
- [ ] Run tests to identify bottlenecks
- [ ] Check for database locks
- [ ] Consider caching implementation (Priority 2)

---

## Rollback Procedure

If deployment fails:

```bash
# Stop the server
# Windows: taskkill /PID <pid> /F
# Mac/Linux: kill <pid>

# Revert to previous version
git revert HEAD
git pull origin main

# Or checkout previous commit
git checkout <previous-commit-sha>

# Reinstall dependencies
pip install -r requirements.txt

# Restart server
python server.py
```

- [ ] Rollback completed
- [ ] Server running on previous version
- [ ] Data verified intact
- [ ] Users notified if needed

---

## Monitoring After Deployment

### Daily Checks
- [ ] Server running (check process list)
- [ ] Error logs reviewed
- [ ] Performance metrics checked
- [ ] No unhandled exceptions
- [ ] Database/data files intact

### Weekly Checks
- [ ] Test suite run: `pytest tests/test_api.py -v`
- [ ] Performance trending (getting faster/slower?)
- [ ] Disk space available
- [ ] Backup completed
- [ ] Logs rotated

### Monthly Checks
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Run security audit
- [ ] Database optimization
- [ ] Performance optimization review
- [ ] Capacity planning

---

## Backup Checklist

Before production deployment:

- [ ] Code backed up (git repository)
- [ ] .env file backed up (secure location)
- [ ] Database backed up (if applicable)
- [ ] Configuration files backed up
- [ ] Logs directory backed up

---

## Documentation Checklist

- [ ] README.md updated with new setup instructions
- [ ] API documentation accessible: http://localhost:5000/api/docs
- [ ] Configuration options documented in `.env.example`
- [ ] Troubleshooting guide available
- [ ] Team trained on new error handling
- [ ] Deployment procedure documented

---

## Sign-Off Checklist

### Development Team
- [ ] Code review completed
- [ ] Tests passing
- [ ] Documentation complete
- [ ] No known issues

### QA Team
- [ ] Manual testing completed
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Performance acceptable

### DevOps/System Admin
- [ ] Infrastructure ready
- [ ] Monitoring configured
- [ ] Backup procedure verified
- [ ] Rollback plan ready

### Product Manager
- [ ] Business requirements met
- [ ] User documentation ready
- [ ] Stakeholders informed

---

## Post-Deployment Support Plan

### First Week
- Daily monitoring
- Quick response to issues
- Performance baseline established
- Team trained on new features

### First Month
- Weekly reviews
- Bug fixes deployed
- Performance optimization
- User feedback collected

### Ongoing
- Monthly updates
- Quarterly performance review
- Annual security audit
- Continuous improvement

---

## Contact & Escalation

For deployment issues:
1. Check logs: `tail -f /path/to/logfile`
2. Review troubleshooting guide
3. Run test suite: `pytest tests/ -v`
4. Check configuration: Review `.env` file
5. Escalate to development team if unresolved

---

## Final Sign-Off

- [ ] All checklists completed
- [ ] Testing passed
- [ ] Configuration verified
- [ ] Documentation ready
- [ ] Team trained
- [ ] Monitoring active
- [ ] Rollback plan ready

**Deployment Date**: _______________
**Deployed By**: _______________
**Approved By**: _______________

---

**Keep this checklist for future reference and updates!**
