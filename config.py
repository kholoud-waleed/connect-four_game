# game setup
player_AI = 0
player_Human = 1
disc_AI = 1
disc_human = 2
empty_space = 0


# colours of game theme, board and discs
bckgrnd_color = (0,0,0)
blue = (0,0,200)
red = (250,0,0)
yellow = (255,215,0)

# dimensions of the game board
board_length = 125
disc_radius = int(board_length/2)-4
num_rows = 6
num_cols = 7

# game levels
EASY_LEVEL = 1
MEDIUM_LEVEL = 2
HARD_LEVEL = 3
SUPERIOR_LEVEL = 4

# gameplay algorithms
MINIMAX = 1
MINIMAX_ALPHA_BETA = 2
EXPECTI_MINIMAX = 3
