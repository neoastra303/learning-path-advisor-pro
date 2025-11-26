"""
SQLite Database Module for Learning Path Advisor
Manages courses, prerequisites, and user progress
"""
import sqlite3
import json
import os
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class Database:
    """SQLite database interface for Learning Path Advisor"""
    
    DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'learning_path.db')
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """Initialize database connection"""
        self.db_path = db_path
        self.ensure_directory()
        self._init_db()
        logger.info(f"Database initialized at {db_path}")
    
    def ensure_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created database directory: {db_dir}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    difficulty INTEGER NOT NULL CHECK (difficulty >= 1 AND difficulty <= 10),
                    time_hours REAL NOT NULL,
                    utility REAL NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Prerequisites table (many-to-many relationship)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prerequisites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    prerequisite_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                    FOREIGN KEY (prerequisite_id) REFERENCES courses(id) ON DELETE CASCADE,
                    UNIQUE(course_id, prerequisite_id)
                )
            ''')
            
            # User progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    course_id INTEGER NOT NULL,
                    completion_percentage REAL DEFAULT 0,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                )
            ''')
            
            # Learning paths table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_paths (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    start_courses TEXT NOT NULL,
                    goal_course TEXT NOT NULL,
                    learning_style TEXT NOT NULL,
                    path_result TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_courses_category ON courses(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_courses_difficulty ON courses(difficulty)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_prerequisites_course ON prerequisites(course_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_paths_user ON learning_paths(user_id)')
            
            logger.info("Database schema initialized successfully")
    
    def add_course(self, name: str, category: str, difficulty: int, time_hours: float,
                   utility: float, description: str = "") -> int:
        """Add a new course to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO courses (name, category, difficulty, time_hours, utility, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, category, difficulty, time_hours, utility, description))
                course_id = cursor.lastrowid
                logger.info(f"Added course: {name} (ID: {course_id})")
                return course_id
        except sqlite3.IntegrityError:
            logger.warning(f"Course '{name}' already exists")
            raise ValueError(f"Course '{name}' already exists")
    
    def get_course(self, course_name: str) -> Optional[Dict]:
        """Get course details by name"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE name = ?', (course_name,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def get_all_courses(self) -> List[Dict]:
        """Get all courses"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_courses_by_category(self, category: str) -> List[Dict]:
        """Get courses by category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE category = ? ORDER BY name', (category,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_courses_by_difficulty(self, min_diff: int, max_diff: int) -> List[Dict]:
        """Get courses within difficulty range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM courses 
                WHERE difficulty >= ? AND difficulty <= ? 
                ORDER BY difficulty
            ''', (min_diff, max_diff))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT category FROM courses ORDER BY category')
            return [row[0] for row in cursor.fetchall()]
    
    def add_prerequisite(self, course_name: str, prerequisite_name: str):
        """Add a prerequisite relationship"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get course IDs
                cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
                course_row = cursor.fetchone()
                if not course_row:
                    raise ValueError(f"Course '{course_name}' not found")
                
                cursor.execute('SELECT id FROM courses WHERE name = ?', (prerequisite_name,))
                prereq_row = cursor.fetchone()
                if not prereq_row:
                    raise ValueError(f"Prerequisite course '{prerequisite_name}' not found")
                
                cursor.execute('''
                    INSERT INTO prerequisites (course_id, prerequisite_id)
                    VALUES (?, ?)
                ''', (course_row[0], prereq_row[0]))
                logger.info(f"Added prerequisite: {prerequisite_name} → {course_name}")
        except sqlite3.IntegrityError:
            logger.warning(f"Prerequisite already exists: {prerequisite_name} → {course_name}")
    
    def get_prerequisites(self, course_name: str) -> List[str]:
        """Get prerequisites for a course"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c2.name FROM prerequisites p
                JOIN courses c1 ON p.course_id = c1.id
                JOIN courses c2 ON p.prerequisite_id = c2.id
                WHERE c1.name = ?
                ORDER BY c2.name
            ''', (course_name,))
            return [row[0] for row in cursor.fetchall()]
    
    def get_prerequisites_dict(self) -> Dict[str, List[str]]:
        """Get all prerequisites as a dictionary"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c1.name, c2.name FROM prerequisites p
                JOIN courses c1 ON p.course_id = c1.id
                JOIN courses c2 ON p.prerequisite_id = c2.id
                ORDER BY c1.name, c2.name
            ''')
            
            prereqs = {}
            for course, prereq in cursor.fetchall():
                if course not in prereqs:
                    prereqs[course] = []
                prereqs[course].append(prereq)
            
            # Add courses with no prerequisites
            cursor.execute('SELECT name FROM courses ORDER BY name')
            for row in cursor.fetchall():
                course = row[0]
                if course not in prereqs:
                    prereqs[course] = []
            
            return prereqs
    
    def record_user_progress(self, user_id: str, course_name: str, 
                            completion_percentage: float = 100,
                            completed_at: Optional[str] = None):
        """Record user progress on a course"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get course ID
            cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
            course_row = cursor.fetchone()
            if not course_row:
                raise ValueError(f"Course '{course_name}' not found")
            
            course_id = course_row[0]
            
            # Insert or update progress
            cursor.execute('''
                INSERT INTO user_progress (user_id, course_id, completion_percentage, completed_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, course_id) DO UPDATE SET
                    completion_percentage = ?,
                    completed_at = ?,
                    updated_at = CURRENT_TIMESTAMP
            ''', (user_id, course_id, completion_percentage, completed_at,
                  completion_percentage, completed_at))
            logger.info(f"Recorded progress for {user_id}: {course_name} ({completion_percentage}%)")
    
    def get_user_completed_courses(self, user_id: str) -> List[str]:
        """Get list of completed courses for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.name FROM user_progress p
                JOIN courses c ON p.course_id = c.id
                WHERE p.user_id = ? AND p.completion_percentage = 100
                ORDER BY c.name
            ''', (user_id,))
            return [row[0] for row in cursor.fetchall()]
    
    def save_learning_path(self, user_id: str, start_courses: List[str],
                          goal_course: str, learning_style: str, path_result: Dict):
        """Save a learning path calculation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_paths (user_id, start_courses, goal_course, learning_style, path_result)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, json.dumps(start_courses), goal_course, learning_style, json.dumps(path_result)))
            logger.info(f"Saved learning path for {user_id}: {goal_course}")
    
    def get_learning_paths(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent learning paths for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, start_courses, goal_course, learning_style, path_result, created_at
                FROM learning_paths
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            paths = []
            for row in cursor.fetchall():
                paths.append({
                    'id': row[0],
                    'start_courses': json.loads(row[1]),
                    'goal_course': row[2],
                    'learning_style': row[3],
                    'path_result': json.loads(row[4]),
                    'created_at': row[5]
                })
            return paths
    
    def get_course_attributes(self) -> Dict[str, Dict]:
        """Get course attributes for advisor (difficulty, time_hours, utility, category)"""
        attributes = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, difficulty, time_hours, utility, category FROM courses')
            for row in cursor.fetchall():
                attributes[row[0]] = {
                    'difficulty': row[1],
                    'time_hours': row[2],
                    'utility': row[3],
                    'category': row[4]
                }
        return attributes
    
    def count_courses(self) -> int:
        """Count total courses in database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM courses')
            return cursor.fetchone()[0]
    
    def delete_course(self, course_name: str):
        """Delete a course (cascades to prerequisites and progress)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM courses WHERE name = ?', (course_name,))
            if cursor.rowcount > 0:
                logger.info(f"Deleted course: {course_name}")
            else:
                logger.warning(f"Course not found: {course_name}")
    
    def clear_all_data(self):
        """Clear all data from database (for testing)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM learning_paths')
            cursor.execute('DELETE FROM user_progress')
            cursor.execute('DELETE FROM prerequisites')
            cursor.execute('DELETE FROM courses')
            logger.warning("All database data cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM courses')
            course_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM prerequisites')
            prerequisite_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_progress')
            user_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM learning_paths')
            path_count = cursor.fetchone()[0]
            
            return {
                'total_courses': course_count,
                'total_prerequisites': prerequisite_count,
                'total_users': user_count,
                'total_learning_paths': path_count
            }


# Global database instance
_db_instance = None

def get_db(db_path: str = Database.DEFAULT_DB_PATH) -> Database:
    """Get or create global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(db_path)
    return _db_instance

def reset_db():
    """Reset global database instance (for testing)"""
    global _db_instance
    _db_instance = None
