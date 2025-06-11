import numpy as np
import sys
import pygame
from pygame.locals import *
from config import *
from connect4_algos import *


def board_display(num_rows, num_cols):
    display = pygame.display.set_mode((num_cols * board_length, (num_rows + 1) * board_length))
    return display


def board_matrix(num_rows, num_cols):
    board= np.zeros((num_rows, num_cols), dtype=int)
    return board



def add_disc(board, col, disc_color, board_background):
    num_rows, num_cols = board.shape
    inserted_flag = 0

    for i in range(0, num_rows, 1):
        cell_value = board[i, col]
        print(f"Inspecting cell ({i}, {col}): {cell_value} (type: {type(cell_value)})")  # Debugging

        if int(cell_value) == 0:
            board[i, col] = disc_color
            inserted_flag = 1

            if i > 0:
                board[i - 1, col] = 0
        draw_board(board_background, board)
        pygame.time.wait(50)

    return board, inserted_flag


def draw_board(board_background, board):
    num_rows, num_cols = board.shape
    board_background.fill(bckgrnd_color)
    for i in range(num_rows):
        for j in range(num_cols):
            pygame.draw.rect(board_background, blue,
                             (j * board_length, i * board_length + board_length, board_length, board_length))
            if board[i, j] == 0:
                pygame.draw.circle(board_background, bckgrnd_color, (
                    int(j * board_length + board_length / 2), int(i * board_length + board_length + board_length / 2)),
                        int(disc_radius))
            elif board[i, j] == 1:
                pygame.draw.circle(board_background, red, (
                    int(j * board_length + board_length / 2), int(i * board_length + board_length + board_length / 2)),
                        int(disc_radius))
            elif board[i, j] == 2:
                pygame.draw.circle(board_background, yellow, (
                    int(j * board_length + board_length / 2), int(i * board_length + board_length + board_length / 2)),
                        int(disc_radius))
            else:
                print("Error: unresolved board value")
    pygame.display.update()


# Debugging
def main():
    board = board_matrix(6, 7)
    pygame.init()

    board_background = board_display(6, 7)
    draw_board(board_background, board)

    # Example disc placements
    board, inserted = add_disc(board, 0, 1, board_background)
    board, inserted = add_disc(board, 0, 2, board_background)
    board, inserted = add_disc(board, 1, 1, board_background)
    board, inserted = add_disc(board, 0, 2, board_background)
    board, inserted = add_disc(board, 2, 1, board_background)
    board, inserted = add_disc(board, 1, 2, board_background)
    board, inserted = add_disc(board, 3, 1, board_background)

    # Correctly check if the board is full
    if check_board_is_full(board,num_rows):
        print("The board is full!")
        # Optionally, check for a winner here
        human_wins, ai_wins = win_connect4(board)
        if human_wins > ai_wins:
            print("Human wins!")
        elif ai_wins > human_wins:
            print("AI wins!")
        else:
            print("It's a draw!")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
