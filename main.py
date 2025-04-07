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
        ...



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
