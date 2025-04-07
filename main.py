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
        ...

    def get_player_guess(self):
        ...

    def play(self):
        ...

    def has_won(self):
        ...

    def prompt_replay(self):
        ...
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
