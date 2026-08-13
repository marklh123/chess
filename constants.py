import pygame

pygame.init()

# piece images
black_queen = pygame.image.load('./assets/images/black_queen1.png')
black_queen = pygame.transform.scale(black_queen, (50, 70))
black_queen_tiny = pygame.transform.scale(black_queen, (45, 60))
black_king = pygame.image.load('./assets/images/black_king1.png')
black_king = pygame.transform.scale(black_king, (50, 70))
black_rook = pygame.image.load('./assets/images/black_rook1.png')
black_rook = pygame.transform.scale(black_rook, (50, 70))
black_rook_tiny = pygame.transform.scale(black_rook, (45, 60))
black_bishop = pygame.image.load('./assets/images/black_bishop1.png')
black_bishop = pygame.transform.scale(black_bishop, (50, 70))
black_bishop_tiny = pygame.transform.scale(black_bishop, (45, 60))
black_knight = pygame.image.load('./assets/images/black_knight1.png')
black_knight = pygame.transform.scale(black_knight, (50, 70))
black_knight_tiny = pygame.transform.scale(black_knight, (45, 60))
black_pawn = pygame.image.load('./assets/images/black_pawn1.png')
black_pawn = pygame.transform.scale(black_pawn, (50, 70))
black_pawn_tiny = pygame.transform.scale(black_pawn, (45, 60))
white_queen = pygame.image.load('./assets/images/white_queen1.png')
white_queen = pygame.transform.scale(white_queen, (50, 70))
white_queen_tiny = pygame.transform.scale(white_queen, (45, 60))
white_king = pygame.image.load('./assets/images/white_king1.png')
white_king = pygame.transform.scale(white_king, (50, 70))
white_rook = pygame.image.load('./assets/images/white_rook1.png')
white_rook = pygame.transform.scale(white_rook, (50, 70))
white_rook_tiny = pygame.transform.scale(white_rook, (45, 60))
white_bishop = pygame.image.load('./assets/images/white_bishop1.png')
white_bishop = pygame.transform.scale(white_bishop, (50, 70))
white_bishop_tiny = pygame.transform.scale(white_bishop, (45, 60))
white_knight = pygame.image.load('./assets/images/white_knight1.png')
white_knight = pygame.transform.scale(white_knight, (50, 70))
white_knight_tiny = pygame.transform.scale(white_knight, (45, 60))
white_pawn = pygame.image.load('./assets/images/white_pawn1.png')
white_pawn = pygame.transform.scale(white_pawn, (50, 70))
white_pawn_tiny = pygame.transform.scale(white_pawn, (45, 60))


yellow_spell_step_1 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step1_2.png')
yellow_spell_step_1 = pygame.transform.scale(yellow_spell_step_1, (90,90))
yellow_spell_step_2 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step2_2.png')
yellow_spell_step_2 = pygame.transform.scale(yellow_spell_step_2, (90,90))
yellow_spell_step_3 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step3_2.png')
yellow_spell_step_3 = pygame.transform.scale(yellow_spell_step_3, (90,90))
yellow_spell_step_4 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step4_2.png')
yellow_spell_step_4 = pygame.transform.scale(yellow_spell_step_4, (90,90))
yellow_spell_step_5 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step5_2.png')
yellow_spell_step_5 = pygame.transform.scale(yellow_spell_step_5, (90,90))
yellow_spell_step_6 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step6_2.png')
yellow_spell_step_6 = pygame.transform.scale(yellow_spell_step_6, (90,90))
yellow_spell_step_7 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step7_2.png')
yellow_spell_step_7 = pygame.transform.scale(yellow_spell_step_7, (90,90))
yellow_spell_step_8 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step8_2.png')
yellow_spell_step_8 = pygame.transform.scale(yellow_spell_step_8, (90,90))
yellow_spell_step_9 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step9_2.png')
yellow_spell_step_9 = pygame.transform.scale(yellow_spell_step_9, (90,90))
yellow_spell_step_10 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step10_2.png')
yellow_spell_step_10 = pygame.transform.scale(yellow_spell_step_10, (90,90))
yellow_spell_step_11 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step11_2.png')
yellow_spell_step_11 = pygame.transform.scale(yellow_spell_step_11, (90,90))
yellow_spell_step_12 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step12_2.png')
yellow_spell_step_12 = pygame.transform.scale(yellow_spell_step_12, (90,90))
yellow_spell_step_13 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step13_2.png')
yellow_spell_step_13 = pygame.transform.scale(yellow_spell_step_13, (90,90))
yellow_spell_step_14 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step14_2.png')
yellow_spell_step_14 = pygame.transform.scale(yellow_spell_step_14, (90,90))
yellow_spell_step_15 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step15_2.png')
yellow_spell_step_15 = pygame.transform.scale(yellow_spell_step_15, (90,90))
yellow_spell_step_16 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step16_2.png')
yellow_spell_step_16 = pygame.transform.scale(yellow_spell_step_16, (90,90))
yellow_spell_step_17 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step17_2.png')
yellow_spell_step_17 = pygame.transform.scale(yellow_spell_step_17, (90,90))
yellow_spell_step_18 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step18_2.png')
yellow_spell_step_18 = pygame.transform.scale(yellow_spell_step_18, (90,90))
yellow_spell_step_19 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step19_2.png')
yellow_spell_step_19 = pygame.transform.scale(yellow_spell_step_19, (90,90))
yellow_spell_step_20 = pygame.image.load('./assets/images/yellow_spell_steps_2/yellow_spell_step20_2.png')
yellow_spell_step_20 = pygame.transform.scale(yellow_spell_step_20, (90,90))

yellow_animation_list = [yellow_spell_step_1,yellow_spell_step_2,yellow_spell_step_3,yellow_spell_step_4,yellow_spell_step_5,yellow_spell_step_6,yellow_spell_step_7,yellow_spell_step_8,yellow_spell_step_9,yellow_spell_step_10,yellow_spell_step_11,yellow_spell_step_12,yellow_spell_step_13,yellow_spell_step_14,yellow_spell_step_15,yellow_spell_step_16,yellow_spell_step_17,yellow_spell_step_18,yellow_spell_step_19,yellow_spell_step_20]
yellow_current_index = 0
yellow_current_image = yellow_animation_list[yellow_current_index]



purple_spell_step_1 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell1.png')
purple_spell_step_1 = pygame.transform.scale(purple_spell_step_1, (130,130))
purple_spell_step_2 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell2.png')
purple_spell_step_2 = pygame.transform.scale(purple_spell_step_2, (130,130))
purple_spell_step_3 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell3.png')
purple_spell_step_3 = pygame.transform.scale(purple_spell_step_3, (130,130))
purple_spell_step_4 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell4.png')
purple_spell_step_4 = pygame.transform.scale(purple_spell_step_4, (130,130))
purple_spell_step_5 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell5.png')
purple_spell_step_5 = pygame.transform.scale(purple_spell_step_5, (130,130))
purple_spell_step_6 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell6.png')
purple_spell_step_6 = pygame.transform.scale(purple_spell_step_6, (130,130))
purple_spell_step_7 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell7.png')
purple_spell_step_7 = pygame.transform.scale(purple_spell_step_7, (130,130))
purple_spell_step_8 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell8.png')
purple_spell_step_8 = pygame.transform.scale(purple_spell_step_8, (130,130))
purple_spell_step_9 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell9.png')
purple_spell_step_9 = pygame.transform.scale(purple_spell_step_9, (130,130))
purple_spell_step_10 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell10.png')
purple_spell_step_10 = pygame.transform.scale(purple_spell_step_10, (130,130))
purple_spell_step_11 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell11.png')
purple_spell_step_11 = pygame.transform.scale(purple_spell_step_11, (130,130))
purple_spell_step_12 = pygame.image.load('./assets/images/purple_spell_frames/purple_spell12.png')
purple_spell_step_12 = pygame.transform.scale(purple_spell_step_12, (130,130))

purple_animation_list = [purple_spell_step_1,purple_spell_step_2,purple_spell_step_3,purple_spell_step_4,purple_spell_step_5,purple_spell_step_6,purple_spell_step_7,purple_spell_step_8,purple_spell_step_9,purple_spell_step_10,purple_spell_step_11,purple_spell_step_12]
purple_current_index = 0
purple_current_image = purple_animation_list[purple_current_index]
purple_current_image.set_alpha(100)



cancel_move = pygame.image.load('./assets/images/redx.png')
cancel_move.set_alpha(128)
cancel_move = pygame.transform.scale(cancel_move, (170,170))

window_size = pygame.display.set_mode((800,900))

# board background image
board_surface = pygame.image.load("./assets/images/board.png")
board_surface = pygame.transform.scale(board_surface, (800, 800))

# where text will be under board
surface_turn_background = pygame.Surface((1000,900)) # width and height
surface_turn_background.fill((0,0,0))
# font_turn = pygame.font.Font(None, 50) # font type, font size
font_turn = pygame.font.Font('./assets/fonts/alagard.ttf',45)

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
pvp_text = font_turn.render(f"PVP", True, "White")

pve_background = pygame.Surface((250,200)) 
pve_background.fill((130,170,230))
pve_text = font_turn.render(f"BOT", True, "White")

move_piece_sound = pygame.mixer.Sound("./assets/sounds/piece_movement.mp3")
check_sound = pygame.mixer.Sound("./assets/sounds/check.mp3")
checkmate_sound = pygame.mixer.Sound("./assets/sounds/checkmate.mp3")

is_running = True

square_size = 100
