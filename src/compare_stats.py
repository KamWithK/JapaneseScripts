# Find frequency lists here - https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw

import json
import jaconv

from utils import separate_word_reading, word_filter

WORD_LIST_PATH = "data/Migaku_Word_List_ja_2022_1_16.json"
FREQUENCY_LIST_PATH = "data/Migaku SoL Top 100 frequency.json"
WORD_FILTER = "KATAKANA"
FREQUENCY_RANGE = 5000

with open(WORD_LIST_PATH, encoding="utf-8-sig") as word_list_file:
    word_list_json = json.load(word_list_file)
    word_list_json = list(filter(lambda input: word_filter(input, WORD_FILTER), map(separate_word_reading, word_list_json)))

    known_words = [(word, reading) for (word, reading, status) in word_list_json if status == 2]
    learning_words = [(word, reading) for (word, reading, status) in word_list_json if status == 1]

with open(FREQUENCY_LIST_PATH, encoding="utf-8-sig") as frequency_file:
    frequency_json = list(filter(word_filter, json.load(frequency_file)))

print(f"TOTAL KNOWN WORD - {len(known_words)}")
print(f"TOTAL LEARNING WORD - {len(learning_words)}")
print()

no_known, no_learning = 0, 0
no_unknown = 0

for word, reading in frequency_json[:FREQUENCY_RANGE]:
    if (word, reading) in known_words:
        no_known += 1
    elif (word, reading) in learning_words:
        no_learning += 1
    else: no_unknown += 1

print(f"KNOWN WORDS IN FREQUENCY LIST - {no_known}")
print(f"LEARNING WORDS IN FREQUENCY LIST - {no_learning}")
print(f"UNKNOWN WORDS IN FREQUENCY LIST - {no_unknown}")
