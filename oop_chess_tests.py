import constants
from oop_chess_backend import Pawn,Rook,Knight,Bishop,Queen,King,Board, print_board_data_table, board_table
index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

# Canonical Kiwipete position:
# r3k2r/p1ppqpb1/bn2pnp1/2pP4/1p2P3/2N2N1p/PPPBBPPP/R3K2R w KQkq - 0 1

# Pawns still on their original rank have moves=0. Pawns elsewhere use
# moves=1 so this engine does not give them another initial double move.
pieces_white = [
    Pawn("white", "pawn", [6, 0], 0, "wpa2", "♙", constants.white_pawn),
    Pawn("white", "pawn", [6, 1], 0, "wpb2", "♙", constants.white_pawn),
    Pawn("white", "pawn", [6, 2], 0, "wpc2", "♙", constants.white_pawn),
    Pawn("white", "pawn", [3, 3], 1, "wpd5", "♙", constants.white_pawn),
    Pawn("white", "pawn", [4, 4], 1, "wpe4", "♙", constants.white_pawn),
    Pawn("white", "pawn", [6, 5], 0, "wpf2", "♙", constants.white_pawn),
    Pawn("white", "pawn", [6, 6], 0, "wpg2", "♙", constants.white_pawn),
    Pawn("white", "pawn", [6, 7], 0, "wph2", "♙", constants.white_pawn),
    Rook("white", "rook", [7, 0], 0, "wra1", "♖", constants.white_rook),
    Rook("white", "rook", [7, 7], 0, "wrh1", "♖", constants.white_rook),
    Knight("white", "knight", [5, 2], 1, "wnc3", "♘", constants.white_knight),
    Queen("white", "queen", [5, 5], 1, "wqf3", "♕", constants.white_queen),
    Bishop("white", "bishop", [6, 3], 1, "wbd2", "♗", constants.white_bishop),
    Bishop("white", "bishop", [6, 4], 1, "wbe2", "♗", constants.white_bishop),
    King("white", "king", [7, 4], 0, "wke1", "♔", constants.white_king),
    Knight("white", "knight", [3,4], 0, "wne5", "♘", constants.white_knight)
]

pieces_black = [
    Pawn("black", "pawn", [1, 0], 0, "bpa7", "♟", constants.black_pawn),
    Pawn("black", "pawn", [4, 1], 1, "bpb4", "♟", constants.black_pawn),
    Pawn("black", "pawn", [1, 2], 0, "bpc7", "♟", constants.black_pawn),
    # Pawn("black", "pawn", [3, 2], 1, "bpc5", "♟", constants.black_pawn),
    Pawn("black", "pawn", [1, 3], 0, "bpd7", "♟", constants.black_pawn),
    Pawn("black", "pawn", [2, 4], 1, "bpe6", "♟", constants.black_pawn),
    Pawn("black", "pawn", [1, 5], 0, "bpf7", "♟", constants.black_pawn),
    Pawn("black", "pawn", [2, 6], 1, "bpg6", "♟", constants.black_pawn),
    Pawn("black", "pawn", [5, 7], 1, "bph3", "♟", constants.black_pawn),
    Rook("black", "rook", [0, 0], 0, "bra8", "♜", constants.black_rook),
    Rook("black", "rook", [0, 7], 0, "brh8", "♜", constants.black_rook),
    Knight("black", "knight", [2, 1], 1, "bnb6", "♞", constants.black_knight),
    Knight("black", "knight", [2, 5], 1, "bnf6", "♞", constants.black_knight),
    Bishop("black", "bishop", [2, 0], 1, "bba6", "♝", constants.black_bishop),
    Bishop("black", "bishop", [1, 6], 1, "bbg7", "♝", constants.black_bishop),
    Queen("black", "queen", [1, 4], 1, "bqe7", "♛", constants.black_queen),
    King("black", "king", [0, 4], 0, "bke8", "♚", constants.black_king),
]

# The backend creates its own global starting board during import. Clear its
# shared occupancy table before initializing this different test position.
for row in range(8):
    for col in range(8):
        board_table[row][col] = "_"

board1 = Board(pieces_white,pieces_black) 
# print_board_data_table(board_table)
board1.active_player_index = 0 # 0 = white, 1 = black

# amount of possible end positions
def perft(board, depth):
    if depth == 0:
        return 1
    
    nodes = 0
    legal_moves = board.get_moves() 
    
    for move in legal_moves:

        starting_pos, ending_pos, last_taken_pieces, valid_move, castling_info, previous_pawn_double_move = board.make_move(selected_piece=move[0],starting_pos=move[1],ending_pos=move[2]) 

        nodes_to_add = perft(board,depth-1)
        nodes += nodes_to_add

        # only undo move if it moved
        if valid_move or castling_info:
            board.undo_move(starting_pos,ending_pos, last_taken_pieces, castling_info, previous_pawn_double_move)

        
    return nodes

# amount of possible end positions for each first move
def perft_divide(board, depth):
    if depth == 0:
        return 
    
    total_nodes = 0
    legal_moves = board.get_moves()
    
    for move in legal_moves:

        starting_pos, ending_pos, last_taken_pieces, valid_move, castling_info, previous_pawn_double_move = board.make_move(selected_piece=move[0],starting_pos=move[1],ending_pos=move[2]) 

        nodes = perft(board, depth - 1)
        total_nodes += nodes

        # only undo move if it moved
        if valid_move or castling_info:
            board.undo_move(starting_pos, ending_pos, last_taken_pieces, castling_info, previous_pawn_double_move)

        print(f"{index_letter[move[1][1]]}{8-(move[1][0])} to {index_letter[move[2][1]]}{8-(move[2][0])}: {nodes}")
        
    print(f"\nTotal Leaf Nodes: {total_nodes}")


perft_divide(board1,3)
# 2 mins 40 seconds to run perft 5
