import os
import datetime
import random


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
            print("1. Add News")
            print("2. Add Private Ad")
            print("3. Add Joke of the Day")
            print("4. Publish to Existing File")
            print("5. Publish to New File")
            print("6. Exit")

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
                break
            else:
                print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    news_feed = NewsFeed()
    news_feed.run()
