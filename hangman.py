<<<<<<< Updated upstream
=======

import requests
import random
# from words import WORD_LIST
from bs4 import BeautifulSoup

def get_random_words(num_words):
    url = "https://www.randomword.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.txt, "html.praser")
    words = soup.find_all("div", {"class": "section", "id": "random_word"})
    word_list = [word.get_text().strip().lower() for word in words]
    random_words = random.sample(word_list, num_words)


#Nustatoma konstanta
MAX_ATEEMPTS = 10

# def choose_random_words():
#     return random.choice(WORD_LIST)

def initialize_game():
    word_to_guess = choose_random_words()
    attempts_left = MAX_ATEEMPTS
    guessed_letters = set()

    return word_to_guess, attempts_left, guessed_letters

def get_guess():
    return input ("Guess a letter or the whole word:").lower()

def update_word_representation(word, guessed_letters) -> str:
    return "".join([letter if letter in guessed_letters else "_" for letter in word])

def game_cycle():
    while True:
        word_to_guess, attempts_left, guessed_letter = initialize_game()

        while attempts_left > 0:
            current_representation = update_word_representation(word_to_guess, guessed_letter)
            print(f'Word: {current_representation}')
            print(f'Attempts left: {attempts_left}')

            guess = get_guess()

            if len(guess) == 1:
                guessed_letter.add(guess)
                if guess in word_to_guess:
                    print("Correct guess!")
                else:
                    print("Incorrect guess!")
                    attempts_left -= 1
            elif len(guess) == len(word_to_guess) and guess == word_to_guess:
                print("Congratulations! You gussed the whole word!")
                break
            else:
                print("Incorrect guess! Try again.")

            if "_" not in current_representation:
                print("Congratulation! You guessed the word!")
                break

        if attempts_left == 0:
            print(f'Sorry, you lost. The word was "{word_to_guess}".')

        play_again = input("Do you play again? (y/n): ").lower()
        if play_again != "yes":
            break

if __name__ == "__main__":
    print("Welcome to Hangman!")
    game_cycle()


>>>>>>> Stashed changes
