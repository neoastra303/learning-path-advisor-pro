<div align="center">

# 🚀 Learning Path Advisor Pro

### AI-Powered Career Development Platform

**Transform your career journey with cutting-edge AI that creates personalized learning paths tailored to your goals!**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-18%20passed-success.svg)](tests/)
[![Code Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](tests/)

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-api-documentation) • [Contributing](#-contributing)

![Learning Path Advisor Demo](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Learning+Path+Advisor+Pro)

</div>

---

## 📊 At a Glance

| Feature | Description |
|---------|-------------|
| 🎓 **Course Database** | 165+ curated courses across 18 categories |
| 🤖 **AI Algorithms** | Dijkstra, A*, BFS pathfinding + MEU, Minimax strategies |
| ⚡ **Performance** | Response caching, rate limiting, performance monitoring |
| 🔒 **Security** | CORS protection, input validation, rate limiting |
| 📱 **UI/UX** | Responsive design, interactive visualizations |
| 🧪 **Testing** | 18 tests, 95%+ coverage |
| 📚 **Documentation** | Complete API docs, contribution guidelines |

---

## 🎯 Why Choose Learning Path Advisor Pro?

Our platform uses advanced AI algorithms to revolutionize how professionals plan and execute their career development. Whether you're looking to switch careers, advance in your current field, or acquire new skills, our intelligent system guides you every step of the way.

<details>
<summary><b>📈 Real-World Use Cases</b></summary>

### 🔄 Career Changers
From Marketing to Data Science? We'll show you exactly which courses to take and in what order, considering your existing skills.

**Example Path:**
```
Marketing Basics → Statistics → Python Basics → Data Analysis → Machine Learning
Estimated time: 6-8 months
```

### 🚀 Career Advancers
Already a developer? Advance to senior roles with targeted skill development.

**Example Path:**
```
Web Development → Cloud Computing → DevOps → System Architecture
Estimated time: 4-6 months
```

### 🎯 Skill Seekers
Exploring new domains? Get personalized recommendations based on your learning style.

**Example Path:**
```
Design Basics → UI/UX Design → Figma Mastery → Design Systems
Estimated time: 3-4 months
```

</details>

### 🌟 Key Features

#### 🤖 **Advanced AI Decision Making**
- **Goal-Based Agents**: Find the most efficient routes to your learning objectives using Dijkstra's, A*, and BFS algorithms
- **Utility-Based Agents**: Optimize for your personal learning style and risk tolerance  
- **Hybrid Intelligence**: Combines multiple AI approaches for superior recommendations
- **Risk Analysis**: Understand the complexity and challenges of each learning path

#### 📚 **Comprehensive Learning Ecosystem**
- **165+ Courses**: Extensive database covering Programming, Marketing, Business, Design, and more
- **Prerequisite Mapping**: Smart course sequencing based on dependencies
- **18 Learning Categories**: From AI/ML to Creative Arts to Business Development
- **Skill Gap Analysis**: Identify what you need to reach your career goals

#### 🎨 **Modern User Experience**
- **Professional UI**: Clean, easy-on-the-eyes interface designed for long learning sessions
- **Interactive Visualizations**: See your learning path mapped out visually
- **Progress Dashboard**: Track your advancement with detailed statistics
- **Mobile Responsive**: Learn anywhere, on any device
- **RESTful API**: Complete API with rate limiting and caching

#### 🎯 **Personalized Learning Paths**
- **Multiple Learning Styles**: Fastest, Easiest, Balanced, or Challenging approaches
- **Career-Specific Planning**: Direct paths to target careers
- **Risk Tolerance Settings**: Match learning intensity to your comfort level
- **Customizable Filters**: Find courses by difficulty, time, or keyword

## 🚀 Quick Start

<table>
<tr>
<td width="50%">

### 🪟 Windows

```bash
# One-click start
start.bat
```

**What it does:**
1. ✅ Creates virtual environment
2. ✅ Installs dependencies
3. ✅ Sets up configuration
4. ✅ Starts server automatically

</td>
<td width="50%">

### 🐧 Linux/macOS

```bash
# One-click start
chmod +x start.sh
./start.sh
```

**What it does:**
1. ✅ Creates virtual environment
2. ✅ Installs dependencies
3. ✅ Sets up configuration
4. ✅ Starts server automatically

</td>
</tr>
</table>

### 🌐 Access the Application

Once started, access:
- 🖥️ **Frontend UI**: Open `learning-path-advisor/frontend/index.html` in browser
- 🔌 **API Endpoint**: http://localhost:5000
- 📖 **API Docs**: http://localhost:5000/api/docs
- 📊 **Health Check**: http://localhost:5000/api/system/health

### 📋 Prerequisites

```bash
python --version  # Should be 3.8 or higher
```

That's it! No database setup, no complex configuration needed.

## 📖 Usage Guide

### 🎬 Getting Your First Learning Path (5 Simple Steps)

<details open>
<summary><b>Step-by-Step Tutorial</b></summary>

#### Step 1️⃣: Add Your Current Skills
```javascript
// Example: You've completed these courses
Completed Courses: ["Python Basics", "HTML & CSS"]
```
<img src="https://via.placeholder.com/600x100/E8F5E9/2E7D32?text=Step+1:+Add+Your+Skills" width="600"/>

#### Step 2️⃣: Choose Your Goal
```javascript
// Example: You want to become a Full Stack Developer
Goal Course: "Full Stack Development"
```
<img src="https://via.placeholder.com/600x100/E3F2FD/1976D2?text=Step+2:+Select+Goal" width="600"/>

#### Step 3️⃣: Select Learning Style
| Style | Best For | Example |
|-------|----------|---------|
| ⚡ **Fastest** | Quick learners, time-pressed | Skip optional courses |
| 🎯 **Easiest** | Beginners, confidence builders | Gentle difficulty curve |
| ⚖️ **Balanced** | Most users | Optimal time/difficulty mix |
| 🚀 **Challenging** | Advanced learners | Maximum skill development |

#### Step 4️⃣: Get AI-Generated Path
```
Your Personalized Learning Path:
├─ JavaScript Fundamentals (4 weeks)
├─ Database Basics (3 weeks)
├─ Backend Development (6 weeks)
├─ Frontend Frameworks (5 weeks)
└─ Full Stack Development (8 weeks)

Total: ~6 months | Difficulty: ⭐⭐⭐⭐
```

#### Step 5️⃣: Track Your Progress
- ✅ Mark courses as completed
- 📊 View progress dashboard
- 🎯 Adjust path as needed

</details>

### 🎨 Interactive Features

<details>
<summary><b>🔍 Course Discovery & Search</b></summary>

**Advanced Filtering:**
```javascript
// Filter by category
GET /api/courses-by-category
{ "category": "Programming" }

// Filter by difficulty (1-10)
GET /api/courses-by-difficulty
{ "min_difficulty": 3, "max_difficulty": 7 }

// Search by keywords
Search: "machine learning python"
Results: All ML courses with Python prerequisites
```

</details>

<details>
<summary><b>📊 Progress Dashboard</b></summary>

Track your learning journey:
- 📈 **Completion Rate**: See % of path completed
- ⏱️ **Time Invested**: Track hours spent learning
- 🏆 **Achievements**: Unlock milestones
- 📅 **Learning Streak**: Daily consistency tracking

</details>

<details>
<summary><b>🎓 Career Planning</b></summary>

**Skill Gap Analysis:**
```javascript
POST /api/skill-gap-analysis
{
  "current_skills": ["Python", "HTML", "CSS"],
  "target_skills": ["Full Stack", "Cloud", "DevOps"]
}

Response:
{
  "missing_skills": ["JavaScript", "Docker", "AWS"],
  "recommended_path": [...],
  "estimated_time": "8 months"
}
```

</details>

## 🔌 API Documentation

### 🌟 Popular Endpoints

<details>
<summary><b>🎯 Get Learning Path</b></summary>

**Request:**
```http
POST /api/path
Content-Type: application/json

{
  "start_courses": ["Python Basics"],
  "goal_course": "Machine Learning",
  "learning_style": "balanced",
  "algorithm": "dijkstra"
}
```

**Response:**
```json
{
  "success": true,
  "path": ["Python Basics", "Data Structures", "Algorithms", "Machine Learning"],
  "total_time": 240,
  "total_difficulty": 28,
  "estimated_weeks": 16,
  "path_details": [
    {
      "course": "Data Structures",
      "difficulty": 7,
      "time_hours": 60,
      "prerequisites_met": true
    }
  ]
}
```

</details>

<details>
<summary><b>💡 Get Course Recommendation</b></summary>

**Request:**
```http
POST /api/recommend
Content-Type: application/json

{
  "completed_courses": ["Python Basics", "Data Structures"],
  "strategy": "meu",
  "risk_tolerance": 0.5
}
```

**Response:**
```json
{
  "success": true,
  "recommendation": {
    "course": "Algorithms",
    "expected_utility": 8.5,
    "confidence": 0.85,
    "reasoning": "High utility, prerequisites met, matches risk profile"
  },
  "alternatives": [
    {"course": "Web Development", "utility": 7.8},
    {"course": "Database Systems", "utility": 7.5}
  ]
}
```

</details>

<details>
<summary><b>📚 Get All Courses</b></summary>

**Request:**
```http
GET /api/all-courses
```

**Response:**
```json
{
  "success": true,
  "count": 165,
  "courses": {
    "Python Basics": {
      "difficulty": 3,
      "time_hours": 40,
      "utility": 9,
      "category": "Programming",
      "prerequisites": []
    },
    "Machine Learning": {
      "difficulty": 8,
      "time_hours": 120,
      "utility": 10,
      "category": "AI/ML",
      "prerequisites": ["Data Structures", "Algorithms"]
    }
  }
}
```

</details>

<details>
<summary><b>🏥 System Health & Monitoring</b></summary>

**Health Check:**
```http
GET /api/system/health
```

**Performance Stats:**
```http
GET /api/system/performance/summary
```

**Cache Statistics:**
```http
GET /api/system/cache/stats
```

</details>

### 📖 Complete API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/path` | POST | Calculate optimal learning path |
| `/api/recommend` | POST | Get next course recommendation |
| `/api/course-details` | POST | Get detailed course information |
| `/api/path-with-alternatives` | POST | Get path with alternative routes |
| `/api/course-sequence` | POST | Get recommended course sequence |
| `/api/available-courses` | POST | Get available courses based on completion |
| `/api/all-courses` | GET | Get all courses in database |
| `/api/all-categories` | GET | Get all course categories |
| `/api/career-path` | POST | Plan career transition path |
| `/api/skill-gap-analysis` | POST | Analyze skill gaps |
| `/api/system/health` | GET | System health status |
| `/api/docs` | GET | Interactive API documentation |

**📚 Full Documentation:** http://localhost:5000/api/docs (when server running)

## 🛠️ Technology Stack

<table>
<tr>
<td width="33%" align="center">

### Backend
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?logo=flask&logoColor=white)

**Core:**
- Flask 2.3.3
- Python 3.8+
- Werkzeug 2.3.7

**Features:**
- Flask-CORS
- Flask-Limiter
- python-dotenv

</td>
<td width="33%" align="center">

### Algorithms
![AI](https://img.shields.io/badge/AI-Algorithms-FF6F00?logo=tensorflow&logoColor=white)

**Pathfinding:**
- Dijkstra's Algorithm
- A* Search
- Breadth-First Search

**Decision Making:**
- Maximum Expected Utility
- Minimax Strategy
- Hybrid Intelligence

</td>
<td width="33%" align="center">

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)

**Technologies:**
- Vanilla JavaScript (ES6+)
- Responsive CSS
- Interactive UI/UX

**Features:**
- State Management
- API Client
- Real-time Updates

</td>
</tr>
</table>

### 🔒 Security Features

- ✅ **Rate Limiting**: Prevents API abuse (100 req/hour default)
- ✅ **CORS Protection**: Configurable origin restrictions
- ✅ **Input Validation**: Sanitizes and validates all inputs
- ✅ **Error Handling**: Graceful error responses
- ✅ **Environment Config**: Separate dev/prod configurations

### ⚡ Performance Features

- 🚀 **Response Caching**: Reduces redundant computations
- 📊 **Performance Monitoring**: Tracks endpoint response times
- 🔄 **Algorithm Optimization**: Efficient pathfinding implementations
- 💾 **Memory Management**: Cached results with TTL

### 🧪 Testing & Quality

- ✅ **18 Unit Tests**: Comprehensive test coverage
- ✅ **95%+ Coverage**: High code coverage
- ✅ **Pytest Framework**: Modern testing tools
- ✅ **CI/CD Ready**: Automated testing pipeline

## 📁 Project Structure

```
goal-planning-aiAgent/
├── learning-path-advisor/
│   ├── backend/
│   │   ├── server.py                 # Flask API server
│   │   ├── enhanced_learning_path_advisor.py
│   │   ├── advanced_goal_based_agent.py
│   │   ├── advanced_utility_based_agent.py
│   │   ├── hybrid_agent.py
│   │   ├── database.py               # Course database
│   │   ├── cache.py                  # Response caching
│   │   ├── performance_monitor.py    # Performance tracking
│   │   └── config.py                 # Configuration
│   └── frontend/
│       ├── index.html                # Main UI
│       ├── script.js                 # Frontend logic
│       ├── styles.css                # Styling
│       ├── api-client.js             # API communication
│       └── state-manager.js          # State management
├── tests/
│   └── test_api.py                   # API tests
├── docs/                             # Documentation
├── setup.py                          # Setup script
├── run.py                            # Run script
├── start.bat                         # Windows launcher
├── start.sh                          # Unix launcher
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment template
└── README.md                         # This file
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file (auto-created by setup script):

```bash
# Server Configuration
FLASK_ENV=development           # Options: development, production, testing
API_HOST=0.0.0.0               # Server host
API_PORT=5000                  # Server port

# CORS Configuration
CORS_ORIGINS=*                 # Comma-separated allowed origins
                              # Production example: http://yourdomain.com,https://yourdomain.com

# Rate Limiting
RATE_LIMIT_ENABLED=true        # Enable/disable rate limiting
RATE_LIMIT_DEFAULT=100 per hour # Requests per time window
RATE_LIMIT_STORAGE_URL=memory:// # Storage backend (memory:// or redis://localhost:6379)

# Logging
LOG_LEVEL=INFO                 # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Algorithm Defaults
DEFAULT_PATHFINDING_ALGORITHM=dijkstra  # Options: dijkstra, astar, bfs
DEFAULT_DECISION_STRATEGY=meu          # Options: meu, minimax, evk
DEFAULT_LEARNING_STYLE=balanced        # Options: fastest, easiest, balanced, challenging
```

### Configuration Profiles

<details>
<summary><b>🔧 Development (default)</b></summary>

```bash
FLASK_ENV=development
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=false
```

**Features:**
- Debug mode enabled
- Detailed logging
- No rate limiting
- Auto-reload on code changes

</details>

<details>
<summary><b>🚀 Production</b></summary>

```bash
FLASK_ENV=production
LOG_LEVEL=WARNING
RATE_LIMIT_ENABLED=true
CORS_ORIGINS=https://yourdomain.com
```

**Features:**
- Debug mode disabled
- Minimal logging
- Rate limiting enabled
- Restricted CORS

</details>

<details>
<summary><b>🧪 Testing</b></summary>

```bash
FLASK_ENV=testing
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=false
```

**Features:**
- Test mode enabled
- Full logging
- No rate limiting
- Isolated test environment

</details>

### Customizing Algorithms

```python
# In your API request
{
  "algorithm": "astar",           # Use A* instead of Dijkstra
  "strategy": "minimax",          # Use Minimax decision strategy
  "learning_style": "challenging", # Maximize learning value
  "risk_tolerance": 0.7           # Higher risk tolerance
}
```

## 🧪 Testing

### Running Tests

<table>
<tr>
<td width="50%">

**Basic Test Run:**
```bash
pytest tests/ -v
```

**Expected Output:**
```
18 passed in 1.23s ✓
```

</td>
<td width="50%">

**With Coverage Report:**
```bash
pytest tests/ --cov=learning-path-advisor/backend --cov-report=html
```

**View Report:**
```bash
open htmlcov/index.html
```

</td>
</tr>
</table>

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| 🔒 **Validation** | 6 tests | Input validation, course existence checks |
| 🌐 **API Endpoints** | 10 tests | All API endpoint functionality |
| ⚠️ **Error Handling** | 2 tests | Exception handling, error responses |

### Writing Tests

```python
def test_custom_learning_path():
    """Test custom learning path generation"""
    payload = {
        'start_courses': ['Python Basics'],
        'goal_course': 'AI Engineer',
        'learning_style': 'challenging'
    }
    response = client.post('/api/path', json=payload)
    
    assert response.status_code == 200
    assert 'path' in response.json
    assert len(response.json['path']) > 0
```

### Continuous Integration

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest tests/ -v
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Quick Contribution Guide

1. **🍴 Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/goal-planning-aiAgent.git
   cd goal-planning-aiAgent
   ```

2. **🌿 Create a Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **✨ Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features

4. **✅ Test Your Changes**
   ```bash
   pytest tests/ -v
   ```

5. **📤 Submit Pull Request**
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes

### Contribution Ideas

<details>
<summary><b>🎯 For Beginners</b></summary>

- 📝 Improve documentation
- 🐛 Fix typos
- ✍️ Write tutorials
- 🌐 Add translations
- 🎨 Improve UI/UX

</details>

<details>
<summary><b>🚀 For Experienced Developers</b></summary>

- ⚡ Performance optimizations
- 🤖 New AI algorithms
- 🔒 Security enhancements
- 📊 Advanced visualizations
- 🧪 Increase test coverage

</details>

**📖 Full Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

### Development Setup

```bash
# Setup development environment
python setup.py

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements.txt

# Run in development mode
python run.py
```

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/)

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What This Means

✅ **You CAN:**
- ✓ Use commercially
- ✓ Modify the code
- ✓ Distribute
- ✓ Use privately

❌ **You CANNOT:**
- ✗ Hold authors liable
- ✗ Use trademark

📋 **You MUST:**
- Include copyright notice
- Include license text

---

## 🌟 Showcase

### Built With Learning Path Advisor

*Add your project here! Submit a PR to showcase how you're using this platform.*

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/neoastra303/learning-path-advisor-pro?style=social)
![GitHub forks](https://img.shields.io/github/forks/neoastra303/learning-path-advisor-pro?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/neoastra303/learning-path-advisor-pro?style=social)

<details>
<summary><b>📈 Development Activity</b></summary>

- **Total Courses**: 165+
- **AI Algorithms**: 6 (3 pathfinding + 3 decision)
- **Test Coverage**: 95%+
- **API Endpoints**: 15+
- **Code Lines**: ~5,000
- **Documentation Pages**: 3

</details>

---

## 🙏 Acknowledgments

### Algorithms & Research
- **Dijkstra's Algorithm**: Edsger W. Dijkstra (1956)
- **A* Search**: Peter Hart, Nils Nilsson, Bertram Raphael (1968)
- **Decision Theory**: Based on classical AI and game theory principles

### Inspiration
- Course databases inspired by industry-standard learning paths
- UI/UX influenced by modern educational platforms
- API design following RESTful best practices

### Contributors
- Thanks to all contributors who help improve this project! 🎉
- See [CONTRIBUTORS.md](CONTRIBUTORS.md) for full list

---

## 📞 Support & Community

<table>
<tr>
<td align="center" width="25%">

### 📖 Documentation
[View Docs](http://localhost:5000/api/docs)

Interactive API documentation with examples

</td>
<td align="center" width="25%">

### 💬 Discussions
[Join Discussion](#)

Ask questions, share ideas

</td>
<td align="center" width="25%">

### 🐛 Issues
[Report Bug](#)

Found a bug? Let us know!

</td>
<td align="center" width="25%">

### ✨ Features
[Request Feature](#)

Have an idea? We'd love to hear it!

</td>
</tr>
</table>

### Getting Help

1. **Check Documentation**: Most questions are answered in docs/
2. **Search Issues**: Someone might have had the same question
3. **Ask the Community**: Open a discussion
4. **Report Bugs**: Use issue templates

---

## 🗺️ Roadmap

### Current Version: 1.0.0

<details>
<summary><b>✅ Completed Features</b></summary>

- [x] Multiple pathfinding algorithms (Dijkstra, A*, BFS)
- [x] Decision strategies (MEU, Minimax, EVK)
- [x] 165+ course database
- [x] RESTful API with documentation
- [x] Rate limiting and caching
- [x] Performance monitoring
- [x] Comprehensive testing
- [x] Interactive frontend UI

</details>

<details>
<summary><b>🚧 In Progress</b></summary>

- [ ] User authentication system
- [ ] Progress persistence (database)
- [ ] Mobile app (React Native)
- [ ] Course recommendation ML model

</details>

<details>
<summary><b>🔮 Future Plans</b></summary>

- [ ] Integration with learning platforms (Coursera, Udemy, etc.)
- [ ] Social features (share paths, compare progress)
- [ ] Gamification enhancements
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] AI-powered course difficulty prediction
- [ ] Personalized learning speed adjustments

</details>

### Version History

| Version | Date | Highlights |
|---------|------|------------|
| 1.0.0 | 2024 | Initial release with core features |

---

## 💡 FAQ

<details>
<summary><b>How accurate are the learning paths?</b></summary>

Learning paths are generated using industry-standard algorithms and curated course data. The accuracy depends on:
- Correct prerequisite mapping
- Accurate course difficulty ratings
- Your learning style selection

Paths are optimized but can be adjusted based on your personal experience.
</details>

<details>
<summary><b>Can I add my own courses?</b></summary>

Currently, the course database is pre-loaded. Custom course addition is planned for future releases. You can modify `database.py` for custom deployments.
</details>

<details>
<summary><b>Is this suitable for corporate training?</b></summary>

Yes! The platform can be customized for:
- Corporate training programs
- Bootcamp curricula
- University course planning
- Personal skill development

Contact for enterprise licensing.
</details>

<details>
<summary><b>How do I deploy to production?</b></summary>

See [DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md) for:
- Production configuration
- Server setup (Gunicorn, Nginx)
- Security hardening
- Monitoring setup
</details>

<details>
<summary><b>Can I use this offline?</b></summary>

Yes! Once set up:
- Frontend works without internet
- Backend runs locally
- No external API calls required

All algorithms and data are self-contained.
</details>

---

<div align="center">

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=neoastra303/learning-path-advisor-pro&type=Date)](https://star-history.com/#neoastra303/learning-path-advisor-pro&Date)

---

### Made with ❤️ by the Learning Path Advisor Team

**Learning Path Advisor Pro** - Where AI meets education for your career success ✨

[⬆ Back to Top](#-learning-path-advisor-pro)

</div>