#!/usr/bin/env python3
"""
Simple test script for CLO835 Final Project
Tests basic application functionality
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        import pymysql
        import boto3
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    try:
        from app import DBHOST, DBUSER, DBPWD, DATABASE, DBPORT, BACKGROUND_IMAGE_URL, MY_NAME
        print(f"✅ Environment variables loaded:")
        print(f"   DBHOST: {DBHOST}")
        print(f"   DBUSER: {DBUSER}")
        print(f"   DATABASE: {DATABASE}")
        print(f"   DBPORT: {DBPORT}")
        print(f"   BACKGROUND_IMAGE_URL: {BACKGROUND_IMAGE_URL}")
        print(f"   MY_NAME: {MY_NAME}")
        return True
    except Exception as e:
        print(f"❌ Environment variable error: {e}")
        return False

def test_templates():
    """Test if all templates exist"""
    templates = [
        'templates/addemp.html',
        'templates/about.html',
        'templates/addempoutput.html',
        'templates/getemp.html',
        'templates/getempoutput.html',
        'templates/error.html'
    ]
    
    missing_templates = []
    for template in templates:
        if not os.path.exists(template):
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ Missing templates: {missing_templates}")
        return False
    else:
        print("✅ All templates exist")
        return True

def test_dockerfile():
    """Test if Dockerfile exists and has correct port"""
    if not os.path.exists('Dockerfile'):
        print("❌ Dockerfile not found")
        return False
    
    with open('Dockerfile', 'r') as f:
        content = f.read()
        if 'EXPOSE 81' in content:
            print("✅ Dockerfile exists and exposes port 81")
            return True
        else:
            print("❌ Dockerfile doesn't expose port 81")
            return False

def test_requirements():
    """Test if requirements.txt exists and has required packages"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
        required_packages = ['Flask', 'pymysql', 'boto3']
        missing_packages = []
        
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages in requirements.txt: {missing_packages}")
            return False
        else:
            print("✅ All required packages in requirements.txt")
            return True

def main():
    """Run all tests"""
    print("🧪 Running CLO835 Final Project Tests...\n")
    
    tests = [
        test_imports,
        test_app_creation,
        test_environment_variables,
        test_templates,
        test_dockerfile,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 