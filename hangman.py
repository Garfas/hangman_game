import random
import sqlite3
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import logging

#constants
MAX_ATTEMPTS = 10
DATABASE_FILE = "hangman.db"

#Set up logging
logging.basicConfig(level=logging.INFO, filename="hangman.log", format="%(asctime)s [%(levelname)s]: %(message)s")


class HangmanGame:
    def __init__(self, word_list: List[str]):
        self.word_list = word_list
        self.word_to_guess: Optional[str] = None
        self.attempts_left =MAX_ATTEMPTS
        self.guessed_letters = set()

    def initialize_game(self):
        self.word_to_guess = random.choice(self.word_list)
        self.attempts_left = MAX_ATTEMPTS
        self.guessed_letters = set()

    def get_guess(self ) -> str:
        return input ("Guess a letter or the whole word:").lower()

    def update_word_representation(self):
        return "".join([letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess])
    
    def make_guess(self, guess: str) -> bool:
        if len (guess) == 1:
            self.guessed_letters.add(guess)
            return guess in self.word_to_guess
        elif len(guess) == len(self.word_to_guess) and guess == self.word_to_guess:
            return True
        return False


class HangmanDatabase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.create_tables()

    def create_tables(self):
        with self.conn:(
                '''
                Create tables if not exists user(
                id integer primary key,
                name text not null,
                email text not null unique
                )'''
        )
        self.conn.execute(
            '''Create tables if not exists games (
            id integer primary key,
            user_id integer not null,
            guessed_letters taxt not null,
            won Boolean not null,
            foreign key (user_id) References user (id)
            )'''
        )
    
    def get_user_statistic(self, user_id: int) -> dict:
        with self.conn:
            cursor = self.conn.ececute(
                "SELECT COUNT(*) AS total_games, SUM(won) AS games_won FROM games WHERE user_id = ?", (user_id)
            )
            row = cursor.fetchone()
            return {"games_played": row[0], "games_won": row[1]}
        

    # def game_cycle():
#         while True:
#             word_to_guess, attempts_left, guessed_letters = initialize_game()

#         while attempts_left > 0:
#             current_representation = update_word_representation(word_to_guess, guessed_letters)
#             print(f'Word: {current_representation}')
#             print(f'Attempts left: {attempts_left}')

#             guess = get_guess()

#             if len(guess) == 1:
#                 guessed_letters.add(guess)
#                 if guess in word_to_guess:
#                     print("Correct guess!")
#                 else:
#                     print("Incorrect guess!")
#                     attempts_left -= 1
#             elif len(guess) == len(word_to_guess) and guess == word_to_guess:
#                 print("Congratulations! You gussed the whole word!")
#                 break
#             else:
#                 print("Incorrect guess! Try again.")

#             if "_" not in current_representation:
#                 print("Congratulation! You guessed the word!")
#                 break

#         if attempts_left == 0:
#             print(f'Sorry, you lost. The word was "{word_to_guess}".')

#         play_again = input("Do you play again? (y/n): ").lower()
#         if play_again != "yes":
#             break

# if __name__ == "__main__":
#     print("Welcome to Hangman!")
#     game_cycle()