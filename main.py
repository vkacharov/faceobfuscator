from utils import load_file_path
from dotenv import load_dotenv
from face_obfuscator import FaceObfuscator
import boto3
    
# Load dotenv from the correct location
load_success = load_dotenv(load_file_path(".env"))
print(f"dotenv loaded: {load_success}")
rekognition_client = boto3.client("rekognition", region_name="us-east-1")

if __name__ == "__main__":
    FaceObfuscator.main(rekognition_client)