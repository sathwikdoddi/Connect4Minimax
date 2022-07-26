import numpy as np
import random
import sys
import pygame
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROWS = 6
COLUMNS = 7
SQUARE = 100

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
    # Horizontal Win Check (not possible to win horizontally past index 3)
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
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE, SQUARE, SQUARE))


board = create_board()
game_over = False
turn = 0

pygame.init()

width = SQUARE * COLUMNS
height = SQUARE * ROWS
size  = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass


            # # Player 1 Input
            # if turn == 0:
            #     column = int(input("Player 1, choose your column (0, 6): "))
            #     if (is_valid_placement(board, column)):
            #         row = get_next_available_row(board, column)
            #         drop_piece(board, row, column, 1)
            #         if winning_move(board, 1):
            #             print("Player 1 Wins! Congratulations.")
            #             game_over = True

            # # Player 2 Input
            # else:
            #     column = int(input("Player 2, choose your column (0, 6): "))
            #     if (is_valid_placement(board, column)):
            #         row = get_next_available_row(board, column)
            #         drop_piece(board, row, column, 2)
            #         if winning_move(board, 2):
            #             print("Player 2 Wins! Congratulations.")
            #             game_over = True
            
            # # Resetting
            # print_board(board)
            # if (turn == 0): turn = 1
            # else: turn = 0