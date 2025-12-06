import requests
import json
import uuid
import os

BASE_URL = "http://localhost:8000/api"

def print_step(step):
    print(f"\n{'='*50}\n{step}\n{'='*50}")

def test_all():
    print_step("STARTING COMPREHENSIVE FEATURE TEST")
    
    # 1. Create Project
    print_step("1. Testing Project Creation")
    project_name = f"test_feat_{uuid.uuid4().hex[:6]}"
    project_data = {
        "name": project_name,
        "description": "Feature test project",
        "ontology": {}
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/projects/create", json=project_data)
        if resp.status_code != 200:
            print(f"FAIL: Create project failed: {resp.text}")
            return
        project = resp.json()
        project_id = project["project_id"]
        print(f"SUCCESS: Created project {project_id} ({project_name})")
    except Exception as e:
        print(f"FAIL: Create project exception: {e}")
        return

    # 2. List Projects
    print_step("2. Testing Project List")
    try:
        resp = requests.get(f"{BASE_URL}/projects/list")
        projects = resp.json()
        # Handle list vs dict response (we fixed frontend to handle list, backend returns list)
        if isinstance(projects, dict) and "projects" in projects:
            projects = projects["projects"]
        
        found = any(p["project_id"] == project_id for p in projects)
        if found:
            print(f"SUCCESS: Project {project_id} found in list")
        else:
            print(f"FAIL: Project {project_id} NOT found in list")
    except Exception as e:
        print(f"FAIL: List projects exception: {e}")

    # 3. Update Ontology
    print_step("3. Testing Ontology Update")
    new_ontology = {"test_class": "test_prompt"}
    try:
        resp = requests.put(f"{BASE_URL}/projects/{project_id}/ontology", json=new_ontology)
        if resp.status_code == 200:
            print("SUCCESS: Ontology updated")
        else:
            print(f"FAIL: Ontology update failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"FAIL: Ontology update exception: {e}")

    # 4. File Upload (Mock)
    print_step("4. Testing File Upload")
    # Create a dummy file
    dummy_filename = "test_upload.txt"
    with open(dummy_filename, "w") as f:
        f.write("dummy content")
    
    try:
        with open(dummy_filename, "rb") as f:
            files = [('files', (dummy_filename, f, 'text/plain'))]
            data = {'project_id': project_id}
            resp = requests.post(f"{BASE_URL}/upload/batch", data=data, files=files)
            
        if resp.status_code == 200:
            print("SUCCESS: File uploaded")
        else:
            print(f"FAIL: File upload failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"FAIL: File upload exception: {e}")
    finally:
        if os.path.exists(dummy_filename):
            os.remove(dummy_filename)

    # 5. Auto-Annotate (Expect 500 if env broken, 200 if fixed)
    print_step("5. Testing Auto-Annotation Trigger")
    # We need a valid file ID for this, but we just uploaded a text file which might fail image processing.
    # Let's just check if the endpoint is reachable and returns a specific error (not 404).
    annotate_req = {
        "file_id": "non_existent_file",
        "ontology": {"a": "b"},
        "save_visualization": False
    }
    try:
        resp = requests.post(f"{BASE_URL}/annotate/auto-annotate", json=annotate_req)
        print(f"Response Status: {resp.status_code}")
        print(f"Response Text: {resp.text}")
        
        if resp.status_code == 503:
             print("INFO: AI Service Unavailable (Expected if setup_ai_env.bat not run)")
        elif resp.status_code == 500:
             print("INFO: Internal Server Error (Likely AI env broken or file not found)")
        elif resp.status_code == 404:
             print("SUCCESS: Endpoint reached (File not found expected)")
        else:
             print(f"INFO: Endpoint returned {resp.status_code}")

    except Exception as e:
        print(f"FAIL: Auto-annotate exception: {e}")

    # 6. Delete Project
    print_step("6. Testing Project Deletion")
    try:
        resp = requests.delete(f"{BASE_URL}/projects/{project_id}")
        if resp.status_code == 200:
            print("SUCCESS: Project deleted")
        else:
            print(f"FAIL: Project deletion failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"FAIL: Project deletion exception: {e}")

    print_step("TEST COMPLETE")

if __name__ == "__main__":
    test_all()
