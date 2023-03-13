import numpy as np

import pygame

import sys

import math

from threading import Timer

import random
import os 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

ROWS = 6
COLS = 7

PLAYER_TURN = 0
AI_TURN = 1

PLAYER_PIECE = 1
AI_PIECE = 2


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    board = np.zeros((ROWS, COLS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()

def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE

    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score

def score_position(board, piece):

    score = 0
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, alpha, beta, maximizing_player):

    # visos galimos vietos lentoje
    valid_locations = get_valid_locations(board)

    is_terminal = is_terminal_node(board)

    # pergalę vertiname labai aukštu balu, o lygiąsias - 0
    if depth == 0 or is_terminal:
        if is_terminal: # winning move 
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        # gylis lygus nuliui, tiesiog įvertiname dabartinę lentą
        else: 
            return (None, score_position(board, AI_PIECE))


    if maximizing_player:

   
        value = -math.inf

        column = random.choice(valid_locations)

        # kiekvienam galiojančiam stulpeliui imituojame figūrėlės išmetimą    naudodami lentos kopiją        
# ir paleidžiame su ja minimax su sumažintu gyliu ir pakeistu žaidėju
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # REKURSIJA
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            # JEIGU Rezultatas sio stulpelio yra geresnis negu jau turime
            if new_score > value:
                value = new_score
                column = col
            # alpha yra geriausia opacija kokia turime
            alpha = max(value, alpha) 
    
            if alpha >= beta:
                break

        return column, value



#implement winning move, get valid locations .....


