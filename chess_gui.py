import pygame
from sys import exit

from chess_backend import white, black, letter_index, index_letter, log_move, Castling, \
    is_opponent_in_check, is_opponents_next_moves_0, is_your_king_in_check, PawnPromotion, Takes
import constants
from constants import pos_to_pixel


def get_pixels(pos):
    """
    Convert a digit position into a pixel position
    :param pos: [row, col] board position as a tuple of digits
    :return: pixel position
    """

    row_pixel = constants.pos_to_pixel[pos[0]]
    col_pixel = constants.pos_to_pixel[pos[1]]

    return col_pixel, row_pixel

def pixel_to_board(x_pixel, y_pixel):
    """Convert a pixel click into a [row, col_letter] board position."""

    if y_pixel is None:
        return None, None

    col = x_pixel // constants.square_size
    row = y_pixel // constants.square_size

    col_letter = index_letter.get(col)
    return row, col_letter

pygame.init()
screen = constants.window_size
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# --- Game state ---
players = ["White", "Black"]
active_player_index = 0
selected_piece = None
available_moves = []
clicked_row = None
clicked_col = None
black_in_check = False
white_in_check = False
checkmate = False
stalemate = False
log_records = []

while constants.is_running:
    player = players[active_player_index]
    you = white if active_player_index == 0 else black
    opp = black if active_player_index == 0 else white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # saves game record
            log_move(log_records)
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not checkmate and not stalemate:
            x, y = event.pos
            if y > 800:
                y = None
            clicked_row, clicked_col = pixel_to_board(x, y)  # turns pixel pos into number letter pos

            if selected_piece is None:
                # First click: select a piece

                pieces = white if active_player_index == 0 else black

                for p in pieces:
                    if p["pos"] == [clicked_row, clicked_col]:
                        selected_piece = p

                        # get valid moves for this piece
                        available_moves = p["rule"](you, opp, p)

                        clicked_row_one, clicked_col_one = clicked_row, clicked_col
                        break
            else:
                # Second click: move if valid

                target = [clicked_row, letter_index[clicked_col]]
                you = white if active_player_index == 0 else black
                you_name = "White" if active_player_index == 0 else "Black"
                opp = black if active_player_index == 0 else white
                opp_name = "Black" if active_player_index == 0 else "White"

                clicked_row_two, clicked_col_two = clicked_row, clicked_col
                check_ = is_your_king_in_check(you, opp,
                                               selected_piece, clicked_row_two, clicked_col_two)

                if check_ and target in available_moves:
                    available_moves.remove(target)

                if target in available_moves:
                    clicked_row_two, clicked_col_two = clicked_row, clicked_col

                    # normal move
                    if ((selected_piece['type'] != 'king') or
                            (selected_piece['move'] != 0)):

                        record = {"player": player,
                                  "type": p["type"],
                                  "id": p["id"],
                                  "col": clicked_col,
                                  "row": clicked_row,}
                        log_records.append(record)

                        # move the piece
                        selected_piece["pos"] = [clicked_row, clicked_col]
                        selected_piece["move"] += 1

                    # check for castling
                    elif selected_piece["type"] == 'king' and selected_piece['move'] == 0:
                        king_row = selected_piece["pos"][0]  # e.g. 7
                        king_col = selected_piece["pos"][1]  # e.g. "e"

                        result = Castling(
                            black, white, letter_index, index_letter,
                            king_row,  # king's current row
                            king_col,  # king's current col letter
                            clicked_col_two,  # destination col letter
                            clicked_row_two,  # destination row
                            you  # your color
                        )

                        if result == "not_castling":
                            selected_piece['pos'] = [clicked_row_two, clicked_col_two]
                            selected_piece['move'] += 1
                        elif result == "done castling":
                            selected_piece['pos'] = [clicked_row_two, clicked_col_two]
                            selected_piece['move'] += 1

                    # remove any captured opponent piece
                    Takes(opp,selected_piece)

                    # pawn promotion
                    PawnPromotion(selected_piece, clicked_row, clicked_col)

                    # check and checkmate
                    white_in_check = False
                    black_in_check = False
                    check_ = is_opponent_in_check(you, opp)
                    if check_:
                        if opp == white:
                            white_in_check = True
                        elif opp == black:
                            black_in_check = True

                        checkmate = is_opponents_next_moves_0(you, opp)

                    #stalemate
                    if not check_:
                        stalemate = is_opponents_next_moves_0(you, opp)

                    # switch turns
                    active_player_index = (active_player_index + 1) % 2

                # either way, deselect
                selected_piece = None
                available_moves = []

    # Draw

    screen.blit(constants.board_surface, (0, 0))
    screen.blit(constants.surface_turn_background, (0, 800))

    for move in available_moves:
        # highlight available squares in yellow
        highlight = pygame.Surface((constants.square_size, constants.square_size),
                                   pygame.SRCALPHA)
        highlight.fill((250, 250, 0, 100))  # semi-transparent yellow

        px = pos_to_pixel[move[1]]
        py = pos_to_pixel[move[0]]

        screen.blit(highlight, (px - 25, py - 25))  # highlighted path is centered

        # highlight under selected piece in red
        square_row = constants.pos_to_pixel[clicked_row]
        square_col = constants.pos_to_pixel[letter_index[clicked_col]]

        cancel_move = pygame.Surface((constants.square_size, constants.square_size), pygame.SRCALPHA)
        cancel_move.fill((255, 0, 0, 100))  # semi-transparent red

        screen.blit(cancel_move, (square_col - 25, square_row - 25))

    # draw all pieces
    for piece in black + white:
        digit_pos = piece["pos"][0], letter_index[piece["pos"][1]]
        pos_in_pixels = get_pixels(digit_pos)
        screen.blit(piece["image"], pos_in_pixels)

        if piece["color"] == "black" and piece["type"] == "king":
            if black_in_check:
                king_digit_pos = piece["pos"][0], letter_index[piece["pos"][1]]
                king_pos_in_pixels = get_pixels(king_digit_pos)

                check_king_surface = pygame.Surface((constants.square_size, constants.square_size),
                                                    pygame.SRCALPHA)
                check_king_surface.fill((0,0,255,100))
                screen.blit(check_king_surface, (king_pos_in_pixels[0]-25,king_pos_in_pixels[1]-25))
        if piece["color"] == "white" and piece["type"] == "king":
            if white_in_check:
                king_digit_pos = piece["pos"][0], letter_index[piece["pos"][1]]
                king_pos_in_pixels = get_pixels(king_digit_pos)

                check_king_surface = pygame.Surface((constants.square_size, constants.square_size),
                                                    pygame.SRCALPHA)
                check_king_surface.fill((0,0,255,100))
                screen.blit(check_king_surface, (king_pos_in_pixels[0]-25,king_pos_in_pixels[1]-25))

    # text
    if stalemate:
        turn_text = constants.font_turn.render(f"Game over! Tie by stalemate!", True, "Black")
    elif checkmate:
        turn_text = constants.font_turn.render(f"Game over! {you_name} wins by checkmate!", True, "Black")
    elif black_in_check or white_in_check:
        turn_text = constants.font_turn.render(f"{player}'s turn, you are in check!", True, "Black")
    else:
        turn_text = constants.font_turn.render(f"It's {player}'s turn.", True, "Black")
    screen.blit(turn_text, (10, 810))

    pygame.display.update()
    clock.tick(60)
