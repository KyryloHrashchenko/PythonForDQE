import csv
import re
from collections import Counter, defaultdict


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
        with open(self.input_file, 'r', encoding='windows-1252') as file:
            text = file.read()

            # Processing every character
            for char in text:
                if char.isalpha():
                    total_letters += 1
                    stats[char.lower()]['count_all'] += 1
                    if char.isupper():
                        stats[char.lower()]['count_uppercase'] += 1

        # Writing statistics to a CSV file
        with open(self.output_file, 'w', newline='', encoding='windows-1252') as csvfile:
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
        with open(self.filename, 'r', encoding='windows-1252') as file:
            content = file.read()

        # Using a regular expression to divide text into words,
        # ignoring words containing only numbers
        words = re.findall(r'\b(?![0-9]+\b)\w+\b', content.lower())

        # Using Counter to count occurrences of each word
        self.word_counts = Counter(words)

    def save_to_csv(self, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='windows-1252') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Word', 'Count'])
            for word, count in self.word_counts.items():
                csv_writer.writerow([word, count])


text_input_file = r'C:\Learn\Python for DQE\5. Classes. OOP\news.txt'
text_output_file = "letter_results.csv"
word_input_file = r'C:\Learn\Python for DQE\5. Classes. OOP\news.txt'
word_output_file = 'word_results.csv'

# Text (letter) processing
text_stats = TextStatistics(text_input_file, text_output_file)
text_stats.process_text()

# Word processing
word_counter = WordCounter(word_input_file)
word_counter.count_words()
word_counter.save_to_csv(word_output_file)

print(f'Results saved to files: {text_output_file}, {word_output_file}')
