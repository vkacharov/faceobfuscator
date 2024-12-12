import os
import concurrent.futures
from image_processor import ImageProcessor
import traceback

class DirectoryProcessor:
    def __init__(self, directory, output_directory):
        self.directory = directory
        self.output_directory = output_directory

    def process_directory(self):
        images = DirectoryProcessor.get_image_files_in_directory(self.directory)
        processed_images = []
        exceptions = []

        for image in images:
            try:
                fixed_file_name = ImageProcessor(image, self.output_directory).obfuscate_image()
                processed_images.append(fixed_file_name)
            except Exception as exc:
                traceback.print_exc()
                exceptions.append(f"An error occurred with {image}: {exc}")
        return (exceptions, processed_images)

    @staticmethod
    def get_image_files_in_directory(directory):
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        image_files = [
            os.path.join(directory, file) for file in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file)) and
            os.path.splitext(file)[1].lower() in image_extensions
        ]
        return image_files
        
