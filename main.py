from copy import deepcopy
import math
import random

import chess
import pygame

X = Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.init()

PIECES = {'p': pygame.image.load('assets/black_pawn.png'),
          'n': pygame.image.load('assets/black_knight.png'),
          'b': pygame.image.load('assets/black_bishop.png'),
          'r': pygame.image.load('assets/black_rook.png'),
          'q': pygame.image.load('assets/black_queen.png'),
          'k': pygame.image.load('assets/black_king.png'),
          'P': pygame.image.load('assets/white_pawn.png'),
          'N': pygame.image.load('assets/white_knight.png'),
          'B': pygame.image.load('assets/white_bishop.png'),
          'R': pygame.image.load('assets/white_rook.png'),
          'Q': pygame.image.load('assets/white_queen.png'),
          'K': pygame.image.load('assets/white_king.png')}

COLORS = {
    "WHITE" : (255, 255, 255),
    "GREY"  : (128, 128, 128),
    "BLACK" : (0, 0, 0),
    "BLUE"  : (50, 255, 255),
    "GREEN" : (0, 255, 0),
    "YELLOW": (255, 255, 31)
}

def update(screen, board):
    # Draw backgrounds
    for i in range(64):
        coordinate = ((i % 8) * 100, 700 - (i // 8) * 100)
        even_row = (i // 8) % 2
        # if even_row:
        #     if i % 2: screen.blit(PIECES['nijika'], coordinate)
        #     else: screen.blit(PIECES['bocchi'], coordinate)
        # else:
        #     if i % 2: screen.blit(PIECES['bocchi'], coordinate)
        #     else: screen.blit(PIECES['nijika'], coordinate)

    # Display pieces
    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            continue
        screen.blit(PIECES[str(piece)], ((i % 8) * 100, 700 - (i // 8) * 100))

    # Draw Lines
    for i in range(7):
        i = i+1
        pygame.draw.line(screen, COLORS["WHITE"], (0, i * 100), (800, i * 100))
        pygame.draw.line(screen, COLORS["WHITE"], (i * 100, 0), (i * 100, 800))
    pygame.display.flip()

def main_one_agent(board, agent, HUMAN_IS_WHITE: bool = True):
    screen.fill(COLORS["GREEN"])
    pygame.display.set_caption('INTERACTIVE CHESS GUI :D')
    
    index_moves = []
    status = True
    while status:
        #update screen
        update(screen, board)

        # Agent to move, assuming black
        if board.turn != HUMAN_IS_WHITE:
            board.push(agent(board))
            screen.fill(COLORS["GREEN"])
            continue

        # Human to move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
                break

            # if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #reset previous screen from clicks
                screen.fill(COLORS["GREEN"])
                #get position of mouse
                pos = pygame.mouse.get_pos()

                #find which square was clicked and index of it
                square = (math.floor(pos[0] / 100), math.floor(pos[1] / 100))
                index = (7 - square[1]) * 8 + square[0]
                
                # if we have already highlighted moves and are making a move
                if index in index_moves: 
                    move = moves[index_moves.index(index)]
                    board.push(move)
                    index_moves.clear() 
                    continue

                # show possible moves
                piece = board.piece_at(index)
                if piece is None:
                    continue
                all_moves = list(board.legal_moves)
                moves = []
                for m in all_moves:
                    if m.from_square == index:
                        moves.append(m)
                        t = m.to_square
                        TX1 = 100 * (t % 8)
                        TY1 = 100 * (7 - t // 8)
                        pygame.draw.rect(screen, COLORS["YELLOW"], pygame.Rect(TX1,TY1,100,100),5)
                index_moves = [a.to_square for a in moves]

        # deactivates the pygame library
        if board.outcome():
            outcome = board.outcome()
            OUTPUT_STRING = f'The game ends with a {outcome.termination}.' + (f'{outcome.winner} wins the game' if outcome.winner else '')
            print(OUTPUT_STRING)
            status = False
    pygame.quit()

#an agent that moves randommly
def random_agent(board):
    return random.choice(list(board.legal_moves))

scoring= {'p': -1,
          'n': -3,
          'b': -3,
          'r': -5,
          'q': -9,
          'k': 0,
          'P': 1,
          'N': 3,
          'B': 3,
          'R': 5,
          'Q': 9,
          'K': 0,
          }
#simple evaluation function
def eval_board(board):
    score = 0
    pieces = board.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]
    return score

#this is min_max at depth one
def most_value_agent(board):
    moves = list(board.legal_moves)
    scores = []
    for move in moves:
        #creates a copy of board so we dont
        #change the original class
        temp = deepcopy(board)
        temp.push(move)
        scores.append(eval_board(temp))

    if board.turn == True:
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]
    return best_move

def min_max2(board):
    moves = list(board.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(board)
        temp.push(move)
        temp_best_move = most_value_agent(temp)
        temp.push(temp_best_move)
        scores.append(eval_board(temp))

    if len(scores) == 0:
        best_move = random.choice(moves)
    elif board.turn == True:
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]
    return best_move

def main(BOARD):

    '''
    for human vs human game
    '''
    #make background black
    screen.fill(COLORS["GREEN"])
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(screen,BOARD)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
                break

            # if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(COLORS["GREEN"])
                pos = pygame.mouse.get_pos()

                #find which square was clicked and index of it
                square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                index = (7-square[1])*8+(square[0])
                
                # if we are moving a piece
                if index in index_moves: 
                    move = moves[index_moves.index(index)]
                    BOARD.push(move)
                    index_moves.clear()
                    continue
                      
                # show possible moves
                # check the square that is clicked
                piece = BOARD.piece_at(index)
                #if empty pass
                if piece is None:
                    continue 
                #figure out what moves this piece can make
                all_moves = list(BOARD.legal_moves)
                moves = []
                for m in all_moves:
                    if m.from_square == index:
                        moves.append(m)
                        t = m.to_square
                        TX1 = 100*(t%8)
                        TY1 = 100*(7-t//8)
                        #highlight squares it can move to
                        pygame.draw.rect(screen, COLORS["YELLOW"], pygame.Rect(TX1,TY1,100,100),5)
                
                index_moves = [a.to_square for a in moves]
        # deactivates the pygame library
        if board.outcome():
            outcome = board.outcome()
            OUTPUT_STRING = f'The game ends with a {outcome.termination}.' + (f'{outcome.winner} wins the game' if outcome.winner else '')
            print(OUTPUT_STRING)
            status = False

board = chess.Board()
main_one_agent(board, min_max2)
# main(board)
