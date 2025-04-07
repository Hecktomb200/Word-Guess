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
        self.hint_used = False

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

    def use_hint(self):
        import random
        remaining_letters = [c for c in set(self.word) if c not in self.guessed_letters]
        if not remaining_letters:
            print("No letters left to hint!")
            return
        hint_letter = random.choice(remaining_letters)
        self.guessed_letters.add(hint_letter)
        print(f"💡 Hint: The letter '{hint_letter}' is in the word!")

    def get_player_guess(self):
        while True:
            guess = input("Enter a letter (or type '!hint' to reveal one letter): ").lower()

            if guess == "!hint":
                if not self.hint_used:
                    self.use_hint()
                    self.hint_used = True
                else:
                    print("You already used your hint!")
                self.display_current_word()
                continue
            
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print("Invalid input. Please enter a single alphabetical character.")
            elif guess in self.guessed_letters:
                print("You already guessed that letter. Try a different one.")
            else:
                return guess
            
    def prompt_difficulty(self):
        print("\nChoose a difficulty level:")
        print("1. Easy (4–6 letter words)")
        print("2. Medium (6–8 letter words)")
        print("3. Hard (8–10 letter words)")
        
        while True:
            choice = input("Enter 1, 2, or 3: ").strip()
            if choice == '1':
                return (4, 6)
            elif choice == '2':
                return (6, 8)
            elif choice == '3':
                return (8, 10)
            else:
                print("❌ Invalid input. Please enter 1, 2, or 3.")


    def play(self):
        min_len, max_len = self.prompt_difficulty()
        self.word = self.fetch_word(min_length=min_len, max_length=max_len)
        self.guessed_letters = set()
        self.remaining_attempts = 7

        print(f"\n🎮 Game started! Your word has {len(self.word)} letters.")
        
        while self.remaining_attempts > 0 and not self.has_won():
            self.display_current_word()
            guess = self.get_player_guess()
            self.guessed_letters.add(guess)
            if guess not in self.word:
                self.remaining_attempts -= 1

        self.display_current_word()
        if self.has_won():
            print("🎉 Congratulations! You guessed the word!")
        else:
            print(f"💀 You're out of guesses! The word was: {self.word}")


    def has_won(self):
        return all(letter in self.guessed_letters for letter in self.word)

    def prompt_replay(self):
        while True:
            choice = input("\nWould you like to play again? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            else:
                print("❌ Invalid input. Please enter 'y' for yes or 'n' for no.")

    
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
