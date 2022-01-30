# import nltk
# nltk.download()

# from nltk.corpus import words
from itertools import filterfalse
from pickletools import read_unicodestring1
from typing import Tuple, List, Callable
import random
from xml.etree.ElementTree import XML

# word_list = words.words()
# five_letter_words = [w for w in word_list if len(w) == 5]

five_letter_words = open("word_list.txt").read().strip().splitlines()

# target_word = random.choice(five_letter_words)
target_word = "could"
print("Target word:", target_word)
print() 

INCORRECT = 0
MISPLACED = 1
CORRECT = 2

class FinishedSignal(Exception):
    pass

def do_guess(input_word: str) -> Tuple[int, int, int, int, int]:
    o = []
    for letter_input, letter_target in zip(input_word, target_word):
        if letter_input == letter_target:
            o.append(CORRECT)
        elif letter_input in target_word:
            o.append(MISPLACED)
        else:
            o.append(INCORRECT)
    assert len(o) == 5
    return tuple(o)

UNKNOWN = -1  # represents an unknown position
known_letters = {}
tried_words = []

Filter = Callable[[str], bool]

def make_filter_function() -> Filter:
    must_contain = [letter for letter in known_letters if known_letters[letter][0] == MISPLACED]
    must_contain_at = {letter: known_letters[letter][1] for letter in known_letters if known_letters[letter][0] == CORRECT}
    must_not_contain = [letter for letter in known_letters if known_letters[letter][0] == INCORRECT]

    def x(word: str) -> bool:
        assert len(word) == 5
        if word in tried_words:
            return False
        for letter in must_not_contain:
            if letter in word:
                return False
        for letter in must_contain:
            if letter not in word:
                return False
        for letter in must_contain_at:
            pos = must_contain_at[letter]
            if word[pos] != letter:
                return False
        return True
    
    return x


letter_frequencies = {
    # https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    "e": 12.02,
    "t": 9.10,
    "a": 8.12,
    "o": 7.68,
    "i": 7.31,
    "n": 6.95,
    "s": 6.28,
    "r": 6.02,
    "h": 5.92,
    "d": 4.32,
    "l": 3.98,
    "u": 2.88,
    "c": 2.71,
    "m": 2.61,
    "f": 2.30,
    "y": 2.11,
    "w": 2.09,
    "g": 2.03,
    "p": 1.82,
    "b": 1.49,
    "v": 1.11,
    "k": 0.69,
    "x": 0.17,
    "q": 0.11,
    "j": 0.10,
    "z": 0.07,
}

def get_highest_scoring_word(words: List[str], f: Callable[[str], bool]) -> str:
    highest = 0
    highest_word = ""
    for word in words:
        if not f(word):
            continue
        x = sum(letter_frequencies[letter] for letter in word)
        if x > highest:
            highest = x
            highest_word = word
    return highest_word


def run_guess():
    global known_letters, tried_words

    highest_score_word = get_highest_scoring_word(five_letter_words, make_filter_function())

    # break guess results into known_letters
    guess_result = do_guess(highest_score_word)

    if guess_result == (CORRECT, CORRECT, CORRECT, CORRECT, CORRECT):
        raise FinishedSignal

    for i, (letter, status) in enumerate(zip(highest_score_word, guess_result)):
        if letter not in known_letters or status == CORRECT:
            known_letters[letter] = (status, i)
    tried_words.append(highest_score_word)

for i in range(250):
    target_word = five_letter_words[i]
    known_letters = {}
    tried_words = []

    print(f"Day {i}, target is {five_letter_words[i]}", end="")
    tries = 0
    try:
        while True:
            tries += 1
            run_guess()
    except FinishedSignal:
        pass
    print(f", got in {tries}", "OK" if tries <= 6 else "NOT OK")
