import numpy as np
import sys
import pygame
import keyboard
import math
import random

BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
DARKRED = (100, 0, 0)
DARKYELLOW = (100, 100, 0)

ROWS = 6
COLUMNS = 7

SQUARE = 100
PIECERADIUS = 45

def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_placement(board, col):
    return board[5][col] == 0

def get_next_available_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    # Bottom left is (0, 0)
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal Win Check
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical Win Check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive Diagonal Win Check
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative Diagonal Win Check
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    temp = np.flip(board, 0)
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(screen, BLACK, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS)
            if temp[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS-3)
                pygame.draw.circle(screen, DARKRED, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS-10)
            elif temp[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS-3)
                pygame.draw.circle(screen, DARKYELLOW, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS-10)
    pygame.display.update()

def window_evaluation(search_window, piece):
    score = 0

    opponent = 1
    if piece == 1: opponent = 2

    if search_window.count(piece) == 4:
        score += 100
    elif search_window.count(piece) == 3 and search_window.count(0) == 1:
        score += 5
    elif search_window.count(piece) == 2 and search_window.count(0) == 2:
        score += 5

    if search_window.count(opponent) == 3 and search_window.count(0) == 1:
        score -= 40

    return score

def score_piece_setup(board, piece):
    score = 0

    # Score Center Column
    center_array = [int(i) for i in list(board[:,COLUMNS//2])]
    score += center_array.count(piece) * 3

    # Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS-3):
            search_window = row_array[c:c+4]
            score += window_evaluation(search_window, piece)

    # Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            search_window = col_array[r:r+4]
            score += window_evaluation(search_window, piece)

    # Score Positive Diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            search_window = [board[r+i][c+i] for i in range(4)]
            score += window_evaluation(search_window, piece)

    # Score Negative Diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            search_window = [board[r+3-i][c+i] for i in range(4)]
            score += window_evaluation(search_window, piece)
             
    return score

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    column = random.choice(valid_locations)

    # Bottom of the Recursion Tree
    if depth == 0 or is_terminal:
        if is_terminal: # If game is over
            if winning_move(board, 2):
                return (None, 1000000000000)
            elif winning_move(board, 1):
                return (None, -1000000000000)
            else: # If the board gets full
                return (None, 0)
        else: # If we reached the end of the depth
            return (None, score_piece_setup(board, 2))

    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            row = get_next_available_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 2)
            new_score = minimax(board_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_available_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 1)
            new_score = minimax(board_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_placement(board, col):
            valid_locations.append(col)

    return valid_locations


# Initializing Game

board = create_board()
game_over = False
turn = 0

pygame.init()

width = SQUARE * COLUMNS
height = SQUARE * ROWS
size  = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe AI")

font = pygame.font.Font('freesansbold.ttf', 75)

turn = random.randint(0,1)

if turn == 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)
    pygame.display.update()
    message = font.render("AI Going First...", 1, (255, 255, 255))
    screen.blit(message, (80, 300 - 75/2))
    pygame.display.update()
    pygame.time.wait(2000)

draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Player 1 Input
            if turn == 0:
                x_position = event.pos[0]
                column = x_position // 100

                if is_valid_placement(board, column):
                    row = get_next_available_row(board, column)
                    for r in range(5, row, -1):
                        if r != 5: drop_piece(board, r+1, column, 0)
                        drop_piece(board, r, column, 1)
                        draw_board(board)
                        pygame.time.wait(40)
                    if row != 5: drop_piece(board, row+1, column, 0)
                    drop_piece(board, row, column, 1)
                    draw_board(board)

                    if winning_move(board, 1):
                        draw_board(board)
                        pygame.time.wait(2000)
                        game_over = True
                        winner = font.render("Player 1 Wins!", 1, RED)
                        screen.fill(BLACK)
                        pygame.display.update()
                        screen.blit(winner, (100, 270))
                        pygame.display.update()

                    if turn == 0: turn = 1
                    else: turn = 0

    if turn == 1 and not game_over:
        # column = random.randint(0, COLUMNS - 1)
        column = minimax(board, 4, True)[0]

        if is_valid_placement(board, column):
            row = get_next_available_row(board, column)
            for r in range(5, row, -1):
                if r != 5: drop_piece(board, r+1, column, 0)
                drop_piece(board, r, column, 2)
                draw_board(board)
                pygame.time.wait(40)
            if row != 5: drop_piece(board, row+1, column, 0)
            drop_piece(board, row, column, 2)
            draw_board(board)

            if winning_move(board, 2):
                draw_board(board)
                pygame.time.wait(2000)
                game_over = True
                winner = font.render("The AI Wins!", 1, YELLOW)
                screen.fill(BLACK)
                pygame.display.update()
                screen.blit(winner, (100, 270))
                pygame.display.update()

            if not game_over: draw_board(board)

            if turn == 0: turn = 1
            else: turn = 0

    if game_over:
        keyboard.wait("esc")
