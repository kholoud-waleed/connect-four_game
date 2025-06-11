import random
import math

from config import *


def win_connect4(board):
    human_wins = 0
    ai_wins = 0
    moves = [[1, 0], [0, 1], [1, 1], [1, -1]]  # Directions: horizontal, vertical, diagonal (positive/negative)
    for m in moves:
        col_move, row_move = m
        for c in range(num_cols):
            for r in range(num_rows):
                max_c, max_r = c + 3 * col_move, r + 3 * row_move
                if 0 <= max_c < num_cols and 0 <= max_r < num_rows:
                    if board[r][c] != empty_space:
                        winner = board[r][c]
                        if (board[r + row_move][c + col_move] == winner and
                            board[r + 2 * row_move][c + 2 * col_move] == winner and
                            board[r + 3 * row_move][c + 3 * col_move] == winner):
                            if winner == disc_human:
                                human_wins += 1
                            elif winner == disc_AI:
                                ai_wins += 1

    print(f"Human Connect Fours: {human_wins}")
    print(f"AI Connect Fours: {ai_wins}")
    return human_wins, ai_wins


def add_disc_to_matrix(board, col, disc_color):
    for i in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[i, col] == empty_space:
            board[i, col] = disc_color
            break
    return board


def check_board_is_full(board,c):
    if (get_incomplete_columns(board) == []):
        return True
    return False


def get_incomplete_columns(board):
    """Check if the column is completely full or not yet."""
    incomplete_cols=[]
    for c in range(num_cols):
        if board[0][c] == 0:
            incomplete_cols.append(c)
    return incomplete_cols


def minimax(board, level, maximizing_player, game_level):
    if level == 0 or check_board_is_full(board, num_cols):
        return None, get_score(board, game_level)

    if maximizing_player:
        best_score = -math.inf
        selected_col = random.choice(get_incomplete_columns(board))
        for col in get_incomplete_columns(board):
            temp_board = board.copy()
            add_disc_to_matrix(temp_board, col, disc_AI)
            _, score = minimax(temp_board, level - 1, False, game_level)
            if score > best_score:
                best_score = score
                selected_col = col
        return selected_col, best_score
    else:
        best_score = math.inf
        selected_col = random.choice(get_incomplete_columns(board))
        for col in get_incomplete_columns(board):
            temp_board = board.copy()
            add_disc_to_matrix(temp_board, col, disc_human)
            _, score = minimax(temp_board, level - 1, True, game_level)
            if score < best_score:
                best_score = score
                selected_col = col
        return selected_col, best_score


def minimax_alpha_beta(board, level, maximizing_player, alpha, beta, game_level):
    if level == 0 or check_board_is_full(board, num_cols):
        return None, get_score(board, game_level)

    if maximizing_player:
        best_score = -math.inf
        selected_col = random.choice(get_incomplete_columns(board))
        for col in get_incomplete_columns(board):
            temp_board = board.copy()
            add_disc_to_matrix(temp_board, col, disc_AI)
            _, score = minimax_alpha_beta(temp_board, level - 1, False, alpha, beta, game_level)
            if score > best_score:
                best_score = score
                selected_col = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return selected_col, best_score
    else:
        best_score = math.inf
        selected_col = random.choice(get_incomplete_columns(board))
        for col in get_incomplete_columns(board):
            temp_board = board.copy()
            add_disc_to_matrix(temp_board, col, disc_human)
            _, score = minimax_alpha_beta(temp_board, level - 1, True, alpha, beta, game_level)
            if score < best_score:
                best_score = score
                selected_col = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return selected_col, best_score


def expecti_minimax(board, level, maximizing_player, game_level):
    """Expectiminimax algorithm for probabilistic decision-making"""

    if level == 0 or check_board_is_full(board, num_cols):
        return None, get_score(board, game_level)

    if maximizing_player:
        """Maximizing player (AI)"""
        best_score = -math.inf
        selected_col = random.choice(get_incomplete_columns(board))  # Initialize randomly for tie-breaking
        # Explore each valid move
        for c in get_incomplete_columns(board):
            temp = board.copy()
            add_disc_to_matrix(temp, c, disc_AI)
            _, new_score = expecti_minimax(temp, level - 1, False, game_level)  # Recursive call for the minimizer
            if new_score > best_score:
                # Update best score and selected column if a better score is found
                best_score = new_score
                selected_col = c
        return selected_col, best_score
    else:
        """Minimizing/Chance player (Human or stochastic event)"""
        total_score = 0  # Total score to be averaged
        num_branches = len(get_incomplete_columns(board))  # Number of possible outcomes
        for c in get_incomplete_columns(board):
            temp = board.copy()
            add_disc_to_matrix(temp, c, disc_human)
            _, branch_score = expecti_minimax(temp, level - 1, True, game_level)
            total_score += branch_score     # Accumulate scores from all branches
        # Expected Utility: by averaging the scores across all possible outcomes
        avg_score = total_score / num_branches if num_branches > 0 else 0
        # Return None as the selected column since chance nodes don't pick moves
        return None, avg_score


def heuristic_fn(line, game_level):
    score = 0
    if game_level == EASY_LEVEL:
        # Attack score
        if line.count(disc_AI) == 4:
            score = 70
        elif line.count(disc_AI) == 3 and line.count(empty_space) == 1:
            score = 30
        elif line.count(disc_AI) == 2 and line.count(empty_space) == 2:
            score = 20
        # Defence score
        elif line.count(disc_human) == 4 and line.count(empty_space) == 0:
            score = -80
        elif line.count(disc_human) == 3 and line.count(empty_space) == 1:
            score = -50
        elif line.count(disc_human) == 2 and line.count(empty_space) == 2:
            score = -15

    elif game_level == MEDIUM_LEVEL:
        if line.count(disc_AI) == 4:
            score = 100
        elif line.count(disc_AI) == 3 and line.count(empty_space) == 1:
            score = 20
        elif line.count(disc_AI) == 2 and line.count(empty_space) == 2:
            score = 10
        # Defence score
        elif line.count(disc_human) == 4 and line.count(empty_space) == 0:
            score = -120
        elif line.count(disc_human) == 3 and line.count(empty_space) == 1:
            score = -50
        elif line.count(disc_human) == 2 and line.count(empty_space) == 2:
            score = -30

    elif game_level == HARD_LEVEL:
        if line.count(disc_AI) == 4:
            score = 100
        elif line.count(disc_AI) == 3 and line.count(empty_space) == 1:
            score = 20
        elif line.count(disc_AI) == 2 and line.count(empty_space) == 2:
            score = 10
        # Defence score
        elif line.count(disc_human) == 4 and line.count(empty_space) == 0:
            score = - 100
        elif line.count(disc_human) == 3 and line.count(empty_space) == 1:
            score = -100
        elif line.count(disc_human) == 2 and line.count(empty_space) == 2:
            score = -30

    elif game_level == SUPERIOR_LEVEL:
        if line.count(disc_AI) == 4:
            score = 100
        elif line.count(disc_AI) == 3 and line.count(empty_space) == 1:
            score = 40
        elif line.count(disc_AI) == 2 and line.count(empty_space) == 2:
            score = 10
        # Defence score
        elif line.count(disc_human) == 4 and line.count(empty_space) == 0:
            score = -130
        elif line.count(disc_human) == 3 and line.count(empty_space) == 1:
            score = -110
        elif line.count(disc_human) == 2 and line.count(empty_space) == 2:
            score = -70
    else:
        print('Error in heuristic_fn')
    return score


def get_score(board, game_level):
    total_score = 0
    # horizontal
    for r in range(num_rows):
        for c in range(num_cols - 3):
            total_score = total_score + heuristic_fn([board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]],
                                                     game_level)
    #  vertical
    for c in range(num_cols):
        for r in range(num_rows - 3):
            total_score = total_score + heuristic_fn([board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]],
                                                     game_level)
    # diagonal positive
    for c in range(num_cols - 3):
        for r in range(num_rows - 3):
            total_score = total_score + heuristic_fn([board[r][c], board[r + 1][c + 1], board[r + 2][c + 2],
                                                      board[r + 3][c + 3]], game_level)
    # diagonal negative
    for c in range(num_cols - 3):
        for r in range(3, num_rows):
            total_score = total_score + heuristic_fn( [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2],
                                                       board[r - 3][c + 3]], game_level)
    # center column
    if game_level != EASY_LEVEL:
        center_col = num_cols // 2
        for r in range(3, num_rows):
            if board[r][center_col]==disc_AI:
                total_score= total_score + 5
    return total_score
