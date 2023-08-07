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
        with self.conn:
            self.conn.execute(
            '''
            CREATE TABLES IF NOT EXISTS user(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email text not null unique
            )
            '''
        )
        self.conn.execute(
            '''
            CREATE TABLES IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            attempts INTEGER NOT NULL,
            guessed_letters TEXT NOT NULL,
            won BOOLEAN NOT NULL,
            FOREING (user_id) REFERENCES user (id)
            )
            '''
        )

    def register_user(self, name: str, surname: str, email: str) -> int:
        with self.conn:
            cursor = self.conn.execute("INSERT INTO user (name, surname, email) VALUE (?, ?, ?)", (name, surname, email))
            return cursor.lastrowid
        
    def save_games(self, user_id: int, game: HangmanGame, won: bool):
        with self.conn:
            guessed_letter_str = ",".join(sorted(game.guessed_letters))
            self.conn.execute(
                '''
                INSERT INTO games (user_id, word, attempts, guessed_letters, won)
                VALUE (?, ?, ?, ?, ?)
                ''',
                (user_id, game.word_to_guess, game.attempts_left, guessed_letter_str, won),
            )
    
    def get_user_statistic(self, user_id: int) -> dict:
        with self.conn:
            cursor = self.conn.ececute(
                "SELECT COUNT(*) AS total_games, SUM(won) AS games_won FROM games WHERE user_id = ?", (user_id)
            )
            row = cursor.fetchone()
            return {"games_played": row[0], "games_won": row[1]}
        

def get_words_from_website() -> List[str]:
    url = "https://random-words-api.vercel.app/"
    try:
        response = requests.get(url)
        response = raise_for_status()
        words = response.json()
        return words
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching data from the web site. Pleas check your internet connection.")
        return[]
    except Exception as e:
        logging.error("An error ocurred while fetching data from the website.")

def main():
    print("Welcome to Hangman!")
    word_list = get_words_from_website()
    if not word_list:
        print("Fai;ed to get words from the website. Exiting the game.")
        return
    
    db = HangmanDatabase
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    email = input("Enter your email: ")
        

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