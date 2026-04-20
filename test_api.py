import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_workflow():
    # 1. Add an agent
    agent_data = {
        "name": "DocParser",
        "description": "Extracts structured data from PDFs and images",
        "endpoint": "https://api.example.com/parse"
    }
    print("Testing registration...")
    resp = requests.post(f"{BASE_URL}/agents", json=agent_data)
    print(resp.status_code, resp.json())
    assert resp.status_code == 201
    
    # 2. List agents
    print("\nTesting listing...")
    resp = requests.get(f"{BASE_URL}/agents")
    print(resp.status_code, len(resp.json()))
    assert resp.status_code == 200
    
    # 3. Search
    print("\nTesting search...")
    resp = requests.get(f"{BASE_URL}/search?q=pdf")
    print(resp.status_code, resp.json())
    assert len(resp.json()) > 0
    
    # 4. Log usage
    usage_data = {
        "caller": "AgentA",
        "target": "DocParser",
        "units": 10,
        "request_id": "abc123"
    }
    print("\nTesting usage logging...")
    resp = requests.post(f"{BASE_URL}/usage", json=usage_data)
    print(resp.status_code, resp.json())
    assert resp.status_code == 202
    
    # 5. Test Idempotency (Same request_id)
    print("\nTesting idempotency (sending same request_id again)...")
    resp = requests.post(f"{BASE_URL}/usage", json=usage_data)
    print(resp.status_code, resp.json())
    assert resp.status_code == 202
    
    # 6. Verify Summary (Should be 10, not 20)
    print("\nVerifying summary...")
    resp = requests.get(f"{BASE_URL}/usage-summary")
    summary = resp.json()
    print(summary)
    assert summary.get("DocParser") == 10
    
    # 7. Test error for unknown agent
    bad_usage = {
        "caller": "AgentA",
        "target": "UnknownAgent",
        "units": 5,
        "request_id": "xyz789"
    }
    print("\nTesting unknown agent error...")
    resp = requests.post(f"{BASE_URL}/usage", json=bad_usage)
    print(resp.status_code, resp.json())
    assert resp.status_code == 400

    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_workflow()
