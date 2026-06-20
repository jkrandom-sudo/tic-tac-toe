#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe 井字棋
Console-based Tic-Tac-Toe game with AI, score tracking, and bilingual support.
"""

import json
import os
import random
import sys
import time
from pathlib import Path

# ── ANSI Color Codes ──────────────────────────────────────────────
BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"  # clear screen + home cursor

# ── Platform detection ────────────────────────────────────────────
IS_WINDOWS = sys.platform.startswith("win")
CLEAR_CMD = "cls" if IS_WINDOWS else "clear"

# ── Language Strings ──────────────────────────────────────────────
LANG = {
    "zh": {
        "title": "井字棋",
        "menu_title": "=== 井字棋 ===",
        "menu_new": "[1] 新游戏",
        "menu_leaderboard": "[2] 排行榜",
        "menu_lang": "[3] 语言切换",
        "menu_help": "[4] 帮助",
        "menu_quit": "[5] 退出",
        "select_mode": "请选择游戏模式：",
        "mode_hvh": "[1] 人人对战",
        "mode_hva_first": "[2] 人机对战（玩家先手）",
        "mode_ai_first": "[3] 人机对战（AI先手）",
        "select_diff": "请选择AI难度：",
        "diff_easy": "[1] 简单（随机）",
        "diff_medium": "[2] 中等（混合）",
        "diff_hard": "[3] 困难（Minimax）",
        "enter_name_x": "请输入玩家X的名字：",
        "enter_name_o": "请输入玩家O的名字：",
        "enter_name": "请输入你的名字：",
        "your_turn": "轮到你了",
        "ai_thinking": "AI思考中",
        "player_turn": "轮到 {player}（{mark}）",
        "enter_move": "请输入格子编号（1-9），或输入命令：",
        "invalid_move": "无效移动！格子 {cell} 已被占用或不存在。",
        "available_cells": "可用格子：{cells}",
        "win_msg": "{player} 获胜！",
        "draw_msg": "平局！",
        "play_again": "再来一局？(y/n)：",
        "back_menu": "返回主菜单",
        "leaderboard_title": "=== 排行榜 ===",
        "leaderboard_header": "{:<12} {:<6} {:<6} {:<6} {:<8}".format("玩家", "胜", "负", "平", "胜率"),
        "leaderboard_row": "{:<12} {:<6} {:<6} {:<6} {:<7.1%}",
        "no_scores": "暂无游戏记录。",
        "help_title": "=== 帮助 ===",
        "help_rules": "游戏规则：",
        "help_rules1": "1. 棋盘为3x3网格，玩家轮流落子。",
        "help_rules2": "2. 玩家X（蓝色）先手，玩家O（红色）后手。",
        "help_rules3": "3. 横、竖、斜任意方向连成三子即获胜。",
        "help_rules4": "4. 棋盘满且无人获胜则为平局。",
        "help_input": "输入方式：",
        "help_input1": "输入数字1-9对应棋盘位置（从左到右，从上到下）。",
        "help_input2": "例如：5 表示棋盘正中央。",
        "help_commands": "游戏内命令：",
        "help_cmd_quit": "  quit  - 退出游戏",
        "help_cmd_menu": "  menu  - 返回主菜单",
        "help_cmd_help": "  help  - 显示此帮助",
        "help_cmd_lang": "  lang  - 切换语言",
        "help_cmd_score": "  score - 显示当前会话分数",
        "help_cmd_sound": "  sound - 切换音效",
        "help_ai": "AI难度：",
        "help_ai1": "  简单 - AI随机落子",
        "help_ai2": "  中等 - AI混合策略（50% minimax + 50% 随机）",
        "help_ai3": "  困难 - AI使用Minimax算法（永不输）",
        "help_scoring": "评分规则：",
        "help_scoring1": "  胜 = +1分，负 = 0分，平 = +0.5分",
        "help_scoring2": "  排行榜按胜率排序。",
        "press_enter": "按回车键继续...",
        "lang_switched": "语言已切换为中文",
        "sound_on": "音效已开启",
        "sound_off": "音效已关闭",
        "score_title": "=== 当前会话分数 ===",
        "score_x": "玩家X：{name} - 胜：{w} 负：{l} 平：{d}",
        "score_o": "玩家O：{name} - 胜：{w} 负：{l} 平：{d}",
        "mode_hvh_str": "人人对战",
        "mode_hva_str": "人机对战（玩家先手）",
        "mode_ai_first_str": "人机对战（AI先手）",
        "diff_str": "难度：{diff}",
        "move_count": "第 {n} 步",
        "current_player": "当前：{player}",
        "game_over": "游戏结束！",
        "ai_wins": "AI 获胜！",
        "you_win": "你获胜！",
        "quit_game": "感谢游玩！再见！",
        "invalid_choice": "无效选择，请重新输入。",
        "enter_name_ai": "请输入AI的名字（默认：AI）：",
        "ai_default_name": "AI",
        "cell_occupied": "格子 {cell} 已被 {mark} 占据。",
        "leaderboard_rank": "第{n}名",
        "sound_effect_play": "♪",
        "win_animation": "恭喜 {player}！",
    },
    "en": {
        "title": "Tic-Tac-Toe",
        "menu_title": "=== Tic-Tac-Toe ===",
        "menu_new": "[1] New Game",
        "menu_leaderboard": "[2] Leaderboard",
        "menu_lang": "[3] Language",
        "menu_help": "[4] Help",
        "menu_quit": "[5] Quit",
        "select_mode": "Select game mode:",
        "mode_hvh": "[1] Human vs Human",
        "mode_hva_first": "[2] Human vs AI (You first)",
        "mode_ai_first": "[3] Human vs AI (AI first)",
        "select_diff": "Select AI difficulty:",
        "diff_easy": "[1] Easy (Random)",
        "diff_medium": "[2] Medium (Mixed)",
        "diff_hard": "[3] Hard (Minimax)",
        "enter_name_x": "Enter player X name:",
        "enter_name_o": "Enter player O name:",
        "enter_name": "Enter your name:",
        "your_turn": "Your turn",
        "ai_thinking": "AI thinking",
        "player_turn": "{player}'s turn ({mark})",
        "enter_move": "Enter cell number (1-9), or enter a command:",
        "invalid_move": "Invalid move! Cell {cell} is occupied or does not exist.",
        "available_cells": "Available cells: {cells}",
        "win_msg": "{player} wins!",
        "draw_msg": "Draw!",
        "play_again": "Play again? (y/n): ",
        "back_menu": "Return to main menu",
        "leaderboard_title": "=== Leaderboard ===",
        "leaderboard_header": "{:<12} {:<6} {:<6} {:<6} {:<8}".format("Player", "Wins", "Loss", "Draw", "Win%"),
        "leaderboard_row": "{:<12} {:<6} {:<6} {:<6} {:<7.1%}",
        "no_scores": "No game records yet.",
        "help_title": "=== Help ===",
        "help_rules": "Game Rules:",
        "help_rules1": "1. The board is a 3x3 grid. Players take turns placing marks.",
        "help_rules2": "2. Player X (blue) goes first, Player O (red) goes second.",
        "help_rules3": "3. Three in a row (horizontal, vertical, or diagonal) wins.",
        "help_rules4": "4. If the board is full with no winner, it's a draw.",
        "help_input": "Input:",
        "help_input1": "Enter numbers 1-9 corresponding to board positions (left to right, top to bottom).",
        "help_input2": "Example: 5 means the center cell.",
        "help_commands": "In-game commands:",
        "help_cmd_quit": "  quit  - Exit the game",
        "help_cmd_menu": "  menu  - Return to main menu",
        "help_cmd_help": "  help  - Show this help",
        "help_cmd_lang": "  lang  - Toggle language",
        "help_cmd_score": "  score - Show current session scores",
        "help_cmd_sound": "  sound - Toggle sound effects",
        "help_ai": "AI Difficulty:",
        "help_ai1": "  Easy - AI makes random moves",
        "help_ai2": "  Medium - AI uses mixed strategy (50% minimax + 50% random)",
        "help_ai3": "  Hard - AI uses Minimax algorithm (never loses)",
        "help_scoring": "Scoring:",
        "help_scoring1": "  Win = +1 point, Loss = 0 points, Draw = +0.5 points",
        "help_scoring2": "  Leaderboard sorted by win rate.",
        "press_enter": "Press Enter to continue...",
        "lang_switched": "Language switched to English",
        "sound_on": "Sound effects ON",
        "sound_off": "Sound effects OFF",
        "score_title": "=== Current Session Scores ===",
        "score_x": "Player X: {name} - W: {w} L: {l} D: {d}",
        "score_o": "Player O: {name} - W: {w} L: {l} D: {d}",
        "mode_hvh_str": "Human vs Human",
        "mode_hva_str": "Human vs AI (You first)",
        "mode_ai_first_str": "Human vs AI (AI first)",
        "diff_str": "Difficulty: {diff}",
        "move_count": "Move {n}",
        "current_player": "Current: {player}",
        "game_over": "Game Over!",
        "ai_wins": "AI wins!",
        "you_win": "You win!",
        "quit_game": "Thanks for playing! Goodbye!",
        "invalid_choice": "Invalid choice, please try again.",
        "enter_name_ai": "Enter AI name (default: AI): ",
        "ai_default_name": "AI",
        "cell_occupied": "Cell {cell} is already occupied by {mark}.",
        "leaderboard_rank": "Rank #{n}",
        "sound_effect_play": "♪",
        "win_animation": "Congratulations {player}!",
    },
}

# ── Board ─────────────────────────────────────────────────────────
class Board:
    """Tic-Tac-Toe board (3x3)."""

    EMPTY = " "
    MARKS = ("X", "O")

    def __init__(self):
        self.cells = [self.EMPTY] * 9
        self.move_count = 0

    def reset(self):
        self.cells = [self.EMPTY] * 9
        self.move_count = 0

    def clone(self):
        b = Board()
        b.cells = self.cells[:]
        b.move_count = self.move_count
        return b

    def is_full(self):
        return self.move_count == 9

    def is_empty(self, idx):
        return self.cells[idx] == self.EMPTY

    def place(self, idx, mark):
        if not (0 <= idx < 9) or not self.is_empty(idx):
            return False
        self.cells[idx] = mark
        self.move_count += 1
        return True

    def undo(self, idx):
        self.cells[idx] = self.EMPTY
        self.move_count -= 1

    def available(self):
        return [i for i, c in enumerate(self.cells) if c == self.EMPTY]

    def check_win(self, mark=None):
        """Check if the given mark (or any mark) has won. Returns the winning mark or None."""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6],              # diagonals
        ]
        for pattern in win_patterns:
            a, b, c = pattern
            if self.cells[a] != self.EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                if mark is None or self.cells[a] == mark:
                    return self.cells[a]
        return None

    def check_draw(self):
        return self.is_full() and self.check_win() is None

    def get_state(self):
        return tuple(self.cells)

    def display(self, lang="zh"):
        """Return a colored string representation of the board."""
        lines = []
        for row_idx in range(3):
            row_cells = []
            for col_idx in range(3):
                idx = row_idx * 3 + col_idx
                cell = self.cells[idx]
                if cell == "X":
                    row_cells.append(f"{BLUE}X{RESET}")
                elif cell == "O":
                    row_cells.append(f"{RED}O{RESET}")
                else:
                    row_cells.append(str(idx + 1))
            sep = f" {WHITE}|{RESET} "
            lines.append(f" {WHITE}{row_cells[0]}{RESET} {sep} {WHITE}{row_cells[1]}{RESET} {sep} {WHITE}{row_cells[2]}{RESET}")
            if row_idx < 2:
                lines.append(f"{WHITE}---+---+---{RESET}")
        return "\n".join(lines)


# ── AI ────────────────────────────────────────────────────────────
class AI:
    """AI player using minimax with alpha-beta pruning."""

    def __init__(self, difficulty="hard"):
        self.difficulty = difficulty  # "easy", "medium", "hard"

    def get_move(self, board, ai_mark):
        """Return the best move index for the AI."""
        avail = board.available()
        if not avail:
            return None

        if self.difficulty == "easy":
            return random.choice(avail)

        if self.difficulty == "medium":
            if random.random() < 0.5:
                return random.choice(avail)
            # Fall through to minimax for the other 50%

        # Hard or medium's minimax branch
        human_mark = "O" if ai_mark == "X" else "X"
        best_score = -float("inf")
        best_move = avail[0]
        alpha = -float("inf")
        beta = float("inf")

        # Prefer center, then corners, then edges when scores are equal
        center = 4
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]

        def move_priority(m):
            if m == center:
                return 0
            if m in corners:
                return 1
            return 2  # edges

        for move in avail:
            board.place(move, ai_mark)
            score = self._minimax(board, 0, False, human_mark, ai_mark, alpha, beta)
            board.undo(move)
            if score > best_score or (score == best_score and move_priority(move) < move_priority(best_move)):
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        return best_move

    def _minimax(self, board, depth, is_maximizing, human_mark, ai_mark, alpha, beta):
        """Minimax with alpha-beta pruning."""
        winner = board.check_win()
        if winner == ai_mark:
            return 10 - depth
        if winner == human_mark:
            return depth - 10
        if board.check_draw():
            return 0

        avail = board.available()
        if is_maximizing:
            best = -float("inf")
            for move in avail:
                board.place(move, ai_mark)
                val = self._minimax(board, depth + 1, False, human_mark, ai_mark, alpha, beta)
                board.undo(move)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float("inf")
            for move in avail:
                board.place(move, human_mark)
                val = self._minimax(board, depth + 1, True, human_mark, ai_mark, alpha, beta)
                board.undo(move)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best


# ── Score Manager ─────────────────────────────────────────────────
SCORES_FILE = Path(__file__).parent / "scores.json"


class ScoreManager:
    """Manage player scores persisted to scores.json."""

    def __init__(self, filepath=None):
        self.filepath = filepath or SCORES_FILE
        self.scores = self._load()

    def _load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=2)

    def _ensure_player(self, name):
        if name not in self.scores:
            self.scores[name] = {"wins": 0, "losses": 0, "draws": 0}

    def record_win(self, name):
        self._ensure_player(name)
        self.scores[name]["wins"] += 1
        self._save()

    def record_loss(self, name):
        self._ensure_player(name)
        self.scores[name]["losses"] += 1
        self._save()

    def record_draw(self, name):
        self._ensure_player(name)
        self.scores[name]["draws"] += 1
        self._save()

    def get_leaderboard(self):
        """Return sorted list of (name, wins, losses, draws, win_rate)."""
        result = []
        for name, data in self.scores.items():
            total = data["wins"] + data["losses"] + data["draws"]
            if total == 0:
                win_rate = 0.0
            else:
                win_rate = (data["wins"] + 0.5 * data["draws"]) / total
            result.append((name, data["wins"], data["losses"], data["draws"], win_rate))
        result.sort(key=lambda x: (-x[4], -x[1], x[0]))
        return result

    def get_player_stats(self, name):
        self._ensure_player(name)
        return self.scores[name]


# ── Game ──────────────────────────────────────────────────────────
class Game:
    """Main game controller."""

    def __init__(self):
        self.board = Board()
        self.score_mgr = ScoreManager()
        self.lang = "zh"
        self.sound_enabled = True
        self.mode = None  # "hvh", "hva_first", "ai_first"
        self.difficulty = "hard"
        self.player_x_name = ""
        self.player_o_name = ""
        self.ai = None
        self.session_scores = {}  # name -> {"wins": 0, "losses": 0, "draws": 0}
        self.running = True

    # ── Helpers ────────────────────────────────────────────────────

    def tr(self, key, **kwargs):
        """Translate a key using current language."""
        text = LANG[self.lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text

    def clear_screen(self):
        os.system(CLEAR_CMD)

    def beep(self):
        if self.sound_enabled:
            sys.stdout.write("\x07")
            sys.stdout.flush()

    def delay(self, seconds=0.5):
        time.sleep(seconds)

    def print_banner(self):
        title = self.tr("title")
        print(f"{CYAN}{BOLD}{'=' * 40}{RESET}")
        print(f"{CYAN}{BOLD}{title:^40}{RESET}")
        print(f"{CYAN}{BOLD}{'=' * 40}{RESET}")

    def get_input(self, prompt):
        """Get user input, stripping whitespace."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def show_status_bar(self):
        """Show status bar below the board."""
        mode_str = self.tr(
            "mode_hvh_str" if self.mode == "hvh" else
            "mode_hva_str" if self.mode == "hva_first" else
            "mode_ai_first_str"
        )
        if self.mode != "hvh":
            diff_names = {"easy": "简单/Easy", "medium": "中等/Medium", "hard": "困难/Hard"}
            mode_str += f" | {self.tr('diff_str', diff=diff_names[self.difficulty])}"

        current = self.board.move_count % 2
        mark = "X" if current == 0 else "O"
        if self.mode == "hvh":
            name = self.player_x_name if mark == "X" else self.player_o_name
        elif self.mode == "hva_first":
            name = self.player_x_name if mark == "X" else self.tr("ai_default_name")
        else:
            name = self.tr("ai_default_name") if mark == "X" else self.player_o_name

        status = f"{self.tr('current_player', player=name)} ({mark}) | {self.tr('move_count', n=self.board.move_count)} | {mode_str}"
        print(f"\n{YELLOW}{status}{RESET}\n")

    # ── Session Score Tracking ─────────────────────────────────────

    def _session_ensure(self, name):
        if name not in self.session_scores:
            self.session_scores[name] = {"wins": 0, "losses": 0, "draws": 0}

    def _session_win(self, name):
        self._session_ensure(name)
        self.session_scores[name]["wins"] += 1

    def _session_loss(self, name):
        self._session_ensure(name)
        self.session_scores[name]["losses"] += 1

    def _session_draw(self, name):
        self._session_ensure(name)
        self.session_scores[name]["draws"] += 1

    def show_session_scores(self):
        self.clear_screen()
        print(f"\n{CYAN}{BOLD}{self.tr('score_title')}{RESET}\n")
        for name, data in self.session_scores.items():
            print(f"  {name}: {data['wins']}W / {data['losses']}L / {data['draws']}D")
        print()
        self.get_input(self.tr("press_enter"))

    # ── Sound ──────────────────────────────────────────────────────

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        print(self.tr("sound_on") if self.sound_enabled else self.tr("sound_off"))
        self.delay(0.5)

    # ── Language ───────────────────────────────────────────────────

    def toggle_lang(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        print(self.tr("lang_switched"))
        self.delay(0.5)

    # ── Menu ───────────────────────────────────────────────────────

    def show_menu(self):
        while self.running:
            self.clear_screen()
            self.print_banner()
            print()
            print(f"  {self.tr('menu_new')}")
            print(f"  {self.tr('menu_leaderboard')}")
            print(f"  {self.tr('menu_lang')}")
            print(f"  {self.tr('menu_help')}")
            print(f"  {self.tr('menu_quit')}")
            print()
            choice = self.get_input("> ")

            if choice == "1":
                self.start_new_game()
            elif choice == "2":
                self.show_leaderboard()
            elif choice == "3":
                self.toggle_lang()
            elif choice == "4":
                self.show_help()
            elif choice == "5" or choice.lower() == "quit":
                self.running = False
                self.clear_screen()
                print(self.tr("quit_game"))
                self.beep()
                self.delay(0.5)
                return
            else:
                print(self.tr("invalid_choice"))
                self.delay(0.5)

    def show_leaderboard(self):
        self.clear_screen()
        print(f"\n{CYAN}{BOLD}{self.tr('leaderboard_title')}{RESET}\n")
        entries = self.score_mgr.get_leaderboard()
        if not entries:
            print(f"  {self.tr('no_scores')}")
        else:
            print(f"  {self.tr('leaderboard_header')}")
            print(f"  {'-' * 40}")
            for i, (name, w, l, d, wr) in enumerate(entries, 1):
                print(f"  {self.tr('leaderboard_row').format(name, w, l, d, wr)}")
        print()
        self.get_input(self.tr("press_enter"))

    def show_help(self):
        self.clear_screen()
        print(f"\n{CYAN}{BOLD}{self.tr('help_title')}{RESET}\n")
        print(f"  {BOLD}{self.tr('help_rules')}{RESET}")
        print(f"    {self.tr('help_rules1')}")
        print(f"    {self.tr('help_rules2')}")
        print(f"    {self.tr('help_rules3')}")
        print(f"    {self.tr('help_rules4')}")
        print()
        print(f"  {BOLD}{self.tr('help_input')}{RESET}")
        print(f"    {self.tr('help_input1')}")
        print(f"    {self.tr('help_input2')}")
        print()
        print(f"  {BOLD}{self.tr('help_commands')}{RESET}")
        print(f"    {self.tr('help_cmd_quit')}")
        print(f"    {self.tr('help_cmd_menu')}")
        print(f"    {self.tr('help_cmd_help')}")
        print(f"    {self.tr('help_cmd_lang')}")
        print(f"    {self.tr('help_cmd_score')}")
        print(f"    {self.tr('help_cmd_sound')}")
        print()
        print(f"  {BOLD}{self.tr('help_ai')}{RESET}")
        print(f"    {self.tr('help_ai1')}")
        print(f"    {self.tr('help_ai2')}")
        print(f"    {self.tr('help_ai3')}")
        print()
        print(f"  {BOLD}{self.tr('help_scoring')}{RESET}")
        print(f"    {self.tr('help_scoring1')}")
        print(f"    {self.tr('help_scoring2')}")
        print()
        self.get_input(self.tr("press_enter"))

    # ── New Game Setup ─────────────────────────────────────────────

    def start_new_game(self):
        self.clear_screen()
        print(f"\n{CYAN}{BOLD}{self.tr('select_mode')}{RESET}\n")
        print(f"  {self.tr('mode_hvh')}")
        print(f"  {self.tr('mode_hva_first')}")
        print(f"  {self.tr('mode_ai_first')}")
        print()
        choice = self.get_input("> ")

        if choice == "1":
            self.mode = "hvh"
            self.clear_screen()
            self.player_x_name = self.get_input(f"  {self.tr('enter_name_x')}: ") or "Player X"
            self.player_o_name = self.get_input(f"  {self.tr('enter_name_o')}: ") or "Player O"
            self.play_hvh()
        elif choice == "2":
            self.mode = "hva_first"
            self.setup_ai_game()
            self.play_hva(player_first=True)
        elif choice == "3":
            self.mode = "ai_first"
            self.setup_ai_game()
            self.play_hva(player_first=False)
        else:
            print(self.tr("invalid_choice"))
            self.delay(0.5)

    def setup_ai_game(self):
        self.clear_screen()
        print(f"\n{CYAN}{BOLD}{self.tr('select_diff')}{RESET}\n")
        print(f"  {self.tr('diff_easy')}")
        print(f"  {self.tr('diff_medium')}")
        print(f"  {self.tr('diff_hard')}")
        print()
        choice = self.get_input("> ")
        diff_map = {"1": "easy", "2": "medium", "3": "hard"}
        self.difficulty = diff_map.get(choice, "hard")
        self.ai = AI(self.difficulty)

        self.clear_screen()
        if self.mode == "hva_first":
            self.player_x_name = self.get_input(f"  {self.tr('enter_name')}: ") or "Player"
            self.player_o_name = self.tr("ai_default_name")
        else:
            ai_name_input = self.get_input(f"  {self.tr('enter_name_ai')}: ")
            self.player_x_name = ai_name_input if ai_name_input else self.tr("ai_default_name")
            self.player_o_name = self.get_input(f"  {self.tr('enter_name')}: ") or "Player"

    # ── Game Loops ─────────────────────────────────────────────────

    def handle_commands(self, cmd):
        """Handle in-game commands. Returns True if the command was handled."""
        cmd = cmd.lower()
        if cmd == "quit":
            self.running = False
            self.clear_screen()
            print(self.tr("quit_game"))
            self.beep()
            self.delay(0.5)
            return True
        elif cmd == "menu":
            return True  # signal to return to menu
        elif cmd == "help":
            self.show_help()
            return False
        elif cmd == "lang":
            self.toggle_lang()
            return False
        elif cmd == "score":
            self.show_session_scores()
            return False
        elif cmd == "sound":
            self.toggle_sound()
            return False
        return None  # not a command

    def play_hvh(self):
        """Human vs Human game loop."""
        self.board.reset()
        while self.running:
            self.clear_screen()
            print()
            print(self.board.display(self.lang))
            self.show_status_bar()

            current_mark = "X" if self.board.move_count % 2 == 0 else "O"
            current_name = self.player_x_name if current_mark == "X" else self.player_o_name

            prompt = f"{GREEN}{self.tr('player_turn', player=current_name, mark=current_mark)}{RESET} > "
            raw = self.get_input(prompt)

            # Check commands
            cmd_result = self.handle_commands(raw)
            if cmd_result is True:
                return  # quit or menu
            if cmd_result is False:
                continue

            # Parse move
            if not raw.isdigit() or not (1 <= int(raw) <= 9):
                print(f"{RED}{self.tr('invalid_move', cell=raw)}{RESET}")
                print(f"{YELLOW}{self.tr('available_cells', cells=', '.join(str(i+1) for i in self.board.available()))}{RESET}")
                self.delay(1)
                continue

            idx = int(raw) - 1
            if not self.board.is_empty(idx):
                print(f"{RED}{self.tr('cell_occupied', cell=raw, mark=self.board.cells[idx])}{RESET}")
                print(f"{YELLOW}{self.tr('available_cells', cells=', '.join(str(i+1) for i in self.board.available()))}{RESET}")
                self.delay(1)
                continue

            # Place mark
            self.board.place(idx, current_mark)
            self.beep()

            # Check game end
            winner = self.board.check_win()
            if winner:
                self.show_game_end_hvh(winner)
                if not self.play_again():
                    return
                self.board.reset()
                continue

            if self.board.check_draw():
                self.show_draw_hvh()
                if not self.play_again():
                    return
                self.board.reset()
                continue

    def play_hva(self, player_first=True):
        """Human vs AI game loop."""
        self.board.reset()
        ai_mark = "O" if player_first else "X"
        human_mark = "X" if player_first else "O"
        human_name = self.player_x_name if player_first else self.player_o_name
        ai_name = self.player_o_name if player_first else self.player_x_name

        while self.running:
            self.clear_screen()
            print()
            print(self.board.display(self.lang))
            self.show_status_bar()

            current_mark = "X" if self.board.move_count % 2 == 0 else "O"
            is_ai_turn = (current_mark == ai_mark)

            if is_ai_turn:
                print(f"{CYAN}{self.tr('ai_thinking')}...{RESET}")
                self.delay(0.5)
                move = self.ai.get_move(self.board, ai_mark)
                if move is None:
                    break
                self.board.place(move, ai_mark)
                self.beep()
            else:
                prompt = f"{GREEN}{self.tr('player_turn', player=human_name, mark=human_mark)}{RESET} > "
                raw = self.get_input(prompt)

                cmd_result = self.handle_commands(raw)
                if cmd_result is True:
                    return
                if cmd_result is False:
                    continue

                if not raw.isdigit() or not (1 <= int(raw) <= 9):
                    print(f"{RED}{self.tr('invalid_move', cell=raw)}{RESET}")
                    print(f"{YELLOW}{self.tr('available_cells', cells=', '.join(str(i+1) for i in self.board.available()))}{RESET}")
                    self.delay(1)
                    continue

                idx = int(raw) - 1
                if not self.board.is_empty(idx):
                    print(f"{RED}{self.tr('cell_occupied', cell=raw, mark=self.board.cells[idx])}{RESET}")
                    print(f"{YELLOW}{self.tr('available_cells', cells=', '.join(str(i+1) for i in self.board.available()))}{RESET}")
                    self.delay(1)
                    continue

                self.board.place(idx, human_mark)
                self.beep()

            # Check game end
            winner = self.board.check_win()
            if winner:
                self.show_game_end_hva(winner, human_name, ai_name)
                if not self.play_again():
                    return
                self.board.reset()
                continue

            if self.board.check_draw():
                self.show_draw_hva(human_name, ai_name)
                if not self.play_again():
                    return
                self.board.reset()
                continue

    # ── Game End ───────────────────────────────────────────────────

    def show_game_end_hvh(self, winner):
        winner_name = self.player_x_name if winner == "X" else self.player_o_name
        self.clear_screen()
        print()
        print(self.board.display(self.lang))
        print()
        print(f"{GREEN}{BOLD}{self.tr('win_msg', player=winner_name)}{RESET}")
        self.beep()
        self.delay(0.3)
        self.beep()
        self.delay(0.3)
        self.beep()

        # Record scores
        loser_name = self.player_o_name if winner == "X" else self.player_x_name
        self.score_mgr.record_win(winner_name)
        self.score_mgr.record_loss(loser_name)
        self._session_win(winner_name)
        self._session_loss(loser_name)
        self.delay(1)

    def show_draw_hvh(self):
        self.clear_screen()
        print()
        print(self.board.display(self.lang))
        print()
        print(f"{YELLOW}{BOLD}{self.tr('draw_msg')}{RESET}")
        self.score_mgr.record_draw(self.player_x_name)
        self.score_mgr.record_draw(self.player_o_name)
        self._session_draw(self.player_x_name)
        self._session_draw(self.player_o_name)
        self.delay(1)

    def show_game_end_hva(self, winner, human_name, ai_name):
        self.clear_screen()
        print()
        print(self.board.display(self.lang))
        print()
        if winner == "X":
            winner_name = human_name if self.mode == "hva_first" else ai_name
        else:
            winner_name = ai_name if self.mode == "hva_first" else human_name

        is_ai_win = (winner_name == ai_name)
        msg = self.tr("ai_wins") if is_ai_win else self.tr("you_win")
        print(f"{GREEN}{BOLD}{msg}{RESET}")
        self.beep()
        self.delay(0.3)
        self.beep()
        self.delay(0.3)
        self.beep()

        if is_ai_win:
            self.score_mgr.record_win(ai_name)
            self.score_mgr.record_loss(human_name)
            self._session_win(ai_name)
            self._session_loss(human_name)
        else:
            self.score_mgr.record_win(human_name)
            self.score_mgr.record_loss(ai_name)
            self._session_win(human_name)
            self._session_loss(ai_name)
        self.delay(1)

    def show_draw_hva(self, human_name, ai_name):
        self.clear_screen()
        print()
        print(self.board.display(self.lang))
        print()
        print(f"{YELLOW}{BOLD}{self.tr('draw_msg')}{RESET}")
        self.score_mgr.record_draw(human_name)
        self.score_mgr.record_draw(ai_name)
        self._session_draw(human_name)
        self._session_draw(ai_name)
        self.delay(1)

    def play_again(self):
        print()
        while True:
            again = self.get_input(f"{CYAN}{self.tr('play_again')}{RESET}").lower()
            if again in ("y", "yes"):
                return True
            if again in ("n", "no"):
                return False
            print(f"{RED}{self.tr('invalid_choice')}{RESET}")


# ── Main ──────────────────────────────────────────────────────────
def main():
    game = Game()
    game.show_menu()


if __name__ == "__main__":
    main()
