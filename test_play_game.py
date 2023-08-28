import unittest
from unittest.mock import patch, Mock
from io import StringIO
from hangman import HangmanGame, HangmanDatabase, welcome_user, get_words_from_website, play

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.word_list = ["apple", "banana", "cherry"]
        self.game = HangmanGame(self.word_list)

    def test_initialize_game(self):
        self.game.initialize_game()
        self.assertIsNotNone(self.game.word_to_guess)
        self.assertEqual(self.game.attempts_left, 65)
        self.assertEqual(len(self.game.guessed_letters), 0)
        self.assertEqual(len(self.game.guessed_words), 0)
        self.assertEqual(len(self.game.correct_letters), 0)
        self.assertIsNotNone(self.game.start_time)
        self.assertIsNone(self.game.game_id)
        

class TestHangmanDatabase(unittest.TestCase):
    def setUp(self):
        self.db = HangmanDatabase()
        # with self.db.conn:
        #     self.db.conn.execute("DELETE FROM user")

    def tearDown(self):
        self.db.conn.close()

    def test_register_user(self):
        user_info = self.db.register_user("Jona", "Dog", "john@gmail.com")
        self.assertTrue(user_info["exists"])  # Does such a user already exist
        self.assertEqual(user_info["name"], "Jona")
        self.assertEqual(user_info["id"], 1)

class TestHangmanIntegration(unittest.TestCase):
    def setUp(self):
        self.word_list = ["apple", "banana", "cherry"]
        self.game = HangmanGame(self.word_list)
        self.db = HangmanDatabase()

    def tearDown(self):
        self.db.conn.close()

    def test_play_game(self):
        mock_input_values = iter(["a", "b", "c", "apple"])
        mock_input = Mock(side_effect=lambda: next(mock_input_values))

        captured_output = StringIO()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
             patch("builtins.input", mock_input):
            user_id = welcome_user(self.db, "Johna", "Dog", "john@gmail.com")  # The name is changed from Johna to Jona
            play(self.game, user_id)

            output = mock_stdout.getvalue()
            self.assertIn("Congratulations! You guessed the word!", output)
            self.assertIn("Elapsed play time:", output)
            self.assertIn("Word: _____", output)
            self.assertIn("Attempts left:", output)
            self.assertIn("If the guess is wrong -1 POINT!", output)


if __name__ == "__main__":
    unittest.main()