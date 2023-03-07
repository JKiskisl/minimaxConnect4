import numpy as np

import pygame

import sys

import math

from threading import Timer

import random
import os 


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


