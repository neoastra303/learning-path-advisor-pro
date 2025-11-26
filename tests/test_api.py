"""
API endpoint tests
"""
import sys
import os
import pytest
import json

# Add backend to path
BACKEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'learning-path-advisor', 'backend')
sys.path.insert(0, BACKEND_PATH)

from server import app, validate_input, validate_courses_exist, ValidationError, CourseNotFoundError
from enhanced_learning_path_advisor import EnhancedLearningPathAdvisor


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def advisor():
    """Create advisor instance"""
    return EnhancedLearningPathAdvisor()


class TestValidation:
    """Test input validation"""
    
    def test_validate_input_missing_field(self):
        """Test validation fails for missing required field"""
        data = {'goal_course': 'Python'}
        with pytest.raises(ValidationError):
            validate_input(data, ['start_courses', 'goal_course'])
    
    def test_validate_input_empty_list(self):
        """Test validation fails for empty list"""
        data = {'start_courses': [], 'goal_course': 'Python'}
        with pytest.raises(ValidationError):
            validate_input(data, ['start_courses', 'goal_course'])
    
    def test_validate_input_empty_string(self):
        """Test validation fails for empty string"""
        data = {'start_courses': ['Python Basics'], 'goal_course': ''}
        with pytest.raises(ValidationError):
            validate_input(data, ['start_courses', 'goal_course'])
    
    def test_validate_input_valid(self):
        """Test validation passes for valid input"""
        data = {'start_courses': ['Python Basics'], 'goal_course': 'Machine Learning'}
        # Should not raise
        validate_input(data, ['start_courses', 'goal_course'])
    
    def test_validate_courses_exist_valid(self, advisor):
        """Test course existence validation with valid courses"""
        courses = ['Python Basics', 'Python Intermediate']
        # Should not raise
        validate_courses_exist(courses, advisor)
    
    def test_validate_courses_exist_invalid(self, advisor):
        """Test course existence validation with invalid course"""
        courses = ['Python Basics', 'NonexistentCourse']
        with pytest.raises(CourseNotFoundError):
            validate_courses_exist(courses, advisor)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_home_endpoint(self, client):
        """Test home endpoint returns documentation"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Learning Path Advisor' in response.get_data(as_text=True)
    
    def test_api_docs_endpoint(self, client):
        """Test API docs endpoint"""
        response = client.get('/api/docs')
        assert response.status_code == 200
        assert 'Learning Path Advisor' in response.get_data(as_text=True)
    
    def test_all_courses_endpoint(self, client):
        """Test all courses endpoint"""
        response = client.get('/api/all-courses')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'courses' in data
        assert 'count' in data
        assert data['count'] > 0
    
    def test_all_categories_endpoint(self, client):
        """Test all categories endpoint"""
        response = client.get('/api/all-categories')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'categories' in data
        assert len(data['categories']) > 0
    
    def test_learning_path_valid(self, client):
        """Test learning path endpoint with valid input"""
        payload = {
            'start_courses': ['Python Basics'],
            'goal_course': 'Data Structures',
            'learning_style': 'balanced'
        }
        response = client.post('/api/path', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'path' in data
    
    def test_learning_path_missing_field(self, client):
        """Test learning path endpoint with missing field"""
        payload = {
            'goal_course': 'Data Structures'
        }
        response = client.post('/api/path', json=payload)
        assert response.status_code == 400
    
    def test_learning_path_invalid_course(self, client):
        """Test learning path endpoint with invalid course"""
        payload = {
            'start_courses': ['NonexistentCourse'],
            'goal_course': 'Data Structures'
        }
        response = client.post('/api/path', json=payload)
        assert response.status_code == 404
    
    def test_learning_path_empty_start_courses(self, client):
        """Test learning path endpoint with empty start courses"""
        payload = {
            'start_courses': [],
            'goal_course': 'Data Structures'
        }
        response = client.post('/api/path', json=payload)
        assert response.status_code == 400
    
    def test_recommend_endpoint(self, client):
        """Test recommend endpoint"""
        payload = {
            'completed_courses': ['Python Basics'],
            'strategy': 'meu',
            'risk_tolerance': 0.5
        }
        response = client.post('/api/recommend', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'recommended_course' in data or 'recommendations' in data
    
    def test_course_details_endpoint(self, client):
        """Test course details endpoint"""
        payload = {
            'course_name': 'Python Basics',
            'completed_courses': []
        }
        response = client.post('/api/course-details', json=payload)
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON"""
        response = client.post('/api/path', 
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code in [400, 500]
    
    def test_missing_json_body(self, client):
        """Test handling of missing JSON body"""
        response = client.post('/api/path')
        assert response.status_code in [400, 500]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
