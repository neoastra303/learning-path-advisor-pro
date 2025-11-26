"""
Admin CLI Tool for Learning Path Advisor Database Management
Manage courses, prerequisites, and database operations
"""
import click
import logging
from tabulate import tabulate
from database import get_db, Database
from db_seed import seed_database, get_seed_status

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Learning Path Advisor Admin CLI"""
    pass

# ============================================================================
# Database Management Commands
# ============================================================================

@cli.group()
def db():
    """Database management commands"""
    pass

@db.command()
def init():
    """Initialize the database"""
    db_instance = get_db()
    click.echo("✅ Database initialized successfully")
    click.echo(f"   Location: {db_instance.db_path}")

@db.command()
def seed():
    """Seed the database with initial courses"""
    db_instance = get_db()
    try:
        seed_database(db_instance)
        click.echo("✅ Database seeded successfully")
        status = get_seed_status(db_instance)
        click.echo(f"   Courses: {status['courses']}")
        click.echo(f"   Prerequisites: {status['prerequisites']}")
    except Exception as e:
        click.echo(f"❌ Error seeding database: {str(e)}", err=True)

@db.command()
def status():
    """Show database status"""
    db_instance = get_db()
    stats = db_instance.get_stats()
    
    data = [
        ["Total Courses", stats['total_courses']],
        ["Total Prerequisites", stats['total_prerequisites']],
        ["Total Users", stats['total_users']],
        ["Saved Learning Paths", stats['total_learning_paths']]
    ]
    
    click.echo("\nDatabase Status:")
    click.echo(tabulate(data, headers=["Metric", "Count"], tablefmt="grid"))

@db.command()
@click.confirmation_option(prompt='Are you sure you want to clear all data?')
def clear():
    """Clear all data from the database"""
    db_instance = get_db()
    db_instance.clear_all_data()
    click.echo("✅ All data cleared")

# ============================================================================
# Course Management Commands
# ============================================================================

@cli.group()
def courses():
    """Course management commands"""
    pass

@courses.command()
def list():
    """List all courses"""
    db_instance = get_db()
    all_courses = db_instance.get_all_courses()
    
    if not all_courses:
        click.echo("No courses found. Seed the database first: admin-cli db seed")
        return
    
    data = []
    for course in all_courses:
        data.append([
            course['name'],
            course['category'],
            course['difficulty'],
            f"{course['time_hours']}h",
            f"{course['utility']}/10"
        ])
    
    click.echo(f"\n{len(all_courses)} Courses Found:\n")
    click.echo(tabulate(data, headers=["Name", "Category", "Difficulty", "Time", "Utility"], tablefmt="grid"))

@courses.command()
@click.option('--category', help='Filter by category')
@click.option('--min-difficulty', type=int, help='Minimum difficulty (1-10)')
@click.option('--max-difficulty', type=int, help='Maximum difficulty (1-10)')
def search(category, min_difficulty, max_difficulty):
    """Search for courses"""
    db_instance = get_db()
    
    results = []
    
    if category:
        results = db_instance.get_courses_by_category(category)
    elif min_difficulty is not None or max_difficulty is not None:
        min_d = min_difficulty or 1
        max_d = max_difficulty or 10
        results = db_instance.get_courses_by_difficulty(min_d, max_d)
    
    if not results:
        click.echo("No courses found matching criteria")
        return
    
    data = []
    for course in results:
        data.append([
            course['name'],
            course['category'],
            course['difficulty'],
            f"{course['time_hours']}h",
            f"{course['utility']}/10"
        ])
    
    click.echo(f"\n{len(results)} Course(s) Found:\n")
    click.echo(tabulate(data, headers=["Name", "Category", "Difficulty", "Time", "Utility"], tablefmt="grid"))

@courses.command()
@click.argument('name')
def info(name):
    """Get detailed information about a course"""
    db_instance = get_db()
    course = db_instance.get_course(name)
    
    if not course:
        click.echo(f"❌ Course '{name}' not found", err=True)
        return
    
    click.echo(f"\n📚 Course: {course['name']}")
    click.echo(f"   Category: {course['category']}")
    click.echo(f"   Difficulty: {course['difficulty']}/10")
    click.echo(f"   Time: {course['time_hours']} hours")
    click.echo(f"   Utility: {course['utility']}/10")
    click.echo(f"   Description: {course['description']}")
    
    prerequisites = db_instance.get_prerequisites(name)
    if prerequisites:
        click.echo(f"   Prerequisites:")
        for prereq in prerequisites:
            click.echo(f"      • {prereq}")
    else:
        click.echo(f"   Prerequisites: None")

@courses.command()
@click.argument('name')
@click.argument('category')
@click.argument('difficulty', type=int)
@click.argument('time_hours', type=float)
@click.argument('utility', type=float)
@click.option('--description', default='', help='Course description')
def add(name, category, difficulty, time_hours, utility, description):
    """Add a new course"""
    if difficulty < 1 or difficulty > 10:
        click.echo("❌ Difficulty must be between 1 and 10", err=True)
        return
    
    db_instance = get_db()
    try:
        db_instance.add_course(name, category, difficulty, time_hours, utility, description)
        click.echo(f"✅ Course '{name}' added successfully")
    except ValueError as e:
        click.echo(f"❌ {str(e)}", err=True)

@courses.command()
@click.argument('name')
def delete(name):
    """Delete a course"""
    db_instance = get_db()
    db_instance.delete_course(name)
    click.echo(f"✅ Course '{name}' deleted")

# ============================================================================
# Prerequisites Management Commands
# ============================================================================

@cli.group()
def prerequisites():
    """Prerequisite management commands"""
    pass

@prerequisites.command()
@click.argument('course')
def list(course):
    """List prerequisites for a course"""
    db_instance = get_db()
    prereqs = db_instance.get_prerequisites(course)
    
    if not prereqs:
        click.echo(f"'{course}' has no prerequisites")
        return
    
    click.echo(f"\nPrerequisites for '{course}':")
    for i, prereq in enumerate(prereqs, 1):
        click.echo(f"  {i}. {prereq}")

@prerequisites.command()
@click.argument('course')
@click.argument('prerequisite')
def add(course, prerequisite):
    """Add a prerequisite to a course"""
    db_instance = get_db()
    try:
        db_instance.add_prerequisite(course, prerequisite)
        click.echo(f"✅ Added '{prerequisite}' as prerequisite for '{course}'")
    except ValueError as e:
        click.echo(f"❌ {str(e)}", err=True)

# ============================================================================
# Category Management Commands
# ============================================================================

@cli.group()
def categories():
    """Category management commands"""
    pass

@categories.command()
def list():
    """List all categories"""
    db_instance = get_db()
    cats = db_instance.get_categories()
    
    if not cats:
        click.echo("No categories found")
        return
    
    click.echo(f"\n{len(cats)} Categories Found:\n")
    for i, cat in enumerate(cats, 1):
        count = len(db_instance.get_courses_by_category(cat))
        click.echo(f"  {i}. {cat} ({count} courses)")

# ============================================================================
# Statistics Commands
# ============================================================================

@cli.command()
def stats():
    """Show database statistics"""
    db_instance = get_db()
    stats = db_instance.get_stats()
    
    # Count by category
    categories = db_instance.get_categories()
    category_counts = []
    for cat in categories:
        count = len(db_instance.get_courses_by_category(cat))
        category_counts.append([cat, count])
    
    click.echo("\n📊 Database Statistics:\n")
    
    # Main stats
    data = [
        ["Total Courses", stats['total_courses']],
        ["Total Prerequisites", stats['total_prerequisites']],
        ["Total Users", stats['total_users']],
        ["Learning Paths Saved", stats['total_learning_paths']]
    ]
    click.echo("Overall:")
    click.echo(tabulate(data, tablefmt="grid"))
    
    # Category breakdown
    if category_counts:
        click.echo("\nCourses by Category:")
        click.echo(tabulate(category_counts, headers=["Category", "Count"], tablefmt="grid"))

# ============================================================================
# Export/Import Commands
# ============================================================================

@cli.group()
def export():
    """Export data commands"""
    pass

@export.command()
@click.option('--format', type=click.Choice(['csv', 'json']), default='csv', help='Export format')
def courses(format):
    """Export all courses"""
    db_instance = get_db()
    all_courses = db_instance.get_all_courses()
    
    if format == 'csv':
        import csv
        filename = 'courses_export.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'category', 'difficulty', 'time_hours', 'utility'])
            writer.writeheader()
            for course in all_courses:
                writer.writerow({
                    'name': course['name'],
                    'category': course['category'],
                    'difficulty': course['difficulty'],
                    'time_hours': course['time_hours'],
                    'utility': course['utility']
                })
        click.echo(f"✅ Exported {len(all_courses)} courses to {filename}")
    
    elif format == 'json':
        import json
        filename = 'courses_export.json'
        data = [{
            'name': c['name'],
            'category': c['category'],
            'difficulty': c['difficulty'],
            'time_hours': c['time_hours'],
            'utility': c['utility']
        } for c in all_courses]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        click.echo(f"✅ Exported {len(all_courses)} courses to {filename}")

# ============================================================================
# Help Command
# ============================================================================

@cli.command()
def help():
    """Show help information"""
    click.echo("""
Learning Path Advisor Admin CLI

Usage:
  admin-cli [COMMAND] [OPTIONS]

Database Commands:
  db init          - Initialize the database
  db seed          - Seed with initial courses
  db status        - Show database statistics
  db clear         - Clear all data (requires confirmation)

Course Commands:
  courses list                          - List all courses
  courses search --category CATEGORY    - Search by category
  courses search --min-difficulty N     - Search by difficulty
  courses info NAME                     - Get course details
  courses add NAME CATEGORY DIFF TIME UTIL - Add a course
  courses delete NAME                   - Delete a course

Prerequisite Commands:
  prerequisites list COURSE             - List prerequisites
  prerequisites add COURSE PREREQUISITE - Add prerequisite

Category Commands:
  categories list                       - List all categories

Other Commands:
  stats           - Show database statistics
  export courses  - Export courses to CSV/JSON

Examples:
  admin-cli db seed
  admin-cli courses list
  admin-cli courses search --category Programming
  admin-cli courses info "Python Basics"
  admin-cli stats
    """)

if __name__ == '__main__':
    cli()
