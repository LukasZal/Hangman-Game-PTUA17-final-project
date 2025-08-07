import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app import app, stats
from hangman import HangmanGame, GameStats

client = TestClient(app)

class TestHangman(unittest.TestCase):

    @patch("app.get_user_email", return_value="test@example.com")                               # Tests that when a user exits the game, their stats are updated in the database
    @patch("app.users.update_one", new_callable=AsyncMock)
    def test_exit_game_updates_stats(self, mock_update, mock_get_email):
        stats["test@example.com"] = GameStats(games_played=1, games_won=1)
        response = client.post("/exit")
        self.assertIn(response.status_code, (200, 302))
        mock_update.assert_called_once()

    @patch("app.get_word", return_value="PYTHON")                                               # Verifies the game initializes with the exact word provided by the word-fetching function, making tests predictable
    def test_game_starts_with_mock_word(self, mock_word):
        game = HangmanGame(mock_word(), stats=GameStats())
        self.assertEqual(game.word, "PYTHON")

    def test_correct_guess(self):                                                               # Tests the core game logic that guessing a correct letter updates the game state and returns the correct success message
        game = HangmanGame("PYTHON", stats=GameStats())
        message = game.guess_letter("P")
        self.assertIn("Good job", message)
        self.assertIn("P", game.word_completion)

if __name__ == "__main__":
    unittest.main()
