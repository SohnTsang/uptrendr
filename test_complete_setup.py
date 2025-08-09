#!/usr/bin/env python3
"""
UPTRENDR COMPLETE SETUP VALIDATION SCRIPT
==========================================

This script comprehensively tests your Uptrendr ML Pipeline setup to ensure:
1. Project configuration is correct (uptrendr-jp)
2. Firebase connectivity works
3. API endpoints are accessible
4. Data pipeline functions work
5. All configurations match your current project

Usage: python test_complete_setup.py
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class UptrendrSetupValidator:
    def __init__(self):
        self.project_id = "uptrendr-jp"
        self.project_number = "626448778297"
        self.region = "asia-northeast1"
        self.api_base_url = f"https://{self.project_id}.{self.region}.run.app"
        
        # Alternative API URL patterns to check
        self.api_url_patterns = [
            f"https://uptrendr-api-{self.project_number}.{self.region}.run.app",  # Actual working URL
            f"https://{self.project_id}.{self.region}.run.app",
            f"https://{self.project_id}-{self.project_number}.{self.region}.run.app",
            f"https://uptrendr-{self.project_number}.{self.region}.run.app"
        ]
        
        self.test_results = {}
        
    def print_header(self, text: str) -> None:
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"🔧 {text}")
        print(f"{'='*60}")
        
    def print_test_result(self, test_name: str, passed: bool, details: str = "") -> None:
        """Print test result with emoji"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results[test_name] = {"passed": passed, "details": details}
        
    def check_project_configuration(self) -> bool:
        """Test 1: Verify project configuration"""
        self.print_header("PROJECT CONFIGURATION VALIDATION")
        
        all_passed = True
        
        # Check GoogleService-Info.plist
        try:
            plist_path = "Uptrendr/Uptrendr/Resources/GoogleService-Info.plist"
            if os.path.exists(plist_path):
                with open(plist_path, 'r') as f:
                    content = f.read()
                    has_correct_project = f"<string>{self.project_id}</string>" in content
                    has_correct_number = f"<string>{self.project_number}</string>" in content
                    
                    self.print_test_result(
                        "GoogleService-Info.plist Project ID",
                        has_correct_project,
                        f"Project ID: {self.project_id}" if has_correct_project else "Wrong project ID found"
                    )
                    
                    self.print_test_result(
                        "GoogleService-Info.plist Project Number", 
                        has_correct_number,
                        f"Project Number: {self.project_number}" if has_correct_number else "Wrong project number found"
                    )
                    
                    all_passed = all_passed and has_correct_project and has_correct_number
            else:
                self.print_test_result("GoogleService-Info.plist exists", False, "File not found")
                all_passed = False
                
        except Exception as e:
            self.print_test_result("GoogleService-Info.plist check", False, str(e))
            all_passed = False
            
        # Check deployment scripts
        script_files = ["deploy_ml_pipeline.sh", "DEPLOYMENT_GUIDE.md"]
        for script_file in script_files:
            if os.path.exists(script_file):
                try:
                    with open(script_file, 'r') as f:
                        content = f.read()
                        has_correct_project = self.project_id in content
                        has_old_project = "uptrendr-api-620356694660" in content
                        
                        self.print_test_result(
                            f"{script_file} project configuration",
                            has_correct_project and not has_old_project,
                            f"Contains {self.project_id}: {has_correct_project}, Contains old project: {has_old_project}"
                        )
                        
                        all_passed = all_passed and has_correct_project and not has_old_project
                except Exception as e:
                    self.print_test_result(f"{script_file} check", False, str(e))
                    all_passed = False
                    
        return all_passed
        
    def check_firebase_connection(self) -> bool:
        """Test 2: Check Firebase connectivity"""
        self.print_header("FIREBASE CONNECTIVITY TEST")
        
        try:
            # Try to import Firebase modules
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            self.print_test_result("Firebase Admin SDK import", True, "Successfully imported")
            
            # Try to initialize Firebase (this might fail if already initialized)
            try:
                # Check if already initialized
                app = firebase_admin.get_app()
                self.print_test_result("Firebase App status", True, "App already initialized")
            except ValueError:
                # Not initialized, try to initialize
                try:
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred)
                    self.print_test_result("Firebase initialization", True, "Successfully initialized")
                except Exception as e:
                    self.print_test_result("Firebase initialization", False, str(e))
                    return False
            
            # Test Firestore connection
            try:
                db = firestore.Client()
                # Try a simple read operation
                test_ref = db.collection('test').document('connection_test')
                test_ref.set({'timestamp': datetime.now(timezone.utc), 'test': True})
                
                # Try to read it back
                doc = test_ref.get()
                if doc.exists:
                    self.print_test_result("Firestore read/write test", True, "Successfully read and wrote test document")
                    # Clean up
                    test_ref.delete()
                    return True
                else:
                    self.print_test_result("Firestore read test", False, "Could not read test document")
                    return False
                    
            except Exception as e:
                self.print_test_result("Firestore connection", False, str(e))
                return False
                
        except ImportError as e:
            self.print_test_result("Firebase SDK availability", False, f"Import error: {e}")
            return False
        except Exception as e:
            self.print_test_result("Firebase connection test", False, str(e))
            return False
            
    def check_api_endpoints(self) -> Tuple[bool, str]:
        """Test 3: Check API endpoints"""
        self.print_header("API ENDPOINTS VALIDATION")
        
        working_url = None
        
        for url_pattern in self.api_url_patterns:
            try:
                print(f"🔍 Testing: {url_pattern}")
                response = requests.get(f"{url_pattern}/", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.print_test_result(
                        f"API endpoint {url_pattern}",
                        True,
                        f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
                    )
                    working_url = url_pattern
                    break
                else:
                    self.print_test_result(
                        f"API endpoint {url_pattern}",
                        False,
                        f"Status: {response.status_code}"
                    )
                    
            except requests.exceptions.RequestException as e:
                self.print_test_result(
                    f"API endpoint {url_pattern}",
                    False,
                    f"Connection error: {str(e)}"
                )
                
        if working_url:
            return True, working_url
        else:
            return False, None
            
    def test_api_functions(self, base_url: str) -> bool:
        """Test 4: Test specific API functions"""
        self.print_header("API FUNCTIONS TESTING")
        
        test_endpoints = [
            {"path": "/", "method": "GET", "name": "Health Check"},
            {"path": "/test-firebase", "method": "GET", "name": "Firebase Test"},
            {"path": "/test-japanese-apis", "method": "GET", "name": "Japanese APIs Test"},
            {"path": "/market-data", "method": "GET", "name": "Market Data"},
        ]
        
        all_passed = True
        
        for endpoint in test_endpoints:
            try:
                url = f"{base_url}{endpoint['path']}"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.print_test_result(
                            endpoint['name'],
                            True,
                            f"Status: {response.status_code}, Response received"
                        )
                    except:
                        self.print_test_result(
                            endpoint['name'],
                            True,
                            f"Status: {response.status_code}, Non-JSON response"
                        )
                else:
                    self.print_test_result(
                        endpoint['name'],
                        False,
                        f"Status: {response.status_code}"
                    )
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.print_test_result(
                    endpoint['name'],
                    False,
                    f"Request error: {str(e)}"
                )
                all_passed = False
                
        return all_passed
        
    def check_deployment_status(self) -> bool:
        """Test 5: Check deployment status"""
        self.print_header("DEPLOYMENT STATUS CHECK")
        
        try:
            # Check if gcloud is available
            result = subprocess.run(['gcloud', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.print_test_result("Google Cloud SDK", True, "Available")
            else:
                self.print_test_result("Google Cloud SDK", False, "Not available")
                return False
                
            # Check current project
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                current_project = result.stdout.strip()
                is_correct = current_project == self.project_id
                self.print_test_result(
                    "Current GCloud Project",
                    is_correct,
                    f"Current: {current_project}, Expected: {self.project_id}"
                )
                
                if not is_correct:
                    print(f"💡 To fix: gcloud config set project {self.project_id}")
                    
                return is_correct
            else:
                self.print_test_result("GCloud project check", False, "Could not get current project")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_test_result("GCloud commands", False, "Commands timed out")
            return False
        except FileNotFoundError:
            self.print_test_result("Google Cloud SDK", False, "gcloud command not found")
            return False
        except Exception as e:
            self.print_test_result("Deployment status check", False, str(e))
            return False
            
    def generate_summary_report(self) -> None:
        """Generate final summary report"""
        self.print_header("VALIDATION SUMMARY REPORT")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['passed'])
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {total_tests - passed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print(f"\n🎉 ALL TESTS PASSED! Your Uptrendr setup is ready!")
            print(f"🚀 Your API should be available at one of these URLs:")
            for url in self.api_url_patterns:
                print(f"   • {url}")
        else:
            print(f"\n⚠️  SOME TESTS FAILED. Please review the failed tests above.")
            
            # Provide specific recommendations
            print(f"\n💡 RECOMMENDATIONS:")
            
            failed_tests = [name for name, result in self.test_results.items() if not result['passed']]
            
            if any("project configuration" in test.lower() for test in failed_tests):
                print(f"   🔧 Update project configuration to use {self.project_id}")
                print(f"   📝 Run: gcloud config set project {self.project_id}")
                
            if any("firebase" in test.lower() for test in failed_tests):
                print(f"   🔥 Check Firebase setup and authentication")
                print(f"   📝 Run: firebase login && firebase use {self.project_id}")
                
            if any("api" in test.lower() for test in failed_tests):
                print(f"   🌐 Deploy your Cloud Functions")
                print(f"   📝 Run: firebase deploy --only functions")
                
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅" if result['passed'] else "❌"
            print(f"   {status} {test_name}")
            if result['details']:
                print(f"      → {result['details']}")
                
    def run_all_tests(self) -> bool:
        """Run all validation tests"""
        print("🚀 UPTRENDR COMPLETE SETUP VALIDATION")
        print("=====================================")
        print(f"📅 Started at: {datetime.now()}")
        print(f"🎯 Target Project: {self.project_id}")
        print(f"🔢 Project Number: {self.project_number}")
        
        # Test 1: Project Configuration
        config_ok = self.check_project_configuration()
        
        # Test 2: Firebase Connection  
        firebase_ok = self.check_firebase_connection()
        
        # Test 3: API Endpoints
        api_ok, working_url = self.check_api_endpoints()
        
        # Test 4: API Functions (only if we have a working URL)
        functions_ok = True
        if working_url:
            functions_ok = self.test_api_functions(working_url)
        else:
            self.print_test_result("API Functions Test", False, "No working API URL found")
            functions_ok = False
            
        # Test 5: Deployment Status
        deployment_ok = self.check_deployment_status()
        
        # Generate summary
        self.generate_summary_report()
        
        return all([config_ok, firebase_ok, api_ok, functions_ok, deployment_ok])

def main():
    """Main function"""
    try:
        validator = UptrendrSetupValidator()
        success = validator.run_all_tests()
        
        if success:
            print(f"\n🎉 SUCCESS: Your Uptrendr ML Pipeline is fully configured and ready!")
            sys.exit(0)
        else:
            print(f"\n⚠️  ISSUES FOUND: Please address the failed tests above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Validation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        logger.exception("Full error details:")
        sys.exit(1)

if __name__ == "__main__":
    main()
