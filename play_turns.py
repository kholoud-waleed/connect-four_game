import pygame
import math
import sys
from config import *
from connect4_board import add_disc, check_board_is_full, win_connect4
from connect4_algos import minimax, minimax_alpha_beta, expecti_minimax

# AI Turn
def ais_turn(board, board_background, level, algo_selected):
    winner_flag = 0
    insertion_flag = 0

    if algo_selected == MINIMAX:
        col = minimax(board, level, True, level)[0]
    elif algo_selected == MINIMAX_ALPHA_BETA:
        col = minimax_alpha_beta(board, level, True, -math.inf, math.inf, level)[0]
    elif algo_selected == EXPECTI_MINIMAX:
        col = expecti_minimax(board, level, True, level)[0]
    else:
        print("Invalid AI algorithm")
        return board, winner_flag

    # Place AI disc
    while insertion_flag == 0:
        board, insertion_flag = add_disc(board, col, disc_AI, board_background)

    # Check if the board is full before comparing wins
    if check_board_is_full(board, num_cols):
        human_wins, ai_wins = win_connect4(board)
        if ai_wins > human_wins:
            winner_flag = 1  # AI wins
        elif human_wins > ai_wins:
            winner_flag = 2  # Player wins
        else:
            winner_flag = 3  # Draw
    return board, winner_flag


# Player's Turn
def players_turn(board, board_background):
    winner_flag = 0
    inserted_flag = 0

    while inserted_flag == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(board_background, bckgrnd_color, (0, 0, board_length * num_cols, board_length))
                col_pos = event.pos[0]
                pygame.draw.circle(board_background, yellow, (col_pos, int(board_length / 2)), disc_radius)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = event.pos[0]
                insertion_col = int(math.floor(click_position / board_length))
                board, inserted_flag = add_disc(board, insertion_col, disc_human, board_background)

    # Check if the board is full before comparing wins
    if check_board_is_full(board, num_cols):
        human_wins, ai_wins = win_connect4(board)
        if ai_wins > human_wins:
            winner_flag = 1  # AI wins
        elif human_wins > ai_wins:
            winner_flag = 2  # Player wins
        else:
            winner_flag = 3  # Draw
    return board, winner_flag

