import requests
import random
import string

API_URL = "https://random-word-api.herokuapp.com/word"

class WordGuessGame:
    def __init__(self):
        self.max_attempts = 7
        self.word = ""
        self.guessed_letters = set()
        self.remaining_attempts = self.max_attempts

    def fetch_word(self, min_length=4, max_length=10):
        try:
            print("🔍 Fetching word from Datamuse...")
            response = requests.get(
                "https://api.datamuse.com/words",
                params={"ml": "thing", "max": 1000},
                timeout=5
            )
            if response.status_code == 200:
                words = [item['word'].lower() for item in response.json()]
                filtered_words = [w for w in words if min_length <= len(w) <= max_length and w.isalpha()]
                if filtered_words:
                    return random.choice(filtered_words)
                else:
                    print("⚠️ No suitable word from API. Using fallback.")
        except requests.RequestException as e:
            print(f"⚠️ Failed to fetch from Datamuse: {e}")
        
        # Fallback word list
        fallback_words = [
            "python", "hangman", "challenge", "developer", "keyboard",
            "function", "variable", "loop", "array", "string"
        ]
        return random.choice(fallback_words)




    def display_welcome(self):
        print("Welcome to the Word Guessing Game!")
        print("Guess the hidden word one letter at a time.")
        input("Press Enter to start a new game...")

    def display_current_word(self):
        display = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
        print("\nWord: ", display)
        print("Guessed Letters: ", " ".join(sorted(self.guessed_letters)))
        print(f"Remaining Attempts: {self.remaining_attempts}")

    def get_player_guess(self):
        while True:
            guess = input("\nEnter a letter: ").lower()
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print("Invalid input. Please enter a single alphabetical character.")
            elif guess in self.guessed_letters:
                print("You already guessed that letter. Try a different one.")
            else:
                return guess

    def play(self):
        self.word = self.fetch_word()
        self.guessed_letters.clear()
        self.remaining_attempts = self.max_attempts

        while self.remaining_attempts > 0 and not self.has_won():
            self.display_current_word()
            guess = self.get_player_guess()
            self.guessed_letters.add(guess)
            if guess not in self.word:
                self.remaining_attempts -= 1

        self.display_current_word()
        if self.has_won():
            print("\nCongratulations! You've guessed the word!")
        else:
            print(f"\nGame Over! The word was: {self.word}")

    def has_won(self):
        return all(letter in self.guessed_letters for letter in self.word)

    def prompt_replay(self):
        choice = input("\nDo you want to play again? (y/n): ").lower()
        return choice == 'y'
    
def main():
    game = WordGuessGame()
    game.display_welcome()
    while True:
        game.play()
        if not game.prompt_replay():
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
