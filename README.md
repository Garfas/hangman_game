# Hangman Game

# Action Plan for Hangman Game (terminal version)

## 1. Project Preparation
1. Create a new GitHub repository for the Hangman game.
2. Create a virtual environment to isolate project dependencies.
3. Create a README file containing information about the project and its usage.
4. Add a .gitignore file to exclude unnecessary files from version control.

## 2. List of words
1. Create a Python module where we will store a list of possible words for the Hangman game.
2. Define a list structure for storing words.
3. Annotate the list with type comments to make the code easier to understand.

## 3. Game Initialization
1. Create a Python module for the Hangman game logic.
2. Define a function to initialize the game.
    - Choose a random word from the word list.
    - Initialize the number of allowed attempts to the maximum allowed (10).
    - Create an empty array where we will store the guessed letters and keep track of the unique letters.

## 4. Input Approx
1. Define a function that receives user input for a guess.
2. Validate the input to ensure it is a single letter or a word (depending on the user's choice).
3. Handle invalid inputs and prompt the user for correct information.

## 5. Game Cycle
1. Create a loop that will continue until the game is won or lost.
2. Show the current state of the word by using underlines for unexposed letters.
3. Ask the user to guess a letter or a whole word.
4. Check whether the guessed letter/or word is correct:
    - If correct, update the word representation, revealing correctly guessed letters.
    - If incorrect, reduce the number of allowed attempts.
    - Add the guessed letter to the set of guessed letters.
5. Check whether there are win or lose conditions:
    - If the user has guessed all the letters correctly, the game is won.
    - If the number of attempts allowed becomes 0, the game is lost.
6. Register relevant information about the progress of the game using "print" or the registration library.

## 6. End of Game
1. Create a function that will show the result of the game (win/loss) to the user.
2. Ask if the user wants to play again.
    - If so, restart the game by calling the game initialization function.
    - If not, end the game.

## 7. Main Program
1. Create a main program that will run the Hangman game.
2. Initialize the game by calling the game initialization function.
3. Start the game cycle.
4. Handle endgame scenarios and ask if the user wants to play again.

## 8. Unit Testing
1. Write unit tests to verify the correctness of game functions and classes.
2. Ensure that the game behaves as expected under different inputs and scenarios.

## 9. Documentation
1. Provide comments in the code to explain complex logic or functions.
2. Update the README file with instructions on how to configure and run the Hangman game.

## 10. Termination
1. Ensure code is clean, follows PEP 8 style guidelines, and is well organized.
2. Make necessary corrections based on feedback or testing.
3. Upload the final version to the GitHub repository.
