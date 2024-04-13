import os
import datetime
import random
import csv
import json
import re
from collections import Counter, defaultdict


class NewsFeedItem:
    def __init__(self, text):
        self.text = text
        self.date_published = datetime.datetime.now()

    def publish(self):
        raise NotImplementedError("Subclasses must implement publish method")


class News(NewsFeedItem):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def publish(self):
        return f"\nNews -------------------------\n{self.text}\n{self.city}, {self.date_published.strftime('%d/%m/%Y %H.%M')}\n"


class PrivateAd(NewsFeedItem):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = expiration_date
        self.days_left = (expiration_date - datetime.datetime.now()).days

    def publish(self):
        if self.days_left < 0:
            return f"\nPrivate Ad ------------------\n{self.text}\nAd is expired. {abs(self.days_left)} days overdue\n"
        else:
            return f"\nPrivate Ad ------------------\n{self.text}\nActual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left} days left\n"


class JokeOfTheDay(NewsFeedItem):
    def __init__(self, text):
        super().__init__(text)
        self.funny_meter = random.randint(1, 10)

    def publish(self):
        return f"\nJoke of the day ------------\n{self.text}\nFunny meter – {self.funny_meter} of 10\n"


class NewsFeed:
    def __init__(self):
        self.feed_items = []

    def add_news(self, text, city):
        self.feed_items.append(News(text, city))

    def add_private_ad(self, text, expiration_date):
        self.feed_items.append(PrivateAd(text, expiration_date))

    def add_joke_of_the_day(self, text):
        self.feed_items.append(JokeOfTheDay(text))

    def publish_to_file(self, filename, mode):
        with open(filename, mode) as file:
            if mode == 'w':
                file.write("News feed:")
            for item in self.feed_items:
                file.write(item.publish())

    def run(self):
        while True:
            print("\nNews Feed Menu:")
            print("1. Add News")
            print("2. Add Private Ad")
            print("3. Add Joke of the Day")
            print("4. Publish to Existing File")
            print("5. Publish to New File")
            print("6. Copy Text to File")
            print("7. Text Statistics")
            print("8. Word Counter")
            print("9. Parse and Copy JSON")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                text = input("Enter news text: ")
                city = input("Enter city: ")
                self.add_news(text, city)
            elif choice == "2":
                text = input("Enter ad text: ")
                expiration_date_str = input("Enter expiration date (format: DD/MM/YYYY): ")
                expiration_date = datetime.datetime.strptime(expiration_date_str, "%d/%m/%Y")
                self.add_private_ad(text, expiration_date)
            elif choice == "3":
                text = input("Enter joke text: ")
                self.add_joke_of_the_day(text)
            elif choice == "4":
                filename = input("Enter filename to publish: ")
                mode = 'a' if os.path.exists(filename) else 'w'
                self.publish_to_file(filename, mode)
                print("Published successfully!")
            elif choice == "5":
                filename = input("Enter new filename to publish: ")
                self.publish_to_file(filename, 'w')
                print("Published successfully!")
            elif choice == "6":
                self.copy_text_to_file()
            elif choice == "7":
                self.text_statistics()
            elif choice == "8":
                self.word_counter()
            elif choice == "9":
                self.parse_and_copy_json()
            elif choice == "10":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    @staticmethod
    def copy_text_to_file():
        copier = FileCopier()
        copier.start()

    @staticmethod
    def text_statistics():
        text_input_file = input("Enter the path to the text file: ")
        text_output_file = input("Enter the output CSV filename for text statistics: ")
        text_stats = TextStatistics(text_input_file, text_output_file)
        text_stats.process_text()

    @staticmethod
    def word_counter():
        word_input_file = input("Enter the path to the text file: ")
        word_output_file = input("Enter the output CSV filename for word counter: ")
        word_counter = WordCounter(word_input_file)
        word_counter.count_words()
        word_counter.save_to_csv(word_output_file)
        print(f'Results saved to file: {word_output_file}')

    def parse_and_copy_json(self):
        json_file = input("Enter the path to the JSON file: ")
        output_file = input("Enter the file name where the text will be copied: ")

        parser = JsonParser()
        data = parser.parse(json_file)
        if data:
            formatted_text = JsonParser.format_data(data)
            num_lines = input("Enter the number of lines to copy (enter 'all' to copy all lines): ")
            if num_lines.lower() == 'all':
                self.copy_to_file(formatted_text, output_file)
            else:
                num_lines = int(num_lines)
                lines = formatted_text.split('\n')[:num_lines]
                partial_text = '\n'.join(lines)
                self.copy_to_file(partial_text, output_file)
            os.remove(json_file)

    @staticmethod
    def copy_to_file(text, output_file):
        try:
            mode = 'a' if os.path.exists(output_file) else 'w'
            with open(output_file, mode, encoding='utf-8') as file:
                if mode == 'a' and len(text) > 0:
                    # Creating a delimiter only if file has already been created and have text > 1
                    delimiter = '-' * 50
                    file.write('\n' + delimiter + '\n')

                file.write(text)

            print("The text was successfully copied to the file", output_file)
            return True
        except Exception as e:
            print("Error while copying file:", e)
            return False


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
        with open(file_path, 'r', encoding='utf-8') as file:
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
            with open(output_file, mode, encoding='utf-8') as file:
                if mode == 'a' and len(text) > 0:
                    # Creating a delimiter only if file has already been created and have text > 1
                    delimiter = '-' * 50
                    file.write('\n' + delimiter + '\n')

                file.write(text)

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


class TextStatistics:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process_text(self):
        # Dictionary for storing statistics for each letter
        stats = defaultdict(lambda: {'count_all': 0, 'count_uppercase': 0})

        # Total number of letters in the text
        total_letters = 0

        # Reading a Source Text File
        with open(self.input_file, 'r', encoding='utf-8') as file:
            text = file.read()

            # Processing every character
            for char in text:
                if char.isalpha():
                    total_letters += 1
                    stats[char.lower()]['count_all'] += 1
                    if char.isupper():
                        stats[char.lower()]['count_uppercase'] += 1

        # Writing statistics to a CSV file
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for letter, data in stats.items():
                percentage = (data['count_all'] / total_letters) * 100 if total_letters > 0 else 0
                writer.writerow({'letter': letter,
                                 'count_all': data['count_all'],
                                 'count_uppercase': data['count_uppercase'],
                                 'percentage': percentage})

        print("Statistics were successfully written to the file:", self.output_file)


class WordCounter:
    def __init__(self, filename):
        self.word_counts = None
        self.filename = filename

    def count_words(self):
        # Opening the file and reading its content
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Using a regular expression to divide text into words,
        # ignoring words containing only numbers
        words = re.findall(r'\b(?![0-9]+\b)\w+\b', content.lower())

        # Using Counter to count occurrences of each word
        self.word_counts = Counter(words)

    def save_to_csv(self, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Word', 'Count'])
            for word, count in self.word_counts.items():
                csv_writer.writerow([word, count])


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


if __name__ == "__main__":
    news_feed = NewsFeed()
    news_feed.run()
