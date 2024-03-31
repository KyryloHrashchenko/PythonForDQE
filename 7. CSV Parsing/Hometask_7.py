import csv
from collections import Counter
import re


class WordCounter:
    def __init__(self, filename):
        self.filename = filename

    def count_words(self):
        # Открываем файл и читаем его содержимое
        with open(self.filename, 'r', encoding='windows-1252') as file:
            content = file.read()

        # Используем регулярное выражение для разделения текста на слова,
        # игнорируя слова, содержащие только цифры
        words = re.findall(r'\b(?![0-9]+\b)\w+\b', content.lower())

        # Используем Counter для подсчета вхождений каждого слова
        self.word_counts = Counter(words)

    def save_to_csv(self, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='windows-1252') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Word', 'Count'])
            for word, count in self.word_counts.items():
                csv_writer.writerow([word, count])


# Пример использования класса
filename = r'C:\Learn\Python for DQE\5. Classes. OOP\news.txt'
csv_filename = 'results.csv'

word_counter = WordCounter(filename)
word_counter.count_words()
word_counter.save_to_csv(csv_filename)

print(f'Results saved to file: {csv_filename}')
