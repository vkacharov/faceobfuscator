import tkinter as tk
from tkinter import filedialog
from directory_processor import DirectoryProcessor
from utils import load_file_path

class FaceObfuscator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Obfuscator")
        self.root.geometry("400x375")
        self.root.iconbitmap(load_file_path("favicon.ico"))

        self.selected_directory = ""
        self.selected_directory_label = tk.StringVar()
        self.selected_directory_label.set("")

        self.output_directory_label = tk.StringVar()
        self.output_directory_label.set("")

        self.output_directory = ""

        self.processed_images = tk.StringVar()

        self.instruction_label = tk.Label(self.root, text="Изберете директория с необработени снимки")
        self.instruction_label.grid(row=0, column=0)

        self.directory_icon = tk.PhotoImage(file=load_file_path("directory.png"))

        self.select_button = tk.Button(self.root, image=self.directory_icon, command=self.__select_directory, pady=5, borderwidth=0)
        self.select_button.grid(row=0, column=1)

        self.directory_label = tk.Label(self.root, textvariable=self.selected_directory_label, fg="blue", pady=10, wraplength=350)
        self.directory_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")

        self.output_instruction_label = tk.Label(self.root, text="Изберете директория за обработените снимки")
        self.output_instruction_label.grid(row=2, column=0)

        self.output_select_button = tk.Button(self.root,image=self.directory_icon,  command=self.__select_output_directory, pady=5)
        self.output_select_button.grid(row=2, column=1)

        self.output_label = tk.Label(self.root, textvariable=self.output_directory_label, fg="blue", pady=10,  wraplength=350)
        self.output_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        self.process_button = tk.Button(self.root, text="Обработване на снимките", command=self.__process_directory, pady=5)
        self.process_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        self.processed_label = tk.Label(self.root, textvariable=self.processed_images, fg="blue", pady=10, wraplength=350)
        self.processed_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

    def __process_directory(self):
        if (len(self.selected_directory) > 0 and len(self.output_directory) > 0):
            self.processed_images.set("Снимките се обработват ...")
            pi = DirectoryProcessor(self.selected_directory, self.output_directory).process_directory()

            if (len(pi) > 0):
                self.processed_images.set(f"{len(pi)} снимки бяха обработени и записани в {self.output_directory}")

            self.selected_directory = ""
            self.selected_directory_label.set("")
            self.output_directory_label.set("")

    def __select_directory(self):
        dir = filedialog.askdirectory()
        if dir:
            self.selected_directory = dir
            number_of_images = len(DirectoryProcessor.get_image_files_in_directory(self.selected_directory))
            self.selected_directory_label.set(f"{number_of_images} снимки в директория {self.selected_directory}")
            self.processed_images.set("")

    def __select_output_directory(self):
        dir = filedialog.askdirectory()
        if dir:
            self.output_directory = dir
            self.output_directory_label.set(f"Обработените снимки ще се запишат в {self.output_directory}")

    @staticmethod
    def main():
        """Entry point for the application."""
        app = FaceObfuscator()
        app.root.mainloop()