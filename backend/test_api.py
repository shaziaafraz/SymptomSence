"""
Python script to test the Flask backend API
Run this script to verify your backend is working correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_test(name):
    """Print test header"""
    print(f"\n{'='*50}")
    print(f"TEST: {name}")
    print(f"{'='*50}")

def print_result(success, message):
    """Print test result"""
    status = "✓ PASS" if success else "✗ FAIL"
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset}: {message}")

def test_health_endpoint():
    """Test health check endpoint"""
    print_test("Health Check Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy' and data.get('model_loaded'):
                print_result(True, "Server is healthy and models are loaded")
                print(f"  Model Loaded: {data.get('model_loaded')}")
                print(f"  TFIDF Loaded: {data.get('tfidf_loaded')}")
                print(f"  Mapping Loaded: {data.get('mapping_loaded')}")
                return True
            else:
                print_result(False, "Health check returned unhealthy status")
                return False
        else:
            print_result(False, f"Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result(False, "Could not connect to server. Make sure Flask is running on port 5000")
        return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    print_test("Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'message' in data and 'endpoints' in data:
                print_result(True, "Root endpoint working correctly")
                print(f"  API Version: {data.get('version')}")
                return True
            else:
                print_result(False, "Root endpoint returned unexpected format")
                return False
        else:
            print_result(False, f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_predict_endpoint():
    """Test prediction endpoint"""
    print_test("Prediction Endpoint")
    
    test_cases = [
        {
            "name": "Simple symptoms",
            "data": {
                "symptoms": "fever headache fatigue",
                "age": 25,
                "gender": "female"
            }
        },
        {
            "name": "Multiple symptoms",
            "data": {
                "symptoms": "cough chest pain difficulty breathing",
                "age": 35,
                "gender": "male"
            }
        },
        {
            "name": "Gastrointestinal symptoms",
            "data": {
                "symptoms": "stomach pain nausea vomiting",
                "age": 28,
                "gender": "female"
            }
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test Case {i}: {test_case['name']}")
        print(f"    Symptoms: '{test_case['data']['symptoms']}'")
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                if 'results' not in data:
                    print_result(False, f"Missing 'results' field in response")
                    all_passed = False
                    continue
                
                results = data['results']
                
                # Check number of results
                if len(results) != 3:
                    print_result(False, f"Expected 3 results, got {len(results)}")
                    all_passed = False
                    continue
                
                # Check each result has required fields
                required_fields = ['disease', 'probability', 'severity', 'medication', 'recommendation', 'description']
                valid = True
                
                for j, result in enumerate(results):
                    for field in required_fields:
                        if field not in result:
                            print_result(False, f"Result {j+1} missing field: {field}")
                            valid = False
                    
                    # Check probability is valid
                    prob = result.get('probability')
                    if not isinstance(prob, (int, float)) or not (0 <= prob <= 1):
                        print_result(False, f"Result {j+1} has invalid probability: {prob}")
                        valid = False
                
                if valid:
                    print_result(True, f"Prediction successful - returned {len(results)} valid diseases")
                    print(f"    Top Prediction: {results[0]['disease']} (Probability: {results[0]['probability']}, Severity: {results[0]['severity']})")
                else:
                    all_passed = False
                    
            else:
                print_result(False, f"Unexpected status code: {response.status_code}")
                print(f"    Response: {response.text}")
                all_passed = False
                
        except Exception as e:
            print_result(False, f"Error: {str(e)}")
            all_passed = False
    
    return all_passed

def test_error_handling():
    """Test error handling"""
    print_test("Error Handling")
    
    # Test 1: Missing symptoms
    print("\n  Test 1: Missing symptoms field")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"age": 25, "gender": "female"},
            timeout=5
        )
        if response.status_code == 400:
            print_result(True, "Correctly returned 400 for missing symptoms")
        else:
            print_result(False, f"Expected 400, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
    
    # Test 2: Empty symptoms
    print("\n  Test 2: Empty symptoms string")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"symptoms": "", "age": 25, "gender": "female"},
            timeout=5
        )
        if response.status_code == 400:
            print_result(True, "Correctly returned 400 for empty symptoms")
        else:
            print_result(False, f"Expected 400, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("Flask Backend API Test Suite")
    print("="*50)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_endpoint()))
    
    if results[0][1]:  # Only continue if health check passed
        results.append(("Root Endpoint", test_root_endpoint()))
        results.append(("Prediction Endpoint", test_predict_endpoint()))
        results.append(("Error Handling", test_error_handling()))
    else:
        print("\n⚠ Skipping other tests - server is not healthy")
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        color = "\033[92m" if result else "\033[91m"
        reset = "\033[0m"
        print(f"{color}{status}{reset}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is working correctly!")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")

