import os
from hometask_3 import cap_sentence


class FileCopier:
    def __init__(self):
        pass

    @staticmethod
    def select_file(directory="."):
        files = os.listdir(directory)
        print("Available files:")
        for idx, file in enumerate(files):
            print(f"{idx + 1}. {file}")

        file_index = int(input("Enter number of file you want to copy: ")) - 1
        return os.path.join(directory, files[file_index])

    @staticmethod
    def select_directory():
        directory = input("Enter the path to the directory: ")
        return directory

    @staticmethod
    def select_lines(file_path):
        with open(file_path, 'r', encoding='windows-1252') as file:
            lines = file.readlines()
            print("Number of rows in the file:", len(lines))
            choice = input("Want to copy all rows? (y/n): ")
            if choice.lower() == 'y':
                return lines
            else:
                num_lines = int(input("Enter the number of rows to copy: "))
                return lines[:num_lines]

    @staticmethod
    def copy_to_file(text, output_file):
        try:
            mode = 'a' if os.path.exists(output_file) else 'w'
            with open(output_file, mode, encoding='windows-1252') as file:
                if mode == 'a' and len(text) > 0:
                    # Creating a delimiter only if file has already been created and have text > 1
                    delimiter = '-' * 50
                    file.write('\n' + delimiter + '\n')

                for line in text:
                    capitalized_line = cap_sentence([line])[0]  # Apply the cap_sentence function to each row
                    file.write(capitalized_line)

            print("The text was successfully copied to the file", output_file)
            return True
        except Exception as e:
            print("Error while copying file:", e)
            return False

    def start(self):
        choice = input("Do you want to choose a file from current directory? (y/n): ")
        if choice.lower() == 'y':
            file_path = self.select_file()
        else:
            directory = self.select_directory()
            file_path = self.select_file(directory)

        lines = self.select_lines(file_path)

        output_file = input("Enter the file name where the text will be copied: ")
        if self.copy_to_file(lines, output_file):
            # Deleting the source file only if the data has been successfully copied
            os.remove(file_path)
            print("The original file was successfully deleted.")


copier = FileCopier()
copier.start()
