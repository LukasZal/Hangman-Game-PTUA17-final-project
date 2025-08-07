from dataclasses import dataclass, field
from typing import List
from logger import get_logger

log = get_logger()

@dataclass
class GameStats:
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0

    def count_games(self, result: bool) -> None:
        self.games_played += 1
        if result:
            self.games_won += 1
        else:
            self.games_lost += 1

    def game_history(self):
        return {
            "games_played": self.games_played,
            "games_won": self.games_won,
            "games_lost": self.games_lost
        }

    @classmethod
    def user_stat(cls, data):
        stats = cls()
        stats.games_played = data.get("games_played", 0)
        stats.games_won = data.get("games_won", 0)
        stats.games_lost = data.get("games_lost", 0)
        return stats

    def __str__(self) -> str:
        return (
            f"Games Played: {self.games_played}\n"
            f"Games Won: {self.games_won}\n"
            f"Games Lost: {self.games_lost}\n"
        )

@dataclass
class RoundStats:
    guesses_made: int = 0
    correct_guesses: int = 0
    incorrect_guesses: int = 0
    guessed_letters: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Guesses Made: {self.guesses_made}\n"
            f"Correct: {self.correct_guesses}\n"
            f"Incorrect: {self.incorrect_guesses}\n"
        )

class HangmanGame:
    def __init__(self, word: str, stats: GameStats):
        self.word = word.upper()
        self.word_completion = "_" * len(word)
        self.tries = 10
        self.guessed = False
        self.guessed_letters: List[str] = []
        self.guessed_words: List[str] = []
        self.round_stats = RoundStats()
        self.stats = stats
        self.messages: List[str] = []
        log.info("Game started with word: %s", self.word)

    def guess_letter(self, guess: str) -> str:
        guess = guess.upper()
        self.round_stats.guesses_made += 1

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                return f"You already guessed the letter {guess}"
            elif guess not in self.word:
                self.tries -= 1
                self.guessed_letters.append(guess)
                self.round_stats.guessed_letters.append(guess)
                self.round_stats.incorrect_guesses += 1
                return f"{guess} is not in the word"
            else:
                self.guessed_letters.append(guess)
                self.round_stats.guessed_letters.append(guess)
                self.round_stats.correct_guesses += 1
                self.update_word_completion(guess)
                return f"Good job! {guess} is in the word"
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess in self.guessed_words:
                return f"You already guessed the word {guess}."
            elif guess != self.word:
                self.tries -= 1
                self.guessed_words.append(guess)
                return f"{guess} is not the word"
            else:
                self.guessed = True
                self.word_completion = self.word
                return "Congratulations! You guessed the word"
        else:
            return "Invalid input"

    def update_word_completion(self, guess: str) -> None:
        word_as_list = list(self.word_completion)
        for i, letter in enumerate(self.word):
            if letter == guess:
                word_as_list[i] = guess
        self.word_completion = ''.join(word_as_list)
        if "_" not in self.word_completion:
            self.guessed = True

    def is_over(self) -> bool:
        if self.guessed or self.tries <= 0:
            self.stats.count_games(self.guessed)
            return True
        return False