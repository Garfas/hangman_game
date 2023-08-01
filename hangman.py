

import random
from words import WORD_LIST

#Nustatoma konstanta
max_ateempts = 10

def choose_random_words() -> str:
    return random.choice(WORD_LIST)

def initialize_game():
    word_to_guess = choose_random_words()
    attempts_left = max_ateempts
    guessed_letters = set()

    return word_to_guess, attempts_left, guessed_letters

def get_guess() -> str:
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

            guess = get_guess

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

