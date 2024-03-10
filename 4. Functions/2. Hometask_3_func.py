import re  # Importing regular expressions module


def replace_iz(text):
    # Replacing all "iz" to "is" except shielded iz with ““
    a = re.sub(r'(?<!“)\b(iz)\b(?!“)', 'is', text)
    return a


def get_last_words(sentence):
    # Getting last word from each sentence
    a = [re.findall(r'\b\w+\b', sentence)[-1] for sentence in sentence]
    return a


default_text = """

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.


"""


def clean_whitespaces(text):
    # Cleaning all whitespaces from default_text to make changes easier
    clean = re.sub(r'\s+', ' ', text).strip()
    return clean


cleaned_text = clean_whitespaces(default_text)


def split_text(text):
    # Splitting cleaned default text on separate sentences
    s = re.split(r'\. ', text)
    return s


sentences = split_text(cleaned_text)


def cap_sentence(text):
    # Transforming first letter in each sentence to upper case
    cs = [s.capitalize() for s in text]
    return cs


capitalized_sentences = cap_sentence(sentences)


def func_join(text, delimiter):
    # Joining (unionising all sentences)
    ct = delimiter.join(text)
    return ct


capitalized_text = func_join(capitalized_sentences, ". ")
# Using replace_iz function on capitalized_text and transforming all misspellings iz to is
capitalized_text = replace_iz(capitalized_text)
# Using function get_last_words, to get last words from capitalized_sentences
new_sentences = get_last_words(capitalized_sentences)
# Making new sentence from last words
last_words_text = func_join(new_sentences, ' ')
# Transforming first letter in new sentence to upper case
last_words_text = last_words_text.capitalize()
# Splitting text to separate sentences again
capitalized_text_sentences = split_text(capitalized_text)


def insert_sentence(text_to_insert, text_to_modify, pos):
    # Inserting new sentence after third sentence in text
    text_to_modify.insert(pos, text_to_insert)
    return text_to_modify


capitalized_text_sentences = insert_sentence(last_words_text, capitalized_text_sentences, 3)

# Joining all sentences together
new_text = func_join(capitalized_text_sentences, ". ")
# Splitting our new text again
tabs_s = split_text(new_text)


def add_symbol(text, symbol):
    # Adding dot after each sentence (to avoid issue with dot after tabulation in final result set)
    for sentence in range(len(text)):
        text[sentence] = text[sentence] + symbol


add_symbol(tabs_s, '. ')


def add_whitespaces(text, t_positions):
    # Choosing after what sentences in text we are going to use tabulation and invisible space symbol (nbsp)
    tabs = "\n\n\n"
    nbsp = '\u00A0'
    # Adding newline and invisible space after positions, we chose before
    for position in t_positions:
        if 0 <= position < len(text):
            text[position] += tabs + nbsp
    # Concatenation of invisible symbol to first sentence, to allign results of default_text and new_text
    text[0] = '\u00A0' + text[0]


add_whitespaces(tabs_s, [0, 3, 5])

# Joining sentences for final result
new_text_with_tabs = func_join(tabs_s, "")


def count_whitespaces(text):
    # Counting number if whitespaces and spaces for old (default) text and new text
    count = sum(1 for symbol in text if symbol.isspace())
    return count


count_whitespaces_old = count_whitespaces(default_text)
count_whitespaces_new = count_whitespaces(new_text_with_tabs)

# printing final results
print(new_text_with_tabs)
print(f"Number of spaces and whitespaces in default_text = {count_whitespaces_old}")
print(f"Number of spaces and whitespaces in new_text = {count_whitespaces_new}")
