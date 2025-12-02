#!/usr/bin/env python3
"""
Main entry point for dbt Certification Quiz Application (Development)
"""

import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for development"""
    print("🎯 dbt Certification Quiz Application")
    print("=" * 40)
    print("1. Start Quiz Server (Local Development)")
    print("2. Run Tests")
    print("3. Manage Questions")
    print("4. Exit")
    print("-" * 40)
    
    while True:
        try:
            choice = input("Select an option (1-4): ").strip()
            
            if choice == '1':
                print("\n🚀 Starting Quiz Server for Local Development...")
                print("   Live version available at: https://dbt-certification-quiz.onrender.com/")
                from backend import create_app
                app = create_app()
                app.run(host='0.0.0.0', port=8000, debug=True)
                break
            elif choice == '2':
                print("\n🧪 Running Tests...")
                import subprocess
                subprocess.run([sys.executable, "-m", "pytest", "backend/tests/", "-v"])
                break
            elif choice == '3':
                print("\n📚 Question Management")
                print("   Questions are now managed in the Markdown file: backend/data/questions.md")
                print("   You can edit this file directly to add or modify questions.")
                print("   The format follows the structure shown in the existing questions.")
                input("\nPress Enter to continue...")
                continue
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Please enter a valid option (1-4)")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
