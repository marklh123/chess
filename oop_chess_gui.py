import pygame  
from pygame.locals import *
from oop_chess_backend import pieces_white, pieces_black, is_your_king_in_check, Castling, Takes, PawnPromotion \
    , is_opponent_king_in_check, is_checkmate_opponent


pygame.init()
pygame.display.set_caption("Chess V2")
clock = pygame.time.Clock()
from constants import pos_to_pixel
import constants
import random

def get_pixels(pos):
    # Convert a digit position into a pixel position

    row_pixel = constants.pos_to_pixel[pos[0]]
    col_pixel = constants.pos_to_pixel[pos[1]]
    return col_pixel, row_pixel

def pixel_to_board(x_pixel, y_pixel):
    # Convert a pixel click into a row, col board position

    if y_pixel is None:
        return None, None

    col = x_pixel // constants.square_size
    row = y_pixel // constants.square_size

    return row, col

class App:
    def __init__(self):
        self.pre_game = True
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1000, 900
        self.active_player_index = 0
        self.you = pieces_white
        self.opp = pieces_black
        self.selected_piece = None
        self.clicked_row = None
        self.clicked_col = None
        self.white_in_check = False
        self.black_in_check = False
        self.checkmate = False
        self.stalemate = False
        self.available_moves = []
        self.log_records = []
        self.taken_pieces_white = []
        self.taken_pieces_black = []
        self.pve = False

    def set_player_and_opp(self):
        self.you = pieces_white if self.active_player_index == 0 else pieces_black
        self.opp = pieces_black if self.active_player_index == 0 else pieces_white

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True
    
    def select_and_move_piece(self):
        # first click: select a piece
        if self.selected_piece is None:
            # for humans
            if not self.pve or (self.pve and self.active_player_index == 0):
                for p in self.you:
                    if p.pos == [self.clicked_row, self.clicked_col]:
                        self.selected_piece = p

                        # get valid moves for this piece
                        self.available_moves = p.rule(pieces_white, pieces_black)
                        break
            # for bot
            else:
                self.bot_select_piece()        

        # second click: check if move valid
        else:
            # see if target position is valid first
            target = [self.clicked_row, self.clicked_col]
            clicked_row_two, clicked_col_two = self.clicked_row, self.clicked_col
            
            check_ = is_your_king_in_check(self.you, self.opp, self.selected_piece, clicked_row_two, clicked_col_two, pieces_white,pieces_black)

            # can't do moves that don't save king while in check
            if check_ and target in self.available_moves:
                self.available_moves.remove(target)

            if target in self.available_moves:
                valid_move = False

                # normal move
                if ((self.selected_piece.type != 'king') or
                        (self.selected_piece.moves != 0)):

                    player = "white" if self.you == pieces_white else "black"

                    record = {"player": player,
                            "type": self.selected_piece.type,
                            "id": self.selected_piece.id,
                            "col": self.clicked_col,
                            "row": self.clicked_row,}
                    self.log_records.append(record)
                    valid_move = True
                
                # check for castling
                elif self.selected_piece.type == 'king' and self.selected_piece.moves == 0:
                    king_row = self.selected_piece.pos[0] 
                    king_col = self.selected_piece.pos[1]  

                    result = Castling(
                        pieces_black, 
                        pieces_white,
                        king_row,  # king's current row
                        king_col,  # king's current col letter
                        clicked_col_two,  # destination col letter
                        clicked_row_two,  # destination row
                        self.you  # your color
                    )

                    # if castling didn't fail its a valid move
                    if result != "cancel castling":
                        valid_move = True
                        
                # move the piece
                if valid_move:
                    self.selected_piece.pos = [clicked_row_two, clicked_col_two]
                    self.selected_piece.moves += 1
                
                # remove any captured opponent piece
                Takes(pieces_white,pieces_black,self.selected_piece,self.taken_pieces_white,self.taken_pieces_black)

                # pawn promotion
                PawnPromotion(self.selected_piece, self.clicked_row, self.clicked_col, pieces_white, pieces_black)

                # check and checkmate (for text)
                self.white_in_check = False
                self.black_in_check = False

                check_ = is_opponent_king_in_check(self.you, self.opp, pieces_white, pieces_black)
                if check_:
                    if self.opp == pieces_white:
                        self.white_in_check = True
                    elif self.opp == pieces_black:
                        self.black_in_check = True

                    self.checkmate = is_checkmate_opponent(self.you, self.opp,pieces_white,pieces_black)
                
                elif not check_:
                    self.stalemate = is_checkmate_opponent(self.you, self.opp,pieces_white,pieces_black)

                self.active_player_index = (self.active_player_index + 1) % 2
                
            # either way, deselect
            self.selected_piece = None
            self.clicked_row = None
            self.clicked_col = None
            self.available_moves = []

    def bot_select_piece(self):
        self.set_player_and_opp()
        self.selected_piece = random.choice(self.you)
        self.available_moves = self.selected_piece.rule(pieces_white, pieces_black)

        if len(self.available_moves) == 0:
            self.bot_select_piece()
            return # stops after inner function ends 

        self.clicked_row, self.clicked_col = random.choice(self.available_moves)

    def on_loop(self):
            # check if its now bots turn
            if self.active_player_index == 1 and self.pve:
                self.select_and_move_piece()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            x,y = event.pos
            
            # title screen button areas, select gamemode
            if self.pre_game:
                if x in range(220,470) and y in range(400,600):
                    self.pre_game = False
                elif x in range(520,770) and y in range(400,600):
                    self.pve = True
                    self.pre_game = False

            # after title screen, actual game
            else:
                if not self.checkmate or self.stalemate:
                    # change player and opponent based of active player index count
                    self.set_player_and_opp()
                    self.clicked_row, self.clicked_col = pixel_to_board(x, y)  
                    
                    self.select_and_move_piece()
                
    def on_render(self):
        if not self.pre_game:
            self.screen.blit(constants.board_surface, (0, 0))
            self.screen.blit(constants.surface_turn_background, (0, 800))
            self.screen.blit(constants.taken_pieces, (800,0))

            # highlight squares for players move
            if self.selected_piece and not self.pve or (self.pve and self.you == pieces_white):
                for move in self.available_moves:
                    # highlight available squares in yellow
                    highlight = pygame.Surface((constants.square_size, constants.square_size),
                                            pygame.SRCALPHA)
                    highlight.fill((250, 250, 0, 100)) 

                    px = pos_to_pixel[move[1]]
                    py = pos_to_pixel[move[0]]

                    self.screen.blit(highlight, (px - 25, py - 25))  # highlighted path is centered

                    # highlight under selected piece in red
                    square_row = constants.pos_to_pixel[self.clicked_row]
                    square_col = constants.pos_to_pixel[self.clicked_col]

                    cancel_move = pygame.Surface((constants.square_size, constants.square_size), pygame.SRCALPHA)
                    cancel_move.fill((255, 0, 0, 100)) 

                    self.screen.blit(cancel_move, (square_col - 25, square_row - 25))

            # draw all pieces
            for piece in pieces_white + pieces_black:
                digit_pos = piece.pos
                pos_in_pixels = get_pixels(digit_pos)
                self.screen.blit(piece.image, pos_in_pixels)
            
                if piece.color == "black" and piece.type == "king":
                    if self.black_in_check:
                        king_digit_pos = piece.pos[0], piece.pos[1]
                        king_pos_in_pixels = get_pixels(king_digit_pos)

                        check_king_surface = pygame.Surface((constants.square_size, constants.square_size),
                                                            pygame.SRCALPHA)
                        check_king_surface.fill((0,0,255,100))
                        self.screen.blit(check_king_surface, (king_pos_in_pixels[0]-25,king_pos_in_pixels[1]-25))
                if piece.color == "white" and piece.type == "king":
                    if self.white_in_check:
                        king_digit_pos = piece.pos[0], piece.pos[1]
                        king_pos_in_pixels = get_pixels(king_digit_pos)

                        check_king_surface = pygame.Surface((constants.square_size, constants.square_size),
                                                            pygame.SRCALPHA)
                        check_king_surface.fill((0,0,255,100))
                        self.screen.blit(check_king_surface, (king_pos_in_pixels[0]-25,king_pos_in_pixels[1]-25))

            # draw taken pieces
            for x, piece in enumerate(self.taken_pieces_black):
                self.screen.blit(piece.image, constants.spots_black[x])
            for x, piece in enumerate(self.taken_pieces_white):
                self.screen.blit(piece.image, constants.spots_white[x])
            
            # text
            name = "white" if self.active_player_index == 0 else "black"
            name2 = "white" if self.active_player_index == 1 else "black"

            if self.stalemate:
                turn_text = constants.font_turn.render(f"Game over! Tie by stalemate!", True, "Black")
            elif self.checkmate:
                turn_text = constants.font_turn.render(f"Game over! {name2} wins by checkmate!", True, "Black")
            elif self.black_in_check or self.white_in_check:
                turn_text = constants.font_turn.render(f"{name}'s turn, you are in check!", True, "Black")
            else:
                turn_text = constants.font_turn.render(f"It's {name}'s turn.", True, "Black")
            
            self.screen.blit(turn_text, (10, 810))
        elif self.pre_game:
            self.screen.blit(constants.pre_game_background,(0,0))
            self.screen.blit(constants.pregame_text,(325,250))
            self.screen.blit(constants.pvp_background,(220,400))
            self.screen.blit(constants.pvp_text,(250,440))
            self.screen.blit(constants.pve_background,(520,400))
            self.screen.blit(constants.pve_text,(550,440))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
