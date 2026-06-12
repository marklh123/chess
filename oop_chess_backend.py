import copy
import constants
letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

#BUG: king cant take rooks 

class Board:
    def __init__(self,pieces_white,pieces_black):
        self.board_data = [["_" for _ in range(8)] for _ in range(8)]
        self.active_player_index = 0
        self.pieces_white = pieces_white
        self.pieces_black = pieces_black
        self.taken_list_white = []
        self.taken_list_black = []

    def board_print(self):

        # reset board state
        self.board_data = [["_" for _ in range(8)] for _ in range(8)]

        for x in self.pieces_white + self.pieces_black:
            row = x.pos[0]
            col = x.pos[1]
            self.board_data[row][col] = x.symbol

        print("    a   b   c   d   e   f   g   h")
        if self.active_player_index == 0:
            for x,y in enumerate(self.board_data):
                print((8-x)," ","   ".join(y)," ",(8-x))
        else:
            for x,y in enumerate(reversed(self.board_data)):
                print((x+1)," ","   ".join(y)," ",(x+1))
        print("    a   b   c   d   e   f   g   h")

    def change_turns(self):
        self.active_player_index = (self.active_player_index + 1) % 2
class Piece():
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        self.color = color
        self.type = type
        self.pos = pos
        self.moves = moves
        self.id = id
        self.symbol = symbol
        self.image = image
   
    def __getstate__(self):
            # Defines exactly what data from a Python class should be saved (serialized) when exporting it to a file or stream or copy
            state = self.__dict__.copy()
            if 'image' in state:
                del state['image']
            return state

    def __setstate__(self, state):
        # Restore the state and give image a default value
        self.__dict__.update(state)
        self.image = None


class Pawn(Piece):  
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id, symbol,image)
    def rule_pawn_takes(self,pieces_white,pieces_black):
        if self.color == "white":
            direction = -1
            op_pieces = pieces_black
        else:
            direction = 1
            op_pieces =pieces_white

        takes = []

        row, col = self.pos

        for op in op_pieces:
            op_row = op.pos[0]
            op_col = op.pos[1]

            if (([op_row, op_col] == [row + direction, col + 1]) or
                ([op_row, op_col] == [row + direction, col - 1])):
                takes.append([op_row, op_col])

        return takes
    def rule(self,pieces_white,pieces_black):

        row, col = self.pos

        if self.color == "white":
            direction = -1
        else:
            direction = 1

        if self.moves == 0:
            new_moves = [(0, direction) , (0, direction*2)]
        else:
            new_moves = [(0, direction)]
        
        new_pos = []
        for move in new_moves:
            delta_col = move[0]
            delta_row = move[1]
            temp_pos = [row + delta_row, col + delta_col]
            new_pos.append(temp_pos)
    
        for piece in pieces_white+pieces_black:
            row = piece.pos[0]
            col = piece.pos[1]
            if len(new_pos) == 0:
                break

            #new_pos[0] is if a piece is right in front of the pawn in which the pawn has zero possible moves
            if [row, col] == new_pos[0]:
                new_pos = []
            
            #this is when a piece is 2 places in front of a pawn, gets rid of the 2 space move option
            if (len(new_pos)>1) and ([row, col] == new_pos[1]):
                new_pos.remove([row, col])

        #takes
        takes = self.rule_pawn_takes(pieces_white,pieces_black)
        new_pos.extend(takes)

        return new_pos
class Knight(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black):
        row, col = self.pos

        new_moves = [(-2,1),(-2,-1),(2,1),(2,-1),(1,-2),(-1,-2),(1,2),(-1,2)]

        new_pos = []

        if self.color == "white":
            your_color = pieces_white
            opponent_color = pieces_black
        else:
            your_color = pieces_black
            opponent_color = pieces_white

        for move in new_moves:
            temp_row = row + move[0]
            temp_col = col + move[1]
            if temp_row < 0 or temp_row > 7:
                continue
            elif temp_col < 0 or temp_col > 7:
                continue

            if any(p.pos == [temp_row, temp_col] for p in your_color):
                continue

            if any(p.pos == [temp_row, temp_col] for p in opponent_color):
                new_pos.append([temp_row, temp_col])
                continue

            new_pos.append([temp_row, temp_col])

        # continue → SKIP this iteration, keep looping

        return new_pos
class Bishop(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black):

        row, col = self.pos
        
        if self.color == 'white':
            your_color = pieces_white
            opponent_color = pieces_black
        else:
            your_color =  pieces_black
            opponent_color = pieces_white
        new_pos = []

        directions = [(1, 1), (-1, 1), (1,-1), (-1, -1)]

        for dr, dc in directions:
            r = row
            c = col

            while True:
                r += dr
                c += dc

                if c < 0 or c > 7:
                    break
                if r < 0 or r > 7:
                    break

                if any(p.pos == [r, c] for p in your_color):
                    break

                if any(p.pos == [r, c] for p in opponent_color):
                    new_pos.append([r, c])
                    break

                new_pos.append([r, c])

        return new_pos
class Rook(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black):
        row, col = self.pos

        if self.color == "white":
            your_color = pieces_white
            opponent_color = pieces_black
        else:
            your_color = pieces_black
            opponent_color = pieces_white


        new_pos = []

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dr, dc in directions:
            r = row
            c = col

            while True:
                r += dr
                c += dc
                
                if c < 0 or c > 7:
                    break
                if r < 0 or r > 7:
                    break

                if any(p.pos == [r, c] for p in your_color):
                    break

                elif any(p.pos == [r, c] for p in opponent_color):
                    new_pos.append([r, c])
                    break
                
                new_pos.append([r, c])

        return new_pos
class Queen(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id, symbol, image)
    
    def rule(self,pieces_white,pieces_black):
        row, col = self.pos

        if self.color == "white":
            your_color = pieces_white
            opponent_color = pieces_black
        else:
            your_color = pieces_black
            opponent_color = pieces_white

        new_pos = []

        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1),(1,0), (-1,0), (0,1), (0,-1)]

        for dr, dc in directions:
            r = row
            c = col

            while True:
                r += dr
                c += dc

                if c < 0 or c > 7:
                    break
                if r < 0 or r > 7:
                    break

                if any(p.pos == [r, c] for p in your_color):
                    break

                if any(p.pos == [r, c] for p in opponent_color):
                    new_pos.append([r, c])
                    break

                new_pos.append([r, c])

        return new_pos
class King(Piece):
    def __init__(self, color, type, pos, moves, id, symbol, image):
        super().__init__(color, type, pos, moves, id, symbol, image)
    def rule(self,pieces_white,pieces_black):
        row, col = self.pos
        all_pieces = pieces_white+pieces_black

        new_moves = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]

        your_color = pieces_white if self.color == "white" else pieces_black

        if self.moves == 0:
            # occupied_cols are all pieces cols that are in the same row as king
            occupied_cols = [p.pos[1] for p in all_pieces if p.pos[0] == row and p.type != "king"]
            # King-side castling: f and g must be empty (col+1 and col+2)
            kingside_clear = (col + 1) not in occupied_cols and (col + 2) not in occupied_cols
            # Queen-side castling: b, c and d must be empty (col-1, col-2, col-3)
            queenside_clear = (col - 1) not in occupied_cols and (col - 2) not in occupied_cols and (
                        col - 3) not in occupied_cols

            kingside_rook = False
            queenside_rook = False

            for p in your_color:
                if p.type == "rook" and p.moves == 0 and p.pos[1] == col+3:
                    kingside_rook = True
                elif p.type == "rook" and p.moves == 0 and p.pos[1] == col-4:
                    queenside_rook = True

       
            if kingside_clear and kingside_rook:
                new_moves.append((0, 2))
            if queenside_clear and queenside_rook:
                new_moves.append((0, -2))

        new_pos = []

        if self.color == 'white':
            your_color = pieces_white
            opponent_color = pieces_black
        else:
            your_color =  pieces_black
            opponent_color = pieces_white
        

        for move in new_moves:
            temp_row = row + move[0]
            temp_col = col + move[1]
            if temp_row < 0 or temp_row > 7:
                continue
            elif temp_col < 0 or temp_col > 7:
                continue

            if any(p.pos == [temp_row, temp_col] for p in your_color):
                continue

            if any(p.pos == [temp_row,temp_col] for p in opponent_color):
                new_pos.append([temp_row, temp_col])
                continue

            new_pos.append([temp_row, temp_col])

        return new_pos

def validate_move(attempted_move):
    if len(attempted_move) > 2 or len(attempted_move) < 2:
        return "bad"
    
    elif attempted_move[0] not in ["a","b","c","d","e","f","g","h"]:
        return "bad"
        
    elif attempted_move[1] not in ["1","2","3","4","5","6","7","8"]:
        return "bad"

p1w = Pawn(id="p1w",type="pawn",symbol="♙",pos=[6, 0],moves=0,color="white",image=constants.white_pawn)
p2w = Pawn(id="p2w",type="pawn",symbol="♙",pos=[6, 1],moves=0,color="white",image=constants.white_pawn)
p3w = Pawn(id="p3w",type="pawn",symbol="♙",pos=[6, 2],moves=0,color="white",image=constants.white_pawn)
p4w = Pawn(id="p4w",type="pawn",symbol="♙",pos=[6, 3],moves=0,color="white",image=constants.white_pawn)
p5w = Pawn(id="p5w",type="pawn",symbol="♙",pos=[6, 4],moves=0,color="white",image=constants.white_pawn)
p6w = Pawn(id="p6w",type="pawn",symbol="♙",pos=[6, 5],moves=0,color="white",image=constants.white_pawn)
p7w = Pawn(id="p7w",type="pawn",symbol="♙",pos=[6, 6],moves=0,color="white",image=constants.white_pawn)
p8w = Pawn(id="p8w",type="pawn",symbol="♙",pos=[6, 7],moves=0,color="white",image=constants.white_pawn)
r1w = Rook(id="r1w",type="rook",symbol="♖",pos=[7, 0],moves=0,color="white",image=constants.white_rook)
r2w = Rook(id="r2w",type="rook",symbol="♖",pos=[7, 7],moves=0,color="white",image=constants.white_rook)
k1w = Knight(id="k1w",type="knight",symbol="♘",pos=[7, 1],moves=0,color="white",image=constants.white_knight)
k2w = Knight(id="k2w",type="knight",symbol="♘",pos=[7, 6],moves=0,color="white",image=constants.white_knight)
b1w = Bishop(id="b1w",type="bishop",symbol="♗",pos=[7, 2],moves=0,color="white",image=constants.white_bishop)
b2w = Bishop(id="b2w",type="bishop",symbol="♗",pos=[7, 5],moves=0,color="white",image=constants.white_bishop)
qw = Queen(id="qw",type="queen",symbol="♕",pos=[7, 3],moves=0,color="white",image=constants.white_queen)
kingw = King(id="kingw",type="king",symbol="♔",pos=[7, 4],moves=0,color="white",image=constants.white_king)

p1b = Pawn(id="p1b",type="pawn",symbol="♟",pos=[1, 0],moves=0,color="black",image=constants.black_pawn)
p2b = Pawn(id="p2b",type="pawn",symbol="♟",pos=[1, 1],moves=0,color="black",image=constants.black_pawn)
p3b = Pawn(id="p3b",type="pawn",symbol="♟",pos=[1, 2],moves=0,color="black",image=constants.black_pawn)
p4b = Pawn(id="p4b",type="pawn",symbol="♟",pos=[1, 3],moves=0,color="black",image=constants.black_pawn)
p5b = Pawn(id="p5b",type="pawn",symbol="♟",pos=[1, 4],moves=0,color="black",image=constants.black_pawn)
p6b = Pawn(id="p6b",type="pawn",symbol="♟",pos=[1, 5],moves=0,color="black",image=constants.black_pawn)
p7b = Pawn(id="p7b",type="pawn",symbol="♟",pos=[1, 6],moves=0,color="black",image=constants.black_pawn)
p8b = Pawn(id="p8b",type="pawn",symbol="♟",pos=[1, 7],moves=0,color="black",image=constants.black_pawn)
r1b = Rook(id="r1b",type="rook",symbol="♜",pos=[0, 0],moves=0,color="black",image=constants.black_rook)
r2b = Rook(id="r2b",type="rook",symbol="♜",pos=[0, 7],moves=0,color="black",image=constants.black_rook)
k1b = Knight(id="k1b",type="knight",symbol="♞",pos=[0, 1],moves=0,color="black",image=constants.black_knight)
k2b = Knight(id="k2b",type="knight",symbol="♞",pos=[0, 6],moves=0,color="black",image=constants.black_knight)
b1b = Bishop(id="b1b",type="bishop",symbol="♝",pos=[0, 2],moves=0,color="black",image=constants.black_bishop)
b2b = Bishop(id="b2b",type="bishop",symbol="♝",pos=[0, 5],moves=0,color="black",image=constants.black_bishop)
qb= Queen(id="qb",type="queen",symbol="♛",pos=[0, 3],moves=0,color="black",image=constants.black_queen)
kingb = King(id="kingb",type="king",symbol="♚",pos=[0, 4],moves=0,color="black",image=constants.black_king)

pieces_white = [p1w,p2w,p3w,p4w,p5w,p6w,p7w,p8w,r1w,r2w,b1w,b2w,k1w,k2w,kingw,qw]
pieces_black = [p1b,p2b,p3b,p4b,p5b,p6b,p7b,p8b,r1b,r2b,b1b,b2b,k1b,k2b,qb,kingb]

board = Board(pieces_white,pieces_black)

def main():
    
    print("\nHello guys welcome to chess! \n")

    player1 = input("White players name: ")
    player2 = input("Black players name: ")
    players = [player1, player2]

    while True:
        print()
        board.board_print()
        print(f"\n it is {players[board.active_player_index]}'s turn. Select piece to move (a5 for example)")
        attempted_move = input()

        if validate_move(attempted_move) == "bad":
            print("Invalid move, try again.")
            continue

        col, row = int(letter_index[attempted_move[0]]),8 - int(attempted_move[1]) 
        
        piece_pos = [row,col]
        
        piece_avialbe_moves = find_piece(board.active_player_index,pieces_white,pieces_black,piece_pos)
        if piece_avialbe_moves == "Not a piece":
            print("Not a piece")
            continue
        else:
            piece_class = [x for x in pieces_white+pieces_black if x.pos == piece_pos]
            piece_class = piece_class[0]

            result = make_a_move(piece_avialbe_moves,pieces_white,pieces_black, piece_class=piece_class)
   
            if result == "checkmate" or result == "stalemate":
                break
            elif result:
                board.change_turns()
                
def find_piece(you,pieces_white,pieces_black,piece_pos):
    # check if the selected cord has one of your pieces on it

    if you == 0:
        your_dict = pieces_white
    else:
        your_dict = pieces_black
    
    for x in your_dict:
        if piece_pos == x.pos:
            piece_aviable_moves = x.rule(pieces_white,pieces_black)
            return piece_aviable_moves
    return "Not a piece"

def PawnPromotion(piece,row,col,pieces_white,pieces_black):
    blackbackranks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
    whitebackranks = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    
    your_pieces = pieces_white if piece.color =="white" else pieces_black

    if piece.color == "white" and piece.type == "pawn":
        if (row, col) in blackbackranks:
            x = your_pieces.index(piece)
            del your_pieces[x]
            q2w = Queen(color="white",type="queen",moves=0,id="q2w",symbol="♕",pos=[row, col],image=constants.white_queen)
            your_pieces.append(q2w)

    elif piece.color == "black" and piece.type == "pawn":
        if (row, col) in whitebackranks:
            x = your_pieces.index(piece)
            del your_pieces[x]
            q2b= Queen(color="black",type="queen",moves=0,id="q2b",symbol="♛",pos=[row, col])
            your_pieces.append(q2b)

def Takes(pieces_white,pieces_black,piece,take_list_white,take_list_black):
    opponent_pieces = pieces_black if piece.color == "white" else pieces_white

    for x, op in enumerate(opponent_pieces):
        
        if op.type == "rook":
            print("Rook Pos, ", op.pos)
            print("king Pos: ", piece.pos)

        if op.pos == piece.pos:
            print("YAYAYAYA")
            del opponent_pieces[x]

            match op.type:
                case "pawn":
                    if op.color == "white":
                        taken_piece = Pawn(image=constants.white_pawn_tiny) 
                    else:
                        taken_piece = Pawn(image=constants.black_pawn_tiny)
                    
                case "rook":
                    if op.color == "white":
                        taken_piece = Rook(image=constants.white_rook_tiny) 
                    else:
                        taken_piece = Rook(image=constants.black_rook_tiny)
                
                case "knight":
                    if op.color == "white":
                        taken_piece = Knight(image=constants.white_knight_tiny) 
                    else:
                        taken_piece = Knight(image=constants.black_knight_tiny)
                
                case "bishop":
                    if op.color == "white":
                        taken_piece = Bishop(image=constants.white_bishop_tiny) 
                    else:
                        taken_piece = Bishop(image=constants.black_bishop_tiny)
                
                case "queen":
                    if op.color == "white":
                        taken_piece = Queen(image=constants.white_queen_tiny) 
                    else:
                        taken_piece = Queen(image=constants.black_queen_tiny)

            if op.color == "white":
                take_list_white.append(taken_piece)
            else:
                take_list_black.append(taken_piece)

            break

       

def Castling(black, white, xx, col, new_col, new_row, your_color):

        # check if it moved 2 squares right 
        if (([new_row, new_col] != [xx, (col + 2)]) and
                ([new_row, new_col] != [xx, (col - 2)])):
                return "not_castling"

        # king side castling
        if [new_row, new_col] == [xx, (col + 2)]:
            targets = [(xx, (col + 1)), (xx, (col + 2))]
            occupied = [p.pos for p in black + white]

            if all(t not in occupied for t in targets):
                rook_col = col + 3
                rook = None
                for piece2 in your_color:
                    if (piece2.pos == [xx, rook_col]) and (piece2.type == "rook"):
                        rook = piece2
                        if piece2.moves > 0:
                            return "cancel castling"
                        break

                if rook:
                    new_rook_col = col + 1
                    rook.pos = [xx, new_rook_col]
                    rook.moves += 1
                    return "done castling"
                
        # queen side castling
        if [new_row, new_col] == [xx, (col - 2)]:
            targets = [(xx, (col - 1)), (xx, (col - 2)), (xx, (col - 3))]
            occupied = [p.pos for p in black + white]

            if all(t not in occupied for t in targets):
                rook_col = col - 4

                rook = None
                for piece2 in your_color:
                    if (piece2.pos == [xx, rook_col]) and (piece2.type == "rook"):
                        rook = piece2
                        if piece2.moves > 0:
                            return "cancel castling"
                        break

                if rook:
                    new_rook_col = col - 1
                    rook.pos = [xx, new_rook_col]
                    rook.moves += 1
                    return "done castling"

        return "cancel castling"

def all_new_moves_opponent_for_check(player, pieces_white, pieces_black):

    # this function just gets all possible take moves for your opponents next move

    all_new_moves_your_color = []
    for i in player: # player = white or black
        if i.type == "pawn":
            all_new_moves_your_color.extend(i.rule_pawn_takes(pieces_white,pieces_black))
        else:
            all_new_moves_your_color.extend(i.rule(pieces_white,pieces_black))

    return all_new_moves_your_color

def castling_check(new_col, original_col, new_row, you_sim):
    if new_col > original_col:
            rook_from = [new_row, original_col + 3]
            rook_to   = [new_row, original_col + 1]
    else:
            rook_from = [new_row, original_col - 4]
            rook_to   = [new_row, original_col - 1]
    for p in you_sim:
            if p.pos == rook_from and p.type == "rook":
                p.pos = rook_to
                break

def is_your_king_in_check(you, opponent, piece, new_row, new_col, pieces_white, pieces_black):

    #update you_sim with new move
    you_sim = copy.deepcopy(you)
    moved_piece = [x for x in you_sim if x.id == piece.id][0] # gets object of piece that's moving
    moved_piece.pos = [new_row, new_col]

    original_col = piece.pos[1]  
    king_moved_two = piece.type == "king" and abs(new_col - original_col) == 2

    # castling detection, update rook pos before making copies if king castled
    if king_moved_two:
        castling_check(new_col=new_col,original_col=original_col,new_row=new_row,you_sim=you_sim)

    #if new move is take, remove the captured piece from opponent
    opponent_sim = copy.deepcopy(opponent)
    captured_piece = None
    for piece in opponent_sim:
        if piece.pos == moved_piece.pos:
            captured_piece = piece
            break
    if captured_piece:
        opponent_sim.remove(captured_piece)

    your_king = [piece for piece in you_sim if piece.type == "king"][0]
    king_row = your_king.pos[0]
    king_col = your_king.pos[1]
    king_pos = [king_row, king_col]

    if you == pieces_white:
        if king_pos in all_new_moves_opponent_for_check(player=opponent_sim, pieces_white=you_sim, pieces_black=opponent_sim):
            print("You cant go here because its a check. Try another move. (1)")
            return True
        else:
            return False
    elif you == pieces_black:
        if king_pos in all_new_moves_opponent_for_check(player=opponent_sim, pieces_white=opponent_sim, pieces_black=you_sim):
            print("You cant go here because its a check. Try another move. (2)")
            return True
        else:
        # if king isn't in check next move it can go forward and update the board
            return False
    
def is_opponent_king_in_check(you, opponent, pieces_white, pieces_black):
    
    # checks if you put your opponent into check
    opponent_king = [piece for piece in opponent if piece.type == "king"][0]
    king_row = opponent_king.pos[0]
    king_col = opponent_king.pos[1]
    king_pos = [king_row, king_col]

    if king_pos in all_new_moves_opponent_for_check(player=you, pieces_white=pieces_white, pieces_black=pieces_black):
        print("You cant go here because its a check. Try another move. (3)")
        return True
    else:
        return False

def is_checkmate_opponent(you, opponent,white_pieces,black_pieces):
    
    kings_original_row, kings_original_col = next(a.pos for a in opponent if a.type == "king")

    # makes list of opponenets possible next moves
    opponent_next_moves_passive = []
    for a in opponent:
        next_move_while_in_check = (a.rule(white_pieces,black_pieces))
        for x in next_move_while_in_check:
            opponent_next_moves_passive.append({
                'pos': [x[0], x[1]],
                'id': a.id,
            })
    
    
    # for each move make a board simulation updating sim_opponenent with theroetical move
    list_of_trues = []
    for a in opponent_next_moves_passive:  
        
        sim_you = copy.deepcopy(you)
        sim_opponent = copy.deepcopy(opponent)

        sim_row = a["pos"][0]
        sim_col = a["pos"][1]

        if "king" in a["id"]:
            
            king_moved_two = abs(sim_col - kings_original_col) == 2 and sim_row == kings_original_row

            if king_moved_two:
                castling_check(new_col=sim_col,original_col=kings_original_col,new_row=sim_row,you_sim=sim_opponent)


        # every other key but pos stays the same, pos is updated
        for x in sim_opponent:
            if x.id == a["id"]:
                x.pos = [sim_row, sim_col]
                break

        # Check if one of your pieces was captured and remove it
        captured_piece = None
        for piece in sim_you:
            if piece.pos == [sim_row, sim_col]:
                captured_piece = piece
                break
        if captured_piece:
            sim_you.remove(captured_piece)

        for k in sim_opponent:
            if k.type == "king":
                king_row = k.pos[0] 
                king_col = k.pos[1]

                if you == white_pieces:
                    if [king_row, king_col] in all_new_moves_opponent_for_check(player=sim_you, pieces_white=sim_you, pieces_black=sim_opponent):
                        list_of_trues.append(True)
                        break
                
                elif you == black_pieces:
                    if [king_row, king_col] in all_new_moves_opponent_for_check(player=sim_opponent, pieces_white=sim_opponent, pieces_black=sim_you):
                        list_of_trues.append(True)
                        break
    
    if len(list_of_trues) == len(opponent_next_moves_passive) and len(opponent_next_moves_passive) > 0:
        return True
    return False

def make_a_move(piece_aviable_moves,pieces_white,pieces_black,piece_class):

    all_pieces = pieces_white+pieces_black    

    if piece_class.color == "white":
        you = pieces_white
        opponent = pieces_black
    else:
        you = pieces_black
        opponent = pieces_white

    while True:

        if len(piece_aviable_moves) == 0:
            print("this piece can't move")
            return False

        print("Select square to move to (example a5) type cancel to cancel move")
        attempted_move_2 = input()

        if attempted_move_2 == "cancel":
            return False

        if validate_move(attempted_move_2) == "bad":
            print("Invalid move, try again.")
            continue

        col, row = int(letter_index[attempted_move_2[0]]) , 8 - int(attempted_move_2[1]) 
    
        if [row,col] in piece_aviable_moves:
            while True:
                for x in all_pieces:
                    if x.id == piece_class.id:

                        check_ = is_your_king_in_check(you=you, opponent=opponent, piece=x, new_row=row, new_col=col, pieces_white=pieces_white,pieces_black=pieces_black)
                        if check_:
                            print("This is an illegal move as it walks into check, try again.")
                            return False

                        if ((x.type != 'king') or (x.type == 'king' and x.moves > 0)):
                            x.pos = [row,col]
                            x.moves+=1
                        else: # castling

                            king_row = x.pos[0]
                            king_col = x.pos[1] 

                            if x.color == "white":
                                result = Castling(black=pieces_black, white=pieces_white,  xx=king_row, col=king_col, new_col=col, new_row=row, your_color=pieces_white)
                            else:
                                result = Castling(black=pieces_black, white=pieces_white,  xx=king_row, col=king_col, new_col=col, new_row=row, your_color=pieces_black)
                            
                            if result == "not_castling":
                                x.pos = [row,col]
                                x.moves+=1
                            elif result == "cancel castling":
                                print("This move is not castling done right, try again.")
                                return False
                            elif result == "done castling":
                                x.pos = [row,col]
                                x.moves+=1
                        
                        Takes(pieces_white,pieces_black,x,board.taken_list_white,board.taken_list_white)
                        PawnPromotion(piece=x,row=row,col=col,pieces_white=pieces_white,pieces_black=pieces_black)

                        check_ = is_opponent_king_in_check(you=you, opponent=opponent,pieces_white=pieces_white,pieces_black=pieces_black)
                        if check_:
                            print(f"Check!")

                            checkmate = is_checkmate_opponent(you=you, opponent=opponent,white_pieces=pieces_white,black_pieces=pieces_black)
                            if checkmate:
                                print("Checkmate!")
                                return "checkmate"
                        else:
                            stalemate = is_checkmate_opponent(you=you, opponent=opponent,white_pieces=pieces_white,black_pieces=pieces_black)
                            if stalemate:
                                print("Stalemate!")
                                return "stalemate"

                        return True
        else:
            print("Piece can't move there, try again.")

if __name__ == "__main__":
    main()