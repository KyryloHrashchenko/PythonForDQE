import re  # Importing regular expressions modules


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
# Cleaning all whitespaces from default_text to make changes easier
cleaned_text = re.sub(r'\s+', ' ', default_text).strip()
# Splitting cleaned default text on separate sentences
sentences = re.split(r'\. ', cleaned_text)
# Transforming first letter in each sentence to upper case
capitalized_sentences = [sentence.capitalize() for sentence in sentences]
# Joining (unionising all sentences)
capitalized_text = ". ".join(capitalized_sentences)
# Using replace_iz function on capitalized_text and transforming all misspellings iz to is
capitalized_text = replace_iz(capitalized_text)
# Using function get_last_words, to get last words from capitalized_sentences
new_sentences = get_last_words(capitalized_sentences)
# Making new sentence from last words
last_words_text = ' '.join(new_sentences)
# Transforming first letter in new sentence to upper case
last_words_text = last_words_text.capitalize()
# Splitting text to separate sentences again
capitalized_text_sentences = capitalized_text.split(". ")
# Inserting new sentence after third sentence in text
capitalized_text_sentences.insert(3, last_words_text)
# Joining all sentences together
new_text = ". ".join(capitalized_text_sentences)
# Splitting our new text again
tabs_s = new_text.split(". ")

# Adding dot after each sentence (to avoid issue with dot after tabulation in final result set)
for sentence in range (len(tabs_s)):
    tabs_s[sentence] = tabs_s[sentence] + '. '

# Choosing after what sentences in text we are going to use tabulation and invisible space symbol (nbsp)
tabs_positions = [0, 3, 5]
tabs = "\n\n\n"
nbsp = '\u00A0'
# Adding newline and invisible space after positions, we chose before
for position in tabs_positions:
    if 0 <= position < len(tabs_s):
        tabs_s[position] += tabs + nbsp
# Concatenation of invisible symbol to first sentence, to allign results of default_text and new_text
tabs_s[0] = '\u00A0' + tabs_s[0]
# Joining sentences for final result
new_text_with_tabs = "".join(tabs_s)
# Coutung number if whitespaces and spaces for old (default) text and new text
count_whitespaces_old = sum(1 for symbol in default_text if symbol.isspace())
count_whitespaces_new = sum(1 for symbol in new_text_with_tabs if symbol.isspace())
# printing final results
print(new_text_with_tabs)
print(f"Number of spaces and whitespaces in default_text = {count_whitespaces_old}")
print(f"Number of spaces and whitespaces in new_text = {count_whitespaces_new}")