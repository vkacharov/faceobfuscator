from utils import load_file_path
from dotenv import load_dotenv
from face_obfuscator import FaceObfuscator
    
# Load dotenv from the correct location
load_success = load_dotenv(load_file_path(".env"))
print(f"dotenv loaded: {load_success}")

if __name__ == "__main__":
    FaceObfuscator.main()