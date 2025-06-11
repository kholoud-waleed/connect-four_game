import os
import sys
import pygame
from PyQt5 import QtWidgets, QtCore

from connect4_algos import win_connect4
from connect4_board import board_matrix, draw_board, board_display, check_board_is_full
from play_turns import players_turn, ais_turn
from config import *


class FirstWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FirstWindow, self).__init__()
        self.vbox = QtWidgets.QWidget(self)
        self.setup_user_interface()
        self.buttons()
        self.show()
        self.resultmsg = QtWidgets.QMessageBox()
        self.resultmsg.setIcon(QtWidgets.QMessageBox.Information)
        self.resultmsg.hide()
        # Set a timer that will trigger events periodically to the update_game method
        self.game_state = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_game)

    def setup_user_interface(self):
        # Set the window screen dimensions.
        self.resize(950, 951)
        # Set the window screen game title.
        self.setWindowTitle("Connect 4 Setting")

        # Set the background image to the widget using setStyleSheet
        """code"""
        self.setStyleSheet("background-image: url('connect4_box.jpg');"
                           "background-repeat: no-repeat;"
                           "background-position: center center;"
                           "background-attachment: fixed;")

        # Ensure the background image fills the widget
        self.vbox.setAutoFillBackground(True)
        # Center the window on the screen.
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_gm = self.frameGeometry()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def buttons(self):
        self.vbox.setGeometry(QtCore.QRect(25, 10, 900, 800))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.vbox)

        # Create buttons with labels
        AI = QtWidgets.QPushButton("AI 🤖", self.vbox)
        ME = QtWidgets.QPushButton("ME 👩🏻‍", self.vbox)
        easy = QtWidgets.QPushButton("Easy  ⭐", self.vbox)
        medium = QtWidgets.QPushButton("Medium ⭐⭐", self.vbox)
        hard = QtWidgets.QPushButton("Hard  ⭐⭐⭐", self.vbox)
        superior = QtWidgets.QPushButton("Superior ⭐⭐⭐⭐", self.vbox)
        minimax = QtWidgets.QPushButton("Minimax", self.vbox)
        minimax_alpha_beta = QtWidgets.QPushButton("Minimax Alpha-Beta", self.vbox)
        expecti_minimax = QtWidgets.QPushButton("Expecti-Minimax", self.vbox)
        start_game = QtWidgets.QPushButton("Play! [▶]", self.vbox)

        # Create labels with text statements
        l1 = QtWidgets.QLabel("1. Select the First Player:", self.vbox)
        l2 = QtWidgets.QLabel("2. Select the Gameplay Algorithm:", self.vbox)
        l3 = QtWidgets.QLabel("3. Select the Difficulty Level:", self.vbox)
        l4 = QtWidgets.QLabel("Click on Play to start the Game", self.vbox)

        # Create a list of label stats and their corresponding buttons
        sections = [(l1, [AI, ME]),
                    (l2, [minimax, minimax_alpha_beta, expecti_minimax]),
                    (l3, [easy, medium, hard, superior]),
                    (l4, [start_game])]
        # Iterate over each section and add the label and buttons to the layout
        for label, buttons in sections:
            self.verticalLayout.addWidget(label)
            for button in buttons:
                self.verticalLayout.addWidget(button)
            self.verticalLayout.addSpacing(5)  # Spacing between sections

        l1.setStyleSheet("font-size: 38px; font-weight: bold; color: white;")
        AI.setMinimumHeight(40)
        AI.setMinimumWidth(20)
        AI.setStyleSheet("""QPushButton {border-radius: 10px; font-size: 36px;
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFC1C1, stop:1 #FF7F7F); 
                            /* Light Red to Soft Red */ color: black; /* black text */
                            border: 2px solid black;  /* Border with 2px thickness and black color */;}
                            QPushButton:hover {background-color: #FF4C4C;  /* Darker red on hover */}
                            QPushButton:pressed { background-color: #FF0000; }  # red when pressed""")
        ME.setMinimumHeight(40)
        ME.setMinimumWidth(20)
        ME.setStyleSheet("""QPushButton {border-radius: 10px; font-size: 36px;
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFACD, stop:1 #FFD700); 
                            /* Gradient from Lemon Chiffon to Gold */ color: black; /* black text */
                            border: 2px solid black;  /* Border with 2px thickness and black color */;}
                            QPushButton:hover {background-color: #FFB300;  /* Darker yellow on hover */}
                            QPushButton:pressed { background-color: #FF8C00; }  # yellow when pressed""")

        l2.setStyleSheet("font-size: 38px; font-weight: bold; color: white;")
        square_buttons1 = [easy, medium, hard, superior]
        # Apply square shape for other buttons
        for button in square_buttons1:
            button.setMinimumHeight(40)
            button.setMinimumWidth(50)
            button.setStyleSheet("""QPushButton {border-radius: 8px; font-size: 26px;
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D8A7FF, stop:1 #800080);
                                    /* Gradient from Light purple to Dark purple */ color: white; /* white text */ 
                                    border: 2px solid black;   /* Border with 2px thickness and black color */;}
                                    QPushButton:hover {background-color: #3e8e41; }  # Darker green when pressed
                                    QPushButton:pressed { background-color: #3e8e41; }  # Darker green when pressed""")

        l3.setStyleSheet("font-size: 38px; font-weight: bold; color: white;")
        square_buttons2 = [minimax, minimax_alpha_beta, expecti_minimax]
        # Apply square shape for other buttons
        for button in square_buttons2:
            button.setMinimumHeight(40)
            button.setMinimumWidth(20)
            button.setStyleSheet("""QPushButton {border-radius: 8px;font-size: 26px;
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E90FF, stop:1 #00008B); 
                                    /* Gradient from Dodger Blue to Dark Blue */ color: white; /* white text */
                                    border: 2px solid black;   /* Border with 2px thickness and black color */;}
                                    QPushButton:hover {background-color: #27ae60;  /* Darker green on hover */}
                                    QPushButton:pressed { background-color: #3e8e41; }  # Darker green when pressed""")

        l4.setStyleSheet("font-size: 38px; font-weight: bold; color: black;")
        start_game.setMinimumHeight(40)
        start_game.setMinimumWidth(20)
        start_game.setStyleSheet("""QPushButton {border-radius: 10px;font-size: 36px;
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #A9A9A9);
                                    ;color: black; /* black text */
                                    border: 2px solid black;   /* Border with 2px thickness and black color */;}
                                    QPushButton:hover {background-color: #ADD8E6;  /* Darker green on hover */}
                                    QPushButton:pressed { background-color: #00008B; }  # Darker Blue  when pressed""")

        AI.clicked.connect(self.set_ai_p1)
        ME.clicked.connect(self.set_me_p1)
        easy.clicked.connect(lambda: self.set_level(EASY_LEVEL))
        medium.clicked.connect(lambda: self.set_level(MEDIUM_LEVEL))
        hard.clicked.connect(lambda: self.set_level(HARD_LEVEL))
        superior.clicked.connect(lambda: self.set_level(SUPERIOR_LEVEL))
        minimax.clicked.connect(lambda: self.set_algo(MINIMAX))
        minimax_alpha_beta.clicked.connect(lambda: self.set_algo(MINIMAX_ALPHA_BETA))
        expecti_minimax.clicked.connect(lambda: self.set_algo(EXPECTI_MINIMAX))
        start_game.clicked.connect(self.start_game)

    def set_ai_p1(self):
        global player_1
        player_1 = "AI"
        print("Player 1 selected is: AI")

    def set_me_p1(self):
        global player_1
        player_1 = "ME"
        print("Player 1 selected is: ME")

    def set_algo(self, algo):
        global selected_algo
        selected_algo = algo
        if algo == 1:
            print(f"Gameplay Algorithm is set to Minimax")
        elif algo == 2:
            print(f"Gameplay Algorithm is set to Minimax Alpha-Beta")
        elif algo == 3:
            print("Gameplay Algorithm is set to Expecti-Minimax")
        else:
            print("Please select a valid algo!")

    def set_level(self, level):
        global selected_level
        selected_level = level
        if level == 1:
            print(f"Difficulty leve is set to Easy")
        elif level == 2:
            print(f"Difficulty level is set to Medium")
        elif level == 3:
            print(f"Difficulty level is set to Hard")
        elif level == 4:
            print(f"Difficulty level is set to Superior")
        else:
            print("Please select a valid level!")

    def start_game(self):
        if not player_1 or not selected_level or not selected_algo:
            self.resultmsg.setText("Please select both a difficulty level and an algorithm!")
            self.resultmsg.setWindowTitle("Error")
            self.resultmsg.exec_()
            return
        global first_player
        self.game_state = GameWindow(selected_level, selected_algo)
        print(f"Starting game with {player_1} as the first player.")
        self.timer.start(100)

    def update_game(self):
        if self.game_state:
            board, winner_flag = self.game_state.get_next_move()
            draw_board(self.game_state.board_background, board)

            # Get Connect Four counts
            human_wins, ai_wins = win_connect4(board)

            if winner_flag == 1:  # AI wins
                self.end_game(f"AI WINS! 😔\nAI Connect Fours: {ai_wins}\nHuman Connect Fours: {human_wins}")
            elif winner_flag == 2:  # Human wins
                self.end_game(f"YOU WIN! 😊\nHuman Connect Fours: {human_wins}\nAI Connect Fours: {ai_wins}")
            elif winner_flag == 3:  # Draw
                self.end_game(f"DRAW! 😐\nAI Connect Fours: {ai_wins}\nHuman Connect Fours: {human_wins}")

    def end_game(self, result):













        self.timer.stop()
        self.resultmsg.setText(result)
        self.resultmsg.setWindowTitle("Game Over")
        self.resultmsg.exec_()
        pygame.quit()
        self.game_state = None


class GameWindow:
    def __init__(self, level, algo=None):
        global player_1

        # Initialize Pygame
        pygame.init()
        # Center the game window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Game Screen dimensions
        self.screen = pygame.display.set_mode((1000, 880))
        pygame.display.set_caption("Connect 4 Game")
        # Initialize the game board, background, and settings
        self.board = board_matrix(num_rows, num_cols)
        self.board_background = board_display(num_rows, num_cols)
        self.current_player = player_1
        self.level = level
        self.algorithm = algo
        self.winner_flag = 0
        # Draw the initial Connect 4 game board
        draw_board(self.board_background, self.board)

    def get_next_move(self):
        try:
            if self.current_player == "ME":  # Player's turn
                self.board, self.winner_flag = players_turn(self.board, self.board_background)
                if self.winner_flag != 0:  # Check if the game is over
                    return self.board, self.winner_flag
                self.current_player = "AI"  # Switch to AI's turn

            elif self.current_player == "AI":  # AI's turn
                self.board, self.winner_flag = ais_turn(self.board, self.board_background, self.level, self.algorithm)
                if self.winner_flag != 0:  # Check if the game is over
                    return self.board, self.winner_flag
                self.current_player = "ME"  # Switch to player's turn

        except Exception as e:
            print(f"Error during game logic: {e}")
            print("Board state:", self.board)
        return self.board, self.winner_flag


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FirstWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
