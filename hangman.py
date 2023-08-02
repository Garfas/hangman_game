
from bs4 import BeautifulSoup
import requests
import random

def get_random_words(num_words):
    url = "https://www.randomlists.com/random-words"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    words = soup.find_all("div", {"class": "stylelistrow"})
    word_list = [word.get_text().strip().lower() for word in words]
    random_words = random.sample(word_list, min(num_words, len(word_list)))
    return random_words



#Nustatoma konstanta
MAX_ATTEMPTS = 10

def initialize_game():
    word_to_guess = random.choice(get_random_words(1))
    attempts_left = MAX_ATTEMPTS
    guessed_letters = set()

    return word_to_guess, attempts_left, guessed_letters

def get_guess():
    return input ("Guess a letter or the whole word:").lower()

def update_word_representation(word, guessed_letters) -> str:
    return "".join([letter if letter in guessed_letters else "_" for letter in word])

def game_cycle():
    while True:
        word_to_guess, attempts_left, guessed_letters = initialize_game()

        while attempts_left > 0:
            current_representation = update_word_representation(word_to_guess, guessed_letters)
            print(f'Word: {current_representation}')
            print(f'Attempts left: {attempts_left}')

            guess = get_guess()

            if len(guess) == 1:
                guessed_letters.add(guess)
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

