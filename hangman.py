import random
import sqlite3
import requests
from typing import List, Optional
import logging
from colorama import Fore, Style
import time


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
        self.guessed_words = set()
        self.correct_letters = set()
        self.start_time = None
        self.conn = sqlite3.connect(DATABASE_FILE) 
        self.game_id = None 

    def initialize_game(self):
        """
        Initialize a new game session.

        This function resets the game parameters, such as the word to guess, the number of attempts left,
        guessed letters and words, and the game start time.

        """
        self.word_to_guess = random.choice(self.word_list)
        self.attempts_left = MAX_ATTEMPTS
        self.guessed_letters = set()
        self.guessed_words = set()
        self.correct_letters = set()
        self.start_time = time.time()
        self.game_id = None
        logging.info("A new game has been initialized.")

    def get_guess(self ) -> str:
        return input ("Guess a letter or the whole word:").lower()

    def make_guess(self, guess: str) -> bool: 
        """
        Process the player's guess.

        :param guess: The guessed letter or word.
        :return: True if the game is won, False otherwise.
        """
        guess = guess.lower()
        if guess in self.guessed_letters:
            print(Fore.YELLOW + f"You've already guessed the letter '{guess}'.Try a different letter." + Style.RESET_ALL)
            return False
        
        if len(guess) == 1:
            self.guessed_letters.add(guess)
        
            if guess in self.word_to_guess:
                self.correct_letters.add(guess)
                self.update_word_representation()
                print(Fore.GREEN + "Correct guess!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "You didn't guess the letter or the whole word!" + Style.RESET_ALL)
                self.attempts_left -= 1
                return False
        
        else:
            self.guessed_words.add(guess)

            if guess == self.word_to_guess:
                self.update_word_representation()
                print(Fore.GREEN + "Correct guess!" + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + "Incorrect guess! -1 point" + Style.RESET_ALL)
                self.attempts_left -= 1
                return False


    def update_word_representation(self): # Update word mapping
        for word in self.guessed_words:
            if word == self.word_to_guess:
                return self.word_to_guess

        return "".join([letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess])


class HangmanDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.create_tables()
        self.game_id = None

    def create_tables(self):# sql request to create two cells in the db: user and games
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
                    elapsed_time REAL,
                    won BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
                '''
            )

    def register_user(self, name: str, surname: str, email: str): 
        """
        Register a new user in the database.

        :param name: The user's name.
        :param surname: The user's surname.
        :param email: The user's email address.
        :return: A dictionary with user information and registration status.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT id, name FROM user WHERE email = ?", ( email,))
            existing_user = cursor.fetchone()
            logging.info(existing_user)
            if existing_user:
                logging.info("User alredy exists with the same email. Returning existing ID.")
                return {"id": existing_user[0], "name": existing_user[1], "exists": True}
            
            cursor = self.conn.execute("INSERT INTO user (name, surname, email) VALUES (?, ?, ?)", (name, surname, email))
            return {"id": cursor.lastrowid, "name": name, "exists": False}
        
    def save_games(self, user_id: int, game: HangmanGame, won: bool):
        with self.conn:
            guessed_letter_str = ",".join(sorted(game.guessed_letters))
            cursor = self.conn.execute(
                """
                INSERT INTO games (user_id, word, attempts, guessed_letters, won)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, game.word_to_guess, game.attempts_left, guessed_letter_str, int(won)),
            )
            self.game_id = cursor.lastrowid # We assign a new game ID
    
    def get_user_statistic(self, user_id: int) -> dict:
        with self.conn:
            cursor = self.conn.execute(
                "SELECT COUNT(*) AS total_games, IFNULL(SUM(won), 0) AS games_won FROM games WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            return {"games_played": row[0], "games_won": row[1]}
        
    def display_user_statistics(self, user_id: int): # prints the player's statistics to the terminal
        user_statistic = self.get_user_statistic(user_id)
        print(f"Games played: {user_statistic['games_played']}")
        print(f"Games won: {user_statistic['games_won']}")

    def display_overall_statistics(self):
        """
        Display overall statistics about all players' games.

        This function retrieves and displays statistics about the total number of games played,
        total games won, total words guessed, total words not guessed, and the percentage of
        words guessed by all players.

        """
        total_games_played = 0
        total_games_won = 0
        total_words_guessed = 0
        total_words_not_guessed = 0

        for user_id in self.get_all_user_ids():
            user_statistics = self.get_user_statistic(user_id)
            total_games_played += user_statistics['games_played']
            total_games_won += user_statistics['games_won']

        total_words_guessed = total_games_won
        total_words_not_guessed = total_games_played - total_games_won

        if total_games_played == 0:
            percentage_guessed = 0
        else:
            percentage_guessed = (total_words_guessed / total_games_played) * 100

        print(f"Overall Statistics:")
        print(f"Total games played: {total_games_played}")
        print(f"Total games won: {total_games_won}")
        print(f"Total words guessed: {total_words_guessed}")
        print(f"Total words not guessed: {total_words_not_guessed}")
        print(f"Percentage of words guessed: {percentage_guessed:.2f}%")

    def get_all_user_ids(self):# we get a list of all users from the db
        with self.conn:
            cursor = self.conn.execute("SELECT id FROM user")
            return [row[0] for row in cursor.fetchall()]

    def save_elapsed_time(self, elapsed_time: float): # updating db used to save past game time
        with self.conn:
            self.conn.execute(
                """
                UPDATE games
                SET elapsed_time = ?
                WHERE id = ?
                """,
                (elapsed_time, self.game_id),
            )

def welcome_user(db: HangmanDatabase, name: str, surname: str, email: str):
        user_registered = db.register_user (name, surname, email)
        if user_registered['exists']:
            print(f"Hi, {user_registered['name']} and Good luck" + Style.RESET_ALL)
        else:
            print(f"Congratulations on registering for the game {name} {surname} {email}, Joins the game for the first time." + Style.RESET_ALL)
        return user_registered['id']

def get_words_from_website() -> List:
    url = "https://random-word-api.herokuapp.com/word?number=10"
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


def main():# the main part of the program and controls the execution of the game
    welcome_message = f"{random.choice(available_colors)} Welcome to Hangman!" + Style.RESET_ALL
    print(welcome_message)
    word_list = get_words_from_website()
    logging.info(word_list)
    if not word_list:
        print("Failed to get words from the website. Exiting the game.")
        return

    db = HangmanDatabase()  # Create an instance of HangmanDatabase

    name_color = random.choice(available_colors)
    name = input(f"{name_color} Enter your name: ")
    surname = input(f"{name_color} Enter your surname: ")
    email = input(f"{name_color}Enter your email: ")

    user_id = welcome_user(db, name, surname, email)
 
    game = HangmanGame(word_list)
   
    while True:
        play(game, user_id)

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != "y":
            break

    db.display_user_statistics(user_id)
    db.display_overall_statistics()

def play(game, user_id):
    """
    Execute the main game loop.

    :param game: An instance of the HangmanGame class representing the game.
    :param user_id: The user ID associated with the game.
    """
    game.initialize_game()
    total_time = 0

    db_instance = HangmanDatabase()

    while game.attempts_left > 0:
        current_representation = game.update_word_representation()

        if "_" not in current_representation:
            print("Congratulations! You guessed the word!")
            print(f"The word was: {game.word_to_guess}")
            print(f"Elapsed play time: {total_time:.2f}")

            elapsed_time = time.time() - game.start_time 
            db_instance.save_games(user_id, game, won=True)  # Save the game results
            db_instance.save_elapsed_time(total_time)  # Save the elapsed time
            return

        print(f'Word: {current_representation}')
        print(f'Attempts left: {game.attempts_left}')
        print("If the guess is wrong -1 POINT!")

        game.start_time = time.time()
        guess = game.get_guess()

        current_time = time.time()
        timesup = current_time - game.start_time > 10

        if timesup:
            print(Fore.RED + "Time's up! You tok too long to make a guess " + Style.RESET_ALL)
            game.attempts_left -= 1
        
        elapsed_time = round(current_time - game.start_time, 3)
        total_time += elapsed_time

        if not timesup:
            game.make_guess(guess)

        if game.attempts_left == 0:
            print(f'Sorry, you lost. The word was "{game.word_to_guess}".')
            print(f"Elapsed play time: {total_time:.2f}")
            db_instance.save_games(user_id, game, won=False)  # Use the same db_instance to save game results
            db_instance.save_elapsed_time(total_time)
            return


if __name__ == "__main__":
    main()