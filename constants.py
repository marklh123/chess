import pygame

pygame.init()

# piece images
black_queen = pygame.image.load('./assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (50, 50))
black_queen_tiny = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('./assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (50, 50))
black_rook = pygame.image.load('./assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (50, 50))
black_rook_tiny = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('./assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (50, 50))
black_bishop_tiny = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('./assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (50, 50))
black_knight_tiny = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('./assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (50, 50))
black_pawn_tiny = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('./assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (50, 50))
white_queen_tiny = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('./assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (50, 50))
white_rook = pygame.image.load('./assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (50, 50))
white_rook_tiny = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('./assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (50, 50))
white_bishop_tiny = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('./assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (50, 50))
white_knight_tiny = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('./assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (50, 50))
white_pawn_tiny = pygame.transform.scale(white_pawn, (45, 45))


window_size = pygame.display.set_mode((800,900))

# board background image
board_surface = pygame.image.load("./assets/images/board.png")
board_surface = pygame.transform.scale(board_surface, (800, 800))

# where text will be under board
surface_turn_background = pygame.Surface((800,100)) # width and height
surface_turn_background.fill((160, 199, 250))
font_turn = pygame.font.Font(None, 50) # font type, font size

# shows taken pieces section
taken_pieces = pygame.Surface((200,900))
taken_pieces.fill((160, 199, 250))
spots_black = [(810,25), (856.6,25), (903.2,25), (950,25), 
               (810,125), (856.6,125), (903.2, 125), (950,125), 
               (810,225), (856.6,225), (903.2, 225), (950,225),
               (810,325), (856.6,325), (903.2, 325), (950,325)]

spots_white = [(810,425), (856.6,425), (903.2,425), (950,425), 
               (810,525), (856.6,525), (903.2, 525), (950,525), 
               (810,625), (856.6,625), (903.2, 625), (950,625),
               (810,725), (856.6,725), (903.2, 725), (950,725)]


pos_to_pixel = {0:25,1:125,2:225,3:325,4:425,5:525,6:625,7:725}
pos_to_pixel_reversed = {0:725,1:625,2:525,3:425,4:325,5:225,6:125,7:25}

# pre game UI, choose gamemode
pre_game_background = pygame.Surface((1000,900)) 
pre_game_background.fill((160, 199, 250))

pregame_text = font_turn.render(f"Choose A Gamemode", True, "Black")

pvp_background = pygame.Surface((250,200)) 
pvp_background.fill((130,170,230))
pvp_text = font_turn.render(f"PVP", True, "Black")

pve_background = pygame.Surface((250,200)) 
pve_background.fill((130,170,230))
pve_text = font_turn.render(f"BOT", True, "Black")



is_running = True

square_size = 100
