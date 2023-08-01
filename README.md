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


#LT version
# Veiksmų Planas Hangman Žaidimui (terminalo versija)

## 1. Projekto Paruošimas
1. Sukurti naują GitHub repozitoriją Hangman žaidimui.
2. Sukurti virtualią aplinką, kad izoliuotumėte projekto priklausomybes.
3. Sukurti README failą, kuriame pateikta informaciją apie projektą ir jo naudojimą.
4. Pridėkite .gitignore failą, kad neįtraukt nereikalingų failų į versijų kontrolę.

## 2. Žodžių Sąrašas
1. Sukurti Python modulį, kuriame saugosime galimų žodžių sąrašą Hangman žaidimui.
2. Apibrėžti sąrašo struktūrą žodžių saugojimui.
3. Anotuoti sąrašą su tipų komentarais, kad kodas būtų geriau suprantamas.

## 3. Žaidimo Inicializacija
1. Sukurti Python modulį Hangman žaidimo logikai.
2. Apibrėžti funkciją žaidimo inicijavimui.
   - Pasirinkti atsitiktinį žodį iš žodžių sąrašo.
   - Inicijuoti leistinų bandymų skaičių maksimaliu leistinų (10).
   - Sukurkite tuščią aibę, kuriame saugosime atspėtus raides ir seksime unikalias raides.

## 4. Įvesties Apytikslis
1. Apibrėžti funkciją, kuri gautų vartotojo įvestį spėjimui.
2. Patikrinti įvestį, kad užtikrintume, jog tai būtų viena raidė arba žodis (priklausomai nuo vartotojo pasirinkimo).
3. Apdoroti neteisingas įvestis ir paprašyti vartotojo įvesti teisingą informaciją.

## 5. Žaidimo Ciklas
1. Sukurti ciklą, kuris tęsis tol, kol žaidimas bus laimėtas ar pralaimėtas.
2. Rodyti dabartinę žodžio būseną, naudojant pabraukimus neatskleistoms raidėms.
3. Paprašyti vartotojo atspėti raidę arba visą žodį.
4. Patikrinti, ar atspėta raidė/arba žodis yra teisingas:
   - Jei teisinga, atnaujinti žodžio atvaizdavimą, atskleidžiant teisingai atspėtas raides.
   - Jei neteisinga, sumažinti leistinų bandymų skaičių.
   - Įtraukti atspėtą raidę į atspėtų raidžių aibę.
5. Patikrinti, ar yra laimėjimo ar pralaimėjimo sąlygos:
   - Jei vartotojas atspėjo visas raides teisingai, žaidimas yra laimėtas.
   - Jei leistinų bandymų skaičius tampa 0, žaidimas yra pralaimėtas.
6. Registruoti atitinkamą informaciją apie žaidimo eigą, naudojant "print" arba registravimo biblioteką.

## 6. Žaidimo Pabaiga
1. Sukurti funkciją, kuri parodytų žaidimo rezultatą (laimėjimas/pralaimėjimas) vartotojui.
2. Paklauskite, ar vartotojas nori žaisti dar kartą.
   - Jei taip, paleisti žaidimą iš naujo, iškviesdami žaidimo inicijavimo funkciją.
   - Jei ne, baigti žaidimą.

## 7. Pagrindinė Programa
1. Sukurti pagrindinę programą, kuri paleis Hangman žaidimą.
2. Inicijuoti žaidimą, iškviesdami žaidimo inicijavimo funkciją.
3. Pradėti žaidimo ciklą.
4. Apdoroti žaidimo pabaigos scenarijus ir paklausti, ar vartotojas nori žaisti dar kartą.

## 8. Vienetų Testavimas
1. Parašyti vienetų testus, kad patikrintume žaidimo funkcijų ir klasių teisingumą.
2. Užtikrinti, kad žaidimas elgtųsi kaip tikimasi, atsižvelgiant į skirtingas įvestis ir scenarijus.

## 9. Dokumentacija
1. Pateikti komentarus kode, kad paaiškintume sudėtingą logiką ar funkcijas.
2. Atnaujinti README failą su instrukcijomis, kaip sukonfigūruoti ir paleisti Hangman žaidimą.

## 10. Baigimas
1. Užtikrinti, kad kodas būtų tvarkingas, laikytųsi PEP 8 stiliaus gairių ir būtų gerai organizuotas.
2. Atlikti būtinas pataisas, remiantis grįžtamąja informacija ar testavimu.
3. Įkelti galutinę versiją į GitHub repozitoriją.