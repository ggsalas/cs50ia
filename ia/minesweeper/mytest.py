from minesweeper import MinesweeperAI

HEIGHT, WIDTH, MINES = 3, 3, 1
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
ai.add_knowledge((2, 2), 0)  # Clue 0, all neighbors safe
print(f"first: {ai.safes}")  # Should include (0, 0)
ai.add_knowledge((0, 1), 1)  # Clue 1
ai.mark_mine((1, 1))  # Mark a mine
ai.add_knowledge((0, 1), 1)  # Reprocess
print(f"second {ai.safes}")  # Should include (0, 0)
