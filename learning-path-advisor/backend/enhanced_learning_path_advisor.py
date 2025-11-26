"""
Enhanced Learning Path Advisor Backend
Implements advanced AI agents to recommend optimal learning paths
"""
import json
from typing import Dict, List, Tuple, Optional, Union, Any
from enum import Enum
from advanced_goal_based_agent import AdvancedGoalBasedAgent, PathfindingAlgorithm
from advanced_utility_based_agent import AdvancedUtilityBasedAgent, DecisionStrategy
from hybrid_agent import HybridAgent


class LearningStyle(Enum):
    """Learning style preferences for path optimization"""
    FASTEST = "fastest"  # Prioritize shortest time
    EASIEST = "easiest"  # Prioritize lowest difficulty
    BALANCED = "balanced"  # Balance time and difficulty
    CHALLENGING = "challenging"  # Prioritize high utility courses


class EnhancedLearningPathAdvisor:
    """
    Enhanced Learning Path Advisor using advanced AI agents to recommend optimal learning paths
    """
    def __init__(self):
        """
        Initialize the enhanced learning path advisor with course prerequisites and utilities
        """
        # Course database with prerequisites and dependencies
        self.course_prerequisites = {
            # Computer Science & Programming
            'Python Basics': [],
            'Python Intermediate': ['Python Basics'],
            'Data Structures': ['Python Intermediate'],
            'Algorithms': ['Data Structures'],
            'Web Development': ['Python Intermediate'],
            'Database Systems': ['Python Basics'],
            'Machine Learning': ['Data Structures', 'Algorithms'],
            'Data Science': ['Machine Learning', 'Database Systems'],
            'Software Engineering': ['Algorithms', 'Web Development'],
            'DevOps': ['Web Development', 'Database Systems'],
            'AI Fundamentals': ['Data Structures', 'Algorithms'],
            'Mathematics': [],
            'Statistics': ['Mathematics'],
            'Data Visualization': ['Python Intermediate', 'Statistics'],
            'Cloud Computing': ['Web Development', 'DevOps'],
            'Cybersecurity': ['Software Engineering'],
            'Mobile Development': ['Web Development'],
            'Game Development': ['Algorithms', 'Mathematics'],
            
            # Marketing & Digital Marketing
            'Marketing Fundamentals': [],
            'Digital Marketing': ['Marketing Fundamentals'],
            'Social Media Marketing': ['Marketing Fundamentals'],
            'Content Marketing': ['Marketing Fundamentals'],
            'SEO Basics': ['Digital Marketing'],
            'Email Marketing': ['Digital Marketing'],
            'Marketing Analytics': ['Statistics', 'Digital Marketing'],
            'Brand Management': ['Marketing Fundamentals'],
            'Marketing Research': ['Marketing Fundamentals', 'Statistics'],
            'Influencer Marketing': ['Social Media Marketing'],
            'E-commerce Marketing': ['Digital Marketing', 'Web Development'],
            'Marketing Automation': ['Email Marketing', 'Digital Marketing'],
            
            # Business & Management
            'Business Fundamentals': [],
            'Entrepreneurship': ['Business Fundamentals'],
            'Business Strategy': ['Business Fundamentals'],
            'Operations Management': ['Business Fundamentals'],
            'Financial Management': ['Business Fundamentals'],
            'Project Management': ['Business Fundamentals'],
            'Business Analytics': ['Statistics', 'Business Fundamentals'],
            'Leadership': ['Business Fundamentals'],
            'Human Resources': ['Business Fundamentals'],
            'Business Law': ['Business Fundamentals'],
            'International Business': ['Business Fundamentals'],
            'Corporate Finance': ['Financial Management'],
            'Business Process Management': ['Operations Management'],
            'Change Management': ['Leadership'],
            
            # Design & Creative Arts
            'Graphic Design': [],
            'UI/UX Design': ['Graphic Design'],
            'Web Design': ['Graphic Design'],
            'Digital Illustration': ['Graphic Design'],
            'Photography': [],
            'Video Editing': ['Photography'],
            'Animation': ['Digital Illustration'],
            '3D Modeling': ['Animation'],
            'Motion Graphics': ['Animation', 'Video Editing'],
            'Color Theory': ['Graphic Design'],
            'Typography': ['Graphic Design'],
            'Branding': ['Graphic Design', 'Marketing Fundamentals'],
            
            # Data & Analytics
            'SQL Basics': ['Database Systems'],
            'Data Analysis': ['Statistics', 'SQL Basics'],
            'Excel Advanced': ['Statistics'],
            'Business Intelligence': ['Data Analysis', 'Business Analytics'],
            'Big Data': ['Data Science', 'Statistics'],
            'Data Mining': ['Statistics', 'Data Structures'],
            'Predictive Analytics': ['Statistics', 'Machine Learning'],
            'Data Warehousing': ['Database Systems'],
            
            # Finance & Accounting
            'Accounting Basics': [],
            'Financial Accounting': ['Accounting Basics'],
            'Managerial Accounting': ['Accounting Basics'],
            'Investment Analysis': ['Financial Management', 'Statistics'],
            'Risk Management': ['Financial Management'],
            'Tax Preparation': ['Accounting Basics'],
            'Auditing': ['Financial Accounting'],
            'Corporate Finance': ['Financial Management'],
            
            # Sales & Customer Success
            'Sales Fundamentals': [],
            'Customer Relationship Management': ['Marketing Fundamentals'],
            'Negotiation': ['Sales Fundamentals'],
            'Consulting': ['Business Fundamentals'],
            'Customer Success': ['Marketing Fundamentals'],
            
            # Languages
            'English Language': [],
            'Spanish Language': [],
            'French Language': [],
            'Business English': ['English Language'],
            'Technical Writing': ['English Language'],
            
            # Health & Wellness
            'Nutrition': [],
            'Fitness Training': [],
            'Mental Health': [],
            'Yoga': [],
            'Meditation': [],
            
            # Creative Writing & Journalism
            'Creative Writing': ['English Language'],
            'Journalism': ['English Language'],
            'Copywriting': ['Marketing Fundamentals', 'English Language'],
            
            # Product Management
            'Product Management': ['Business Fundamentals'],
            'Product Design': ['Product Management', 'UI/UX Design'],
            'Agile Methodology': ['Project Management'],
            'Scrum Master': ['Agile Methodology'],

            # Education & Training
            'Teaching Fundamentals': [],
            'Curriculum Design': ['Teaching Fundamentals'],
            'Educational Technology': ['Teaching Fundamentals'],
            'Adult Learning': ['Teaching Fundamentals'],
            'Online Teaching': ['Educational Technology'],
            'Special Education': ['Teaching Fundamentals'],
            'Educational Psychology': ['Teaching Fundamentals'],

            # Law & Legal Studies
            'Legal Fundamentals': [],
            'Contract Law': ['Legal Fundamentals'],
            'Corporate Law': ['Legal Fundamentals'],
            'Intellectual Property': ['Legal Fundamentals'],
            'Cyber Law': ['Legal Fundamentals', 'Cybersecurity'],

            # Healthcare & Medicine
            'Medical Fundamentals': [],
            'Medical Coding': ['Medical Fundamentals'],
            'Healthcare Administration': ['Medical Fundamentals'],
            'Pharmacology': ['Medical Fundamentals'],
            'Medical Ethics': ['Medical Fundamentals'],

            # Arts & Music
            'Music Theory': [],
            'Digital Music Production': ['Music Theory'],
            'Art History': [],
            'Drawing': [],
            'Painting': ['Drawing'],
            'Pottery': [],
            'Sculpture': ['Drawing'],
            'Music Performance': ['Music Theory'],
        }

        # Course difficulty and time estimates (hours)
        self.course_attributes = {
            # Computer Science & Programming
            'Python Basics': {'difficulty': 3, 'time_hours': 20, 'utility': 8, 'prerequisites_count': 0, 'category': 'Programming'},
            'Python Intermediate': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Programming'},
            'Data Structures': {'difficulty': 7, 'time_hours': 40, 'utility': 9, 'prerequisites_count': 1, 'category': 'Programming'},
            'Algorithms': {'difficulty': 8, 'time_hours': 50, 'utility': 10, 'prerequisites_count': 1, 'category': 'Programming'},
            'Web Development': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Programming'},
            'Database Systems': {'difficulty': 6, 'time_hours': 30, 'utility': 8, 'prerequisites_count': 1, 'category': 'Programming'},
            'Machine Learning': {'difficulty': 9, 'time_hours': 60, 'utility': 10, 'prerequisites_count': 2, 'category': 'AI/ML'},
            'Data Science': {'difficulty': 8, 'time_hours': 50, 'utility': 9, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Software Engineering': {'difficulty': 7, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Programming'},
            'DevOps': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Programming'},
            'AI Fundamentals': {'difficulty': 8, 'time_hours': 45, 'utility': 9, 'prerequisites_count': 2, 'category': 'AI/ML'},
            'Mathematics': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 0, 'category': 'Foundation'},
            'Statistics': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Foundation'},
            'Data Visualization': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Cloud Computing': {'difficulty': 7, 'time_hours': 50, 'utility': 8, 'prerequisites_count': 2, 'category': 'Infrastructure'},
            'Cybersecurity': {'difficulty': 8, 'time_hours': 45, 'utility': 9, 'prerequisites_count': 1, 'category': 'Security'},
            'Mobile Development': {'difficulty': 6, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Programming'},
            'Game Development': {'difficulty': 7, 'time_hours': 50, 'utility': 8, 'prerequisites_count': 2, 'category': 'Programming'},
            
            # Marketing & Digital Marketing
            'Marketing Fundamentals': {'difficulty': 3, 'time_hours': 20, 'utility': 8, 'prerequisites_count': 0, 'category': 'Marketing'},
            'Digital Marketing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Social Media Marketing': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Content Marketing': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'SEO Basics': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Email Marketing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Marketing Analytics': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Marketing'},
            'Brand Management': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Marketing Research': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Marketing'},
            'Influencer Marketing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'E-commerce Marketing': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Marketing'},
            'Marketing Automation': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 2, 'category': 'Marketing'},
            
            # Business & Management
            'Business Fundamentals': {'difficulty': 3, 'time_hours': 20, 'utility': 7, 'prerequisites_count': 0, 'category': 'Business'},
            'Entrepreneurship': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Business Strategy': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Operations Management': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Financial Management': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Project Management': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Business Analytics': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Business'},
            'Leadership': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Human Resources': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Business Law': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Business'},
            'International Business': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Corporate Finance': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Business Process Management': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Change Management': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            
            # Design & Creative Arts
            'Graphic Design': {'difficulty': 4, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 0, 'category': 'Design'},
            'UI/UX Design': {'difficulty': 7, 'time_hours': 40, 'utility': 9, 'prerequisites_count': 1, 'category': 'Design'},
            'Web Design': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Design'},
            'Digital Illustration': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Design'},
            'Photography': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 0, 'category': 'Creative'},
            'Video Editing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Creative'},
            'Animation': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Creative'},
            '3D Modeling': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 1, 'category': 'Creative'},
            'Motion Graphics': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Creative'},
            'Color Theory': {'difficulty': 4, 'time_hours': 20, 'utility': 6, 'prerequisites_count': 1, 'category': 'Design'},
            'Typography': {'difficulty': 5, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 1, 'category': 'Design'},
            'Branding': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Marketing'},
            
            # Data & Analytics
            'SQL Basics': {'difficulty': 5, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Data Science'},
            'Data Analysis': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Excel Advanced': {'difficulty': 4, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Data Science'},
            'Business Intelligence': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Big Data': {'difficulty': 9, 'time_hours': 50, 'utility': 9, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Data Mining': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Predictive Analytics': {'difficulty': 9, 'time_hours': 50, 'utility': 9, 'prerequisites_count': 2, 'category': 'Data Science'},
            'Data Warehousing': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Data Science'},
            
            # Finance & Accounting
            'Accounting Basics': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 0, 'category': 'Finance'},
            'Financial Accounting': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Managerial Accounting': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Investment Analysis': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Finance'},
            'Risk Management': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Finance'},
            'Tax Preparation': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Finance'},
            'Auditing': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Corporate Finance': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Finance'},
            
            # Sales & Customer Success
            'Sales Fundamentals': {'difficulty': 3, 'time_hours': 20, 'utility': 7, 'prerequisites_count': 0, 'category': 'Sales'},
            'Customer Relationship Management': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Sales'},
            'Negotiation': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Sales'},
            'Consulting': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Customer Success': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Sales'},
            
            # Languages
            'English Language': {'difficulty': 4, 'time_hours': 40, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'Spanish Language': {'difficulty': 4, 'time_hours': 40, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'French Language': {'difficulty': 4, 'time_hours': 40, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'Business English': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Languages'},
            'Technical Writing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Languages'},
            
            # Health & Wellness
            'Nutrition': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 0, 'category': 'Health'},
            'Fitness Training': {'difficulty': 3, 'time_hours': 20, 'utility': 6, 'prerequisites_count': 0, 'category': 'Health'},
            'Mental Health': {'difficulty': 3, 'time_hours': 20, 'utility': 6, 'prerequisites_count': 0, 'category': 'Health'},
            'Yoga': {'difficulty': 2, 'time_hours': 15, 'utility': 5, 'prerequisites_count': 0, 'category': 'Health'},
            'Meditation': {'difficulty': 2, 'time_hours': 15, 'utility': 5, 'prerequisites_count': 0, 'category': 'Health'},
            
            # Creative Writing & Journalism
            'Creative Writing': {'difficulty': 4, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Creative'},
            'Journalism': {'difficulty': 5, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Creative'},
            'Copywriting': {'difficulty': 5, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 2, 'category': 'Marketing'},
            
            # Product Management
            'Product Management': {'difficulty': 7, 'time_hours': 40, 'utility': 9, 'prerequisites_count': 1, 'category': 'Business'},
            'Product Design': {'difficulty': 8, 'time_hours': 45, 'utility': 9, 'prerequisites_count': 2, 'category': 'Design'},
            'Agile Methodology': {'difficulty': 5, 'time_hours': 30, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},
            'Scrum Master': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Business'},

            # Computer Science & Programming (additional)
            'Frontend Development': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Programming'},
            'Backend Development': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Programming'},
            'Full Stack Development': {'difficulty': 8, 'time_hours': 50, 'utility': 9, 'prerequisites_count': 2, 'category': 'Programming'},
            'API Development': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Programming'},
            'Blockchain': {'difficulty': 9, 'time_hours': 55, 'utility': 9, 'prerequisites_count': 2, 'category': 'Programming'},
            'IoT': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Programming'},
            'Computer Vision': {'difficulty': 9, 'time_hours': 55, 'utility': 9, 'prerequisites_count': 1, 'category': 'AI/ML'},
            'Natural Language Processing': {'difficulty': 9, 'time_hours': 55, 'utility': 9, 'prerequisites_count': 1, 'category': 'AI/ML'},
            'Robotics': {'difficulty': 8, 'time_hours': 50, 'utility': 8, 'prerequisites_count': 2, 'category': 'Programming'},

            # Marketing & Digital Marketing (additional)
            'Growth Hacking': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Performance Marketing': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Marketing'},
            'Video Marketing': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 2, 'category': 'Marketing'},

            # Business & Management (additional)
            'Innovation Management': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Supply Chain Management': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Business'},
            'Business Ethics': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Business'},

            # Design & Creative Arts (additional)
            'User Research': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Design'},
            'Interaction Design': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Design'},
            'Design Systems': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 1, 'category': 'Design'},
            'Print Design': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Design'},
            'Package Design': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Design'},
            'Web Animation': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 2, 'category': 'Design'},

            # Data & Analytics (additional)
            'Data Governance': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Data Science'},
            'Business Intelligence Tools': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Data Science'},
            'A/B Testing': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Data Science'},
            'Data Storytelling': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 2, 'category': 'Data Science'},

            # Finance & Accounting (additional)
            'Personal Finance': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Financial Planning': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Cryptocurrency': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},
            'Real Estate Investment': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Finance'},

            # Sales & Customer Success (additional)
            'Account Management': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Sales'},
            'Sales Management': {'difficulty': 6, 'time_hours': 35, 'utility': 8, 'prerequisites_count': 1, 'category': 'Sales'},
            'Business Development': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Sales'},

            # Languages (additional)
            'German Language': {'difficulty': 5, 'time_hours': 45, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'Chinese Language': {'difficulty': 8, 'time_hours': 60, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'Japanese Language': {'difficulty': 7, 'time_hours': 55, 'utility': 6, 'prerequisites_count': 0, 'category': 'Languages'},
            'Translation Studies': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Languages'},
            'Linguistics': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Languages'},

            # Health & Wellness (additional)
            'Public Health': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Health'},
            'Sports Science': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Health'},
            'Nutrition Therapy': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Health'},
            'Wellness Coaching': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 2, 'category': 'Health'},

            # Creative Writing & Journalism (additional)
            'Technical Writing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Creative'},
            'Content Writing': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 1, 'category': 'Creative'},
            'Script Writing': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Creative'},
            'Editing': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 1, 'category': 'Creative'},
            'Publishing': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Creative'},

            # Product Management (additional)
            'Product Analytics': {'difficulty': 7, 'time_hours': 40, 'utility': 8, 'prerequisites_count': 2, 'category': 'Business'},
            'Product Strategy': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Business'},

            # Education & Training
            'Teaching Fundamentals': {'difficulty': 4, 'time_hours': 25, 'utility': 7, 'prerequisites_count': 0, 'category': 'Education'},
            'Curriculum Design': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Education'},
            'Educational Technology': {'difficulty': 5, 'time_hours': 30, 'utility': 7, 'prerequisites_count': 1, 'category': 'Education'},
            'Adult Learning': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Education'},
            'Online Teaching': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Education'},
            'Special Education': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Education'},
            'Educational Psychology': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Education'},

            # Law & Legal Studies
            'Legal Fundamentals': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 0, 'category': 'Law'},
            'Contract Law': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Law'},
            'Corporate Law': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Law'},
            'Intellectual Property': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Law'},
            'Cyber Law': {'difficulty': 8, 'time_hours': 45, 'utility': 8, 'prerequisites_count': 2, 'category': 'Law'},

            # Healthcare & Medicine
            'Medical Fundamentals': {'difficulty': 8, 'time_hours': 45, 'utility': 7, 'prerequisites_count': 0, 'category': 'Healthcare'},
            'Medical Coding': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Healthcare'},
            'Healthcare Administration': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Healthcare'},
            'Pharmacology': {'difficulty': 8, 'time_hours': 45, 'utility': 7, 'prerequisites_count': 1, 'category': 'Healthcare'},
            'Medical Ethics': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Healthcare'},

            # Arts & Music
            'Music Theory': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 0, 'category': 'Arts'},
            'Digital Music Production': {'difficulty': 7, 'time_hours': 40, 'utility': 7, 'prerequisites_count': 1, 'category': 'Arts'},
            'Art History': {'difficulty': 4, 'time_hours': 25, 'utility': 6, 'prerequisites_count': 0, 'category': 'Arts'},
            'Drawing': {'difficulty': 3, 'time_hours': 20, 'utility': 6, 'prerequisites_count': 0, 'category': 'Arts'},
            'Painting': {'difficulty': 5, 'time_hours': 30, 'utility': 6, 'prerequisites_count': 1, 'category': 'Arts'},
            'Pottery': {'difficulty': 4, 'time_hours': 25, 'utility': 5, 'prerequisites_count': 0, 'category': 'Arts'},
            'Sculpture': {'difficulty': 6, 'time_hours': 35, 'utility': 6, 'prerequisites_count': 1, 'category': 'Arts'},
            'Music Performance': {'difficulty': 6, 'time_hours': 35, 'utility': 7, 'prerequisites_count': 1, 'category': 'Arts'},
        }

        # Create graph representation for pathfinding
        self.course_graph = self._build_course_graph()

    def _build_course_graph(self) -> Dict[str, List[Tuple[str, Union[int, float]]]]:
        """
        Build a graph representation of courses for pathfinding
        Each edge represents (next_course, cost) where cost could be difficulty, time, etc.
        """
        # Include all known courses (even those without explicit prerequisites)
        all_courses = set(self.course_attributes.keys()) | set(self.course_prerequisites.keys())
        graph = {course: [] for course in all_courses}

        # Add edges for courses that have prerequisites
        for course, prereqs in self.course_prerequisites.items():
            for prereq in prereqs:
                if prereq in graph:
                    # Default cost is difficulty
                    cost = self.course_attributes[course]['difficulty']
                    graph[prereq].append((course, cost))

        return graph

    def _build_weighted_graph(self, 
                             learning_style: LearningStyle,
                             cost_weights: Optional[Dict[str, float]] = None) -> Dict[str, List[Tuple[str, float]]]:
        """Build a graph with weights based on learning style and optional cost weights.

        The edge weight for a course combines multiple objectives:
        - time_hours: prefer shorter courses
        - difficulty: prefer easier courses
        - utility: prefer higher-utility courses (converted via 10-utility)
        - prerequisites_count: prefer shallower prerequisite chains
        """
        # Include all known courses (even those without explicit prerequisites)
        all_courses = set(self.course_attributes.keys()) | set(self.course_prerequisites.keys())
        graph = {course: [] for course in all_courses}

        # Default weights based on learning style, overridden by cost_weights if provided
        if cost_weights is None:
            if learning_style == LearningStyle.FASTEST:
                base_weights = {"time": 0.7, "difficulty": 0.2, "utility": 0.1, "prereq": 0.0}
            elif learning_style == LearningStyle.EASIEST:
                base_weights = {"time": 0.2, "difficulty": 0.6, "utility": 0.2, "prereq": 0.0}
            elif learning_style == LearningStyle.CHALLENGING:
                # Focus strongly on high-utility courses even if harder/longer
                base_weights = {"time": 0.2, "difficulty": 0.2, "utility": 0.5, "prereq": 0.1}
            else:  # BALANCED
                base_weights = {"time": 0.4, "difficulty": 0.3, "utility": 0.2, "prereq": 0.1}
        else:
            # Merge user-provided weights with defaults for any missing keys
            default_for_style = {
                LearningStyle.FASTEST: {"time": 0.7, "difficulty": 0.2, "utility": 0.1, "prereq": 0.0},
                LearningStyle.EASIEST: {"time": 0.2, "difficulty": 0.6, "utility": 0.2, "prereq": 0.0},
                LearningStyle.CHALLENGING: {"time": 0.2, "difficulty": 0.2, "utility": 0.5, "prereq": 0.1},
                LearningStyle.BALANCED: {"time": 0.4, "difficulty": 0.3, "utility": 0.2, "prereq": 0.1},
            }[learning_style]
            base_weights = {
                "time": float(cost_weights.get("time", default_for_style["time"])),
                "difficulty": float(cost_weights.get("difficulty", default_for_style["difficulty"])),
                "utility": float(cost_weights.get("utility", default_for_style["utility"])),
                "prereq": float(cost_weights.get("prereq", default_for_style["prereq"])),
            }

        # Normalize weights so they sum to 1 (unless they are all zero)
        total_w = sum(base_weights.values())
        if total_w == 0:
            # Fallback to difficulty if everything is zero
            norm_weights = {"time": 0.0, "difficulty": 1.0, "utility": 0.0, "prereq": 0.0}
        else:
            norm_weights = {k: v / total_w for k, v in base_weights.items()}

        for course, prereqs in self.course_prerequisites.items():
            for prereq in prereqs:
                if prereq in graph:
                    attrs = self.course_attributes.get(course, {})
                    time_component = float(attrs.get("time_hours", 0.0)) / 10.0
                    difficulty_component = float(attrs.get("difficulty", 0.0))
                    # Convert utility into a cost-like component (lower cost for higher utility)
                    utility_component = float(10.0 - float(attrs.get("utility", 0.0)))
                    prereq_component = float(attrs.get("prerequisites_count", 0.0))

                    weight = (
                        norm_weights["time"] * time_component
                        + norm_weights["difficulty"] * difficulty_component
                        + norm_weights["utility"] * utility_component
                        + norm_weights["prereq"] * prereq_component
                    )

                    # Guard against zero/negative weights which can break some algorithms
                    if weight <= 0:
                        weight = max(difficulty_component, 1.0)

                    graph[prereq].append((course, float(weight)))

        return graph

    def find_learning_path(self, 
                          start_courses: List[str], 
                          goal_course: str, 
                          learning_style: LearningStyle = LearningStyle.BALANCED,
                          algorithm: PathfindingAlgorithm = PathfindingAlgorithm.DIJKSTRA,
                          cost_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Find the optimal learning path from start courses to the goal course
        using advanced pathfinding algorithms and learning preferences.

        Args:
            start_courses: List of courses the learner has already completed
            goal_course: The target course to reach
            learning_style: Preferred learning approach (fastest, easiest, etc.)
            algorithm: Pathfinding algorithm to use

        Returns:
            Dictionary with path information
        """
        # Create a temporary graph based on learning style
        weighted_graph = self._build_weighted_graph(learning_style, cost_weights=cost_weights)
        
        # Add virtual start node to connect all start courses
        temp_graph = {**weighted_graph, 'virtual_start': []}
        for start_course in start_courses:
            if start_course in weighted_graph:
                temp_graph['virtual_start'].append((start_course, 0.0))

        # Use advanced goal-based agent to find path
        agent = AdvancedGoalBasedAgent(
            routes=temp_graph,
            start='virtual_start',
            goal=goal_course,
            algorithm=algorithm
        )
        
        path_str, cost = agent.plan()

        # Remove virtual_start from the path
        if path_str and path_str.startswith('virtual_start -> '):
            path = path_str.replace('virtual_start -> ', '', 1)
        else:
            path = path_str

        # Get detailed path information
        path_details = agent.get_path_details()
        
        return {
            'success': path is not None and cost != float('inf'),
            'path': path,
            'path_list': path.split(' -> ') if path else [],
            'total_cost': cost,
            'start_courses': start_courses,
            'goal_course': goal_course,
            'learning_style': learning_style.value,
            'algorithm_used': algorithm.value,
            'path_details': path_details
        }

    def find_multiple_learning_paths(self, 
                                   start_courses: List[str], 
                                   goal_course: str, 
                                   learning_style: LearningStyle = LearningStyle.BALANCED,
                                   cost_weights: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """
        Find multiple alternative learning paths to the goal course.

        Args:
            start_courses: List of courses the learner has already completed
            goal_course: The target course to reach
            learning_style: Preferred learning approach

        Returns:
            List of dictionaries with alternative path information
        """
        # Create a temporary graph based on learning style
        weighted_graph = self._build_weighted_graph(learning_style, cost_weights=cost_weights)
        
        # Add virtual start node to connect all start courses
        temp_graph = {**weighted_graph, 'virtual_start': []}
        for start_course in start_courses:
            if start_course in weighted_graph:
                temp_graph['virtual_start'].append((start_course, 0.0))

        # Use advanced goal-based agent to find multiple paths
        agent = AdvancedGoalBasedAgent(
            routes=temp_graph,
            start='virtual_start',
            goal=goal_course
        )
        
        all_paths = agent.find_all_paths(max_cost=float('inf'))
        
        results = []
        for path_list, cost in all_paths:
            # Remove virtual_start if present in the path
            clean_path_list = [course for course in path_list if course != 'virtual_start']
            results.append({
                'path': ' -> '.join(clean_path_list),
                'path_list': clean_path_list,
                'total_cost': cost,
                'learning_style': learning_style.value
            })
        
        return results

    def recommend_course_sequence(self, 
                                start_courses: List[str], 
                                goal_course: str, 
                                learning_style: LearningStyle = LearningStyle.BALANCED,
                                risk_tolerance: float = 0.5,
                                cost_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Recommend an optimal sequence of courses using hybrid AI approach.

        Args:
            start_courses: List of courses the learner has already completed
            goal_course: The target course to reach
            learning_style: Preferred learning approach
            risk_tolerance: Tolerance for high-difficulty courses (0-1)

        Returns:
            Dictionary with course sequence recommendation
        """
        # Build weighted graph based on learning style
        weighted_graph = self._build_weighted_graph(learning_style, cost_weights=cost_weights)
        
        # Add virtual start node to connect all start courses
        temp_graph = {**weighted_graph, 'virtual_start': []}
        for start_course in start_courses:
            if start_course in weighted_graph:
                temp_graph['virtual_start'].append((start_course, 0.0))

        # Use hybrid agent for sophisticated decision making
        hybrid_agent = HybridAgent(
            routes=temp_graph,
            start='virtual_start', 
            goal=goal_course,
            path_evaluation_factors={
                'path_length_factor': -0.5,  # Prefer shorter paths
                'node_penalties': {
                    course: -self.course_attributes[course]['utility'] * risk_tolerance 
                    if self.course_attributes[course]['difficulty'] > 7 else 0
                    for course in self.course_attributes.keys() 
                    if course in temp_graph
                }
            }
        )
        
        decision = hybrid_agent.make_decision()
        
        # Remove virtual_start from the path
        clean_path_list = [course for course in decision['path_as_list'] if course != 'virtual_start']
        
        # Calculate additional metrics
        total_time = sum(self.course_attributes[course]['time_hours'] 
                        for course in clean_path_list if course in self.course_attributes)
        total_difficulty = sum(self.course_attributes[course]['difficulty'] 
                              for course in clean_path_list if course in self.course_attributes)
        
        return {
            'success': decision['success'],
            'recommended_sequence': ' -> '.join(clean_path_list),
            'sequence_list': clean_path_list,
            'utility': decision['best_utility'],
            'total_time_hours': total_time,
            'average_difficulty': total_difficulty / len(clean_path_list) if clean_path_list else 0,
            'start_courses': start_courses,
            'goal_course': goal_course,
            'learning_style': learning_style.value,
            'risk_tolerance': risk_tolerance,
            'decision_info': decision['decision_info']
        }

    def evaluate_learning_options(self, 
                                completed_courses: List[str], 
                                decision_strategy: DecisionStrategy = DecisionStrategy.MAXIMUM_EXPECTED_UTILITY,
                                risk_tolerance: float = 0.5) -> Dict[str, Any]:
        """
        Evaluate next learning options using advanced utility-based decision making.

        Args:
            completed_courses: List of courses already completed
            decision_strategy: Strategy to use for decision making

        Returns:
            Dictionary with evaluation and recommendation
        """
        available_courses = self.get_available_courses(completed_courses)
        
        if not available_courses:
            return {
                'success': False,
                'recommended_course': None,
                'available_courses': [],
                'message': 'No courses currently available. Complete more prerequisites.'
            }

        # Create action outcomes for utility-based evaluation
        action_outcomes = {}
        
        for course in available_courses:
            attr = self.course_attributes[course]
            difficulty = float(attr['difficulty'])

            # Calculate utility based on multiple factors
            # Time utility: prefer courses that take less time
            time_utility = 100 / (attr['time_hours'] + 1)
            
            # Difficulty utility: based on difficulty level (inverse for easier courses)
            difficulty_utility = (10 - difficulty)  # Higher for easier courses
            
            # Base utility from course attributes
            base_utility = float(attr['utility'])
            
            # Risk-adjusted success probability based on difficulty and user risk tolerance
            # Start from a base probability that is lower for harder courses
            base_success = 0.9 if difficulty <= 7 else 0.6
            # Adjust around the base using risk_tolerance (0 = very risk averse, 1 = very risk seeking)
            adjust = (risk_tolerance - 0.5) * 0.4  # +/- 0.2 at extremes
            success_prob = max(0.1, min(0.95, base_success + adjust))
            failure_prob = 1.0 - success_prob
            
            # For each course, consider success and failure scenarios
            good_utility = (base_utility * 0.4 + time_utility * 0.3 + difficulty_utility * 0.3)
            bad_utility = (base_utility * 0.1 + time_utility * 0.1 + difficulty_utility * 0.1)

            outcomes = [
                {
                    'probability': success_prob,
                    'utility': good_utility,
                },
                {
                    'probability': failure_prob,
                    'utility': bad_utility,
                },
            ]
            
            action_outcomes[course] = outcomes

        # Use advanced utility-based agent to decide
        agent = AdvancedUtilityBasedAgent(action_outcomes, decision_strategy=decision_strategy)
        best_course, best_utility, additional_info = agent.decide()
        
        # Get risk analysis
        risk_analysis = agent.analyze_risk_profile()
        
        return {
            'success': True,
            'recommended_course': best_course,
            'recommended_utility': best_utility,
            'decision_strategy': decision_strategy.value,
            'all_options': {course: agent.calculate_expected_utility(outcomes) 
                           for course, outcomes in action_outcomes.items()},
            'available_courses': available_courses,
            'risk_analysis': risk_analysis,
            'additional_info': additional_info
        }

    def get_learning_path_with_alternatives(self, 
                                          start_courses: List[str], 
                                          goal_course: str, 
                                          learning_style: LearningStyle = LearningStyle.BALANCED) -> Dict[str, Any]:
        """
        Get primary learning path with alternative options.

        Args:
            start_courses: List of courses already completed
            goal_course: Target course to reach
            learning_style: Preferred learning approach

        Returns:
            Dictionary with primary path and alternatives
        """
        # Get primary path
        primary_result = self.find_learning_path(start_courses, goal_course, learning_style)
        
        # Get multiple alternative paths
        alternative_paths = self.find_multiple_learning_paths(start_courses, goal_course, learning_style)
        
        # Filter out the primary path from alternatives
        primary_path_list = primary_result['path_list'] if primary_result['success'] else []
        alternative_paths = [
            path for path in alternative_paths 
            if path['path_list'] != primary_path_list
        ]
        
        # Calculate additional metrics for each alternative
        for path in alternative_paths:
            course_list = path['path_list']
            time = sum(self.course_attributes[course]['time_hours'] 
                      for course in course_list if course in self.course_attributes)
            difficulty = sum(self.course_attributes[course]['difficulty'] 
                            for course in course_list if course in self.course_attributes)
            path['total_time_hours'] = time
            path['average_difficulty'] = difficulty / len(course_list) if course_list else 0

        return {
            'primary_path': primary_result,
            'alternative_paths': alternative_paths,
            'start_courses': start_courses,
            'goal_course': goal_course,
            'learning_style': learning_style.value
        }

    def get_available_courses(self, completed_courses: List[str]) -> List[str]:
        """
        Get courses that are available to take based on completed prerequisites.

        Args:
            completed_courses: List of courses the learner has completed

        Returns:
            List of courses that can be taken next
        """
        available_courses = []
        completed_set = set(completed_courses)

        for course, prereqs in self.course_prerequisites.items():
            # Check if all prerequisites are completed and course not already taken
            if course not in completed_courses and all(prereq in completed_set for prereq in prereqs):
                available_courses.append(course)

        return available_courses

    def get_courses_by_category(self, category: str) -> List[str]:
        """
        Get all courses in a specific category.

        Args:
            category: The category to filter by

        Returns:
            List of course names in the category
        """
        return [course for course, attrs in self.course_attributes.items() 
                if attrs.get('category', '').lower() == category.lower()]

    def get_all_categories(self) -> List[str]:
        """
        Get all unique course categories.

        Returns:
            List of all unique categories
        """
        categories = set(attrs.get('category', 'Uncategorized') for attrs in self.course_attributes.values())
        return sorted(list(categories))

    def get_course_by_difficulty_range(self, min_difficulty: int, max_difficulty: int) -> List[str]:
        """
        Get courses within a specific difficulty range.

        Args:
            min_difficulty: Minimum difficulty level (1-10)
            max_difficulty: Maximum difficulty level (1-10)

        Returns:
            List of course names within the difficulty range
        """
        return [course for course, attrs in self.course_attributes.items() 
                if min_difficulty <= attrs['difficulty'] <= max_difficulty]

    def get_course_prerequisites_status(self, course_name: str, completed_courses: List[str]) -> Dict[str, Any]:
        """
        Get the status of prerequisites for a specific course.

        Args:
            course_name: Name of the course to check
            completed_courses: List of courses that have been completed

        Returns:
            Dictionary with prerequisite status information
        """
        # Validate against the master course list
        if course_name not in self.course_attributes:
            return {
                'success': False,
                'error': f'Course "{course_name}" not found'
            }

        prerequisites = self.course_prerequisites.get(course_name, [])
        completed_prereqs = [prereq for prereq in prerequisites if prereq in completed_courses]
        remaining_prereqs = [prereq for prereq in prerequisites if prereq not in completed_courses]

        return {
            'success': True,
            'course_name': course_name,
            'prerequisites': prerequisites,
            'completed_prereqs': completed_prereqs,
            'remaining_prereqs': remaining_prereqs,
            'prerequisites_met': len(remaining_prereqs) == 0
        }

    def get_learning_path_by_category(self, start_courses: List[str], category: str) -> Dict[str, Any]:
        """
        Find learning paths that lead to courses in a specific category.

        Args:
            start_courses: List of courses already completed
            category: Target category to find courses for

        Returns:
            Dictionary with paths to courses in the category
        """
        target_courses = self.get_courses_by_category(category)
        
        if not target_courses:
            return {
                'success': False,
                'message': f'No courses found in category: {category}',
                'available_categories': self.get_all_categories()
            }

        # Find the most suitable target course based on current knowledge
        suitable_courses = []
        for course in target_courses:
            prereqs = set(self.course_prerequisites[course])
            completed = set(completed_courses)
            
            # Calculate how many prerequisites are met
            prereqs_met = len(prereqs.intersection(completed))
            prereqs_needed = len(prereqs)
            
            if prereqs_needed == 0 or prereqs_met == prereqs_needed:
                # Course is immediately available
                suitable_courses.append((course, 0))
            elif prereqs_met > 0:
                # Course has some prereqs met
                suitability_score = prereqs_met / prereqs_needed
                suitable_courses.append((course, suitability_score))

        # Sort by suitability
        suitable_courses.sort(key=lambda x: x[1], reverse=True)
        
        if not suitable_courses:
            return {
                'success': False,
                'message': f'No courses in category "{category}" are accessible with your current knowledge',
                'suggestions': f'Complete more foundational courses to unlock {category} courses'
            }

        # Get path to the most suitable course
        best_course, _ = suitable_courses[0]
        path_result = self.find_learning_path(start_courses, best_course)
        
        return {
            'success': path_result['success'],
            'target_category': category,
            'recommended_course': best_course,
            'learning_path': path_result['path'],
            'path_list': path_result['path_list'],
            'total_cost': path_result['total_cost'],
            'alternative_suitable_courses': [course for course, _ in suitable_courses[:5]],
            'category_courses_count': len(target_courses)
        }

    def get_learning_progression(self, start_courses: List[str], goal_course: str) -> Dict[str, Any]:
        """
        Get a detailed learning progression plan.

        Args:
            start_courses: List of courses already completed
            goal_course: Target course to reach

        Returns:
            Dictionary with detailed progression plan
        """
        # Get the learning path
        path_result = self.find_learning_path(start_courses, goal_course)
        
        if not path_result['success']:
            return {
                'success': False,
                'message': 'No path found to reach the goal course',
                'suggestions': 'Consider taking some prerequisite courses first'
            }

        path_courses = path_result['path_list']
        
        # Calculate course-by-course details
        course_details = []
        for course in path_courses:
            if course in self.course_attributes:
                attr = self.course_attributes[course]
                course_details.append({
                    'course_name': course,
                    'difficulty': attr['difficulty'],
                    'time_hours': attr['time_hours'],
                    'utility': attr['utility'],
                    'prerequisites': self.course_prerequisites[course]
                })

        # Calculate overall metrics
        total_time = sum(detail['time_hours'] for detail in course_details)
        average_difficulty = sum(detail['difficulty'] for detail in course_details) / len(course_details) if course_details else 0
        total_utility = sum(detail['utility'] for detail in course_details)

        return {
            'success': True,
            'path': path_result['path'],
            'course_sequence': path_courses,
            'course_details': course_details,
            'total_time_hours': total_time,
            'average_difficulty': average_difficulty,
            'total_utility': total_utility,
            'estimated_completion_time': f"Approximately {round(total_time / 40)} weeks (assuming 10 hours/week)"
        }

    def assess_learning_style(self, user_responses: Dict[str, Any]) -> LearningStyle:
        """
        Assess user's learning style based on their preferences and responses
        
        Args:
            user_responses: Dictionary containing user preferences and learning style indicators
            
        Returns:
            LearningStyle enum value
        """
        # Extract responses
        time_preference = user_responses.get('time_preference', 'moderate')
        difficulty_tolerance = user_responses.get('difficulty_tolerance', 'medium')
        learning_goal = user_responses.get('learning_goal', 'general')
        
        # Calculate scores for each learning style
        fastest_score = 0
        easiest_score = 0
        challenging_score = 0
        balanced_score = 0
        
        # Time preference affects fastest score
        if time_preference == 'minimum':
            fastest_score += 2
            balanced_score += 1
        elif time_preference == 'maximum':
            easiest_score += 1
        else:  # moderate
            balanced_score += 1
            
        # Difficulty tolerance affects challenging/easiest scores
        if difficulty_tolerance == 'high':
            challenging_score += 2
            balanced_score += 1
        elif difficulty_tolerance == 'low':
            easiest_score += 2
            balanced_score += 1
        else:  # medium
            balanced_score += 2
            
        # Learning goal affects the approach
        if learning_goal == 'career_advancement':
            challenging_score += 1
            balanced_score += 1
        elif learning_goal == 'career_change':
            balanced_score += 1
            easiest_score += 1
        elif learning_goal == 'interest_exploration':
            balanced_score += 1
            
        # Determine the highest score
        scores = {
            LearningStyle.FASTEST: fastest_score,
            LearningStyle.EASIEST: easiest_score,
            LearningStyle.CHALLENGING: challenging_score,
            LearningStyle.BALANCED: balanced_score
        }
        
        return max(scores, key=scores.get)

    def plan_career_path(self, 
                         current_skills: List[str], 
                         target_career: str,
                         time_horizon_months: int = 12) -> Dict[str, Any]:
        """
        Plan a comprehensive career path based on target career and available time
        
        Args:
            current_skills: List of current skills/courses the user has
            target_career: Target career path (e.g., 'Data Scientist', 'Software Engineer')
            time_horizon_months: Time horizon for the career transition (in months)
            
        Returns:
            Dictionary with career path plan
        """
        # Define career requirements based on target career
        career_requirements = {
            'Data Scientist': [
                'Statistics', 'Python Basics', 'Data Analysis', 
                'Machine Learning', 'Data Visualization', 'SQL Basics'
            ],
            'Software Engineer': [
                'Python Basics', 'Data Structures', 'Algorithms', 
                'Web Development', 'Software Engineering', 'Database Systems'
            ],
            'UI/UX Designer': [
                'Graphic Design', 'UI/UX Design', 'User Research', 
                'Interaction Design', 'Prototyping', 'Web Design'
            ],
            'Digital Marketer': [
                'Marketing Fundamentals', 'Digital Marketing', 'Social Media Marketing', 
                'SEO Basics', 'Marketing Analytics', 'Content Marketing'
            ],
            'Product Manager': [
                'Business Fundamentals', 'Product Management', 'Project Management', 
                'User Research', 'Data Analysis', 'Business Strategy'
            ],
            'Cybersecurity Specialist': [
                'Computer Security', 'Network Security', 'Cybersecurity', 
                'Risk Management', 'Ethical Hacking', 'Cryptography'
            ]
        }
        
        # Additional possible careers with their requirements
        career_requirements.update({
            'Full Stack Developer': [
                'Python Basics', 'Web Development', 'Frontend Development', 
                'Backend Development', 'Database Systems', 'API Development'
            ],
            'DevOps Engineer': [
                'Linux', 'Cloud Computing', 'DevOps', 'Docker', 
                'Kubernetes', 'CI/CD Pipelines'
            ],
            'Machine Learning Engineer': [
                'Python Basics', 'Mathematics', 'Statistics', 'Data Structures', 
                'Algorithms', 'Machine Learning', 'Computer Vision'
            ]
        })
        
        if target_career not in career_requirements:
            return {
                'success': False,
                'error': f'Career path for "{target_career}" not available',
                'available_careers': list(career_requirements.keys())
            }
        
        required_courses = career_requirements[target_career]
        # All missing courses from the career requirements
        all_missing_courses = [course for course in required_courses if course not in current_skills]
        # Only those missing courses that we have detailed data for
        known_missing_courses = [course for course in all_missing_courses if course in self.course_attributes]
        
        # Find the best path to acquire missing courses (for those we know about)
        if known_missing_courses:
            # For simplicity, find path to the most complex missing course as an example
            # In a real implementation, we'd plan for all courses
            most_complex_course = max(
                known_missing_courses,
                key=lambda c: self.course_attributes.get(c, {}).get('utility', 0)
            )
            
            path_result = self.find_learning_path(current_skills, most_complex_course)
            
            estimated_completion_time = path_result['total_cost'] * 0.5  # Approximate time per difficulty unit
            
            return {
                'success': path_result['success'],
                'target_career': target_career,
                'required_courses': required_courses,
                'current_skills': current_skills,
                'missing_courses': all_missing_courses,
                'recommended_path': path_result,
                'estimated_completion_time_months': min(estimated_completion_time, time_horizon_months),
                'feasibility': 'high' if len(all_missing_courses) < 4 else 'medium' if len(all_missing_courses) < 8 else 'challenging'
            }
        elif all_missing_courses:
            # There are missing skills, but we don't have course data for them
            return {
                'success': False,
                'target_career': target_career,
                'required_courses': required_courses,
                'current_skills': current_skills,
                'missing_courses': all_missing_courses,
                'error': 'Some required skills do not have course mappings yet, so a detailed path cannot be generated.'
            }
        else:
            return {
                'success': True,
                'target_career': target_career,
                'current_skills': current_skills,
                'missing_courses': [],
                'message': 'You already have all required skills for this career path!',
                'feasibility': 'excellent'
            }

    def get_skill_gap_analysis(self, 
                              current_skills: List[str], 
                              target_skills: List[str]) -> Dict[str, Any]:
        """
        Analyze the gap between current skills and target skills
        
        Args:
            current_skills: List of current skills/courses
            target_skills: List of target skills/courses
            
        Returns:
            Dictionary with skill gap analysis
        """
        current_set = set(current_skills)
        target_set = set(target_skills)
        
        missing_skills = list(target_set - current_set)
        extra_skills = list(current_set - target_set)
        matched_skills = list(current_set & target_set)
        
        # For each missing skill, find the learning path (where possible)
        missing_skills_with_paths = {}
        for skill in missing_skills:
            if skill in self.course_attributes:
                # Find shortest path to this skill
                path_result = self.find_learning_path(current_skills, skill)
                missing_skills_with_paths[skill] = {
                    'path': path_result,
                    'attributes': self.course_attributes[skill],
                    'prerequisites_needed': [
                        p for p in self.course_prerequisites.get(skill, [])
                        if p not in current_skills
                    ]
                }
            else:
                # We don't have course data for this skill, but still include a placeholder
                missing_skills_with_paths[skill] = {
                    'path': {'path': None},
                    'attributes': None,
                    'prerequisites_needed': []
                }
        
        return {
            'success': True,
            'current_skills': current_skills,
            'target_skills': target_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills,
            'matched_skills': matched_skills,
            'missing_skills_with_paths': missing_skills_with_paths,
            'gap_severity': 'low' if len(missing_skills) <= 2 else 
                          'medium' if len(missing_skills) <= 5 else 'high'
        }


# Simple API functions for frontend
def get_learning_path(start_courses: List[str], 
                     goal_course: str, 
                     learning_style: str = "balanced", 
                     algorithm: str = "dijkstra",
                     cost_weights: Optional[Dict[str, float]] = None) -> Dict:
    """
    API function to get learning path with learning style preference
    """
    advisor = EnhancedLearningPathAdvisor()
    style_enum = LearningStyle(learning_style.lower())
    try:
        algorithm_enum = PathfindingAlgorithm(algorithm.lower())
    except ValueError:
        algorithm_enum = PathfindingAlgorithm.DIJKSTRA
    result = advisor.find_learning_path(
        start_courses,
        goal_course,
        learning_style=style_enum,
        algorithm=algorithm_enum,
        cost_weights=cost_weights,
    )

    return result


def get_learning_path_with_alternatives(start_courses: List[str], 
                                       goal_course: str, 
                                       learning_style: str = "balanced",
                                       cost_weights: Optional[Dict[str, float]] = None) -> Dict:
    """
    API function to get learning path with alternatives
    """
    advisor = EnhancedLearningPathAdvisor()
    style_enum = LearningStyle(learning_style.lower())
    result = advisor.get_learning_path_with_alternatives(
        start_courses,
        goal_course,
        learning_style=style_enum,
        cost_weights=cost_weights,
    )

    return result


def get_course_recommendation(completed_courses: List[str], 
                             strategy: str = "meu",
                             risk_tolerance: float = 0.5) -> Dict:
    """
    API function to get course recommendations with decision strategy
    """
    advisor = EnhancedLearningPathAdvisor()
    strategy_enum = DecisionStrategy(strategy.lower().replace(' ', '_'))
    result = advisor.evaluate_learning_options(
        completed_courses,
        decision_strategy=strategy_enum,
        risk_tolerance=risk_tolerance,
    )

    return result


def get_course_details(course_name: str, completed_courses: List[str] = None) -> Dict:
    """
    Get details for a specific course including prerequisite status
    """
    advisor = EnhancedLearningPathAdvisor()

    if completed_courses is None:
        completed_courses = []

    if course_name not in advisor.course_attributes:
        return {
            'success': False,
            'error': f'Course "{course_name}" not found'
        }

    attributes = advisor.course_attributes[course_name]
    prerequisites = advisor.course_prerequisites.get(course_name, [])
    
    # Get prerequisite status
    prereq_status = advisor.get_course_prerequisites_status(course_name, completed_courses)

    return {
        'success': True,
        'course_name': course_name,
        'attributes': attributes,
        'prerequisites': prerequisites,
        'prerequisites_status': prereq_status
    }


def get_learning_progression(start_courses: List[str], goal_course: str) -> Dict:
    """
    Get a detailed learning progression plan
    """
    advisor = EnhancedLearningPathAdvisor()
    result = advisor.get_learning_progression(start_courses, goal_course)

    return result


def get_course_recommendation_sequence(start_courses: List[str], 
                                      goal_course: str, 
                                      learning_style: str = "balanced",
                                      risk_tolerance: float = 0.5,
                                      cost_weights: Optional[Dict[str, float]] = None) -> Dict:
    """
    Get a recommended sequence of courses to reach the goal
    """
    advisor = EnhancedLearningPathAdvisor()
    style_enum = LearningStyle(learning_style.lower())
    result = advisor.recommend_course_sequence(
        start_courses,
        goal_course,
        learning_style=style_enum,
        risk_tolerance=risk_tolerance,
        cost_weights=cost_weights,
    )

    return result


def get_available_courses(completed_courses: List[str]) -> Dict:
    """
    Get courses available to take based on completed prerequisites
    """
    advisor = EnhancedLearningPathAdvisor()
    available = advisor.get_available_courses(completed_courses)

    return {
        'success': True,
        'available_courses': available,
        'completed_courses': completed_courses,
        'count': len(available)
    }


def get_courses_by_category(category: str) -> Dict:
    """
    Get all courses in a specific category
    """
    advisor = EnhancedLearningPathAdvisor()
    courses = advisor.get_courses_by_category(category)
    
    return {
        'success': True,
        'category': category,
        'courses': courses,
        'count': len(courses)
    }


def get_all_categories() -> Dict:
    """
    Get all available course categories
    """
    advisor = EnhancedLearningPathAdvisor()
    categories = advisor.get_all_categories()
    
    return {
        'success': True,
        'categories': categories,
        'count': len(categories)
    }


def get_course_recommendation_by_category(start_courses: List[str], target_category: str) -> Dict:
    """
    Get course recommendation from a specific category based on learning path
    """
    advisor = EnhancedLearningPathAdvisor()
    result = advisor.get_learning_path_by_category(start_courses, target_category)
    
    return result


def get_courses_by_difficulty_range(min_difficulty: int, max_difficulty: int) -> Dict:
    """
    Get courses within a specific difficulty range
    """
    advisor = EnhancedLearningPathAdvisor()
    courses = advisor.get_course_by_difficulty_range(min_difficulty, max_difficulty)
    
    return {
        'success': True,
        'min_difficulty': min_difficulty,
        'max_difficulty': max_difficulty,
        'courses': courses,
        'count': len(courses)
    }


def assess_learning_style(user_responses: Dict[str, Any]) -> Dict:
    """
    Assess user's learning style based on their preferences
    """
    advisor = EnhancedLearningPathAdvisor()
    learning_style = advisor.assess_learning_style(user_responses)

    return {
        'success': True,
        'recommended_learning_style': learning_style.value
    }


def plan_career_path(current_skills: List[str], target_career: str, time_horizon_months: int = 12) -> Dict:
    """
    Plan a comprehensive career path based on target career and available time
    """
    advisor = EnhancedLearningPathAdvisor()
    result = advisor.plan_career_path(current_skills, target_career, time_horizon_months)

    return result


def get_skill_gap_analysis(current_skills: List[str], target_skills: List[str]) -> Dict:
    """
    Analyze the gap between current skills and target skills
    """
    advisor = EnhancedLearningPathAdvisor()
    result = advisor.get_skill_gap_analysis(current_skills, target_skills)

    return result