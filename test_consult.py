import requests
import json

def test_consult():
    url = "http://localhost:5000/consult"
    payload = {
        "question": "Analisis investasi bank saat ini",
        "user_id": "test_user"
    }
    
    try:
        print(f"Sending POST to {url}...")
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("\n=== AI RESPONSE CHECK ===")
            resp_json = response.json()
            print("Response Message:", resp_json.get("response", "No response field"))
            print("=========================\n")
        else:
            print("Error Response:", response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_consult()
