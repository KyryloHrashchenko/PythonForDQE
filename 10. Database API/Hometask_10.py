import os
import datetime
import random
import csv
import json
import re
import xml.etree.ElementTree as Et
import pyodbc
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
    def __init__(self, database_file):
        self.feed_items = []
        self.db_file = database_file
        self.db = pyodbc.connect(f"DRIVER={{SQLite3 ODBC Driver}};DATABASE={self.db_file}")

    def add_news(self, text, city):
        if not self.check_uniqueness('news', 'news_text', text):
            print("Error: This news text already exists in the database. Please enter a unique news text.")
            return
        self.feed_items.append(News(text, city))

    def add_private_ad(self, text, expiration_date):
        if not self.check_uniqueness('private_ad', 'ad_text', text):
            print("Error: This ad text already exists in the database. Please enter a unique ad text.")
            return
        self.feed_items.append(PrivateAd(text, expiration_date))

    def add_joke_of_the_day(self, text):
        if not self.check_uniqueness('joke_of_the_day', 'joke_text', text):
            print("Error: This joke text already exists in the database. Please enter a unique joke text.")
            return
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
            print("10. Parse and Copy XML")
            print("11. Add to Database")
            print("12. Exit")

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
                self.parse_and_copy_xml()
            elif choice == "11":
                self.add_to_database()
            elif choice == "12":
                self.db.close()
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

    def parse_and_copy_xml(self):
        xml_file = input("Enter the path to the XML file: ")
        output_file = input("Enter the file name where the text will be copied: ")

        parser = XmlParser()
        root = parser.parse(xml_file)
        if root:
            formatted_text = XmlParser.format_data(root)
            num_lines = input("Enter the number of lines to copy (enter 'all' to copy all lines): ")
            if num_lines.lower() == 'all':
                self.copy_to_file(formatted_text, output_file)
            else:
                num_lines = int(num_lines)
                lines = formatted_text.split('\n')[:num_lines]
                partial_text = '\n'.join(lines)
                self.copy_to_file(partial_text, output_file)
            os.remove(xml_file)

    @staticmethod
    def copy_to_file(text, output_file):
        try:
            mode = 'a' if os.path.exists(output_file) else 'w'
            with open(output_file, mode, encoding='utf-8') as file:
                if mode == 'a' and len(text) > 0:
                    delimiter = '-' * 50
                    file.write('\n' + delimiter + '\n')
                file.write(text)

            print("The text was successfully copied to the file", output_file)
            return True
        except Exception as e:
            print("Error while copying file:", e)
            return False

    def add_to_database(self):
        while True:
            print("\nAdd to Database Menu:")
            print("1. Add News")
            print("2. Add Private Ad")
            print("3. Add Joke of the Day")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                news_text = input("Enter news text: ")
                news_city = input("Enter city: ")
                if self.check_uniqueness('news', 'news_text', news_text):
                    news_date = input("Enter date (format: YYYY-MM-DD HH:MM:SS): ")
                    sql = "INSERT INTO news (news_text, news_city, news_date) VALUES (?, ?, ?)"
                    self.db.execute(sql, (news_text, news_city, news_date))
                    self.db.commit()
                    print("News added to database.")
                else:
                    print("Error: This news text already exists in the database. Please enter a unique news text.")
            elif choice == "2":
                ad_text = input("Enter ad text: ")
                if self.check_uniqueness('private_ad', 'ad_text', ad_text):
                    actual_until = input("Enter actual until date (format: YYYY-MM-DD HH:MM:SS): ")
                    sql = "INSERT INTO private_ad (ad_text, actual_until) VALUES (?, ?)"
                    self.db.execute(sql, (ad_text, actual_until))
                    self.db.commit()
                    print("Private Ad added to database.")
                else:
                    print("Error: This ad text already exists in the database. Please enter a unique ad text.")
            elif choice == "3":
                joke_text = input("Enter joke text: ")
                if self.check_uniqueness('joke_of_the_day', 'joke_text', joke_text):
                    funny_meter = random.randint(1, 10)
                    sql = "INSERT INTO joke_of_the_day (joke_text, funny_meter) VALUES (?, ?)"
                    self.db.execute(sql, (joke_text, funny_meter))
                    self.db.commit()
                    print("Joke of the Day added to database.")
                else:
                    print("Error: This joke text already exists in the database. Please enter a unique joke text.")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def check_uniqueness(self, table, field, value):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {field} = ?", (value,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count == 0


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
            os.remove(file_path)
            print("The original file was successfully deleted.")


class TextStatistics:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process_text(self):
        stats = defaultdict(lambda: {'count_all': 0, 'count_uppercase': 0})
        total_letters = 0

        with open(self.input_file, 'r', encoding='utf-8') as file:
            text = file.read()

            for char in text:
                if char.isalpha():
                    total_letters += 1
                    stats[char.lower()]['count_all'] += 1
                    if char.isupper():
                        stats[char.lower()]['count_uppercase'] += 1

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


class WordCounter:
    def __init__(self, filename):
        self.word_counts = None
        self.filename = filename

    def count_words(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        words = re.findall(r'\b(?![0-9]+\b)\w+\b', content.lower())
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


class XmlParser(FileCopier):
    @staticmethod
    def parse(xml_file):
        try:
            tree = Et.parse(xml_file)
            root = tree.getroot()
            return root
        except Exception as e:
            print("Error while parsing XML file:", e)
            return None

    @staticmethod
    def format_data(root):
        formatted_text = ""
        for item in root.findall('item'):
            item_type_element = item.find('type')
            if item_type_element is not None:
                item_type = item_type_element.text.capitalize()
                formatted_text += f"{item_type} {'-' * (30 - len(item_type))}\n"

            content_element = item.find('content')
            if content_element is not None:
                content = content_element.text.capitalize()
                formatted_text += f"{content}\n"

            location = item.find('location')
            if location is not None:
                formatted_text += f"{location.text.capitalize()}, "

            date_element = item.find('date')
            time_element = item.find('time')
            if date_element is not None and time_element is not None:
                formatted_text += f"{date_element.text} {time_element.text}\n"
            else:
                expiration_date_element = item.find('expiration_date')
                if expiration_date_element is not None:
                    formatted_text += f"Actual until: {expiration_date_element.text}, "

                days_left_element = item.find('days_left')
                if days_left_element is not None:
                    formatted_text += f"{days_left_element.text} days left\n"

            funny_meter_element = item.find('funny_meter')
            if funny_meter_element is not None:
                formatted_text += f"Funny meter - {funny_meter_element.text}\n"

            formatted_text += '\n'

        return formatted_text


if __name__ == "__main__":
    db_file = "test.db"
    news_feed = NewsFeed(db_file)
    news_feed.run()
