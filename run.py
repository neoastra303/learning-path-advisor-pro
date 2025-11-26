#!/usr/bin/env python
"""
Run script for Learning Path Advisor
Starts the Flask backend server
"""
import os
import sys
import subprocess

def main():
    """Main run function"""
    backend_path = os.path.join("learning-path-advisor", "backend")
    server_file = os.path.join(backend_path, "server.py")
    
    if not os.path.exists(server_file):
        print(f"❌ Error: Server file not found at {server_file}")
        sys.exit(1)
    
    if not os.path.exists(".env"):
        print("⚠ Warning: .env file not found")
        print("   Please run setup.py first or create .env from .env.example")
        sys.exit(1)
    
    print("="*60)
    print("  Starting Learning Path Advisor Server")
    print("="*60)
    print()
    print("Server will be available at: http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)
    print()
    
    original_dir = os.getcwd()
    try:
        os.chdir(backend_path)
        subprocess.run([sys.executable, "server.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
