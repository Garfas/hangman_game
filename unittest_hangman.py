import unittest
from unittest.mock import patch
from io import StringIO
import hangman
from hangman import HangmanGame
import os


#constants
MAX_ATTEMPTS = 10
DATABASE_FILE = "hangman.db"


class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.word_list = ['apple', "banana", "cherry"]
        self.game = hangman.HangmanGame(self.word_list)

    def test_initialize_game(self):
        self.game.initialize_game()
        self.assertIsNotNone(self.game.word_to_guess)
        self.assertEqual(self.game.attempts_left, hangman.MAX_ATTEMPTS)
        self.assertEqual(len(self.game.guessed_letters), 0)

    def test_get_guess(self):
        with patch("builtins.input", side_effect = ["a"]):
            guess = self.game.get_guess()
        self.assertEqual(guess, "a")

    def test_make_guess_single_letter_correct(self):
        self.game.word_to_guess = "banana"
        self.assertTrue(self.game.make_guess("b"))

    def test_make_guess_single_letter_incorect(self):
        self.game.word_to_guess = "banana"
        self.assertFalse(self.game.make_guess("c"))

    def test_make_guess_whole_word_correct(self):
        self.game.word_to_guess = "cherry"
        self.assertTrue(self.game.make_guess("cherry"))

    def test_make_guess_whole_word_incorect(self):
        self.game.word_to_guess = "cherry"
        self.assertFalse(self.game.make_guess("banana"))

    def test_update_word_representation(self):
        self.game.word_to_guess = "apple"
        self.game.guessed_letters = {"a", "p"}
        representation = self.game.update_word_representation()
        self.assertEqual(representation, "app__")

class TestHangmanDatabase(unittest.TestCase):
    def setUp(self):
        self.db = hangman.HangmanDatabase()

    def tearDown(self):
        self.db.conn.close()
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)





    def test_register_user(self):
        user_id = self.db.register_user("Mantas", "Jankauskas", "bdsdgdhjjjd@gmail.com")
        self.assertIsInstance(user_id, int)

        #uzdaryti sujungima su duomenu baze
        self.db.conn.close()

    def test_save_and_get_user_statistic(self):
        user_id = self.db.register_user("Dorianas", "Jankauskas", "sdssagjjjil@gmail.com")
        game = hangman.HangmanGame(["apple"])
        game.word_to_guess = "apple"
        game.attempts_left = 5
        game.guessed_letters = {"a", "e"}
        self.db.save_games(user_id, game, True)
        user_statistic = self.db.get_user_statistic(user_id)
        self.assertEqual(user_statistic["games_played"], 1)
        self.assertEqual(user_statistic["games_won"], 1)

        #uzdaryti sujungima su duomenu baze
        self.db.conn.close() 


class TestHangmanIntegration(unittest.TestCase):
    def setUp(self) -> None:
        word_list = ["apple"]
        game = hangman.HangmanGame(word_list)
        game.word_to_guess = "apple"
        game.guessed_letters = set("apple")
        self.assertEqual(game.update_word_representation(), "apple")



if __name__ == "__main__":
    unittest.main   