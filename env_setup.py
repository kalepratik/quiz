#!/usr/bin/env python3
"""
Environment Setup Script for Google OAuth
Run this script to set up your environment variables
"""

import os
import sys

def create_env_file():
    """Create .env file with Google OAuth credentials"""
    
    env_content = """# Google OAuth Configuration
GOOGLE_CLIENT_ID=1044148804632-ppneakp0mcl08lgk8pl23cj9hs57mhn9.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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

# Flask Configuration
SECRET_KEY=dbt-quiz-secret-key-2024-change-in-production

# For development:
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# For production (uncomment when deploying):
# GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Environment variables configured:")
        print("   - GOOGLE_CLIENT_ID: 1044148804632-ppneakp0mcl08lgk8pl23cj9hs57mhn9.apps.googleusercontent.com")
        print("   - GOOGLE_CLIENT_SECRET: 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")
        print("   - SECRET_KEY: dbt-quiz-secret-key-2024-change-in-production")
        print("   - GOOGLE_REDIRECT_URI: http://localhost:8000/auth/google/callback")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def set_environment_variables():
    """Set environment variables directly"""
    
    env_vars = {
        'GOOGLE_CLIENT_ID': '1044148804632-ppneakp0mcl08lgk8pl23cj9hs57mhn9.apps.googleusercontent.com',
        'GOOGLE_CLIENT_SECRET': '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',
        'SECRET_KEY': 'dbt-quiz-secret-key-2024-change-in-production',
        'GOOGLE_REDIRECT_URI': 'http://localhost:8000/auth/google/callback'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Environment variables set successfully!")
    return True

def main():
    print("🔧 Google OAuth Environment Setup")
    print("=" * 40)
    
    # Try to create .env file first
    if create_env_file():
        print("\n🎉 Setup complete! You can now run your Flask application.")
        print("\n📋 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Start the application: python main.py")
        print("   3. Test OAuth: http://localhost:8000")
    else:
        print("\n⚠️  Could not create .env file. Setting environment variables directly...")
        if set_environment_variables():
            print("\n🎉 Environment variables set! You can now run your Flask application.")
        else:
            print("\n❌ Setup failed. Please set environment variables manually.")

if __name__ == "__main__":
    main()
