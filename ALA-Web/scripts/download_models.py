import os
import subprocess
import sys
import urllib.request
from pathlib import Path

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_file(url, dest_path):
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Downloaded to {dest_path}")

def main():
    print("========================================")
    print("  ALA-Web AI Model Downloader")
    print("========================================")

    # Define paths
    base_dir = Path(__file__).parent.parent
    backend_dir = base_dir / "backend"
    lib_dir = backend_dir / "lib"
    cache_dir = lib_dir / "cache"
    
    # Create directories
    lib_dir.mkdir(exist_ok=True)
    cache_dir.mkdir(exist_ok=True)

    # 1. Install SAM2
    print("\n[1/3] Setting up SAM2...")
    sam2_dir = lib_dir / "sam2"
    if not sam2_dir.exists():
        print("Cloning SAM2 repository...")
        subprocess.run(["git", "clone", "https://github.com/facebookresearch/segment-anything-2.git", str(sam2_dir)], check=True)
    else:
        print("SAM2 repository already exists.")

    # 2. Download Checkpoint
    print("\n[2/3] Downloading SAM2 Checkpoint...")
    checkpoint_url = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt"
    checkpoint_path = cache_dir / "sam2_hiera_base_plus.pt"
    
    if not checkpoint_path.exists():
        download_file(checkpoint_url, checkpoint_path)
    else:
        print("Checkpoint already exists.")

    # 3. Install Python Packages
    print("\n[3/3] Installing AI Packages...")
    try:
        install_package("autodistill-grounded-sam-2")
        install_package("autodistill-florence-2")
        print("Packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")
        print("You may need to install them manually.")

    print("\n========================================")
    print("  AI Model Setup Complete!")
    print("========================================")

if __name__ == "__main__":
    main()
