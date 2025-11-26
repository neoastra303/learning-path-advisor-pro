"""
API Documentation and schemas for Learning Path Advisor
"""

SWAGGER_CONFIG = {
    "swagger": "2.0",
    "info": {
        "title": "Learning Path Advisor API",
        "description": "AI-powered API for personalized learning path recommendations",
        "version": "2.0.0",
        "contact": {
            "name": "Learning Path Advisor Team"
        }
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"]
}

ENDPOINTS_DOCS = {
    "/path": {
        "post": {
            "summary": "Calculate optimal learning path",
            "description": "Find the shortest/optimal learning path from starting courses to a goal course",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["start_courses", "goal_course"],
                        "properties": {
                            "start_courses": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["Python Basics"],
                                "description": "List of courses already completed"
                            },
                            "goal_course": {
                                "type": "string",
                                "example": "Machine Learning",
                                "description": "Target course to reach"
                            },
                            "learning_style": {
                                "type": "string",
                                "enum": ["balanced", "fastest", "easiest", "challenging"],
                                "default": "balanced",
                                "description": "Preferred learning approach"
                            },
                            "algorithm": {
                                "type": "string",
                                "enum": ["dijkstra", "bfs", "astar"],
                                "default": "dijkstra",
                                "description": "Pathfinding algorithm to use"
                            },
                            "cost_weights": {
                                "type": "object",
                                "description": "Custom weights for cost calculation (optional)"
                            }
                        }
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Learning path found successfully",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "cost": {"type": "number"},
                            "learning_style": {"type": "string"}
                        }
                    }
                },
                "400": {
                    "description": "Invalid input parameters"
                },
                "404": {
                    "description": "Course not found"
                }
            }
        }
    },
    
    "/recommend": {
        "post": {
            "summary": "Get course recommendations",
            "description": "Recommend courses based on completed courses and decision strategy",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["completed_courses"],
                        "properties": {
                            "completed_courses": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["Python Basics", "Data Structures"]
                            },
                            "strategy": {
                                "type": "string",
                                "enum": ["meu", "minimax", "evk"],
                                "default": "meu",
                                "description": "Decision strategy for recommendations"
                            },
                            "risk_tolerance": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.5
                            }
                        }
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Recommendations generated"
                },
                "400": {
                    "description": "Invalid input"
                }
            }
        }
    },
    
    "/all-courses": {
        "get": {
            "summary": "Get all available courses",
            "description": "List all available courses with their attributes",
            "responses": {
                "200": {
                    "description": "List of courses",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "courses": {
                                "type": "object",
                                "description": "Course data keyed by course name"
                            },
                            "count": {"type": "integer"}
                        }
                    }
                }
            }
        }
    },
    
    "/all-categories": {
        "get": {
            "summary": "Get all course categories",
            "description": "List all available learning categories",
            "responses": {
                "200": {
                    "description": "List of categories",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "categories": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
}


def generate_api_docs() -> str:
    """Generate HTML API documentation page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Learning Path Advisor API Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #fafafa;
                color: #3f3f3f;
                font-family: 'Roboto', sans-serif;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            .endpoint {
                background: white;
                border-left: 4px solid #3498db;
                margin: 20px 0;
                padding: 15px;
                border-radius: 4px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                color: white;
                font-weight: bold;
                margin-right: 10px;
            }
            .post { background-color: #f39c12; }
            .get { background-color: #27ae60; }
            code {
                background: #ecf0f1;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Learning Path Advisor API Documentation</h1>
            
            <h2>Base URL</h2>
            <code>http://localhost:5000/api</code>
            
            <h2>Key Endpoints</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/path</code>
                <p>Calculate optimal learning path</p>
                <strong>Required:</strong> start_courses, goal_course
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/path-with-alternatives</code>
                <p>Get multiple path options</p>
                <strong>Required:</strong> start_courses, goal_course
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/recommend</code>
                <p>Get course recommendations</p>
                <strong>Required:</strong> completed_courses
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/course-details</code>
                <p>Get details for a specific course</p>
                <strong>Required:</strong> course_name
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/all-courses</code>
                <p>Get all available courses</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/all-categories</code>
                <p>Get all course categories</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/career-path</code>
                <p>Plan a career path</p>
                <strong>Required:</strong> target_career
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/skill-gap-analysis</code>
                <p>Analyze skill gaps</p>
                <strong>Required:</strong> current_skills, target_skills
            </div>
            
            <h2>Error Codes</h2>
            <ul>
                <li><strong>400 Bad Request:</strong> Invalid or missing parameters</li>
                <li><strong>404 Not Found:</strong> Course not found</li>
                <li><strong>500 Internal Server Error:</strong> Unexpected server error</li>
            </ul>
            
            <h2>Example Request</h2>
            <pre><code>curl -X POST http://localhost:5000/api/path \\
  -H "Content-Type: application/json" \\
  -d '{
    "start_courses": ["Python Basics"],
    "goal_course": "Machine Learning",
    "learning_style": "balanced"
  }'</code></pre>
        </div>
    </body>
    </html>
    """
