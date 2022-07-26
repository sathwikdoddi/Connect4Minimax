import numpy as np
import sys
import pygame
import keyboard

BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

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
            if temp[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS)
            elif temp[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (c*SQUARE + 50, r*SQUARE + 50), PIECERADIUS)
    pygame.display.update()


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

font = pygame.font.Font('freesansbold.ttf', 75)

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
                    drop_piece(board, row, column, 1)

                    if winning_move(board, 1):
                        game_over = True
                        winner = font.render("Player 1 Wins!", 1, RED)
                        screen.fill(BLACK)
                        pygame.display.update()
                        screen.blit(winner, (100, 270))
                        pygame.display.update()
            
            # Player 2 Input
            else:
                x_position = event.pos[0]
                column = x_position // 100

                if is_valid_placement(board, column):
                    row = get_next_available_row(board, column)
                    drop_piece(board, row, column, 2)

                    if winning_move(board, 2):
                        game_over = True
                        winner = font.render("Player 2 Wins!", 1, YELLOW)
                        screen.fill(BLACK)
                        pygame.display.update()
                        screen.blit(winner, (100, 270))
                        pygame.display.update()

            if not game_over: draw_board(board)

            if turn == 0: turn = 1
            else: turn = 0

            if game_over:
                keyboard.wait("esc")