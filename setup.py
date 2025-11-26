#!/usr/bin/env python
"""
Setup script for Learning Path Advisor
Handles initial setup including dependency installation and environment configuration
"""
import os
import sys
import subprocess
import shutil

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_section("Checking Python Version")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def create_virtualenv():
    """Create virtual environment if it doesn't exist"""
    print_section("Setting Up Virtual Environment")
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"✓ Virtual environment already exists at {venv_path}")
        return
    
    print(f"Creating virtual environment at {venv_path}...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print(f"✓ Virtual environment created successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        sys.exit(1)

def install_dependencies():
    """Install Python dependencies"""
    print_section("Installing Dependencies")
    
    pip_executable = os.path.join("venv", "Scripts" if os.name == "nt" else "bin", "pip")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    print("Installing packages from requirements.txt...")
    try:
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Setup environment file"""
    print_section("Setting Up Environment")
    
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return
    
    if os.path.exists(".env.example"):
        print("Creating .env file from .env.example...")
        shutil.copy(".env.example", ".env")
        print("✓ .env file created successfully")
        print("⚠ Please review and update .env file with your configuration")
    else:
        print("❌ .env.example not found")

def verify_structure():
    """Verify project structure"""
    print_section("Verifying Project Structure")
    
    required_dirs = [
        "learning-path-advisor/backend",
        "learning-path-advisor/frontend",
        "tests"
    ]
    
    required_files = [
        "requirements.txt",
        "README.md",
        "learning-path-advisor/backend/server.py",
        "learning-path-advisor/frontend/index.html"
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_ok = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_ok = False
    
    if not all_ok:
        print("\n⚠ Some files or directories are missing")
        return False
    
    return True

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Learning Path Advisor - Setup Script")
    print("="*60)
    
    check_python_version()
    
    if not verify_structure():
        print("\n❌ Project structure verification failed")
        sys.exit(1)
    
    create_virtualenv()
    install_dependencies()
    setup_environment()
    
    print_section("Setup Complete!")
    print("✓ All setup tasks completed successfully\n")
    print("Next steps:")
    print("  1. Activate virtual environment:")
    if os.name == "nt":
        print("     venv\\Scripts\\activate")
    else:
        print("     source venv/bin/activate")
    print("  2. Review and update .env file if needed")
    print("  3. Run the application:")
    print("     python run.py")
    print()

if __name__ == "__main__":
    main()
