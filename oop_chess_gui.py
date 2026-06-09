import pygame
from pygame.locals import *
from oop_chess_backend import pieces_white, pieces_black, is_your_king_in_check


pygame.init()
pygame.display.set_caption("Chess V2")
clock = pygame.time.Clock()
import constants


def get_pixels(pos):
    """ Convert a digit position into a pixel position """

    row_pixel = constants.pos_to_pixel[pos[0]]
    col_pixel = constants.pos_to_pixel[pos[1]]
    return col_pixel, row_pixel

def pixel_to_board(x_pixel, y_pixel):
    #Convert a pixel click into a row, col board position

    if y_pixel is None:
        return None, None

    col = x_pixel // constants.square_size
    row = y_pixel // constants.square_size

    return row, col

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1000, 900
        self.active_player_index = 0
        self.you = pieces_white if self.active_player_index == 0 else pieces_black
        self.opp = pieces_black if self.active_player_index == 0 else pieces_white
        self.selected_piece = None
        self.log_records = []

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            x,y = event.pos
            clicked_row, clicked_col = pixel_to_board(x, y)  

            if self.selected_piece is None:
                # First click: select a piece

                for p in self.you:
                    if p.pos == [clicked_row, clicked_col]:
                        self.selected_piece = p

                        # get valid moves for this piece
                        available_moves = p.rule(pieces_white, pieces_black)
                        break
            else:
                # Second click: move if valid

                target = [clicked_row, clicked_col]
                clicked_row_two, clicked_col_two = clicked_row, clicked_col
                
                check_ = is_your_king_in_check(self.you, self.opp, self.selected_piece, clicked_row_two, clicked_col_two, pieces_white,pieces_black)

                if check_ and target in available_moves:
                    available_moves.remove(target)

                if target in available_moves:
                    clicked_row_two, clicked_col_two = clicked_row, clicked_col

                    # normal move
                    if ((self.selected_piece.type != 'king') or
                            (self.selected_piece.moves != 0)):

                        player = "white" if self.you == pieces_white else "black"

                        record = {"player": player,
                                "type": p.type,
                                "id": p.id,
                                "col": clicked_col,
                                "row": clicked_row,}
                        self.log_records.append(record)

                        # move the piece
                        self.selected_piece.pos = [clicked_row, clicked_col]
                        print("piece moved!")
            self.selected_piece.moves += 1
            print(x,y)
    
    def on_loop(self):
        
        self.screen.blit(constants.board_surface, (0, 0))
        self.screen.blit(constants.surface_turn_background, (0, 800))
        self.screen.blit(constants.taken_pieces, (800,0))

        # draw all pieces
        for piece in pieces_white + pieces_black:
            digit_pos = piece.pos
            pos_in_pixels = get_pixels(digit_pos)
            self.screen.blit(piece.image, pos_in_pixels)

        pygame.display.update()

    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
