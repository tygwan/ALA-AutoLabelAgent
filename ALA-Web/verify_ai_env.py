import sys
import os

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"[OK] {module_name}")
        return True
    except ImportError as e:
        print(f"[FAIL] {module_name}: {e}")
        return False

def verify_env():
    print("Verifying AI Environment...")
    print(f"Python: {sys.version}")
    
    checks = [
        "torch",
        "torchvision",
        "autodistill",
        "autodistill_grounded_sam_2",
        "roboflow",
        "supervision",
        "cv2"
    ]
    
    all_pass = True
    for module in checks:
        if not check_import(module):
            all_pass = False
            
    try:
        import torch
        print(f"Torch Version: {torch.__version__}")
        print(f"CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    except:
        pass

    if all_pass:
        print("\nEnvironment looks good!")
    else:
        print("\nSome dependencies are missing. Please run setup_ai_env.bat")

if __name__ == "__main__":
    verify_env()
