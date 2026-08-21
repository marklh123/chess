import constants
from oop_chess_backend import Pawn,Rook,Knight,Bishop,Queen,King,Board
index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

# White pieces

p1w = Pawn(
    color="white", type="pawn", pos=[6, 0], moves=0,
    id="p1w", symbol="♙", image=constants.white_pawn
)
p2w = Pawn(
    color="white", type="pawn", pos=[6, 1], moves=0,
    id="p2w", symbol="♙", image=constants.white_pawn
)
p3w = Pawn(
    color="white", type="pawn", pos=[6, 2], moves=0,
    id="p3w", symbol="♙", image=constants.white_pawn
)
p4w = Pawn(
    color="white", type="pawn", pos=[6, 3], moves=0,
    id="p4w", symbol="♙", image=constants.white_pawn
)
p5w = Pawn(
    color="white", type="pawn", pos=[6, 4], moves=0,
    id="p5w", symbol="♙", image=constants.white_pawn
)
p6w = Pawn(
    color="white", type="pawn", pos=[6, 5], moves=0,
    id="p6w", symbol="♙", image=constants.white_pawn
)
p7w = Pawn(
    color="white", type="pawn", pos=[6, 6], moves=0,
    id="p7w", symbol="♙", image=constants.white_pawn
)
p8w = Pawn(
    color="white", type="pawn", pos=[6, 7], moves=0,
    id="p8w", symbol="♙", image=constants.white_pawn
)

r1w = Rook(
    color="white", type="rook", pos=[7, 0], moves=0,
    id="r1w", symbol="♖", image=constants.white_rook
)
r2w = Rook(
    color="white", type="rook", pos=[7, 7], moves=0,
    id="r2w", symbol="♖", image=constants.white_rook
)

k1w = Knight(
    color="white", type="knight", pos=[7, 1], moves=0,
    id="k1w", symbol="♘", image=constants.white_knight
)
k2w = Knight(
    color="white", type="knight", pos=[7, 6], moves=0,
    id="k2w", symbol="♘", image=constants.white_knight
)

b1w = Bishop(
    color="white", type="bishop", pos=[7, 2], moves=0,
    id="b1w", symbol="♗", image=constants.white_bishop
)
b2w = Bishop(
    color="white", type="bishop", pos=[7, 5], moves=0,
    id="b2w", symbol="♗", image=constants.white_bishop
)

qw = Queen(
    color="white", type="queen", pos=[7, 3], moves=0,
    id="qw", symbol="♕", image=constants.white_queen
)

kingw = King(
    color="white", type="king", pos=[7, 4], moves=0,
    id="kingw", symbol="♔", image=constants.white_king
)


# Black pieces

p1b = Pawn(
    color="black", type="pawn", pos=[1, 0], moves=0,
    id="p1b", symbol="♟", image=constants.black_pawn
)
p2b = Pawn(
    color="black", type="pawn", pos=[1, 1], moves=0,
    id="p2b", symbol="♟", image=constants.black_pawn
)
p3b = Pawn(
    color="black", type="pawn", pos=[1, 2], moves=0,
    id="p3b", symbol="♟", image=constants.black_pawn
)
p4b = Pawn(
    color="black", type="pawn", pos=[1, 3], moves=0,
    id="p4b", symbol="♟", image=constants.black_pawn
)
p5b = Pawn(
    color="black", type="pawn", pos=[1, 4], moves=0,
    id="p5b", symbol="♟", image=constants.black_pawn
)
p6b = Pawn(
    color="black", type="pawn", pos=[1, 5], moves=0,
    id="p6b", symbol="♟", image=constants.black_pawn
)
p7b = Pawn(
    color="black", type="pawn", pos=[1, 6], moves=0,
    id="p7b", symbol="♟", image=constants.black_pawn
)
p8b = Pawn(
    color="black", type="pawn", pos=[1, 7], moves=0,
    id="p8b", symbol="♟", image=constants.black_pawn
)

r1b = Rook(
    color="black", type="rook", pos=[0, 0], moves=0,
    id="r1b", symbol="♜", image=constants.black_rook
)
r2b = Rook(
    color="black", type="rook", pos=[0, 7], moves=0,
    id="r2b", symbol="♜", image=constants.black_rook
)

k1b = Knight(
    color="black", type="knight", pos=[0, 1], moves=0,
    id="k1b", symbol="♞", image=constants.black_knight
)
k2b = Knight(
    color="black", type="knight", pos=[0, 6], moves=0,
    id="k2b", symbol="♞", image=constants.black_knight
)

b1b = Bishop(
    color="black", type="bishop", pos=[0, 2], moves=0,
    id="b1b", symbol="♝", image=constants.black_bishop
)
b2b = Bishop(
    color="black", type="bishop", pos=[0, 5], moves=0,
    id="b2b", symbol="♝", image=constants.black_bishop
)

qb = Queen(
    color="black", type="queen", pos=[0, 3], moves=0,
    id="qb", symbol="♛", image=constants.black_queen
)

kingb = King(
    color="black", type="king", pos=[0, 4], moves=0,
    id="kingb", symbol="♚", image=constants.black_king
)


pieces_white = [
    p1w, p2w, p3w, p4w, p5w, p6w, p7w, p8w,
    r1w, r2w, k1w, k2w, b1w, b2w, qw, kingw
]

pieces_black = [
    p1b, p2b, p3b, p4b, p5b, p6b, p7b, p8b,
    r1b, r2b, k1b, k2b, b1b, b2b, qb, kingb
]

board1 = Board(pieces_white,pieces_black) 
board1.active_player_index = 0 # 0 = white, 1 = black

# amount of possible end positions
def perft(board, depth):
    if depth == 0:
        return 1
    
    nodes = 0
    legal_moves = board.get_moves() 

    # if depth == 2:
    #     print(f"There are {len(legal_moves)} legal moves")
    
    for move in legal_moves:

        # if depth == 2:
        #     print(f"white plays {index_letter[move[0][1]]}{8-(move[0][0])} to {index_letter[move[1][1]]}{8-(move[1][0])}")

        # print(f"move is {move} and type is {type(move)}")
        starting_pos, ending_pos, last_taken_pieces, valid_move = board.make_move(move[0],move[1]) # move the piece and give starting and ending positions for it

        # if depth == 1:
        #     print(f"{index_letter[starting_pos[1]]}{8-starting_pos[0]} to {index_letter[ending_pos[1]]}{8-(ending_pos[0])}")

        nodes_to_add = perft(board,depth-1)
        # if depth == 2:
        #     print("Nodes to add: ", nodes_to_add)
        nodes += nodes_to_add

        # only undo move if it moved
        if valid_move:
            board.undo_move(starting_pos,ending_pos, last_taken_pieces)

        
    return nodes

# amount of possible end positions for each first move
def perft_divide(board, depth):
    if depth == 0:
        return
    
    total_nodes = 0
    legal_moves = board.get_moves()
    
    for move in legal_moves:

        starting_pos, ending_pos, last_taken_pieces, valid_move = board.make_move(move[0],move[1]) 

        nodes = perft(board, depth - 1)
        total_nodes += nodes

        # only undo move if it moved
        if valid_move:
            board.undo_move(starting_pos, ending_pos, last_taken_pieces)

        print(f"{index_letter[move[0][1]]}{8-(move[0][0])} to {index_letter[move[1][1]]}{8-(move[1][0])}: {nodes}")
        
    print(f"\nTotal Leaf Nodes: {total_nodes}")


perft_divide(board1,5)

