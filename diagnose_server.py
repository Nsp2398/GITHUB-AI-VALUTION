import subprocess
import time
import requests

def check_server_status():
    print("=== Server Diagnostics ===")
    
    # Check if port 5000 is listening
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
        if ':5000' in result.stdout:
            print("✅ Port 5000 is being used")
        else:
            print("❌ Port 5000 is not listening")
    except:
        print("⚠️ Could not check port status")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test the health endpoint
    print("\n=== Health Endpoint Test ===")
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=5)
        print(f"✅ Health endpoint responded: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
    except requests.exceptions.Timeout:
        print("❌ Server response timeout")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test CORS with a simple request
    print("\n=== CORS Test ===")
    try:
        headers = {
            'Origin': 'http://localhost:5177',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options("http://127.0.0.1:5000/api/files/upload", headers=headers, timeout=5)
        print(f"✅ CORS preflight responded: {response.status_code}")
        print(f"CORS headers: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

if __name__ == "__main__":
    check_server_status()
