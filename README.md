# 井字棋 (Tic-Tac-Toe)

一个功能完整的终端井字棋游戏，支持 AI 对战、分数追踪、中英文切换。

A feature-rich console Tic-Tac-Toe game with AI opponent, score tracking, and bilingual support.

## ASCII Mockup

```
=== 井字棋 ===

 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9

当前：Player X (X) | 第 0 步 | 人人对战
轮到 Player X（X） >
```

During gameplay:

```
 X | O | X
---+---+---
 O | X | O
---+---+---
 7 | 8 | 9

当前：Player O (O) | 第 6 步 | 人机对战（玩家先手） | 难度：困难/Hard
轮到 Player O（O） >
```

## 安装 (Installation)

```bash
pip install -r requirements.txt
```

## 运行 (How to Run)

```bash
python3 game.py
```

## 玩法 (How to Play)

- 棋盘为 3×3 网格，编号 1-9（从左到右，从上到下）
- 玩家 X（蓝色）先手，玩家 O（红色）后手
- 输入数字 1-9 落子
- 横、竖、斜任意方向连成三子即获胜

## 游戏模式 (Game Modes)

| 模式 | 说明 |
|------|------|
| 人人对战 | 两名玩家轮流在同一台电脑上对战 |
| 人机对战（玩家先手） | 玩家执 X 先手，AI 执 O |
| 人机对战（AI 先手） | AI 执 X 先手，玩家执 O |

## AI 难度 (AI Difficulty)

| 难度 | 说明 |
|------|------|
| 简单 (Easy) | AI 随机落子 |
| 中等 (Medium) | AI 混合策略（50% minimax + 50% 随机） |
| 困难 (Hard) | AI 使用 Minimax + Alpha-Beta 剪枝，永不输 |

## 评分 (Scoring)

- 胜 = +1 分，负 = 0 分，平 = +0.5 分
- 分数保存在 `scores.json` 文件中
- 排行榜按胜率排序

## 语言支持 (Language Support)

- 默认中文，可通过 `lang` 命令切换为英文
- 所有菜单、提示、消息均跟随语言设置

## 游戏内命令 (In-Game Commands)

| 命令 | 功能 |
|------|------|
| `quit` | 退出游戏 |
| `menu` | 返回主菜单 |
| `help` | 显示帮助 |
| `lang` | 切换语言（中文/English） |
| `score` | 显示当前会话分数 |
| `sound` | 切换音效 |

## 主菜单 (Main Menu)

1. 新游戏 - 选择游戏模式
2. 排行榜 - 查看所有玩家排名
3. 语言切换 - 中英文切换
4. 帮助 - 查看游戏说明
5. 退出 - 退出游戏

## 运行测试 (Running Tests)

```bash
pytest tests/ -v
```

要求 30+ 个测试用例，覆盖：
- 棋盘状态管理
- 赢局检测（所有 8 种赢法）
- 平局检测
- AI Minimax 逻辑（AI 作为 O 永不输）
- 输入验证
- 分数持久化
- 语言切换

## 兼容性 (Compatibility)

- Python 3.8+
- macOS / Linux / Windows
- 仅使用标准库（`os`, `sys`, `json`, `random`, `time`, `pathlib`）
- 无外部依赖（测试需要 `pytest`）
