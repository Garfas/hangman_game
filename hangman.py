import random
import sqlite3
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import logging
from colorama import Fore, Style


#constants
MAX_ATTEMPTS = 10
DATABASE_FILE = "hangman.db"

#  Define a list of available colors from colorama
available_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

#Set up logging
logging.basicConfig(level=logging.INFO, filename="hangman.log", format="%(asctime)s [%(levelname)s]: %(message)s")


class HangmanGame:
    def __init__(self, word_list: List[str]):
        self.word_list = word_list
        self.word_to_guess: Optional[str] = None
        self.attempts_left =MAX_ATTEMPTS
        self.guessed_letters = set()
        self.correct_letters = set()

    def initialize_game(self):
        self.word_to_guess = random.choice(self.word_list)
        self.attempts_left = MAX_ATTEMPTS
        self.guessed_letters = set()

    def get_guess(self ) -> str:
        return input ("Guess a letter or the whole word:").lower()

    def make_guess(self, guess: str) -> bool:
        guess = guess.lower()
        if guess in self.guessed_letters:
            print(Fore.YELLOW + f"You've already guessed the letter '{guess}'.Try a different letter." + Style.RESET_ALL)
            return False
        
        if guess in self.correct_letters:
             print(Fore.WHITE + "You've already guessed the letter '{guess}' correctly. Try a different letter." + Style.RESET_ALL)
             return False
        
        self.guessed_letters.add(guess)
        
        if len(guess) == 1:
            if guess in self.word_to_guess:
                self.correct_letters.add(guess)
                self.update_word_representation()
                print(Fore.GREEN + "Correct guess!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "You didn't guess the letter or the whole word!" + Style.RESET_ALL)
                self.attempts_left -= 1
        
        else:
            if guess == self.word_to_guess:
                self.update_word_representation()
                print("Congratulations! Yo've guessed the whole word.")
            else:
                print("Incorrect guess -1!")
                self.attempts_left -= 1

        current_representation = self.update_word_representation()
        print(f"Word: {current_representation}")
        print(f"Attempts left: {self.attempts_left}")

        if current_representation == self.word_to_guess:
            print("Congratulations! You've won")
            return True
        elif self.attempts_left == 0:
            print(f"Game over!!! The word was {self.word_to_guess}. Better luck next time.")
            return True
        
        return False

    def update_word_representation(self):
        return "".join([letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess])

class HangmanDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
                """
            )
            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    word TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    guessed_letters TEXT NOT NULL,
                    won BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
                '''
            )

    def register_user(self, name: str, surname: str, email: str) -> int:
        with self.conn:
            cursor = self.conn.execute("SELECT id FROM user WHERE email = ?", ( email,))
            existing_user = cursor.fetchone()
            if existing_user:
                logging.info("User alredy exists with the same email. Returning existing ID.")
                return existing_user[0]
            
            cursor = self.conn.execute("INSERT INTO user (name, surname, email) VALUES (?, ?, ?)", (name, surname, email))
            return cursor.lastrowid
        
    def save_games(self, user_id: int, game: HangmanGame, won: bool):
        with self.conn:
            guessed_letter_str = ",".join(sorted(game.guessed_letters))
            self.conn.execute(
                """
                INSERT INTO games (user_id, word, attempts, guessed_letters, won)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, game.word_to_guess, game.attempts_left, guessed_letter_str, int(won)),
            )
    
    def get_user_statistic(self, user_id: int) -> dict:
        with self.conn:
            cursor = self.conn.execute(
                "SELECT COUNT(*) AS total_games, SUM(won) AS games_won FROM games WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            return {"games_played": row[0], "games_won": row[1]}
        
    def display_user_statistics(self, user_id: int):
        user_statistic = self.get_user_statistic(user_id)
        print(f"Games played: {user_statistic['games_played']}")
        print(f"Games won: {user_statistic['games_won']}")
        

def get_words_from_website() -> List[str]:
    url = "https://random-word-api.herokuapp.com/word"
    try:
        response = requests.get(url)
        response.raise_for_status()
        words = response.json()
        logging.info("Successfully fetched words from the website, https://random-word-api.herokuapp.com/word.")
        return words
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching data from the web site. Pleas check your internet connection.")
        return[]
    except Exception as e:
        logging.error("An error ocurred while fetching data from the website.")
        return[]





def main():
    welcome_message = f"{random.choice(available_colors)} Welcome to Hangman!" + Style.RESET_ALL
    print(welcome_message)
    word_list = get_words_from_website()
    if not word_list:
        print("Failed to get words from the website. Exiting the game.")
        return
    
    db = HangmanDatabase()
    name_color = random.choice(available_colors)
    name = input(f"{name_color} Enter your name: ") + Style.RESET_ALL
    surname = input(f"{name_color} Enter your surname: ") + Style.RESET_ALL
    email = input(f"{name_color}Enter your email: ") + Style.RESET_ALL

    user_id = db.register_user(name, surname, email)
    game = HangmanGame(word_list)
    game.initialize_game()

    while True:
        game.initialize_game() #pradeti zaidima is naujo
        while game.attempts_left > 0:
            current_representation = game.update_word_representation()
            print(f'Word: {current_representation}')
            print(f'Attempts left: {game.attempts_left}')

            guess = game.get_guess()
   
            if game.make_guess(guess):
                print("Correct guess!")
            else:
                print("If the guess is wrong -1 POINT!")
                

            if "_" not in current_representation:
                print("Congratulation! You guessed the word!")
                db.save_games(user_id, game, won=True)
                break

        if game.attempts_left == 0:
            print(f'Sorry, you lost. The word was "{game.word_to_guess}".')
            db.save_games(user_id, game, won=False)

        play_again = input("Do you play again? (y/n): ").lower()
        if play_again != "y":
            break
    
    db.display_user_statistics(user_id)


if __name__ == "__main__":
    main()