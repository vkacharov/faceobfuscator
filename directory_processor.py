import os
import concurrent.futures
from image_processor import ImageProcessor

class DirectoryProcessor:
    def __init__(self, directory, output_directory):
        self.directory = directory
        self.output_directory = output_directory

    def process_directory(self):
        images = DirectoryProcessor.get_image_files_in_directory(self.directory)
        processed_images = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures_to_params = {executor.submit(ImageProcessor(image, self.output_directory).obfuscate_image) : image for image in images}

            for future in concurrent.futures.as_completed(futures_to_params):
                image = futures_to_params[future]
                try:
                    fixed_file_name = future.result()
                    processed_images.append(fixed_file_name)
                except Exception as exc:
                    print(f"An error occurred with {image}: {exc}")
        return processed_images

    @staticmethod
    def get_image_files_in_directory(directory):
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        image_files = [
            os.path.join(directory, file) for file in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file)) and
            os.path.splitext(file)[1].lower() in image_extensions
        ]
        return image_files
        
