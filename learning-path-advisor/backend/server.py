"""
Flask API server for Enhanced Learning Path Advisor
"""
import logging
import time
from typing import Tuple, Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps

from enhanced_learning_path_advisor import (
    get_learning_path,
    get_course_recommendation,
    get_course_details,
    get_learning_path_with_alternatives,
    get_learning_progression,
    get_course_recommendation_sequence,
    get_available_courses,
    get_courses_by_category,
    get_all_categories,
    get_course_recommendation_by_category,
    get_courses_by_difficulty_range,
    assess_learning_style,
    plan_career_path,
    get_skill_gap_analysis,
    EnhancedLearningPathAdvisor
)
from api_docs import generate_api_docs
from config import config
from cache import cached, get_global_cache, clear_global_cache, get_cache_stats
from performance_monitor import (
    get_global_monitor, get_performance_stats, 
    clear_performance_stats, timed
)

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
CORS(app, origins=config.CORS_ORIGINS)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATE_LIMIT_DEFAULT] if config.RATE_LIMIT_ENABLED else [],
    storage_uri=config.RATE_LIMIT_STORAGE_URL,
    enabled=config.RATE_LIMIT_ENABLED
)

@app.before_request
def track_request_start():
    """Track request start time"""
    request.start_time = time.time()

@app.after_request
def track_request_end(response):
    """Track request duration and record metrics"""
    if hasattr(request, 'start_time'):
        duration = (time.time() - request.start_time) * 1000
        monitor = get_global_monitor()
        monitor.record_endpoint(
            request.path,
            request.method,
            duration,
            response.status_code
        )
        logger.info(f"{request.method} {request.path} - {response.status_code} ({duration:.2f}ms)")
    return response

# Custom exception handlers
class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

class CourseNotFoundError(Exception):
    """Raised when a course is not found in the database"""
    pass

# Validation helper functions
def validate_courses_exist(courses: list, advisor: EnhancedLearningPathAdvisor = None) -> None:
    """Validate that all courses exist in the database"""
    if advisor is None:
        advisor = EnhancedLearningPathAdvisor()
    
    available_courses = set(advisor.course_prerequisites.keys())
    for course in courses:
        if course and course not in available_courses:
            raise CourseNotFoundError(f"Course '{course}' not found in database")

def validate_input(data: dict, required_fields: list) -> None:
    """Validate required fields are present and non-empty"""
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        
        value = data[field]
        if isinstance(value, (list, str)):
            if not value:
                raise ValidationError(f"Field '{field}' cannot be empty")

# Global error handlers
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    logger.warning(f"Validation error: {str(error)}")
    return jsonify({'error': str(error), 'error_type': 'ValidationError'}), 400

@app.errorhandler(CourseNotFoundError)
def handle_course_not_found(error):
    logger.warning(f"Course not found: {str(error)}")
    return jsonify({'error': str(error), 'error_type': 'CourseNotFoundError'}), 404

@app.errorhandler(Exception)
def handle_generic_error(error):
    logger.error(f"Unexpected error: {str(error)}", exc_info=True)
    return jsonify({'error': 'An unexpected error occurred', 'error_type': 'InternalServerError'}), 500

@app.route('/')
def home():
    return generate_api_docs()

@app.route('/api/docs', methods=['GET'])
def api_documentation():
    """API documentation endpoint"""
    logger.info("API documentation accessed")
    return generate_api_docs()

@app.route('/api/path', methods=['POST'])
def learning_path():
    """Calculate optimal learning path from start courses to goal course"""
    try:
        data = request.json or {}
        validate_input(data, ['start_courses', 'goal_course'])
        
        start_courses = data.get('start_courses', [])
        goal_course = data.get('goal_course', '')
        learning_style = data.get('learning_style', 'balanced')
        algorithm = data.get('algorithm', 'dijkstra')
        cost_weights = data.get('cost_weights')
        
        advisor = EnhancedLearningPathAdvisor()
        validate_courses_exist(start_courses + [goal_course], advisor)
        
        logger.info(f"Calculating path from {start_courses} to {goal_course} using {learning_style}/{algorithm}")
        result = get_learning_path(start_courses, goal_course, learning_style, algorithm, cost_weights)
        return jsonify(result)
    except (ValidationError, CourseNotFoundError) as e:
        raise
    except Exception as e:
        logger.error(f"Error in learning_path endpoint: {str(e)}", exc_info=True)
        raise

@app.route('/api/recommend', methods=['POST'])
def course_recommendation():
    try:
        data = request.json
        completed_courses = data.get('completed_courses', [])
        strategy = data.get('strategy', 'meu')
        risk_tolerance = float(data.get('risk_tolerance', 0.5))

        if not completed_courses:
            return jsonify({'error': 'completed_courses is required'}), 400

        result = get_course_recommendation(completed_courses, strategy, risk_tolerance)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/course-details', methods=['POST'])
def course_details():
    try:
        data = request.json
        course_name = data.get('course_name', '')

        if not course_name:
            return jsonify({'error': 'course_name is required'}), 400

        completed_courses = data.get('completed_courses', [])
        result = get_course_details(course_name, completed_courses)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/path-with-alternatives', methods=['POST'])
def path_with_alternatives():
    try:
        data = request.json
        start_courses = data.get('start_courses', [])
        goal_course = data.get('goal_course', '')
        learning_style = data.get('learning_style', 'balanced')
        cost_weights = data.get('cost_weights') or None

        if not start_courses or not goal_course:
            return jsonify({'error': 'start_courses and goal_course are required'}), 400

        result = get_learning_path_with_alternatives(start_courses, goal_course, learning_style, cost_weights)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning-progression', methods=['POST'])
def learning_progression():
    try:
        data = request.json
        start_courses = data.get('start_courses', [])
        goal_course = data.get('goal_course', '')

        if not start_courses or not goal_course:
            return jsonify({'error': 'start_courses and goal_course are required'}), 400

        result = get_learning_progression(start_courses, goal_course)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/course-sequence', methods=['POST'])
def course_sequence():
    try:
        data = request.json
        start_courses = data.get('start_courses', [])
        goal_course = data.get('goal_course', '')
        learning_style = data.get('learning_style', 'balanced')
        risk_tolerance = float(data.get('risk_tolerance', 0.5))
        cost_weights = data.get('cost_weights') or None

        if not start_courses or not goal_course:
            return jsonify({'error': 'start_courses and goal_course are required'}), 400

        result = get_course_recommendation_sequence(
            start_courses,
            goal_course,
            learning_style,
            risk_tolerance,
            cost_weights,
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/available-courses', methods=['POST'])
def available_courses():
    try:
        data = request.json
        completed_courses = data.get('completed_courses', [])

        result = get_available_courses(completed_courses)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses-by-category', methods=['POST'])
def courses_by_category():
    try:
        data = request.json
        category = data.get('category', '')

        if not category:
            return jsonify({'error': 'category is required'}), 400

        result = get_courses_by_category(category)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/all-categories', methods=['GET'])
def all_categories():
    try:
        result = get_all_categories()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend-by-category', methods=['POST'])
def recommend_by_category():
    try:
        data = request.json
        start_courses = data.get('start_courses', [])
        target_category = data.get('target_category', '')

        if not target_category:
            return jsonify({'error': 'target_category is required'}), 400

        result = get_course_recommendation_by_category(start_courses, target_category)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses-by-difficulty', methods=['POST'])
def courses_by_difficulty():
    try:
        data = request.json
        min_difficulty = data.get('min_difficulty', 1)
        max_difficulty = data.get('max_difficulty', 10)

        result = get_courses_by_difficulty_range(min_difficulty, max_difficulty)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assess-learning-style', methods=['POST'])
def assess_learning_style_endpoint():
    try:
        data = request.json
        user_responses = data.get('user_responses', {})

        result = assess_learning_style(user_responses)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/career-path', methods=['POST'])
def career_path():
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_career = data.get('target_career', '')
        time_horizon_months = data.get('time_horizon_months', 12)

        if not target_career:
            return jsonify({'error': 'target_career is required'}), 400

        result = plan_career_path(current_skills, target_career, time_horizon_months)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skill-gap-analysis', methods=['POST'])
def skill_gap_analysis():
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_skills = data.get('target_skills', [])

        if not current_skills or not target_skills:
            return jsonify({'error': 'Both current_skills and target_skills are required'}), 400

        result = get_skill_gap_analysis(current_skills, target_skills)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/all-courses', methods=['GET'])
def all_courses():
    """Get all available courses with their attributes"""
    try:
        from enhanced_learning_path_advisor import EnhancedLearningPathAdvisor
        advisor = EnhancedLearningPathAdvisor()
        
        courses_with_attributes = {}
        for course, attrs in advisor.course_attributes.items():
            courses_with_attributes[course] = {
                'difficulty': attrs['difficulty'],
                'time_hours': attrs['time_hours'],
                'utility': attrs['utility'],
                'category': attrs['category'],
                'prerequisites': advisor.course_prerequisites.get(course, [])
            }
        
        return jsonify({
            'success': True,
            'courses': courses_with_attributes,
            'count': len(courses_with_attributes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MONITORING & SYSTEM ENDPOINTS ====================

@app.route('/api/system/cache/stats', methods=['GET'])
def cache_stats():
    """Get cache statistics"""
    try:
        stats = get_cache_stats()
        return jsonify({
            'success': True,
            'cache': stats
        })
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the cache"""
    try:
        clear_global_cache()
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/performance/summary', methods=['GET'])
def performance_summary():
    """Get performance summary"""
    try:
        stats = get_performance_stats('all')
        return jsonify({
            'success': True,
            'performance': stats
        })
    except Exception as e:
        logger.error(f"Error getting performance stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/performance/endpoints', methods=['GET'])
def performance_endpoints():
    """Get endpoint performance statistics"""
    try:
        stats = get_performance_stats('endpoints')
        return jsonify({
            'success': True,
            'endpoints': stats
        })
    except Exception as e:
        logger.error(f"Error getting endpoint stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/performance/algorithms', methods=['GET'])
def performance_algorithms():
    """Get algorithm performance statistics"""
    try:
        stats = get_performance_stats('algorithms')
        return jsonify({
            'success': True,
            'algorithms': stats
        })
    except Exception as e:
        logger.error(f"Error getting algorithm stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/performance/clear', methods=['POST'])
def clear_performance():
    """Clear performance statistics"""
    try:
        clear_performance_stats()
        return jsonify({
            'success': True,
            'message': 'Performance statistics cleared'
        })
    except Exception as e:
        logger.error(f"Error clearing performance stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/health', methods=['GET'])
def system_health():
    """Get system health status"""
    try:
        cache_stats_data = get_cache_stats()
        perf_summary = get_performance_stats('all')
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': time.time(),
            'cache': cache_stats_data,
            'performance': perf_summary['summary']
        })
    except Exception as e:
        logger.error(f"Error getting health status: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info(f"Starting Learning Path Advisor API on {config.API_HOST}:{config.API_PORT}")
    logger.info(f"Environment: {config.__class__.__name__}")
    logger.info(f"API Documentation available at http://{config.API_HOST}:{config.API_PORT}/api/docs")
    app.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)