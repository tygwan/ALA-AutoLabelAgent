import requests
import os
import json

API_URL = "http://localhost:8000/api"
SOURCE_DIR = r"C:\Users\user\Desktop\샘플사진\Class_3, traffic cone"
FILES = [
    "AA_2_1_frame_0007_masked.png",
    "AJ_1_6_frame_0003_masked.png",
    "D_10_16_frame_0002_masked.png",
    "L_1_2_frame_0007_masked.png",
    "U_2_1_frame_0003_masked.png"
]

def main():
    # 1. Get Project ID
    print("Fetching projects...")
    try:
        resp = requests.get(f"{API_URL}/projects/list")
        resp.raise_for_status()
        data = resp.json()
        
        if isinstance(data, dict) and "projects" in data:
            projects = data["projects"]
        else:
            projects = data
            
        print(f"Projects found: {len(projects)}")
        
        target_project = next((p for p in projects if p["name"] == "test1"), None)
        
        if not target_project:
            print("Error: Project 'test1' not found. Please create it first.")
            return
            
        project_id = target_project["project_id"]
        print(f"Found project 'test1' with ID: {project_id}")
        
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return

    # 2. Upload Files
    print(f"Uploading {len(FILES)} files from {SOURCE_DIR}...")
    
    files_to_upload = []
    opened_files = []
    
    try:
        for filename in FILES:
            file_path = os.path.join(SOURCE_DIR, filename)
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
                
            f = open(file_path, 'rb')
            opened_files.append(f)
            files_to_upload.append(('files', (filename, f, 'image/png')))
            
        if not files_to_upload:
            print("No files to upload.")
            return

        resp = requests.post(
            f"{API_URL}/upload/batch",
            data={'project_id': project_id},
            files=files_to_upload
        )
        
        if resp.status_code == 200:
            print("Upload successful!")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"Upload failed with status {resp.status_code}")
            print(resp.text)
            
    except Exception as e:
        print(f"Error during upload: {e}")
    finally:
        for f in opened_files:
            f.close()

if __name__ == "__main__":
    main()
