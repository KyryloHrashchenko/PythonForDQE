import os
import datetime
import random
from hometask_3 import cap_sentence


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
            print("7. Exit")

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
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    @staticmethod
    def copy_text_to_file():
        copier = FileCopier()
        copier.start()


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


if __name__ == "__main__":
    news_feed = NewsFeed()
    news_feed.run()
