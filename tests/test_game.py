#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Tic-Tac-Toe game.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path so we can import game
sys.path.insert(0, str(Path(__file__).parent.parent))

from game import Board, AI, ScoreManager, Game, LANG


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def board():
    return Board()


@pytest.fixture
def empty_board():
    return Board()


@pytest.fixture
def full_board_no_winner():
    """A full board with no winner (draw)."""
    b = Board()
    # X O X
    # X O O
    # O X X
    moves = [(0, "X"), (1, "O"), (2, "X"),
             (3, "X"), (4, "O"), (5, "O"),
             (6, "O"), (7, "X"), (8, "X")]
    for idx, mark in moves:
        b.place(idx, mark)
    return b


@pytest.fixture
def score_manager():
    """ScoreManager with a temp file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{}")
        tmp_path = Path(f.name)
    sm = ScoreManager(filepath=tmp_path)
    yield sm
    # Cleanup
    if tmp_path.exists():
        tmp_path.unlink()


# ── Board Tests ───────────────────────────────────────────────────

class TestBoardInitialization:
    def test_board_has_9_empty_cells(self, board):
        assert len(board.cells) == 9
        assert all(c == Board.EMPTY for c in board.cells)
        assert board.move_count == 0

    def test_board_reset(self, board):
        board.place(0, "X")
        board.place(4, "O")
        board.reset()
        assert all(c == Board.EMPTY for c in board.cells)
        assert board.move_count == 0

    def test_clone_is_independent(self, board):
        board.place(0, "X")
        clone = board.clone()
        assert clone.cells[0] == "X"
        clone.place(1, "O")
        assert board.cells[1] == Board.EMPTY
        assert clone.cells[1] == "O"

    def test_is_full_returns_false_initially(self, board):
        assert not board.is_full()

    def test_is_full_returns_true_when_full(self, full_board_no_winner):
        assert full_board_no_winner.is_full()

    def test_is_empty_returns_correctly(self, board):
        assert board.is_empty(0)
        board.place(0, "X")
        assert not board.is_empty(0)

    def test_available_returns_all_initially(self, board):
        assert board.available() == list(range(9))

    def test_available_after_moves(self, board):
        board.place(0, "X")
        board.place(4, "O")
        assert board.available() == [1, 2, 3, 5, 6, 7, 8]

    def test_place_valid(self, board):
        assert board.place(0, "X")
        assert board.cells[0] == "X"
        assert board.move_count == 1

    def test_place_invalid_index(self, board):
        assert not board.place(9, "X")
        assert board.move_count == 0

    def test_place_occupied(self, board):
        board.place(0, "X")
        assert not board.place(0, "O")
        assert board.cells[0] == "X"

    def test_undo(self, board):
        board.place(0, "X")
        board.undo(0)
        assert board.cells[0] == Board.EMPTY
        assert board.move_count == 0

    def test_get_state(self, board):
        board.place(0, "X")
        board.place(1, "O")
        state = board.get_state()
        assert state[0] == "X"
        assert state[1] == "O"
        assert all(state[i] == Board.EMPTY for i in range(2, 9))


# ── Win Detection Tests ──────────────────────────────────────────

class TestWinDetection:
    def _setup_board(self, moves):
        b = Board()
        for idx, mark in moves:
            b.place(idx, mark)
        return b

    def test_win_top_row(self):
        b = self._setup_board([(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")])
        assert b.check_win() == "X"

    def test_win_middle_row(self):
        b = self._setup_board([(3, "X"), (0, "O"), (4, "X"), (1, "O"), (5, "X")])
        assert b.check_win() == "X"

    def test_win_bottom_row(self):
        b = self._setup_board([(6, "X"), (0, "O"), (7, "X"), (1, "O"), (8, "X")])
        assert b.check_win() == "X"

    def test_win_left_col(self):
        b = self._setup_board([(0, "X"), (1, "O"), (3, "X"), (2, "O"), (6, "X")])
        assert b.check_win() == "X"

    def test_win_middle_col(self):
        b = self._setup_board([(1, "X"), (0, "O"), (4, "X"), (2, "O"), (7, "X")])
        assert b.check_win() == "X"

    def test_win_right_col(self):
        b = self._setup_board([(2, "X"), (0, "O"), (5, "X"), (1, "O"), (8, "X")])
        assert b.check_win() == "X"

    def test_win_diagonal_top_left(self):
        b = self._setup_board([(0, "X"), (1, "O"), (4, "X"), (2, "O"), (8, "X")])
        assert b.check_win() == "X"

    def test_win_diagonal_top_right(self):
        b = self._setup_board([(2, "X"), (0, "O"), (4, "X"), (1, "O"), (6, "X")])
        assert b.check_win() == "X"

    def test_win_o_player(self):
        b = self._setup_board([(0, "X"), (3, "O"), (1, "X"), (4, "O"), (8, "X"), (5, "O")])
        assert b.check_win() == "O"

    def test_no_win_early_game(self, board):
        board.place(0, "X")
        board.place(4, "O")
        assert board.check_win() is None

    def test_no_win_draw(self, full_board_no_winner):
        assert full_board_no_winner.check_win() is None

    def test_check_win_specific_mark(self):
        b = self._setup_board([(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")])
        assert b.check_win("X") == "X"
        assert b.check_win("O") is None


# ── Draw Detection Tests ─────────────────────────────────────────

class TestDrawDetection:
    def test_draw_detection(self, full_board_no_winner):
        assert full_board_no_winner.check_draw()

    def test_not_draw_when_winner(self):
        b = Board()
        moves = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
        for idx, mark in moves:
            b.place(idx, mark)
        assert not b.check_draw()

    def test_not_draw_when_moves_left(self, board):
        board.place(0, "X")
        assert not board.check_draw()

    def test_draw_full_board_no_winner(self, full_board_no_winner):
        assert full_board_no_winner.is_full()
        assert full_board_no_winner.check_win() is None
        assert full_board_no_winner.check_draw()


# ── AI Tests ──────────────────────────────────────────────────────

class TestAI:
    def test_ai_easy_returns_valid_move(self):
        ai = AI("easy")
        b = Board()
        move = ai.get_move(b, "O")
        assert move in range(9)
        assert b.is_empty(move)

    def test_ai_easy_returns_none_on_full(self, full_board_no_winner):
        ai = AI("easy")
        move = ai.get_move(full_board_no_winner, "O")
        assert move is None

    def test_ai_hard_returns_valid_move(self):
        ai = AI("hard")
        b = Board()
        move = ai.get_move(b, "O")
        assert move in range(9)
        assert b.is_empty(move)

    def test_ai_hard_takes_winning_move(self):
        """AI should take an immediate winning move."""
        ai = AI("hard")
        b = Board()
        # X at 0, 1; O at 3, 4. AI as X should play 2 to win.
        b.place(0, "X")
        b.place(3, "O")
        b.place(1, "X")
        b.place(4, "O")
        move = ai.get_move(b, "X")
        assert move == 2, f"Expected winning move at 2, got {move}"

    def test_ai_hard_blocks_opponent_win(self):
        """AI should block opponent's winning move."""
        ai = AI("hard")
        b = Board()
        # X at 0, 1 (about to win); O at 3. AI as O should block at 2.
        b.place(0, "X")
        b.place(3, "O")
        b.place(1, "X")
        move = ai.get_move(b, "O")
        assert move == 2, f"Expected blocking move at 2, got {move}"

    def test_ai_hard_never_loses_as_o(self):
        """AI playing as O on a 3x3 board should never lose (always at least draw)."""
        ai = AI("hard")
        b = Board()

        # Simulate all possible first moves for X and verify AI (O) never loses
        for first_move in range(9):
            b.reset()
            b.place(first_move, "X")

            # Play out the game with AI as O
            game_over = False
            while not game_over:
                if b.move_count % 2 == 1:  # O's turn (AI)
                    move = ai.get_move(b, "O")
                    if move is None:
                        break
                    b.place(move, "O")
                else:  # X's turn - use a reasonable response
                    avail = b.available()
                    if not avail:
                        break
                    # Try to find a winning move for X, else pick first available
                    x_move = None
                    for m in avail:
                        b.place(m, "X")
                        if b.check_win("X"):
                            x_move = m
                            b.undo(m)
                            break
                        b.undo(m)
                    if x_move is None:
                        x_move = avail[0]
                    b.place(x_move, "X")

                winner = b.check_win()
                if winner == "O":
                    # AI won - that's fine
                    game_over = True
                elif winner == "X":
                    pytest.fail(f"AI (O) lost when X started at position {first_move + 1}")
                elif b.check_draw():
                    game_over = True

    def test_ai_medium_returns_valid_move(self):
        ai = AI("medium")
        b = Board()
        for _ in range(20):  # Test multiple times due to randomness
            b.reset()
            move = ai.get_move(b, "X")
            assert move in range(9)
            assert b.is_empty(move)

    def test_ai_hard_center_opening(self):
        """AI as X should prefer center (4) as opening move."""
        ai = AI("hard")
        b = Board()
        move = ai.get_move(b, "X")
        # Center is the optimal opening move
        assert move == 4, f"Expected center (4), got {move}"


# ── Score Manager Tests ──────────────────────────────────────────

class TestScoreManager:
    def test_load_empty(self, score_manager):
        assert score_manager.scores == {}

    def test_record_win(self, score_manager):
        score_manager.record_win("Alice")
        assert score_manager.scores["Alice"]["wins"] == 1
        assert score_manager.scores["Alice"]["losses"] == 0
        assert score_manager.scores["Alice"]["draws"] == 0

    def test_record_loss(self, score_manager):
        score_manager.record_loss("Bob")
        assert score_manager.scores["Bob"]["losses"] == 1

    def test_record_draw(self, score_manager):
        score_manager.record_draw("Charlie")
        assert score_manager.scores["Charlie"]["draws"] == 1

    def test_multiple_records(self, score_manager):
        score_manager.record_win("Alice")
        score_manager.record_win("Alice")
        score_manager.record_loss("Alice")
        score_manager.record_draw("Alice")
        assert score_manager.scores["Alice"]["wins"] == 2
        assert score_manager.scores["Alice"]["losses"] == 1
        assert score_manager.scores["Alice"]["draws"] == 1

    def test_get_player_stats(self, score_manager):
        score_manager.record_win("Alice")
        stats = score_manager.get_player_stats("Alice")
        assert stats["wins"] == 1

    def test_get_player_stats_new(self, score_manager):
        stats = score_manager.get_player_stats("Nobody")
        assert stats["wins"] == 0
        assert stats["losses"] == 0
        assert stats["draws"] == 0

    def test_leaderboard_order_by_win_rate(self, score_manager):
        score_manager.record_win("Alice")  # 100%
        score_manager.record_win("Bob")    # 100% but fewer wins
        score_manager.record_win("Bob")
        score_manager.record_loss("Charlie")  # 0%
        lb = score_manager.get_leaderboard()
        # Bob: 2 wins, 0 losses, 0 draws, 100% -> first
        # Alice: 1 win, 0 losses, 0 draws, 100% -> second
        # Charlie: 0 wins, 1 loss, 0 draws, 0% -> third
        assert lb[0][0] == "Bob"
        assert lb[1][0] == "Alice"
        assert lb[2][0] == "Charlie"

    def test_leaderboard_empty(self, score_manager):
        lb = score_manager.get_leaderboard()
        assert lb == []

    def test_persistence(self, score_manager):
        score_manager.record_win("Alice")
        # Create a new ScoreManager pointing to the same file
        sm2 = ScoreManager(filepath=score_manager.filepath)
        assert sm2.scores["Alice"]["wins"] == 1

    def test_persistence_with_multiple_players(self, score_manager):
        score_manager.record_win("Alice")
        score_manager.record_loss("Bob")
        score_manager.record_draw("Charlie")
        sm2 = ScoreManager(filepath=score_manager.filepath)
        assert sm2.scores["Alice"]["wins"] == 1
        assert sm2.scores["Bob"]["losses"] == 1
        assert sm2.scores["Charlie"]["draws"] == 1


# ── Language Tests ────────────────────────────────────────────────

class TestLanguage:
    def test_chinese_default(self):
        game = Game()
        assert game.lang == "zh"

    def test_toggle_language(self):
        game = Game()
        assert game.lang == "zh"
        game.toggle_lang()
        assert game.lang == "en"
        game.toggle_lang()
        assert game.lang == "zh"

    def test_translation_exists_for_all_keys(self):
        """All keys in zh should exist in en."""
        for key in LANG["zh"]:
            assert key in LANG["en"], f"Missing key '{key}' in English translations"

    def test_translation_format_strings(self):
        """Test that format strings work correctly."""
        text = LANG["zh"]["invalid_move"].format(cell="5")
        assert "5" in text

    def test_lang_switched_message(self):
        game = Game()
        game.lang = "en"
        assert game.tr("lang_switched") == "Language switched to English"
        game.lang = "zh"
        assert game.tr("lang_switched") == "语言已切换为中文"

    def test_player_turn_format(self):
        game = Game()
        game.lang = "zh"
        text = game.tr("player_turn", player="Alice", mark="X")
        assert "Alice" in text
        assert "X" in text


# ── Game Logic Tests ─────────────────────────────────────────────

class TestGameLogic:
    def test_win_condition_rows(self):
        """Test all 3 row win conditions."""
        for row in range(3):
            b = Board()
            start = row * 3
            for col in range(3):
                b.place(start + col, "X")
                if col < 2:
                    # Place O in a non-interfering position
                    b.place((row + 1) % 3 * 3 + col, "O")
            assert b.check_win() == "X", f"Row {row} win not detected"

    def test_win_condition_cols(self):
        """Test all 3 column win conditions."""
        for col in range(3):
            b = Board()
            for row in range(3):
                b.place(row * 3 + col, "X")
                if row < 2:
                    b.place(row * 3 + (col + 1) % 3, "O")
            assert b.check_win() == "X", f"Col {col} win not detected"

    def test_win_condition_diagonals(self):
        """Test both diagonal win conditions."""
        # Top-left to bottom-right
        b = Board()
        for i in range(3):
            b.place(i * 4, "X")
            if i < 2:
                b.place(i * 4 + 1, "O")
        assert b.check_win() == "X"

        # Top-right to bottom-left
        b = Board()
        for i in range(3):
            b.place(i * 2 + 2, "X")
            if i < 2:
                b.place(i * 2, "O")
        assert b.check_win() == "X"

    def test_alternating_turns(self):
        """Test that moves alternate between X and O correctly."""
        b = Board()
        b.place(0, "X")
        assert b.move_count == 1
        b.place(1, "O")
        assert b.move_count == 2
        b.place(2, "X")
        assert b.move_count == 3

    def test_board_state_after_undo(self):
        b = Board()
        b.place(0, "X")
        b.place(1, "O")
        b.undo(1)
        assert b.cells[1] == Board.EMPTY
        assert b.move_count == 1

    def test_available_correct_after_moves(self):
        b = Board()
        b.place(0, "X")
        b.place(4, "O")
        b.place(8, "X")
        avail = b.available()
        assert 0 not in avail
        assert 4 not in avail
        assert 8 not in avail
        assert len(avail) == 6


# ── Input Validation Tests ───────────────────────────────────────

class TestInputValidation:
    def test_invalid_index_rejected(self, board):
        assert not board.place(-1, "X")
        assert not board.place(9, "X")
        assert not board.place(100, "X")

    def test_occupied_cell_rejected(self, board):
        board.place(0, "X")
        assert not board.place(0, "O")

    def test_empty_string_not_a_move(self):
        """Verify that empty string is not a valid move number."""
        assert not "".isdigit()

    def test_non_numeric_rejected(self):
        assert not "abc".isdigit()
        assert not "5a".isdigit()


# ── Sound Toggle Tests ───────────────────────────────────────────

class TestSoundToggle:
    def test_sound_default_on(self):
        game = Game()
        assert game.sound_enabled is True

    def test_toggle_sound(self):
        game = Game()
        game.toggle_sound()
        assert game.sound_enabled is False
        game.toggle_sound()
        assert game.sound_enabled is True


# ── Session Score Tests ──────────────────────────────────────────

class TestSessionScores:
    def test_session_score_tracking(self):
        game = Game()
        game._session_win("Alice")
        assert game.session_scores["Alice"]["wins"] == 1

    def test_session_score_multiple(self):
        game = Game()
        game._session_win("Alice")
        game._session_loss("Alice")
        game._session_draw("Alice")
        assert game.session_scores["Alice"]["wins"] == 1
        assert game.session_scores["Alice"]["losses"] == 1
        assert game.session_scores["Alice"]["draws"] == 1


# ── Board Display Tests ──────────────────────────────────────────

class TestBoardDisplay:
    def test_display_empty_board(self, board):
        display = board.display()
        assert "1" in display
        assert "2" in display
        assert "9" in display

    def test_display_with_moves(self, board):
        board.place(0, "X")
        board.place(4, "O")
        display = board.display()
        assert "X" in display
        assert "O" in display


if __name__ == "__main__":
    pytest.main(["-v", __file__])
