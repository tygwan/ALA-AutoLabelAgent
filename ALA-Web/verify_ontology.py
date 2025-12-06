import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api"

def test_ontology_update():
    print("1. Creating a temporary project...")
    # Create a project first
    project_data = {
        "name": f"test_proj_{uuid.uuid4().hex[:6]}",
        "description": "Temporary project for testing",
        "ontology": {}
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/projects/create", json=project_data)
        if resp.status_code != 200:
            print(f"Failed to create project: {resp.text}")
            return
        
        project = resp.json()
        project_id = project["project_id"]
        print(f"Created project: {project_id}")
        
        print("\n2. Testing Ontology Update (PUT)...")
        new_ontology = {"class_a": "prompt_a", "class_b": "prompt_b"}
        
        # Test PUT request
        resp = requests.put(f"{BASE_URL}/projects/{project_id}/ontology", json=new_ontology)
        
        if resp.status_code == 200:
            print("SUCCESS: Ontology updated successfully via PUT.")
            print(f"Response: {resp.json()}")
        elif resp.status_code == 405:
            print("FAILURE: Method Not Allowed (405). The fix is NOT working.")
        else:
            print(f"FAILURE: Unexpected status code {resp.status_code}")
            print(f"Response: {resp.text}")
            
        # Cleanup (optional, but good practice)
        # requests.delete(f"{BASE_URL}/projects/{project_id}")
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_ontology_update()
