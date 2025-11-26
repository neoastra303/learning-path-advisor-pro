// script.js - Learning Path Advisor JavaScript functionality

// Base URL for the API
const API_BASE_URL = 'http://localhost:5000/api';

// DOM elements
const completedCoursesContainer = document.getElementById('completed-courses-container');
const addCourseBtn = document.getElementById('add-course-btn');
const goalCourseSelect = document.getElementById('goal-course');
const learningStyleSelect = document.getElementById('learning-style');
const algorithmSelect = document.getElementById('path-algorithm');
const findPathBtn = document.getElementById('find-path-btn');
const pathResults = document.getElementById('path-results');
const pathDisplay = document.getElementById('path-display');
const pathCost = document.getElementById('path-cost');
const getRecommendationBtn = document.getElementById('get-recommendation-btn');
const recommendationResults = document.getElementById('recommendation-results');
const recommendationDisplay = document.getElementById('recommendation-display');
const allOptions = document.getElementById('all-options');
const courseNameSelect = document.getElementById('course-name');
const getCourseDetailsBtn = document.getElementById('get-course-details-btn');
const courseDetailsResults = document.getElementById('course-details-results');
const courseInfo = document.getElementById('course-info');

// New DOM elements for career path and skill gap
const targetCareerSelect = document.getElementById('target-career');
const timeHorizonInput = document.getElementById('time-horizon');
const planCareerPathBtn = document.getElementById('plan-career-path-btn');
const careerPathResults = document.getElementById('career-path-results');
const careerPathDisplay = document.getElementById('career-path-display');
const targetSkillsInput = document.getElementById('target-skills');
const analyzeSkillGapBtn = document.getElementById('analyze-skill-gap-btn');
const skillGapResults = document.getElementById('skill-gap-results');
const skillGapDisplay = document.getElementById('skill-gap-display');

// Additional DOM elements for new features
const decisionStrategySelect = document.getElementById('decision-strategy');
const goalCourseProgressSelect = document.getElementById('goal-course-progress');
const getProgressBtn = document.getElementById('get-progress-btn');
const progressResults = document.getElementById('progress-results');
const progressDisplay = document.getElementById('progress-display');

// New DOM elements for course explorer
const courseSearch = document.getElementById('course-search');
const categoryFilter = document.getElementById('category-filter');
const difficultyMin = document.getElementById('difficulty-min');
const difficultyMax = document.getElementById('difficulty-max');
const difficultyMinValue = document.getElementById('difficulty-min-value');
const difficultyMaxValue = document.getElementById('difficulty-max-value');
const timeFilter = document.getElementById('time-filter');
const applyFiltersBtn = document.getElementById('apply-filters-btn');
const courseResults = document.getElementById('course-results');
const courseGrid = document.getElementById('course-grid');

// New DOM elements for visualization and dashboard
const pathVisualContent = document.getElementById('path-visual-content');
const exportPathBtn = document.getElementById('export-path-btn');
const coursesCompleted = document.getElementById('courses-completed');
const learningHours = document.getElementById('learning-hours');
const learningStreak = document.getElementById('learning-streak');
const achievementCount = document.getElementById('achievement-count');

// Available courses for selection
const availableCourses = [
    // Computer Science & Programming
    'Python Basics', 'Python Intermediate', 'Data Structures',
    'Algorithms', 'Web Development', 'Database Systems',
    'Machine Learning', 'Data Science', 'Software Engineering', 'DevOps',
    'AI Fundamentals', 'Mathematics', 'Statistics', 'Data Visualization',
    'Cloud Computing', 'Cybersecurity', 'Mobile Development', 'Game Development',
    'Frontend Development', 'Backend Development', 'Full Stack Development',
    'API Development', 'Blockchain', 'IoT', 'Computer Vision',
    'Natural Language Processing', 'Robotics',
    
    // Marketing & Digital Marketing
    'Marketing Fundamentals', 'Digital Marketing', 'Social Media Marketing',
    'Content Marketing', 'SEO Basics', 'Email Marketing', 'Marketing Analytics',
    'Brand Management', 'Marketing Research', 'Influencer Marketing',
    'E-commerce Marketing', 'Marketing Automation', 'Growth Hacking',
    'Performance Marketing', 'Video Marketing',
    
    // Business & Management
    'Business Fundamentals', 'Entrepreneurship', 'Business Strategy',
    'Operations Management', 'Financial Management', 'Project Management',
    'Business Analytics', 'Leadership', 'Human Resources', 'Business Law',
    'International Business', 'Corporate Finance', 'Business Process Management',
    'Change Management', 'Innovation Management', 'Supply Chain Management',
    'Business Ethics',
    
    // Design & Creative Arts
    'Graphic Design', 'UI/UX Design', 'Web Design', 'Digital Illustration',
    'Photography', 'Video Editing', 'Animation', '3D Modeling',
    'Motion Graphics', 'Color Theory', 'Typography', 'Branding',
    'User Research', 'Interaction Design', 'Design Systems', 'Print Design',
    'Package Design', 'Web Animation',
    
    // Data & Analytics
    'SQL Basics', 'Data Analysis', 'Excel Advanced', 'Business Intelligence',
    'Big Data', 'Data Mining', 'Predictive Analytics', 'Data Warehousing',
    'Data Governance', 'Business Intelligence Tools', 'A/B Testing',
    'Data Storytelling',
    
    // Finance & Accounting
    'Accounting Basics', 'Financial Accounting', 'Managerial Accounting',
    'Investment Analysis', 'Risk Management', 'Tax Preparation', 'Auditing',
    'Corporate Finance', 'Personal Finance', 'Financial Planning',
    'Cryptocurrency', 'Real Estate Investment',
    
    // Sales & Customer Success
    'Sales Fundamentals', 'Customer Relationship Management', 'Negotiation',
    'Consulting', 'Customer Success', 'Account Management', 'Sales Management',
    'Business Development',
    
    // Languages
    'English Language', 'Spanish Language', 'French Language',
    'German Language', 'Chinese Language', 'Japanese Language',
    'Business English', 'Technical Writing', 'Translation Studies',
    'Linguistics',
    
    // Health & Wellness
    'Nutrition', 'Fitness Training', 'Mental Health', 'Yoga', 'Meditation',
    'Public Health', 'Sports Science', 'Nutrition Therapy', 'Wellness Coaching',
    
    // Creative Writing & Journalism
    'Creative Writing', 'Journalism', 'Copywriting', 'Technical Writing',
    'Content Writing', 'Script Writing', 'Editing', 'Publishing',
    
    // Product Management
    'Product Management', 'Product Design', 'Agile Methodology',
    'Scrum Master', 'Product Analytics', 'Product Strategy',
    
    // Education & Training
    'Teaching Fundamentals', 'Curriculum Design', 'Educational Technology',
    'Adult Learning', 'Online Teaching', 'Special Education',
    'Educational Psychology',
    
    // Law & Legal Studies
    'Legal Fundamentals', 'Contract Law', 'Corporate Law',
    'Intellectual Property', 'Cyber Law',
    
    // Healthcare & Medicine
    'Medical Fundamentals', 'Medical Coding', 'Healthcare Administration',
    'Pharmacology', 'Medical Ethics',
    
    // Arts & Music
    'Music Theory', 'Digital Music Production', 'Art History', 'Drawing',
    'Painting', 'Pottery', 'Sculpture', 'Music Performance'
];

// Store user's completed courses and progress
let userCompletedCourses = [];
let userProgress = {
    completedCourses: [],
    learningHours: 0,
    learningStreak: 0,
    achievements: [],
    lastActivity: new Date().toISOString(),
    preferences: {
        learningStyle: 'balanced',
        riskTolerance: 0.5,
        theme: 'light'
    }
};


// Function to populate course dropdowns dynamically
function populateCourseDropdowns() {
    // Populate goal course dropdown
    const goalCourseSelect = document.getElementById('goal-course');
    goalCourseSelect.innerHTML = '<option value="">Select a goal course</option>';
    availableCourses.forEach(course => {
        const option = document.createElement('option');
        option.value = course;
        option.textContent = course;
        goalCourseSelect.appendChild(option);
    });

    // Populate course details dropdown
    const courseNameSelect = document.getElementById('course-name');
    courseNameSelect.innerHTML = '<option value="">Select a course to view details</option>';
    availableCourses.forEach(course => {
        const option = document.createElement('option');
        option.value = course;
        option.textContent = course;
        courseNameSelect.appendChild(option);
    });
    
    // Populate goal course for progress section
    const goalCourseProgressSelect = document.getElementById('goal-course-progress');
    goalCourseProgressSelect.innerHTML = '<option value="">Select goal course</option>';
    availableCourses.forEach(course => {
        const option = document.createElement('option');
        option.value = course;
        option.textContent = course;
        goalCourseProgressSelect.appendChild(option);
    });
}

// Function to add a course to the user's progress
function addCourseToProgress() {
    const courseToAdd = prompt('Enter the course you have completed:');
    
    if (courseToAdd && availableCourses.includes(courseToAdd) && !userCompletedCourses.includes(courseToAdd)) {
        markCourseCompleted(courseToAdd);
    } else if (userCompletedCourses.includes(courseToAdd)) {
        alert('You have already added this course.');
    } else if (courseToAdd) {
        alert('Please enter a valid course name.');
    }
}

// Function to remove a course from the user's progress
function removeCourseFromProgress(course) {
    userCompletedCourses = userCompletedCourses.filter(c => c !== course);
    userProgress.completedCourses = userCompletedCourses;
    
    // Save progress
    saveUserProgress();
    
    updateCompletedCoursesDisplay();
    updateDashboard();
}

// Function to update the completed courses display
function updateCompletedCoursesDisplay() {
    completedCoursesContainer.innerHTML = '';
    
    if (userCompletedCourses.length === 0) {
        const noCourses = document.createElement('p');
        noCourses.textContent = 'No courses added yet. Click "Add Completed Course" to get started.';
        noCourses.style.color = '#777';
        noCourses.style.fontStyle = 'italic';
        completedCoursesContainer.appendChild(noCourses);
    } else {
        userCompletedCourses.forEach(course => {
            const courseTag = document.createElement('span');
            courseTag.className = 'course-tag';
            courseTag.innerHTML = `${course} <button class="remove-btn" data-course="${course}">×</button>`;
            completedCoursesContainer.appendChild(courseTag);
        });
        
        // Add event listeners to remove buttons
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const course = this.getAttribute('data-course');
                removeCourseFromProgress(course);
            });
        });
    }

    // Update summary bar completed count
    const summaryCompleted = document.getElementById('summary-completed');
    if (summaryCompleted) {
        const count = userCompletedCourses.length;
        summaryCompleted.textContent = count === 1 ? '1 course' : `${count} courses`;
    }
}

// Function to find learning path
async function findLearningPath() {
    const goalCourse = goalCourseSelect.value;
    
    if (!goalCourse) {
        alert('Please select a goal course.');
        return;
    }
    
    if (userCompletedCourses.length === 0) {
        alert('Please add at least one completed course first.');
        return;
    }
    
    try {
        showLoading(pathResults);

        // Use the selected learning style if available, otherwise fall back to preferences
        const style = (learningStyleSelect && learningStyleSelect.value) || userProgress.preferences.learningStyle || 'balanced';
        const algorithm = (algorithmSelect && algorithmSelect.value) || 'dijkstra';

        // Update summary bar goal & style
        const summaryGoal = document.getElementById('summary-goal');
        const summaryStyle = document.getElementById('summary-style');
        if (summaryGoal) summaryGoal.textContent = goalCourse;
        if (summaryStyle) summaryStyle.textContent = style.charAt(0).toUpperCase() + style.slice(1);

        // Collect optional cost weights from the advanced controls
        const weights = {};
        const timeInput = document.getElementById('weight-time');
        const diffInput = document.getElementById('weight-difficulty');
        const utilInput = document.getElementById('weight-utility');
        const prereqInput = document.getElementById('weight-prereq');

        const timeVal = timeInput ? parseFloat(timeInput.value) : NaN;
        const diffVal = diffInput ? parseFloat(diffInput.value) : NaN;
        const utilVal = utilInput ? parseFloat(utilInput.value) : NaN;
        const prereqVal = prereqInput ? parseFloat(prereqInput.value) : NaN;

        if (!Number.isNaN(timeVal)) weights.time = timeVal;
        if (!Number.isNaN(diffVal)) weights.difficulty = diffVal;
        if (!Number.isNaN(utilVal)) weights.utility = utilVal;
        if (!Number.isNaN(prereqVal)) weights.prereq = prereqVal;

        const costWeights = Object.keys(weights).length > 0 ? weights : null;

        const response = await fetch(`${API_BASE_URL}/path`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_courses: userCompletedCourses,
                goal_course: goalCourse,
                learning_style: style,
                algorithm: algorithm,
                cost_weights: costWeights
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            pathDisplay.textContent = data.path || 'No path found';
            // Only show the numeric cost; label lives in the HTML
            const costValue = typeof data.total_cost === 'number' ? data.total_cost.toFixed(2) : data.total_cost;
            pathCost.textContent = costValue;

            const pathExplanation = document.getElementById('path-explanation');

            // Build a richer explanation using algorithm/style and progression metrics
            if (pathExplanation) {
                const usedStyle = data.learning_style || style;
                const usedAlgorithm = data.algorithm_used || algorithm;
                const details = data.path_details || {};
                const altCount = Array.isArray(details.all_alternative_paths)
                    ? details.all_alternative_paths.length
                    : 0;

                let explanationHtml = `
                    <p><strong>Learning style:</strong> ${usedStyle}</p>
                    <p><strong>Algorithm:</strong> ${usedAlgorithm}</p>
                    <p><strong>Alternative paths considered:</strong> ${altCount}</p>
                `;

                try {
                    const progResp = await fetch(`${API_BASE_URL}/learning-progression`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            start_courses: userCompletedCourses,
                            goal_course: goalCourse
                        })
                    });

                    const progData = await progResp.json();
                    if (progData && progData.success) {
                        const avgDiff = typeof progData.average_difficulty === 'number'
                            ? progData.average_difficulty.toFixed(2)
                            : progData.average_difficulty;

                        explanationHtml += `
                            <p><strong>Total time (path):</strong> ${progData.total_time_hours} hours</p>
                            <p><strong>Average difficulty:</strong> ${avgDiff}</p>
                            <p><strong>Total utility:</strong> ${progData.total_utility}</p>
                        `;
                    }
                } catch (e) {
                    console.error('Error fetching progression metrics:', e);
                }

                pathExplanation.innerHTML = explanationHtml;
            }

            pathResults.classList.remove('hidden');
            
            // Update the visualization
            updatePathVisualization(data.path_list || []);
        } else {
            showError(pathResults, 'No learning path found. Check your prerequisites.');
        }
    } catch (error) {
        console.error('Error finding learning path:', error);
        showError(pathResults, 'Error finding learning path. Please try again.');
    }
}

// Function to get course recommendations
async function getCourseRecommendation() {
    if (userCompletedCourses.length === 0) {
        alert('Please add at least one completed course first.');
        return;
    }
    
    try {
        showLoading(recommendationResults);

        const strategy = (decisionStrategySelect && decisionStrategySelect.value) || 'meu';
        const riskTolerance = userProgress.preferences.riskTolerance || 0.5;

        // Update summary bar risk
        const summaryRisk = document.getElementById('summary-risk');
        if (summaryRisk) summaryRisk.textContent = riskTolerance.toFixed(1);
        
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                completed_courses: userCompletedCourses,
                strategy: strategy,
                risk_tolerance: riskTolerance
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.recommended_course) {
                // Show main recommendation with strategy and risk info
                const strategyUsed = data.decision_strategy || strategy;
                const riskInfo = data.risk_analysis && data.risk_analysis[data.recommended_course];
                const riskLevel = riskInfo ? riskInfo.risk_level : 'Unknown';

                recommendationDisplay.innerHTML = `
                    <p><strong>Course:</strong> ${data.recommended_course}</p>
                    <p><strong>Strategy:</strong> ${strategyUsed}</p>
                    <p><strong>Risk tolerance:</strong> ${riskTolerance.toFixed(1)}</p>
                    <p><strong>Risk level (course):</strong> ${riskLevel}</p>
                `;
                
                // Display all options
                allOptions.innerHTML = '';
                Object.entries(data.all_options).forEach(([course, utility]) => {
                    const optionCard = document.createElement('div');
                    optionCard.className = 'option-card';
                    optionCard.innerHTML = `
                        <h4>${course}</h4>
                        <div class="utility">Utility: ${utility.toFixed(2)}</div>
                    `;
                    allOptions.appendChild(optionCard);
                });
                
                recommendationResults.classList.remove('hidden');
            } else {
                showError(recommendationResults, 'No recommendations available. Complete more courses.');
            }
        } else {
            showError(recommendationResults, data.message || 'No recommendations available.');
        }
    } catch (error) {
        console.error('Error getting recommendations:', error);
        showError(recommendationResults, 'Error getting recommendations. Please try again.');
    }
}

// Function to get course details
async function getCourseDetails() {
    const courseName = courseNameSelect.value;
    
    if (!courseName) {
        alert('Please select a course to view details.');
        return;
    }
    
    try {
        showLoading(courseDetailsResults);
        
        const response = await fetch(`${API_BASE_URL}/course-details`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                course_name: courseName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            courseInfo.innerHTML = `
                <div class="course-info-card">
                    <h3>${data.course_name}</h3>
                    <p><strong>Utility:</strong> ${data.attributes.utility}/10</p>
                    <p><strong>Difficulty:</strong> ${data.attributes.difficulty}/10</p>
                    <p><strong>Estimated Time:</strong> ${data.attributes.time_hours} hours</p>
                    <p><strong>Prerequisites:</strong></p>
                    <ul class="prerequisites-list">
                        ${data.prerequisites.map(prereq => `<li>${prereq}</li>`).join('')}
                    </ul>
                </div>
            `;
            
            courseDetailsResults.classList.remove('hidden');
        } else {
            showError(courseDetailsResults, data.error || 'Error getting course details.');
        }
    } catch (error) {
        console.error('Error getting course details:', error);
        showError(courseDetailsResults, 'Error getting course details. Please try again.');
    }
}

// Helper function to show loading state
function showLoading(element) {
    element.classList.remove('hidden');
    element.innerHTML = '<p>Loading...</p>';
}

// Helper function to show error message
function showError(element, message) {
    element.classList.remove('hidden');
    element.innerHTML = `<div class="error-message">${message}</div>`;
}

// Helper function to show success message
function showSuccess(element, message) {
    element.classList.remove('hidden');
    element.innerHTML = `<div class="success-message">${message}</div>`;
}

// Function to plan career path
async function planCareerPath() {
    const targetCareer = targetCareerSelect.value;
    const timeHorizon = parseInt(timeHorizonInput.value);

    if (!targetCareer) {
        alert('Please select a target career.');
        return;
    }

    if (userCompletedCourses.length === 0) {
        alert('Please add at least one completed course first.');
        return;
    }

    try {
        showLoading(careerPathResults);

        const response = await fetch(`${API_BASE_URL}/career-path`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_skills: userCompletedCourses,
                target_career: targetCareer,
                time_horizon_months: timeHorizon
            })
        });

        const data = await response.json();

        if (data.success) {
            let resultHTML = `
                <div class="career-path-result">
                    <h4>Target Career: ${data.target_career}</h4>
                    <p><strong>Feasibility:</strong> ${data.feasibility}</p>
                    <p><strong>Required Courses:</strong> ${data.required_courses.join(', ')}</p>
                    <p><strong>Missing Courses:</strong> ${data.missing_courses.join(', ') || 'None - You have all required skills!'}</p>
                    ${data.missing_courses.length > 0 ? `
                        <p><strong>Recommended Path:</strong></p>
                        <div class="path-details">
                            <p><strong>Path:</strong> ${data.recommended_path.path}</p>
                            <p><strong>Total Cost:</strong> ${data.recommended_path.total_cost}</p>
                        </div>
                    ` : ''}
                </div>
            `;

            careerPathDisplay.innerHTML = resultHTML;
            careerPathResults.classList.remove('hidden');
        } else {
            showError(careerPathResults, data.error || 'Error planning career path.');
        }
    } catch (error) {
        console.error('Error planning career path:', error);
        showError(careerPathResults, 'Error planning career path. Please try again.');
    }
}

// Function to analyze skill gap
async function analyzeSkillGap() {
    const targetSkills = targetSkillsInput.value.split(',').map(skill => skill.trim()).filter(skill => skill);

    if (targetSkills.length === 0) {
        alert('Please enter target skills (comma-separated).');
        return;
    }

    if (userCompletedCourses.length === 0) {
        alert('Please add at least one completed course first.');
        return;
    }

    try {
        showLoading(skillGapResults);

        const response = await fetch(`${API_BASE_URL}/skill-gap-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_skills: userCompletedCourses,
                target_skills: targetSkills
            })
        });

        const data = await response.json();

        if (data.success) {
            let resultHTML = `
                <div class="skill-gap-result">
                    <h4>Skill Gap Analysis</h4>
                    <p><strong>Current Skills:</strong> ${data.current_skills.join(', ')}</p>
                    <p><strong>Target Skills:</strong> ${data.target_skills.join(', ')}</p>
                    <p><strong>Matched Skills:</strong> ${data.matched_skills.join(', ')}</p>
                    <p><strong>Extra Skills:</strong> ${data.extra_skills.join(', ') || 'None'}</p>
                    <p><strong>Missing Skills:</strong> ${data.missing_skills.join(', ') || 'None - No gaps!'}</p>
                    <p><strong>Gap Severity:</strong> ${data.gap_severity}</p>
                    
                    ${data.missing_skills.length > 0 ? `
                        <div class="missing-skills-details">
                            <h5>Missing Skills Details:</h5>
                            ${data.missing_skills.map(skill => {
                                const skillInfo = data.missing_skills_with_paths[skill] || { path: { path: null }, prerequisites_needed: [] };
                                const pathText = (skillInfo.path && skillInfo.path.path) ? skillInfo.path.path : 'Path not available';
                                const prereqsText = (skillInfo.prerequisites_needed && skillInfo.prerequisites_needed.length > 0)
                                    ? skillInfo.prerequisites_needed.join(', ')
                                    : 'None';
                                return `
                                <div class="missing-skill">
                                    <h6>${skill}</h6>
                                    <p>Path: ${pathText}</p>
                                    <p>Prerequisites needed: ${prereqsText}</p>
                                </div>
                                `;
                            }).join('')}
                        </div>
                    ` : ''}
                </div>
            `;

            skillGapDisplay.innerHTML = resultHTML;
            skillGapResults.classList.remove('hidden');
        } else {
            showError(skillGapResults, 'Error analyzing skill gap.');
        }
    } catch (error) {
        console.error('Error analyzing skill gap:', error);
        showError(skillGapResults, 'Error analyzing skill gap. Please try again.');
    }
}

// Function to get detailed learning progression
async function getLearningProgress() {
    const goalCourse = goalCourseProgressSelect.value;

    if (!goalCourse) {
        alert('Please select a goal course.');
        return;
    }

    if (userCompletedCourses.length === 0) {
        alert('Please add at least one completed course first.');
        return;
    }

    try {
        showLoading(progressResults);

        const response = await fetch(`${API_BASE_URL}/learning-progression`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_courses: userCompletedCourses,
                goal_course: goalCourse
            })
        });

        const data = await response.json();

        if (data.success) {
            let courseDetailsHtml = '';
            if (Array.isArray(data.course_details)) {
                courseDetailsHtml = data.course_details.map(detail => `
                    <div class="progress-course">
                        <h5>${detail.course_name}</h5>
                        <p><strong>Difficulty:</strong> ${detail.difficulty}/10</p>
                        <p><strong>Estimated Time:</strong> ${detail.time_hours} hours</p>
                        <p><strong>Utility:</strong> ${detail.utility}/10</p>
                    </div>
                `).join('');
            }

            const averageDifficulty = typeof data.average_difficulty === 'number'
                ? data.average_difficulty.toFixed(2)
                : data.average_difficulty;

            progressDisplay.innerHTML = `
                <div class="learning-progression-result">
                    <h4>Learning Progression</h4>
                    <p><strong>Path:</strong> ${data.path}</p>
                    <p><strong>Total Time:</strong> ${data.total_time_hours} hours</p>
                    <p><strong>Average Difficulty:</strong> ${averageDifficulty}</p>
                    <p><strong>Total Utility:</strong> ${data.total_utility}</p>
                    <p><strong>Estimated Completion:</strong> ${data.estimated_completion_time}</p>
                    ${courseDetailsHtml ? `<h5>Course-by-course details:</h5>${courseDetailsHtml}` : ''}
                </div>
            `;

            progressResults.classList.remove('hidden');
        } else {
            showError(progressResults, data.message || 'No learning progression found.');
        }
    } catch (error) {
        console.error('Error getting learning progression:', error);
        showError(progressResults, 'Error getting learning progression. Please try again.');
    }
}

// Function to load all courses and populate filters
async function loadAllCourses() {
    try {
        const response = await fetch(`${API_BASE_URL}/all-courses`);
        const data = await response.json();

        if (data.success) {
            // Update available courses array from API
            availableCourses.length = 0; // Clear the array
            Object.keys(data.courses).forEach(course => {
                availableCourses.push(course);
            });

            // Populate course dropdowns dynamically
            populateCourseDropdowns();

            // Populate category filter
            const categories = [...new Set(Object.values(data.courses).map(course => course.category))];
            categoryFilter.innerHTML = '<option value="">All Categories</option>';
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilter.appendChild(option);
            });

            // Pre-populate with sample courses if empty
            if (userCompletedCourses.length === 0) {
                userCompletedCourses = ['Python Basics'];
                updateCompletedCoursesDisplay();
            }
        }
    } catch (error) {
        console.error('Error loading courses:', error);
    }
}

// Function to filter courses based on search and filters
async function filterCourses() {
    const searchTerm = courseSearch.value.toLowerCase();
    const category = categoryFilter.value;
    const minDifficulty = parseInt(difficultyMin.value);
    const maxDifficulty = parseInt(difficultyMax.value);
    const maxTime = parseInt(timeFilter.value) || 100;

    try {
        // Using the API to get all courses
        const response = await fetch(`${API_BASE_URL}/all-courses`);
        const data = await response.json();

        if (data.success) {
            let filteredCourses = Object.entries(data.courses)
                .filter(([course, attrs]) => {
                    // Search term filter
                    const matchesSearch = !searchTerm || 
                        course.toLowerCase().includes(searchTerm) || 
                        attrs.category.toLowerCase().includes(searchTerm);
                    
                    // Category filter
                    const matchesCategory = !category || attrs.category === category;
                    
                    // Difficulty filter
                    const matchesDifficulty = attrs.difficulty >= minDifficulty && 
                                            attrs.difficulty <= maxDifficulty;
                    
                    // Time filter
                    const matchesTime = attrs.time_hours <= maxTime;

                    return matchesSearch && matchesCategory && matchesDifficulty && matchesTime;
                });

            displayCourseResults(filteredCourses);
        }
    } catch (error) {
        console.error('Error filtering courses:', error);
    }
}

// Function to display course results in a grid
function displayCourseResults(courses) {
    courseGrid.innerHTML = '';

    if (courses.length === 0) {
        courseResults.classList.remove('hidden');
        courseGrid.innerHTML = '<p class="no-results">No courses match your criteria.</p>';
        return;
    }

    courses.forEach(([course, attrs]) => {
        const courseCard = document.createElement('div');
        courseCard.className = 'course-card';
        courseCard.innerHTML = `
            <h4>${course}</h4>
            <div class="course-category">${attrs.category}</div>
            <div class="course-attributes">
                <div class="attribute">
                    <div class="attribute-value">${attrs.difficulty}/10</div>
                    <div class="attribute-label">Difficulty</div>
                </div>
                <div class="attribute">
                    <div class="attribute-value">${attrs.time_hours}h</div>
                    <div class="attribute-label">Time</div>
                </div>
                <div class="attribute">
                    <div class="attribute-value">${attrs.utility}/10</div>
                    <div class="attribute-label">Utility</div>
                </div>
            </div>
        `;
        
        courseCard.addEventListener('click', () => {
            // When a course card is clicked, populate the course details section
            courseNameSelect.value = course;
            getCourseDetails();
            
            // Scroll to the course details section
            document.getElementById('course-details').scrollIntoView({ behavior: 'smooth' });
        });
        
        courseGrid.appendChild(courseCard);
    });

    courseResults.classList.remove('hidden');
}

// Function to update the progress dashboard
function updateDashboard() {
    // Update dashboard values from stored progress
    coursesCompleted.textContent = userProgress.completedCourses.length;
    learningHours.textContent = userProgress.learningHours;
    learningStreak.textContent = userProgress.learningStreak;
    achievementCount.textContent = userProgress.achievements.length;
    
    // Initialize the progress chart if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeProgressChart();
    }
}

// Function to initialize the progress chart
function initializeProgressChart() {
    const ctx = document.getElementById('progress-chart');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (window.progressChart) {
        window.progressChart.destroy();
    }
    
    // Create a sample chart
    window.progressChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
            datasets: [{
                label: 'Courses Completed',
                data: [2, 3, 5, 6, 7, 8],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.4
            }, {
                label: 'Learning Hours',
                data: [15, 25, 40, 55, 60, 70],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Learning Progress Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to update the path visualization
function updatePathVisualization(pathList) {
    const container = document.getElementById('path-visual-content');
    
    if (!pathList || pathList.length === 0) {
        container.innerHTML = '<p>No learning path to visualize. Find a path first.</p>';
        return;
    }
    
    // Create a simple visualization of the path
    let html = '<h3>Your Learning Path Visualization</h3>';
    html += '<div class="path-visualization">';
    
    pathList.forEach((course, index) => {
        const isLast = index === pathList.length - 1;
        html += `
            <div class="path-node">
                <div class="node-content">${course}</div>
                ${!isLast ? '<div class="arrow">→</div>' : ''}
            </div>
        `;
    });
    
    html += '</div>';
    
    container.innerHTML = html;
}

// Function to export learning path
function exportLearningPath() {
    // Get the current path display content
    const pathContent = pathDisplay.textContent;
    
    if (!pathContent || pathContent === '') {
        alert('No learning path to export. Find a learning path first.');
        return;
    }
    
    // Create a basic text file with the path
    const path = pathDisplay.textContent;
    const cost = pathCost.textContent;
    
    const content = `Learning Path Export\n\nPath: ${path}\n${cost}\n\nGenerated on: ${new Date().toLocaleString()}`;
    
    // Create and download the file
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `learning-path-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

// Load user progress from localStorage
function loadUserProgress() {
    const savedProgress = localStorage.getItem('learningPathProgress');
    if (savedProgress) {
        try {
            userProgress = JSON.parse(savedProgress);
            userCompletedCourses = userProgress.completedCourses || [];
        } catch (e) {
            console.error('Error loading user progress:', e);
            // Reset to default if there's an error
            userProgress = {
                completedCourses: [],
                learningHours: 0,
                learningStreak: 0,
                achievements: [],
                lastActivity: new Date().toISOString(),
                preferences: {
                    learningStyle: 'balanced',
                    riskTolerance: 0.5,
                    theme: 'light'
                }
            };
        }
    } else {
        // Set default progress if no saved data
        userProgress = {
            completedCourses: [],
            learningHours: 0,
            learningStreak: 0,
            achievements: [],
            lastActivity: new Date().toISOString(),
            preferences: {
                learningStyle: 'balanced',
                riskTolerance: 0.5,
                theme: 'light'
            }
        };
    }
}

// Save user progress to localStorage
function saveUserProgress() {
    localStorage.setItem('learningPathProgress', JSON.stringify(userProgress));
}

// Function to mark a course as completed
function markCourseCompleted(courseName) {
    if (!userCompletedCourses.includes(courseName)) {
        userCompletedCourses.push(courseName);
        userProgress.completedCourses = userCompletedCourses;
        
        // Calculate time for this course (in a real app, this would come from the API)
        // For now, let's assume each course takes some time
        userProgress.learningHours += 10; // Default value for demo
        
        // Update streak
        const today = new Date().toDateString();
        const lastActivityDate = new Date(userProgress.lastActivity).toDateString();
        
        if (today === lastActivityDate) {
            // Same day, don't increment streak
        } else if (new Date().getTime() - new Date(userProgress.lastActivity).getTime() <= 86400000) {
            // Consecutive day, increment streak
            userProgress.learningStreak += 1;
        } else {
            // Not consecutive, reset to 1
            userProgress.learningStreak = 1;
        }
        
        userProgress.lastActivity = new Date().toISOString();
        
        // Check for achievements
        checkForAchievements();
        
        // Save progress
        saveUserProgress();
        
        // Update UI
        updateCompletedCoursesDisplay();
        updateDashboard();
    }
}

// Function to check for achievements
function checkForAchievements() {
    const completedCount = userCompletedCourses.length;
    
    // Add achievements based on progress
    if (completedCount >= 1 && !userProgress.achievements.includes('first-course')) {
        userProgress.achievements.push('first-course');
        showAchievement('First Course', 'Completed your first course!');
    }
    
    if (completedCount >= 5 && !userProgress.achievements.includes('learner')) {
        userProgress.achievements.push('learner');
        showAchievement('Dedicated Learner', 'Completed 5 courses!');
    }
    
    if (userProgress.learningStreak >= 5 && !userProgress.achievements.includes('streak')) {
        userProgress.achievements.push('streak');
        showAchievement('Learning Streak', '5-day learning streak!');
    }
    
    if (userProgress.learningHours >= 50 && !userProgress.achievements.includes('hours')) {
        userProgress.achievements.push('hours');
        showAchievement('Time Invested', '50+ hours of learning!');
    }
}

// Function to show achievement notification
function showAchievement(title, description) {
    // Create a simple achievement notification
    const achievementNotif = document.createElement('div');
    achievementNotif.className = 'achievement-notification';
    achievementNotif.innerHTML = `
        <div class="achievement-content">
            <h4>🏆 Achievement Unlocked!</h4>
            <h5>${title}</h5>
            <p>${description}</p>
        </div>
    `;
    
    document.body.appendChild(achievementNotif);
    
    // Add animation
    setTimeout(() => {
        achievementNotif.style.opacity = '1';
        achievementNotif.style.transform = 'translateY(0)';
    }, 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
        achievementNotif.style.opacity = '0';
        achievementNotif.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            if (document.body.contains(achievementNotif)) {
                document.body.removeChild(achievementNotif);
            }
        }, 300);
    }, 5000);
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // Load user progress from localStorage
    loadUserProgress();
    
    // Set up event listeners
    addCourseBtn.addEventListener('click', addCourseToProgress);
    findPathBtn.addEventListener('click', findLearningPath);
    getRecommendationBtn.addEventListener('click', getCourseRecommendation);
    getCourseDetailsBtn.addEventListener('click', getCourseDetails);
    planCareerPathBtn.addEventListener('click', planCareerPath);
    analyzeSkillGapBtn.addEventListener('click', analyzeSkillGap);
    getProgressBtn.addEventListener('click', getLearningProgress);

    // Course explorer event listeners
    applyFiltersBtn.addEventListener('click', filterCourses);
    courseSearch.addEventListener('input', filterCourses);
    difficultyMin.addEventListener('input', function() {
        difficultyMinValue.textContent = this.value;
        filterCourses();
    });
    difficultyMax.addEventListener('input', function() {
        difficultyMaxValue.textContent = this.value;
        filterCourses();
    });
    timeFilter.addEventListener('input', filterCourses);
    
    // Export path button
    exportPathBtn.addEventListener('click', exportLearningPath);

    // Mobile navigation
    setupMobileNavigation();

    // User preferences
    initializeUserPreferences();

    // Initialize with loaded data
    updateCompletedCoursesDisplay();
    
    // Load all courses and populate filters
    loadAllCourses();
    
    // Initialize dashboard
    updateDashboard();
});

// Function to set up navigation (tab-like behavior on all screen sizes)
function setupMobileNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('main > section');

    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = section.id === sectionId ? 'block' : 'none';
        });
    }

    // Initial state: show user-progress, set corresponding button active
    showSection('user-progress');
    const defaultBtn = document.querySelector('.nav-btn[data-section="user-progress"]');
    if (defaultBtn) {
        defaultBtn.classList.add('active');
    }

    navButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetSection = this.getAttribute('data-section');

            showSection(targetSection);

            // Scroll to the section
            document.getElementById(targetSection).scrollIntoView({ behavior: 'smooth', block: 'start' });

            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // On resize, keep the current active section visible and hide the rest
    window.addEventListener('resize', function () {
        const activeBtn = document.querySelector('.nav-btn.active');
        const targetSection = activeBtn ? activeBtn.getAttribute('data-section') : 'user-progress';
        showSection(targetSection);
    });
}

// Function to initialize user preferences
function initializeUserPreferences() {
    // Get DOM elements for preferences
    const prefLearningStyle = document.getElementById('pref-learning-style');
    const prefRiskTolerance = document.getElementById('pref-risk-tolerance');
    const riskToleranceValue = document.getElementById('risk-tolerance-value');
    const prefTheme = document.getElementById('pref-theme');
    const prefEmail = document.getElementById('pref-email');
    const prefGoal = document.getElementById('pref-goal');
    const saveSettingsBtn = document.getElementById('save-settings-btn');
    const resetProgressBtn = document.getElementById('reset-progress-btn');
    
    // Set up event listeners for preferences
    if (prefLearningStyle) prefLearningStyle.addEventListener('change', updatePreferences);
    if (prefRiskTolerance) {
        prefRiskTolerance.addEventListener('input', function() {
            riskToleranceValue.textContent = this.value;
            updatePreferences();
        });
    }
    if (prefTheme) prefTheme.addEventListener('change', updateTheme);
    if (prefEmail) prefEmail.addEventListener('change', updatePreferences);
    if (prefGoal) prefGoal.addEventListener('change', updatePreferences);
    if (saveSettingsBtn) saveSettingsBtn.addEventListener('click', savePreferences);
    if (resetProgressBtn) resetProgressBtn.addEventListener('click', resetUserProgress);
    
    // Load saved preferences
    loadSavedPreferences();
}

// Function to update user preferences in memory
function updatePreferences() {
    const prefLearningStyle = document.getElementById('pref-learning-style');
    const prefRiskTolerance = document.getElementById('pref-risk-tolerance');
    const prefEmail = document.getElementById('pref-email');
    const prefGoal = document.getElementById('pref-goal');
    
    if (prefLearningStyle) userProgress.preferences.learningStyle = prefLearningStyle.value;
    if (prefRiskTolerance) userProgress.preferences.riskTolerance = parseFloat(prefRiskTolerance.value);
    if (prefEmail) userProgress.preferences.emailNotifications = prefEmail.checked;
    if (prefGoal) userProgress.preferences.goal = prefGoal.value;
    
    // Save to localStorage
    saveUserProgress();
}

// Function to save preferences to localStorage
function savePreferences() {
    // Make sure all preferences are updated first
    updatePreferences();
    
    // Show confirmation
    showSuccessMessage('Preferences saved successfully!');
}

// Function to load saved preferences from localStorage
function loadSavedPreferences() {
    // Set the form values from userProgress.preferences
    const prefLearningStyle = document.getElementById('pref-learning-style');
    const prefRiskTolerance = document.getElementById('pref-risk-tolerance');
    const riskToleranceValue = document.getElementById('risk-tolerance-value');
    const prefTheme = document.getElementById('pref-theme');
    const prefEmail = document.getElementById('pref-email');
    const prefGoal = document.getElementById('pref-goal');
    
    if (prefLearningStyle) prefLearningStyle.value = userProgress.preferences.learningStyle || 'balanced';
    if (prefRiskTolerance) {
        prefRiskTolerance.value = userProgress.preferences.riskTolerance || 0.5;
        if (riskToleranceValue) riskToleranceValue.textContent = userProgress.preferences.riskTolerance || 0.5;
    }
    if (prefTheme) prefTheme.value = userProgress.preferences.theme || 'light';
    if (prefEmail) prefEmail.checked = userProgress.preferences.emailNotifications || false;
    if (prefGoal) prefGoal.value = userProgress.preferences.goal || '';
    
    // Apply theme
    updateTheme();
}

// Function to update the app theme
function updateTheme() {
    const themeSelect = document.getElementById('pref-theme');
    const theme = themeSelect ? themeSelect.value : 'light';
    
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        document.documentElement.style.setProperty('--bg-white', '#1a1a1a');
        document.documentElement.style.setProperty('--bg-light', '#222');
        document.documentElement.style.setProperty('--dark-color', '#f0f0f0');
        document.documentElement.style.setProperty('--light-color', '#333');
        document.documentElement.style.setProperty('--dark-light', '#ddd');
    } else if (theme === 'light') {
        document.body.classList.remove('dark-mode');
        // Reset to default light theme values
        document.documentElement.style.setProperty('--bg-white', '#ffffff');
        document.documentElement.style.setProperty('--bg-light', '#f8f9fa');
        document.documentElement.style.setProperty('--dark-color', '#34495e');
        document.documentElement.style.setProperty('--light-color', '#ecf0f1');
        document.documentElement.style.setProperty('--dark-light', '#2c3e50');
    }
    // For 'auto', let the media query handle it
    
    // Update preferences
    userProgress.preferences.theme = theme;
    saveUserProgress();
}

// Function to reset user progress
function resetUserProgress() {
    if (confirm('Are you sure you want to reset all your progress? This cannot be undone.')) {
        // Reset to default values
        userProgress = {
            completedCourses: [],
            learningHours: 0,
            learningStreak: 0,
            achievements: [],
            lastActivity: new Date().toISOString(),
            preferences: {
                learningStyle: 'balanced',
                riskTolerance: 0.5,
                theme: 'light',
                emailNotifications: false,
                goal: ''
            }
        };
        
        userCompletedCourses = [];
        
        // Save to localStorage
        saveUserProgress();
        
        // Update UI
        updateCompletedCoursesDisplay();
        updateDashboard();
        loadSavedPreferences();
        
        showSuccessMessage('Progress has been reset successfully.');
    }
}

// Function to show success message
function showSuccessMessage(message) {
    // Create a simple notification
    const successNotif = document.createElement('div');
    successNotif.className = 'success-notification';
    successNotif.innerHTML = `
        <div class="success-content">
            <h5>✅ ${message}</h5>
        </div>
    `;
    
    document.body.appendChild(successNotif);
    
    // Add animation
    setTimeout(() => {
        successNotif.style.opacity = '1';
        successNotif.style.transform = 'translateY(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        successNotif.style.opacity = '0';
        successNotif.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            if (document.body.contains(successNotif)) {
                document.body.removeChild(successNotif);
            }
        }, 300);
    }, 3000);
}