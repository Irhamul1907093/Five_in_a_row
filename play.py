from sys import exit
import pygame
from pygame.locals import *
from status import State
from game import GameRender
from AlphaBeta import ABPruningAI
import setup.game_setup as game_setup
import setup.ai_setup as ai_setup
import setup.ui_setup as ui_setup


if __name__ == "__main__":

    current_match = State()
    render = GameRender(current_match)
    ai = ABPruningAI(current_match)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(ui_setup.FPS)
        pygame.display.update()

        # DRAW
        if (len(current_match.moves) == game_setup.MAX_MOVE_COUNT):
            render.render_state(current_match.board, game_setup.NO_ONE, game_setup.NO_ONE, current_match.moves[-1])
            continue
        # AI move first
        if(game_setup.FIRST_TURN == game_setup.COM and len(current_match.moves) == 0):
            
            # Announcement
            print("AI is calculating next move...")
            print("---------------------------------")

            AI_calulation_time = -pygame.time.get_ticks()
            ai_move = ai.next_move()
            AI_calulation_time += pygame.time.get_ticks()
            
            # Announcement
            print("---------------------------------")
            print("AI calculation time: ", AI_calulation_time/1000 ," seconds (depth = ", ai_setup.MAX_TREE_DEPTH_LEVEL, ").")
            
            render.handle_com_move(ai_move, current_match)
            render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board), current_match.moves[-1])
        #
        # HUMAN move first
        #         
        for event in pygame.event.get():

            #exit
            if event.type == pygame.QUIT:
                running = False
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(render.is_new_game_button_pressed()):
                    current_match = State()
                    ai = ABPruningAI(current_match)
                    render.render_state(current_match.board, game_setup.FIRST_TURN, False, (-1, -1))
                    break

                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue
                
                # HUMAN turn
                if(current_match.current_turn == game_setup.HUMAN):

                    render.handle_human_move(current_match) 
                    render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board), current_match.moves[-1])
                    ai.state.board = current_match.board

                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue

                # AI turn
                if(current_match.current_turn == game_setup.COM):
                    
                    AI_calulation_time = -pygame.time.get_ticks()

                    # Announcement
                    print("AI is calculating next move...")
                    print("---------------------------------")

                    ai_move = ai.next_move()
                    AI_calulation_time += pygame.time.get_ticks()
                    
                    # Announcement
                    print("---------------------------------")
                    print("AI calculation time: ", AI_calulation_time/1000 ," seconds.")
                    
                    render.handle_com_move(ai_move, current_match)
                    render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board), current_match.moves[-1])

                    # Announcement
                    print("Waiting for HUMAN's move...")

                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue

                



