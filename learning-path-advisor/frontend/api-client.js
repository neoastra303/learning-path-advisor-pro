/**
 * Centralized API Client for Learning Path Advisor
 * Handles all backend communication with caching and error handling
 */

class APIClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.requestTimeout = 30000; // 30 seconds
        this.cache = new Map();
        this.requestQueue = [];
        this.isProcessing = false;
    }
    
    /**
     * Make HTTP request with error handling
     */
    async request(method, endpoint, data = null, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = `${method}:${endpoint}:${JSON.stringify(data || {})}`;
        
        // Check cache for GET requests
        if (method === 'GET' && !options.skipCache && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < (options.cacheTTL || 5 * 60 * 1000)) {
                return cached.data;
            }
        }
        
        try {
            appState.setLoading(true, `${method} ${endpoint}`);
            
            const fetchOptions = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                timeout: this.requestTimeout
            };
            
            if (data && (method === 'POST' || method === 'PUT')) {
                fetchOptions.body = JSON.stringify(data);
            }
            
            const response = await fetch(url, fetchOptions);
            const responseData = await response.json();
            
            if (!response.ok) {
                throw new Error(responseData.error || `HTTP ${response.status}`);
            }
            
            // Cache successful responses
            if (method === 'GET') {
                this.cache.set(cacheKey, {
                    data: responseData,
                    timestamp: Date.now()
                });
            }
            
            appState.setLoading(false);
            return responseData;
        } catch (error) {
            appState.setLoading(false);
            appState.setError(error.message);
            throw error;
        }
    }
    
    /**
     * GET request
     */
    get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }
    
    /**
     * POST request
     */
    post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }
    
    /**
     * PUT request
     */
    put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }
    
    /**
     * DELETE request
     */
    delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }
    
    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }
    
    // ==================== LEARNING PATH ENDPOINTS ====================
    
    async getPath(startCourses, goalCourse, learningStyle = 'balanced', algorithm = 'dijkstra') {
        try {
            const response = await this.post('/api/path', {
                start_courses: startCourses,
                goal_course: goalCourse,
                learning_style: learningStyle,
                algorithm
            });
            
            if (response.success) {
                appState.setCurrentLearningPath(response);
            }
            return response;
        } catch (error) {
            console.error('Error getting learning path:', error);
            throw error;
        }
    }
    
    async getPathWithAlternatives(startCourses, goalCourse, learningStyle = 'balanced') {
        try {
            const response = await this.post('/api/path-with-alternatives', {
                start_courses: startCourses,
                goal_course: goalCourse,
                learning_style: learningStyle
            });
            
            if (response.success) {
                appState.setAlternativePaths(response.paths || []);
            }
            return response;
        } catch (error) {
            console.error('Error getting alternative paths:', error);
            throw error;
        }
    }
    
    // ==================== COURSE ENDPOINTS ====================
    
    async getAllCourses() {
        try {
            const response = await this.get('/api/all-courses', { cacheTTL: 10 * 60 * 1000 });
            
            if (response.success) {
                appState.setAllCourses(Object.keys(response.courses));
                appState.cacheData('courseDetails', response.courses);
            }
            return response;
        } catch (error) {
            console.error('Error getting all courses:', error);
            throw error;
        }
    }
    
    async getCourseDetails(courseName) {
        try {
            // Check cache first
            const cached = appState.getCachedData('courseDetails');
            if (cached && cached[courseName]) {
                return { success: true, course: cached[courseName] };
            }
            
            const response = await this.post('/api/course-details', {
                course_name: courseName
            });
            return response;
        } catch (error) {
            console.error('Error getting course details:', error);
            throw error;
        }
    }
    
    async getCoursesByCategory(category) {
        try {
            const response = await this.post('/api/courses-by-category', {
                category
            }, { cacheTTL: 5 * 60 * 1000 });
            return response;
        } catch (error) {
            console.error('Error getting courses by category:', error);
            throw error;
        }
    }
    
    async getAllCategories() {
        try {
            const response = await this.get('/api/all-categories', { cacheTTL: 60 * 60 * 1000 });
            return response;
        } catch (error) {
            console.error('Error getting categories:', error);
            throw error;
        }
    }
    
    async getCoursesByDifficulty(minDifficulty, maxDifficulty) {
        try {
            const response = await this.post('/api/courses-by-difficulty', {
                min_difficulty: minDifficulty,
                max_difficulty: maxDifficulty
            }, { cacheTTL: 5 * 60 * 1000 });
            return response;
        } catch (error) {
            console.error('Error getting courses by difficulty:', error);
            throw error;
        }
    }
    
    // ==================== RECOMMENDATION ENDPOINTS ====================
    
    async getRecommendation(completedCourses, strategy = 'meu', riskTolerance = 0.5) {
        try {
            const response = await this.post('/api/recommend', {
                completed_courses: completedCourses,
                strategy,
                risk_tolerance: riskTolerance
            });
            return response;
        } catch (error) {
            console.error('Error getting recommendation:', error);
            throw error;
        }
    }
    
    async getAvailableCourses(completedCourses) {
        try {
            const response = await this.post('/api/available-courses', {
                completed_courses: completedCourses
            });
            return response;
        } catch (error) {
            console.error('Error getting available courses:', error);
            throw error;
        }
    }
    
    async getRecommendationByCategory(startCourses, targetCategory) {
        try {
            const response = await this.post('/api/recommend-by-category', {
                start_courses: startCourses,
                target_category: targetCategory
            });
            return response;
        } catch (error) {
            console.error('Error getting category recommendation:', error);
            throw error;
        }
    }
    
    // ==================== LEARNING SEQUENCE ENDPOINTS ====================
    
    async getCourseSequence(startCourses, goalCourse, learningStyle = 'balanced', riskTolerance = 0.5) {
        try {
            const response = await this.post('/api/course-sequence', {
                start_courses: startCourses,
                goal_course: goalCourse,
                learning_style: learningStyle,
                risk_tolerance: riskTolerance
            });
            return response;
        } catch (error) {
            console.error('Error getting course sequence:', error);
            throw error;
        }
    }
    
    async getCareerPath(currentSkills, targetCareer, timeHorizonMonths = 12) {
        try {
            const response = await this.post('/api/career-path', {
                current_skills: currentSkills,
                target_career: targetCareer,
                time_horizon_months: timeHorizonMonths
            });
            return response;
        } catch (error) {
            console.error('Error getting career path:', error);
            throw error;
        }
    }
    
    async getSkillGapAnalysis(currentSkills, targetSkills) {
        try {
            const response = await this.post('/api/skill-gap-analysis', {
                current_skills: currentSkills,
                target_skills: targetSkills
            });
            return response;
        } catch (error) {
            console.error('Error getting skill gap analysis:', error);
            throw error;
        }
    }
    
    // ==================== MONITORING ENDPOINTS ====================
    
    async getSystemHealth() {
        try {
            const response = await this.get('/api/system/health', { skipCache: true });
            appState.updateSystemStats(response);
            return response;
        } catch (error) {
            console.error('Error getting system health:', error);
            return { status: 'unhealthy', error: error.message };
        }
    }
    
    async getCacheStats() {
        try {
            const response = await this.get('/api/system/cache/stats');
            return response;
        } catch (error) {
            console.error('Error getting cache stats:', error);
            throw error;
        }
    }
    
    async clearServerCache() {
        try {
            const response = await this.post('/api/system/cache/clear', {});
            return response;
        } catch (error) {
            console.error('Error clearing server cache:', error);
            throw error;
        }
    }
    
    async getPerformanceStats(category = 'all') {
        try {
            let endpoint = '/api/system/performance/summary';
            if (category === 'endpoints') {
                endpoint = '/api/system/performance/endpoints';
            } else if (category === 'algorithms') {
                endpoint = '/api/system/performance/algorithms';
            }
            
            const response = await this.get(endpoint);
            return response;
        } catch (error) {
            console.error('Error getting performance stats:', error);
            throw error;
        }
    }
    
    async clearPerformanceStats() {
        try {
            const response = await this.post('/api/system/performance/clear', {});
            return response;
        } catch (error) {
            console.error('Error clearing performance stats:', error);
            throw error;
        }
    }
    
    // ==================== UTILITY METHODS ====================
    
    /**
     * Get cache statistics
     */
    getCacheInfo() {
        return {
            size: this.cache.size,
            entries: Array.from(this.cache.keys())
        };
    }
    
    /**
     * Check if API is available
     */
    async isAPIAvailable() {
        try {
            const response = await this.getSystemHealth();
            return response.status === 'healthy';
        } catch {
            return false;
        }
    }
}

// Global API client instance
const apiClient = new APIClient();

// Export for use in other modules
window.apiClient = apiClient;
