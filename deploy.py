#!/usr/bin/env python3
"""
Quick deployment helper script for Streamlit Patient Queue Simulator
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        for req in requirements:
            if req.strip():
                package = req.split('>=')[0].split('==')[0]
                try:
                    __import__(package.replace('-', '_'))
                except ImportError:
                    print(f"❌ Missing package: {package}")
                    return False
        
        print("✅ All requirements are installed")
        return True
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def test_app():
    """Test the Streamlit app locally"""
    print("🧪 Testing Streamlit app...")
    return run_command("streamlit run Simulator.py --server.headless=true --server.port=8501", "Local app test")

def main():
    """Main deployment helper"""
    print("🚀 Streamlit Patient Queue Simulator - Deployment Helper")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('Simulator.py'):
        print("❌ Simulator.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("📦 Installing requirements...")
        if not run_command("pip install -r requirements.txt", "Install requirements"):
            print("❌ Failed to install requirements. Please install manually.")
            sys.exit(1)
    
    print("\n🎯 Deployment Options:")
    print("1. Streamlit Community Cloud (Recommended - FREE)")
    print("2. Heroku")
    print("3. Railway")
    print("4. Test locally first")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n📋 Streamlit Community Cloud Deployment:")
        print("1. Push your code to GitHub")
        print("2. Go to https://share.streamlit.io")
        print("3. Sign in with GitHub")
        print("4. Click 'New app'")
        print("5. Select your repository")
        print("6. Set main file path: Simulator.py")
        print("7. Click 'Deploy!'")
        
    elif choice == "2":
        print("\n📋 Heroku Deployment:")
        print("1. Install Heroku CLI")
        print("2. Run: heroku create your-app-name")
        print("3. Create Procfile with: web: streamlit run Simulator.py --server.port=$PORT --server.address=0.0.0.0")
        print("4. Run: git push heroku main")
        
    elif choice == "3":
        print("\n📋 Railway Deployment:")
        print("1. Install Railway CLI: npm install -g @railway/cli")
        print("2. Run: railway login")
        print("3. Run: railway init")
        print("4. Run: railway up")
        
    elif choice == "4":
        print("\n🧪 Testing locally...")
        if test_app():
            print("✅ App is working! You can now deploy to any platform.")
        else:
            print("❌ App test failed. Please fix issues before deploying.")
    
    else:
        print("❌ Invalid choice. Please run the script again.")
    
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
