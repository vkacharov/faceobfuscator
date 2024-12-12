from PIL import Image
import io
import os
import boto3
from utils import load_file_path

class ImageProcessor:
    rekognition_client = None

    @classmethod
    def initialize(cls):
        cls.rekognition_client = boto3.client(
            "rekognition", 
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name = os.getenv("AWS_DEFAULT_REGION")
            )
    
    def __init__(self, image_file, output_directory):
        self.image_file = image_file
        self.output_directory = output_directory
        self.bear_image = Image.open(load_file_path("bear.png")).convert("RGBA")

    def obfuscate_image(self):
        with open(self.image_file, "rb") as image_file:
            image_bytes = image_file.read()
            faces = self.__detect_faces(image_bytes)

            raw_image = Image.open(io.BytesIO(image_bytes))
            image = self.__rotate_image(raw_image)

            for face in faces:
                low_age_range = face["AgeRange"]["Low"]
                if (low_age_range <= 18):
                    width, height, left, top = self.__calculate_face_rectangle(image.size, face)
                    resized_bear = self.bear_image.resize((int(width), int(height)))
                    image.paste(resized_bear, (int(left), int(top)), mask=resized_bear)

            file_name = os.path.basename(self.image_file)
            fixed_image_name = self.output_directory + "/" + self.__generate_fixed_file_name(file_name)
            image.save(fixed_image_name)
            return fixed_image_name

    def __generate_fixed_file_name(self, file_name):
        name, ext = os.path.splitext(file_name)
        return f"{name}-fixed{ext}"

    def __detect_faces(self, image):
        response = ImageProcessor.rekognition_client.detect_faces(
            Image={"Bytes" : image}, Attributes=["AGE_RANGE"]
        )
        faces = [face for face in response["FaceDetails"]]
        return faces
    
    def __calculate_face_rectangle(self, image_size, face):
            image_width, image_height = image_size
            rw = face["BoundingBox"]["Width"]
            rh = face["BoundingBox"]["Height"]
            rl = face["BoundingBox"]["Left"]
            rt = face["BoundingBox"]["Top"]
            width, height, left, top = self.__calculate_rectangle(image_width, image_height, rw, rh, rl, rt)
            return (width, height, left, top)
    
    def __calculate_rectangle(self, image_width, image_height, relative_width, relative_height, relative_left, relative_top):
        relative_width = image_width * relative_width
        rectangle_height = image_height * relative_height
        rectangle_left = image_width * relative_left
        rectangle_top = image_height * relative_top
        return (relative_width, rectangle_height, rectangle_left, rectangle_top)
    
    def __rotate_image(self, image):
        rotated_image = image
        exif_data = image._getexif()
        try:
            exif_data = image._getexif()
            if exif_data:
                # Look for the Orientation tag (key 274 in EXIF data)
                for tag, value in exif_data.items():
                    if tag == 274: 
                        if value == 3:
                            rotated_image = image.rotate(180, expand=True)
                        elif value == 6:
                            rotated_image = image.rotate(270, expand=True)
                        elif value == 8:
                            rotated_image = image.rotate(90, expand=True)
                        break
            return rotated_image
        except (AttributeError, KeyError, IndexError):
            pass