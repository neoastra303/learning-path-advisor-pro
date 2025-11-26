"""
Database Seeding System for Learning Path Advisor
Populates the database with initial course data
"""
import logging
from typing import List, Tuple
from database import get_db, Database

logger = logging.getLogger(__name__)

# Course data: (name, category, difficulty, time_hours, utility, description)
COURSES_DATA = [
    # Computer Science & Programming
    ('Python Basics', 'Programming', 2, 20, 8.5, 'Learn Python fundamentals and syntax'),
    ('Python Intermediate', 'Programming', 4, 30, 8.0, 'Intermediate Python concepts and libraries'),
    ('Data Structures', 'Programming', 5, 35, 9.0, 'Master essential data structures'),
    ('Algorithms', 'Programming', 6, 40, 9.5, 'Algorithm design and optimization'),
    ('Web Development', 'Programming', 5, 45, 8.5, 'Build web applications with Python'),
    ('Database Systems', 'Programming', 4, 25, 8.5, 'Design and manage databases'),
    ('Machine Learning', 'Programming', 7, 50, 9.5, 'ML algorithms and applications'),
    ('Data Science', 'Programming', 7, 55, 9.0, 'Data analysis and visualization'),
    ('Software Engineering', 'Programming', 6, 40, 8.5, 'Best practices in software development'),
    ('DevOps', 'Programming', 6, 35, 8.0, 'Deployment and operations'),
    ('AI Fundamentals', 'Programming', 7, 45, 9.0, 'Introduction to AI concepts'),
    ('Mathematics', 'Programming', 4, 30, 8.0, 'Calculus, linear algebra basics'),
    ('Statistics', 'Programming', 4, 25, 8.5, 'Statistical analysis and probability'),
    ('Data Visualization', 'Programming', 4, 20, 8.0, 'Create effective data visualizations'),
    ('Cloud Computing', 'Programming', 5, 30, 8.5, 'Cloud platforms and services'),
    ('Cybersecurity', 'Programming', 6, 40, 9.0, 'Security principles and practices'),
    ('Mobile Development', 'Programming', 6, 40, 8.0, 'Build mobile applications'),
    ('Game Development', 'Programming', 7, 50, 8.5, 'Create games with game engines'),
    
    # Marketing & Digital Marketing
    ('Marketing Fundamentals', 'Marketing', 2, 15, 7.5, 'Core marketing concepts'),
    ('Digital Marketing', 'Marketing', 3, 20, 8.0, 'Online marketing strategies'),
    ('Social Media Marketing', 'Marketing', 3, 18, 7.5, 'Social media campaigns'),
    ('Content Marketing', 'Marketing', 3, 22, 7.8, 'Create and manage content'),
    ('SEO Basics', 'Marketing', 4, 20, 8.0, 'Search engine optimization'),
    ('Email Marketing', 'Marketing', 3, 15, 7.5, 'Email campaign strategies'),
    ('Marketing Analytics', 'Marketing', 5, 25, 8.5, 'Measure marketing performance'),
    ('Brand Management', 'Marketing', 4, 18, 7.5, 'Build and manage brands'),
    ('Marketing Research', 'Marketing', 4, 25, 8.0, 'Market research methods'),
    ('Influencer Marketing', 'Marketing', 3, 16, 7.5, 'Partner with influencers'),
    ('E-commerce Marketing', 'Marketing', 4, 25, 8.0, 'Online sales strategies'),
    ('Marketing Automation', 'Marketing', 4, 20, 8.0, 'Automate marketing tasks'),
    
    # Business & Management
    ('Business Fundamentals', 'Business', 2, 18, 7.5, 'Core business principles'),
    ('Entrepreneurship', 'Business', 4, 30, 8.0, 'Start and run a business'),
    ('Business Strategy', 'Business', 5, 35, 8.5, 'Strategic planning and execution'),
    ('Operations Management', 'Business', 4, 25, 8.0, 'Manage business operations'),
    ('Financial Management', 'Business', 4, 28, 8.5, 'Finance and budgeting'),
    ('Project Management', 'Business', 4, 25, 8.0, 'Manage projects effectively'),
    ('Business Analytics', 'Business', 5, 30, 8.5, 'Analyze business data'),
    ('Leadership', 'Business', 4, 22, 8.0, 'Leadership skills and styles'),
    ('Human Resources', 'Business', 4, 24, 7.8, 'HR practices and management'),
    ('Business Law', 'Business', 4, 26, 7.5, 'Legal aspects of business'),
    ('International Business', 'Business', 4, 28, 7.8, 'Global business operations'),
    ('Corporate Finance', 'Business', 5, 32, 8.5, 'Advanced finance concepts'),
    ('Business Process Management', 'Business', 4, 24, 8.0, 'Improve business processes'),
    ('Change Management', 'Business', 3, 20, 7.8, 'Manage organizational change'),
    
    # Design & Creative Arts
    ('Graphic Design', 'Design', 4, 30, 8.0, 'Visual design fundamentals'),
    ('UI/UX Design', 'Design', 5, 35, 8.5, 'User interface and experience'),
    ('Web Design', 'Design', 4, 28, 8.0, 'Design websites'),
    ('Digital Illustration', 'Design', 5, 35, 8.0, 'Create digital art'),
    ('Photography', 'Design', 3, 25, 7.5, 'Photography basics'),
    ('Video Editing', 'Design', 4, 30, 8.0, 'Edit video content'),
    ('Animation', 'Design', 6, 40, 8.5, 'Create animations'),
    ('3D Modeling', 'Design', 6, 40, 8.5, '3D design and modeling'),
    ('Motion Graphics', 'Design', 6, 38, 8.5, 'Create motion graphics'),
    ('Color Theory', 'Design', 3, 15, 7.5, 'Color in design'),
    ('Typography', 'Design', 3, 18, 7.8, 'Font and text design'),
    ('Branding', 'Design', 4, 25, 8.0, 'Create brand identities'),
    
    # Data & Analytics
    ('SQL Basics', 'Data Science', 3, 20, 8.0, 'Learn SQL queries'),
    ('Data Analysis', 'Data Science', 5, 28, 8.5, 'Analyze and interpret data'),
    ('Excel Advanced', 'Data Science', 3, 18, 7.5, 'Advanced Excel techniques'),
    ('Business Intelligence', 'Data Science', 6, 35, 8.5, 'BI tools and dashboards'),
    ('Big Data', 'Data Science', 7, 45, 9.0, 'Work with large datasets'),
    ('Advanced Analytics', 'Data Science', 6, 40, 8.5, 'Statistical modeling'),
    
    # Finance
    ('Finance Basics', 'Finance', 3, 20, 7.8, 'Financial principles'),
    ('Accounting Fundamentals', 'Finance', 3, 22, 7.8, 'Basic accounting'),
    ('Investment Strategy', 'Finance', 5, 30, 8.5, 'Investment planning'),
    ('Financial Analysis', 'Finance', 5, 28, 8.5, 'Analyze financial statements'),
    ('Risk Management', 'Finance', 5, 32, 8.5, 'Manage financial risk'),
    
    # Languages
    ('English Writing', 'Languages', 3, 20, 7.5, 'Improve English writing'),
    ('Spanish Basics', 'Languages', 3, 25, 7.5, 'Learn Spanish'),
    ('Spanish Advanced', 'Languages', 4, 30, 7.5, 'Advanced Spanish'),
    ('Mandarin Chinese', 'Languages', 5, 40, 7.5, 'Learn Mandarin'),
    
    # Health & Wellness
    ('Nutrition Basics', 'Health', 2, 15, 7.5, 'Nutrition fundamentals'),
    ('Fitness Training', 'Health', 3, 20, 7.8, 'Physical fitness'),
    ('Mental Health', 'Health', 3, 18, 7.8, 'Mental wellness'),
    ('Wellness Coaching', 'Health', 4, 25, 8.0, 'Health coaching skills'),
]

# Prerequisites data: (course_name, prerequisite_name)
PREREQUISITES_DATA = [
    # Programming prerequisites
    ('Python Intermediate', 'Python Basics'),
    ('Data Structures', 'Python Intermediate'),
    ('Algorithms', 'Data Structures'),
    ('Machine Learning', 'Data Structures'),
    ('Machine Learning', 'Algorithms'),
    ('Data Science', 'Machine Learning'),
    ('Data Science', 'Database Systems'),
    ('Web Development', 'Python Intermediate'),
    ('Software Engineering', 'Algorithms'),
    ('Software Engineering', 'Web Development'),
    ('DevOps', 'Web Development'),
    ('DevOps', 'Database Systems'),
    ('AI Fundamentals', 'Data Structures'),
    ('AI Fundamentals', 'Algorithms'),
    ('Statistics', 'Mathematics'),
    ('Data Visualization', 'Python Intermediate'),
    ('Data Visualization', 'Statistics'),
    ('Cloud Computing', 'Web Development'),
    ('Cloud Computing', 'DevOps'),
    ('Cybersecurity', 'Software Engineering'),
    ('Mobile Development', 'Web Development'),
    ('Game Development', 'Algorithms'),
    ('Game Development', 'Mathematics'),
    
    # Marketing prerequisites
    ('Digital Marketing', 'Marketing Fundamentals'),
    ('Social Media Marketing', 'Marketing Fundamentals'),
    ('Content Marketing', 'Marketing Fundamentals'),
    ('SEO Basics', 'Digital Marketing'),
    ('Email Marketing', 'Digital Marketing'),
    ('Marketing Analytics', 'Statistics'),
    ('Marketing Analytics', 'Digital Marketing'),
    ('Brand Management', 'Marketing Fundamentals'),
    ('Marketing Research', 'Marketing Fundamentals'),
    ('Marketing Research', 'Statistics'),
    ('Influencer Marketing', 'Social Media Marketing'),
    ('E-commerce Marketing', 'Digital Marketing'),
    ('E-commerce Marketing', 'Web Development'),
    ('Marketing Automation', 'Email Marketing'),
    ('Marketing Automation', 'Digital Marketing'),
    
    # Business prerequisites
    ('Entrepreneurship', 'Business Fundamentals'),
    ('Business Strategy', 'Business Fundamentals'),
    ('Operations Management', 'Business Fundamentals'),
    ('Financial Management', 'Business Fundamentals'),
    ('Project Management', 'Business Fundamentals'),
    ('Business Analytics', 'Statistics'),
    ('Business Analytics', 'Business Fundamentals'),
    ('Leadership', 'Business Fundamentals'),
    ('Human Resources', 'Business Fundamentals'),
    ('Business Law', 'Business Fundamentals'),
    ('International Business', 'Business Fundamentals'),
    ('Corporate Finance', 'Financial Management'),
    ('Business Process Management', 'Operations Management'),
    ('Change Management', 'Leadership'),
    
    # Design prerequisites
    ('UI/UX Design', 'Graphic Design'),
    ('Web Design', 'Graphic Design'),
    ('Digital Illustration', 'Graphic Design'),
    ('Video Editing', 'Photography'),
    ('Animation', 'Digital Illustration'),
    ('3D Modeling', 'Animation'),
    ('Motion Graphics', 'Animation'),
    ('Motion Graphics', 'Video Editing'),
    ('Color Theory', 'Graphic Design'),
    ('Typography', 'Graphic Design'),
    ('Branding', 'Graphic Design'),
    ('Branding', 'Marketing Fundamentals'),
    
    # Data & Analytics prerequisites
    ('SQL Basics', 'Database Systems'),
    ('Data Analysis', 'Statistics'),
    ('Data Analysis', 'SQL Basics'),
    ('Excel Advanced', 'Statistics'),
    ('Business Intelligence', 'Data Analysis'),
    ('Business Intelligence', 'Business Analytics'),
    ('Big Data', 'Data Science'),
    ('Big Data', 'Statistics'),
    ('Advanced Analytics', 'Data Analysis'),
    
    # Finance prerequisites
    ('Accounting Fundamentals', 'Finance Basics'),
    ('Investment Strategy', 'Finance Basics'),
    ('Financial Analysis', 'Accounting Fundamentals'),
    ('Risk Management', 'Financial Analysis'),
    
    # Languages prerequisites
    ('Spanish Advanced', 'Spanish Basics'),
]


def seed_database(db: Database = None):
    """Seed the database with initial data"""
    if db is None:
        db = get_db()
    
    logger.info("Starting database seeding...")
    
    # Check if already seeded
    if db.count_courses() > 0:
        logger.warning("Database already contains courses. Skipping seed.")
        return False
    
    try:
        # Add all courses
        logger.info(f"Adding {len(COURSES_DATA)} courses...")
        for course_name, category, difficulty, time_hours, utility, description in COURSES_DATA:
            db.add_course(course_name, category, difficulty, time_hours, utility, description)
        
        # Add all prerequisites
        logger.info(f"Adding {len(PREREQUISITES_DATA)} prerequisites...")
        for course_name, prerequisite_name in PREREQUISITES_DATA:
            db.add_prerequisite(course_name, prerequisite_name)
        
        # Get stats
        stats = db.get_stats()
        logger.info(f"Database seeding complete. Stats: {stats}")
        return True
        
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        raise


def get_seed_status(db: Database = None) -> dict:
    """Get database seeding status"""
    if db is None:
        db = get_db()
    
    stats = db.get_stats()
    return {
        'seeded': stats['total_courses'] > 0,
        'courses': stats['total_courses'],
        'prerequisites': stats['total_prerequisites'],
        'expected_courses': len(COURSES_DATA),
        'expected_prerequisites': len(PREREQUISITES_DATA)
    }


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Seed the database
    db = get_db()
    seed_database(db)
    
    # Print status
    status = get_seed_status(db)
    print("\nDatabase Seeding Status:")
    print(f"  Courses: {status['courses']}/{status['expected_courses']}")
    print(f"  Prerequisites: {status['prerequisites']}/{status['expected_prerequisites']}")
    print(f"  Seeded: {status['seeded']}")
