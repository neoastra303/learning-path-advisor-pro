/**
 * Frontend State Manager for Learning Path Advisor
 * Centralized state management with event-based updates
 */

class StateManager {
    constructor() {
        // Application state
        this.state = {
            // User data
            user: {
                id: this.generateUserId(),
                completedCourses: [],
                preferences: {
                    learningStyle: 'balanced',
                    riskTolerance: 0.5,
                    theme: 'dark',
                    notifications: true
                },
                achievements: [],
                lastUpdated: new Date()
            },
            
            // Course data
            courses: {
                all: [],
                byCategory: {},
                selected: null,
                lastLoaded: null
            },
            
            // Learning path data
            learningPath: {
                current: null,
                history: [],
                alternatives: [],
                selectedAlgorithm: 'dijkstra'
            },
            
            // UI state
            ui: {
                currentView: 'dashboard',
                loading: false,
                error: null,
                filters: {
                    category: null,
                    difficulty: { min: 1, max: 10 },
                    timeCommitment: null
                },
                sidebarOpen: true,
                selectedTab: 0
            },
            
            // API cache
            cache: {
                courseDetails: {},
                recommendations: {},
                paths: {},
                lastCleared: new Date()
            },
            
            // System stats
            system: {
                performanceMetrics: {},
                cacheStats: {},
                apiEndpoints: {},
                lastHealthCheck: null
            }
        };
        
        // Event listeners
        this.listeners = new Map();
        
        // State history for undo/redo
        this.history = [];
        this.historyIndex = -1;
        this.maxHistory = 50;
        
        // Persist state to localStorage
        this.loadFromStorage();
        this.setupAutoSave();
    }
    
    /**
     * Generate unique user ID
     */
    generateUserId() {
        let id = localStorage.getItem('lpa_user_id');
        if (!id) {
            id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem('lpa_user_id', id);
        }
        return id;
    }
    
    /**
     * Get current state (immutable copy)
     */
    getState() {
        return JSON.parse(JSON.stringify(this.state));
    }
    
    /**
     * Get specific state slice
     */
    getStateSlice(path) {
        const keys = path.split('.');
        let value = this.state;
        for (const key of keys) {
            if (value && typeof value === 'object' && key in value) {
                value = value[key];
            } else {
                return undefined;
            }
        }
        return value;
    }
    
    /**
     * Update state (merge with existing)
     */
    setState(updates) {
        const previousState = JSON.parse(JSON.stringify(this.state));
        
        // Deep merge updates
        this.deepMerge(this.state, updates);
        
        // Add to history (undo/redo)
        this.addToHistory(previousState);
        
        // Emit change event
        this.emit('stateChanged', { previous: previousState, current: this.state });
        
        return this.state;
    }
    
    /**
     * Set state at specific path
     */
    setStatePath(path, value) {
        const keys = path.split('.');
        const lastKey = keys.pop();
        
        let target = this.state;
        for (const key of keys) {
            if (!(key in target)) {
                target[key] = {};
            }
            target = target[key];
        }
        
        const previousValue = target[lastKey];
        target[lastKey] = value;
        
        this.emit('stateChanged', { path, previous: previousValue, current: value });
    }
    
    /**
     * Deep merge objects
     */
    deepMerge(target, source) {
        for (const key in source) {
            if (source.hasOwnProperty(key)) {
                if (typeof source[key] === 'object' && !Array.isArray(source[key]) && source[key] !== null) {
                    if (!(key in target)) {
                        target[key] = {};
                    }
                    this.deepMerge(target[key], source[key]);
                } else {
                    target[key] = source[key];
                }
            }
        }
    }
    
    /**
     * Add state to history for undo/redo
     */
    addToHistory(state) {
        // Remove any redo history
        if (this.historyIndex < this.history.length - 1) {
            this.history = this.history.slice(0, this.historyIndex + 1);
        }
        
        this.history.push(state);
        
        // Limit history size
        if (this.history.length > this.maxHistory) {
            this.history.shift();
        } else {
            this.historyIndex++;
        }
    }
    
    /**
     * Undo last state change
     */
    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.state = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
            this.emit('stateRestored', { state: this.state, action: 'undo' });
            return true;
        }
        return false;
    }
    
    /**
     * Redo last undone change
     */
    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.state = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
            this.emit('stateRestored', { state: this.state, action: 'redo' });
            return true;
        }
        return false;
    }
    
    /**
     * User-related operations
     */
    addCompletedCourse(courseName) {
        if (!this.state.user.completedCourses.includes(courseName)) {
            this.setState({
                user: {
                    ...this.state.user,
                    completedCourses: [...this.state.user.completedCourses, courseName],
                    lastUpdated: new Date()
                }
            });
            this.emit('courseCompleted', { course: courseName });
        }
    }
    
    removeCompletedCourse(courseName) {
        this.setState({
            user: {
                ...this.state.user,
                completedCourses: this.state.user.completedCourses.filter(c => c !== courseName),
                lastUpdated: new Date()
            }
        });
        this.emit('courseRemoved', { course: courseName });
    }
    
    updateUserPreferences(preferences) {
        this.setState({
            user: {
                ...this.state.user,
                preferences: { ...this.state.user.preferences, ...preferences }
            }
        });
        this.emit('preferencesChanged', preferences);
    }
    
    addAchievement(achievement) {
        if (!this.state.user.achievements.find(a => a.id === achievement.id)) {
            this.setState({
                user: {
                    ...this.state.user,
                    achievements: [...this.state.user.achievements, achievement]
                }
            });
            this.emit('achievementUnlocked', achievement);
        }
    }
    
    /**
     * Course-related operations
     */
    setAllCourses(courses) {
        this.setState({
            courses: {
                ...this.state.courses,
                all: courses,
                lastLoaded: new Date()
            }
        });
        this.emit('coursesLoaded', { count: courses.length });
    }
    
    setCoursesByCategory(coursesByCategory) {
        this.setState({
            courses: {
                ...this.state.courses,
                byCategory: coursesByCategory
            }
        });
    }
    
    selectCourse(course) {
        this.setState({
            courses: {
                ...this.state.courses,
                selected: course
            }
        });
        this.emit('courseSelected', course);
    }
    
    /**
     * Learning path operations
     */
    setCurrentLearningPath(path) {
        this.setState({
            learningPath: {
                ...this.state.learningPath,
                current: path,
                history: [...this.state.learningPath.history, path]
            }
        });
        this.emit('pathCalculated', path);
    }
    
    setAlternativePaths(paths) {
        this.setState({
            learningPath: {
                ...this.state.learningPath,
                alternatives: paths
            }
        });
        this.emit('alternativePathsLoaded', { count: paths.length });
    }
    
    setSelectedAlgorithm(algorithm) {
        this.setState({
            learningPath: {
                ...this.state.learningPath,
                selectedAlgorithm: algorithm
            }
        });
    }
    
    /**
     * UI state operations
     */
    setCurrentView(view) {
        this.setState({
            ui: { ...this.state.ui, currentView: view }
        });
        this.emit('viewChanged', { view });
    }
    
    setLoading(isLoading, message = null) {
        this.setState({
            ui: {
                ...this.state.ui,
                loading: isLoading
            }
        });
        this.emit('loadingStateChanged', { isLoading, message });
    }
    
    setError(error) {
        this.setState({
            ui: { ...this.state.ui, error }
        });
        this.emit('errorOccurred', { error });
    }
    
    clearError() {
        this.setState({
            ui: { ...this.state.ui, error: null }
        });
    }
    
    setFilters(filters) {
        this.setState({
            ui: {
                ...this.state.ui,
                filters: { ...this.state.ui.filters, ...filters }
            }
        });
        this.emit('filtersChanged', filters);
    }
    
    /**
     * Cache operations
     */
    cacheData(key, value) {
        this.setState({
            cache: {
                ...this.state.cache,
                [key]: value
            }
        });
    }
    
    getCachedData(key) {
        return this.state.cache[key];
    }
    
    clearCache() {
        this.setState({
            cache: {
                courseDetails: {},
                recommendations: {},
                paths: {},
                lastCleared: new Date()
            }
        });
        this.emit('cacheCleared');
    }
    
    /**
     * System stats
     */
    updateSystemStats(stats) {
        this.setState({
            system: {
                ...this.state.system,
                ...stats,
                lastHealthCheck: new Date()
            }
        });
    }
    
    /**
     * Event system
     */
    on(eventName, callback) {
        if (!this.listeners.has(eventName)) {
            this.listeners.set(eventName, []);
        }
        this.listeners.get(eventName).push(callback);
        
        // Return unsubscribe function
        return () => {
            const callbacks = this.listeners.get(eventName);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        };
    }
    
    emit(eventName, data) {
        if (this.listeners.has(eventName)) {
            this.listeners.get(eventName).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${eventName}:`, error);
                }
            });
        }
    }
    
    off(eventName) {
        this.listeners.delete(eventName);
    }
    
    /**
     * Persistence
     */
    saveToStorage() {
        try {
            // Only save user and preferences data
            const persistedState = {
                user: this.state.user,
                learningPath: {
                    history: this.state.learningPath.history
                }
            };
            localStorage.setItem('lpa_state', JSON.stringify(persistedState));
        } catch (error) {
            console.error('Error saving state to storage:', error);
        }
    }
    
    loadFromStorage() {
        try {
            const stored = localStorage.getItem('lpa_state');
            if (stored) {
                const persistedState = JSON.parse(stored);
                // Merge persisted state
                this.state.user = { ...this.state.user, ...persistedState.user };
                if (persistedState.learningPath) {
                    this.state.learningPath.history = persistedState.learningPath.history;
                }
            }
        } catch (error) {
            console.error('Error loading state from storage:', error);
        }
    }
    
    setupAutoSave() {
        // Auto-save every 30 seconds
        setInterval(() => {
            this.saveToStorage();
        }, 30000);
        
        // Save before leaving page
        window.addEventListener('beforeunload', () => {
            this.saveToStorage();
        });
    }
    
    /**
     * Export state
     */
    exportState() {
        return JSON.stringify(this.state, null, 2);
    }
    
    /**
     * Reset to initial state
     */
    reset() {
        this.state = {
            user: { ...this.state.user, completedCourses: [], achievements: [] },
            courses: { all: [], byCategory: {}, selected: null, lastLoaded: null },
            learningPath: { current: null, history: [], alternatives: [], selectedAlgorithm: 'dijkstra' },
            ui: { currentView: 'dashboard', loading: false, error: null, filters: {}, sidebarOpen: true, selectedTab: 0 },
            cache: { courseDetails: {}, recommendations: {}, paths: {}, lastCleared: new Date() },
            system: { performanceMetrics: {}, cacheStats: {}, apiEndpoints: {}, lastHealthCheck: null }
        };
        this.history = [];
        this.historyIndex = -1;
        this.emit('stateReset');
    }
}

// Global state manager instance
const appState = new StateManager();

// Export for use in other modules
window.appState = appState;
