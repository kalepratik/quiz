#!/usr/bin/env python3
"""
Main entry point for dbt Certification Quiz Application
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    """Main entry point"""
    print("🎯 dbt Certification Quiz Application")
    print("=" * 40)
    print("1. Start Quiz Server")
    print("2. Manage Questions")
    print("3. Exit")
    print("-" * 40)
    
    while True:
        try:
            choice = input("Select an option (1-3): ").strip()
            
            if choice == '1':
                print("\n🚀 Starting Quiz Server...")
                from core.fast_quiz_server import main as start_server
                start_server()
                break
            elif choice == '2':
                print("\n📚 Question Management")
                print("   Questions are now managed in the Markdown file: data/questions.md")
                print("   You can edit this file directly to add or modify questions.")
                print("   The format follows the structure shown in the existing questions.")
                input("\nPress Enter to continue...")
                continue
            elif choice == '3':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Please enter a valid option (1-3)")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
