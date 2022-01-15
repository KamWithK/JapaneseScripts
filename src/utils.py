import jaconv
import unicodedata

# Returns word without reading or learning status
def get_word(input):
    return input[0].split("◴")[0]

# Breaks single string into separate word and reading
def separate_word_reading(input):
    entry = input[0].split("◴")
    entry[1] = jaconv.hira2kata(entry[1])

    return [*entry, input[1]]

# Ignore words based on linguistic script
def word_filter(input, filter=""):
    if filter == "KANJI": # Ignore anything which doens't include an ideograph
        return any("IDEOGRAPH" in unicodedata.name(character) for character in input[0])
    elif filter == "KATAKANA": # Ignore anything which is just katakana
        return not all("KATAKANA" in unicodedata.name(character) for character in input[0])
    else: return True
