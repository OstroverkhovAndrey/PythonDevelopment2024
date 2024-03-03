
from collections import defaultdict
import random
import urllib.request
import argparse
import sys
import cowsay

def bullscows(guess: str, secret: str) -> (int, int):
    bolls = 0
    for i, j in zip(guess, secret):
        if i == j:
            bolls += 1
    cows = 0
    guess_dict = defaultdict(lambda: 0)
    for i in guess:
        guess_dict[i] += 1
    for i in secret:
        if guess_dict[i] != 0:
            cows += 1
            guess_dict[i] -= 1
    return (bolls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = random.choice(words)
    count_move = 0
    b = -1
    while b != len(words[0]):
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, word)
        inform("Быки: {}, Коровы: {}", b, c)
        count_move += 1
    return count_move


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
            "This is console game bullscows")
    parser.add_argument("words_dict", help=\
            "Words that can be used in the game (file name or URL)")
    parser.add_argument("word_length", type=int, default=5, nargs="?",\
            help="Length of words")
    args = parser.parse_args()

    text = ""
    url_flag, file_flag = True, True
    try:
        with urllib.request.urlopen(args.words_dict) as f:
            text = f.read().decode('utf-8')
    except:
        url_flag = False
    try:
        with open(args.words_dict) as f:
            text = f.read()
    except:
        file_flag = False
    if not url_flag and not file_flag:
        print("Invalid dictionary!!!")
        sys.exit()
    words = list()
    for i in text.split():
        if len(i) == args.word_length:
            words.append(i)
    if len(words) == 0:
        print("Invalid dictionary!!! No words of the required length!!!")
        sys.exit()


    def ask(prompt: str, valid: list[str] = None) -> str:
        print(cowsay.cowsay(prompt, cow=cowsay.get_random_cow()))
        ans = input()
        while valid and ans not in valid:
            print(cowsay.cowsay(prompt, cow=cowsay.get_random_cow()))
            ans = input()
        return ans

    def inform(format_string: str, bulls: int, cows: int) -> None:
        print(cowsay.cowsay(format_string.format(bulls, cows),\
                cow=cowsay.get_random_cow()))

    res = gameplay(ask, inform, words)
    print(cowsay.cowsay("Результат: {}".format(res), cow=cowsay.get_random_cow()))

