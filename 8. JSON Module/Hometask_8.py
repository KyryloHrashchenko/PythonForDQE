import os
import json


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
                    delimiter = '-' * 50
                    file.write('\n' + delimiter + '\n')
                if isinstance(text, list):  # Check if text is a list (i.e., lines)
                    for line in text:
                        file.write(line.strip() + '\n')  # Each line is written with a newline character
                else:  # If text is a single string (i.e., entire content)
                    file.write(text.strip() + '\n')  # Write the entire content with a newline character

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

        if file_path.endswith('.json'):
            data = JsonParser.parse(file_path)
            if data:
                formatted_text = JsonParser.format_data(data)
                output_file = input("Enter the file name where the text will be copied: ")
                num_lines_choice = input("How many lines to copy from JSON? (Type 'all' for all lines, 'custom' for custom number): ")
                if num_lines_choice.lower() == 'all':
                    if self.copy_to_file(formatted_text.split('\n'), output_file):  # Split text into lines
                        os.remove(file_path)
                        print("The original file was successfully deleted.")
                elif num_lines_choice.lower() == 'custom':
                    num_lines = int(input("Enter the number of lines to copy: "))
                    if num_lines > len(formatted_text.split('\n')):
                        print("The specified number of lines exceeds the total number of lines in the text.")
                    else:
                        if self.copy_to_file(formatted_text.split('\n')[:num_lines], output_file):
                            os.remove(file_path)
                            print("The original file was successfully deleted.")
                else:
                    print("Invalid choice.")
        else:
            lines = self.select_lines(file_path)
            output_file = input("Enter the file name where the text will be copied: ")
            if self.copy_to_file(lines, output_file):
                os.remove(file_path)
                print("The original file was successfully deleted.")


class JsonParser(FileCopier):
    @staticmethod
    def parse(json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print("Error while parsing JSON file:", e)
            return None

    @staticmethod
    def format_data(data):
        formatted_text = ""
        for item in data['news_feed']:
            formatted_text += f"{item['type'].capitalize()} {'-' * (30 - len(item['type']))}\n"
            formatted_text += f"{item['content'].capitalize()}\n"
            if item.get('location'):
                formatted_text += f"{item['location'].capitalize()}, {item['date']} {item['time']}\n"
            elif item.get('expiration_date'):
                formatted_text += f"Actual until: {item['expiration_date']}, {item['days_left']} days left\n"
            elif item.get('status'):
                formatted_text += f"Ad is {item['status'].lower()}. {item['overdue_days']} days overdue\n"
            elif item.get('funny_meter'):
                formatted_text += f"Funny meter - {item['funny_meter']}\n"
            formatted_text += '\n'
        return formatted_text


copier = FileCopier()
copier.start()
