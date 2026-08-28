import copy
import constants
letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

def init_board_table(pieces_white,pieces_black):
    for x in pieces_white + pieces_black:
                        row = x.pos[0]
                        col = x.pos[1]
                        board_table[row][col] = x

board_table = [["_" for _ in range(8)] for _ in range(8)]

def print_board_data_table(board_data):
        for x in reversed(board_data):
            list_to_print = []
            for piece in x:
                try:
                    symbol = " "+piece.symbol+" "
                except:
                    symbol = " _ "
                list_to_print.append(symbol)

            # print(list_to_print)

class Board:
    def __init__(self,pieces_white,pieces_black):
        self.board_data = [["_" for _ in range(8)] for _ in range(8)]
        self.active_player_index = 0
        self.pieces_white = pieces_white
        self.pieces_black = pieces_black
        self.taken_list_white = []
        self.taken_list_black = []
        self.pawn_double_move = None

        init_board_table(self.pieces_white,self.pieces_black)   

    def board_print(self):

        # reset board state
        self.board_data = [["_" for _ in range(8)] for _ in range(8)]

        self.set_board_data_table()

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

    # functions for testing
    def get_moves(self):

        you = self.pieces_white if self.active_player_index == 0 else self.pieces_black
        opp = self.pieces_white if self.active_player_index == 1 else self.pieces_black
        moves = []

        for piece in you:
            piece_moves = piece.rule(self.pieces_white,self.pieces_black,self.pawn_double_move) if piece.type == "pawn" else piece.rule(self.pieces_white,self.pieces_black)
            for move in piece_moves:
                # if kings in check and move doesn't save king, skip it
                check_ = is_your_king_in_check(you, opp, piece, move[0], move[1], self.pieces_white,self.pieces_black,self.pawn_double_move)
                if check_: continue 
                
                moves.append([piece,piece.pos,move])
                # print(f"pos: {piece.pos} symbol: {piece.symbol} color: {piece.color}")
                # print_board_data_table(board_table)
                
        return moves

    def make_move(self, selected_piece, starting_pos, ending_pos):

        # At the beginning of make_move, before changing it
        previous_pawn_double_move = self.pawn_double_move
        # selected_piece = None
        valid_move = False
        castling_info = None

        you = self.pieces_white if selected_piece.color == "white" else self.pieces_black
        
        # if the piece isn't found in white or black
        if starting_pos not in [piece.pos for piece in self.pieces_white+self.pieces_black]:
            print("PROBLEM: this starting position isnt found for make move")
            return

        # normal move
        if ((selected_piece.type != 'king') or
                (selected_piece.moves != 0)):

            valid_move = True
        
        # check for castling
        elif selected_piece.type == 'king' and selected_piece.moves == 0:
            king_row = selected_piece.pos[0] 
            king_col = selected_piece.pos[1]  

            result = Castling(
                self.pieces_black, 
                self.pieces_white,
                king_row,  # king's current row
                king_col,  # king's current col letter
                ending_pos[1],  # destination col letter
                ending_pos[0],  # destination row
                you  # your color
            )

            # if castling didn't fail its a valid move
            if result[0] != "cancel castling":
                valid_move = True

            if "done castling" in result[0]: # need to get king and rook starting and ending positons for undo 

                side = result[0][14:]
                castled_king = selected_piece
                castled_king_original_pos = [king_row,king_col]
                castled_rook = result[1]
                castled_rook_original_pos = result[2]

                castling_info = {"castled_king" : castled_king, "castled_king_original_pos" : castled_king_original_pos, "castled_rook" : castled_rook, "castled_rook_original_pos" : castled_rook_original_pos}

                # update board_table with castled postions
                board_table[castled_king_original_pos[0]][castled_king_original_pos[1]] = "_"
                board_table[castled_king.pos[0]][castled_king.pos[1]] = castled_king

                board_table[castled_rook_original_pos[0]][castled_rook_original_pos[1]] = "_"
                board_table[castled_rook.pos[0]][castled_rook.pos[1]] = castled_rook
  
        # if the move is valid then move, look for takes, and change turns
        if valid_move:

            # check if the move was a double pawn move
            if selected_piece.type == "pawn" and abs(ending_pos[0] - selected_piece.pos[0]) == 2:
                self.pawn_double_move = {"double_move_pawn" : selected_piece, "original_pos" : selected_piece.pos}
            else:
                self.pawn_double_move = None

            board_table[selected_piece.pos[0]][selected_piece.pos[1]] = "_"
            selected_piece.pos = ending_pos
            selected_piece.moves += 1
            board_table[selected_piece.pos[0]][selected_piece.pos[1]] = selected_piece

            # check if move took any pieces
            last_taken_piece = Takes(self.pieces_white,self.pieces_black,selected_piece,self.taken_list_white,self.taken_list_black, previous_pawn_double_move)

            self.change_turns()
        return starting_pos, ending_pos, last_taken_piece, valid_move, castling_info, previous_pawn_double_move

    def undo_move(self, starting_pos, ending_pos,taken_piece, castling_info, previous_pawn_double_move):

        # undo castling
        if castling_info:
            king = castling_info.get("castled_king")
            king_original_pos = castling_info.get("castled_king_original_pos")
            rook = castling_info["castled_rook"]
            rook_original_pos = castling_info["castled_rook_original_pos"]

            # undo moved king 
            board_table[king.pos[0]][king.pos[1]] = "_"
            king.pos = king_original_pos
            king.moves -= 1
            board_table[king.pos[0]][king.pos[1]] = king

            # undo moved rook
            board_table[rook.pos[0]][rook.pos[1]] = "_"
            rook.pos = rook_original_pos
            rook.moves -= 1
            board_table[rook.pos[0]][rook.pos[1]] = rook

            self.change_turns()
            self.pawn_double_move = previous_pawn_double_move
            return
            

        selected_piece = None
                
        # if new moves positon isn't one of the pieces
        if ending_pos not in [piece.pos for piece in self.pieces_white+self.pieces_black]:
            print("PROBLEM: this move to undo isnt found")
            print(f"Piece went from {index_letter[starting_pos[1]]}{8-(starting_pos[0])} to {index_letter[ending_pos[1]]}{8-(ending_pos[0])}")
            print(f"Pieces in black and white:")
            print(f"Black: {[(index_letter[piece.pos[1]],8-(piece.pos[0])) for piece in self.pieces_black]}")
            print(f"White: {[(index_letter[piece.pos[1]],8-(piece.pos[0])) for piece in self.pieces_white]}")
            return

        # get the piece from the new moved position
        for piece in self.pieces_white:
            if ending_pos == piece.pos:
                selected_piece = piece
        for piece in self.pieces_black:
            if ending_pos == piece.pos:
                selected_piece = piece

        # undo moved piece 
        board_table[selected_piece.pos[0]][selected_piece.pos[1]] = "_"
        selected_piece.pos = starting_pos
        selected_piece.moves -= 1
        board_table[selected_piece.pos[0]][selected_piece.pos[1]] = selected_piece

        # undo takes
        if taken_piece:
            if selected_piece.color == "white":
                if taken_piece.color == "black":
                    self.pieces_black.append(taken_piece)

            elif selected_piece.color == "black":
                if taken_piece.color == "white":
                    self.pieces_white.append(taken_piece)

            board_table[taken_piece.pos[0]][taken_piece.pos[1]] = taken_piece

        self.pawn_double_move = previous_pawn_double_move

        self.change_turns() 
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
            # Defines exactly what data from a Python class should be saved (serialized) when exporting it to a file or copy
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
    def rule_pawn_takes(self,pieces_white,pieces_black,pawn_double_move,look_for_check=None):
        if self.color == "white":
            direction = -1
            op_pieces = pieces_black
        else:
            direction = 1
            op_pieces =pieces_white

        takes = []

        row, col = self.pos

        # checks through castling
        if look_for_check and ([row + direction, col + 1] == look_for_check or [row + direction, col - 1] == look_for_check):
            return True

        for op in op_pieces:
            op_row = op.pos[0]
            op_col = op.pos[1]

            if (([op_row, op_col] == [row + direction, col + 1]) or
                ([op_row, op_col] == [row + direction, col - 1])):
                    
                takes.append([op_row, op_col])

        # en passant, check if opponents pawn that just moved twice is in en passant range
        if pawn_double_move:

            pawn = pawn_double_move.get("double_move_pawn")
            
            if (pawn.pos == [row, col+1] or
                                pawn.pos == [row, col-1]):

        
                if look_for_check and ([row, col+1] == look_for_check or [row, col] == look_for_check):
                    return True
                
                takes.append([pawn.pos[0]+direction,pawn.pos[1]]) 

        if look_for_check:
            return False
        else:
            return takes
    
    def rule(self,pieces_white,pieces_black,pawn_double_move):

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
        takes = self.rule_pawn_takes(pieces_white,pieces_black,pawn_double_move)
        new_pos.extend(takes)

        return new_pos
class Knight(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black,look_for_check=None):
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

            # cant take your own color
            if any(p.pos == [temp_row, temp_col] for p in your_color):
                continue

            if look_for_check and [temp_row, temp_col] == look_for_check:
                return True
            
            new_pos.append([temp_row, temp_col])

        if look_for_check:
            return False
        else:
            return new_pos
class Bishop(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black,look_for_check=None):

        row, col = self.pos
        
        if self.color == 'white':
            opp_color = "black"
        else:
            opp_color = "white"

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

                occupant = board_table[r][c]

                # your color
                if occupant != "_" and occupant.color == self.color:
                    break

                # outside of opp color if statement because for castling the square might be empty
                elif look_for_check and [r, c] == look_for_check:
                    return True
                
                # opp color
                elif occupant != "_" and occupant.color == opp_color:
                    new_pos.append([r, c])
                    
                    break

                new_pos.append([r, c])

        if look_for_check:
            return False
        else:
            return new_pos
class Rook(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id,symbol, image)
    def rule(self,pieces_white,pieces_black,look_for_check=None):
        row, col = self.pos

        if self.color == "white":
            your_color = pieces_white
            opponent_color = pieces_black
            opp_color = "black"
        else:
            your_color = pieces_black
            opponent_color = pieces_white
            opp_color = "white"

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

                occupant = board_table[r][c]
            
                # your color
                if occupant != "_" and occupant.color == self.color:
                    break

                # outside of opp color if statement because for castling the square might be empty
                elif look_for_check and [r, c] == look_for_check:
                    return True
                
                # opp color
                elif occupant != "_" and occupant.color == opp_color:
                    new_pos.append([r, c])                    
                    break


                new_pos.append([r, c])

        if look_for_check:
            return False
        else:
            return new_pos
class Queen(Piece):
    def __init__(self,color=None,type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id, symbol, image)
    
    def rule(self,pieces_white,pieces_black,look_for_check=None):
        row, col = self.pos

        if self.color == "white":
            opp_color = "black"
        else:
            opp_color = "white"

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

                occupant = board_table[r][c]

                # your color
                if occupant != "_" and occupant.color == self.color:
                    break

                # outside of opp color if statement because for castling the square might be empty
                elif look_for_check and [r, c] == look_for_check:
                    return True

                # opp color
                elif occupant != "_" and occupant.color == opp_color:
                    new_pos.append([r, c])
                    break

                new_pos.append([r, c])

        if look_for_check:
            return False
        else:
            return new_pos
class King(Piece):
    def __init__(self, color=None, type=None,pos=None,moves=None,id=None,symbol=None,image=None):
        super().__init__(color, type, pos, moves, id, symbol, image)
    def rule(self,pieces_white,pieces_black, look_for_check=None):
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
            opp_color = "black"
        else:
            your_color =  pieces_black
            opponent_color = pieces_white
            opp_color = "white"
        

        for move in new_moves:
            temp_row = row + move[0]
            temp_col = col + move[1]
            if temp_row < 0 or temp_row > 7:
                continue
            elif temp_col < 0 or temp_col > 7:
                continue

            occupant = board_table[temp_row][temp_col]

            # your color
            if occupant != "_" and occupant.color == self.color:
                continue    

            elif look_for_check and [temp_row, temp_col] == look_for_check:
                return True
            
            # opp color
            elif occupant != "_" and occupant.color == opp_color:
                new_pos.append([temp_row, temp_col])                
                continue

            new_pos.append([temp_row, temp_col])

        if look_for_check:
            return False
        else:
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
r1w = Rook(id="r1w",type="rook",symbol="♖",pos=[7, 7],moves=0,color="white",image=constants.white_rook)
r2w = Rook(id="r2w",type="rook",symbol="♖",pos=[7, 0],moves=0,color="white",image=constants.white_rook)
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
pawn_double_move = None

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
    # check if the selected pos has one of your pieces on it

    if you == 0:
        your_dict = pieces_white
    else:
        your_dict = pieces_black
    
    for x in your_dict:
        if piece_pos == x.pos:
            if x.type == "pawn":
                piece_aviable_moves = x.rule(pieces_white,pieces_black,pawn_double_move)
            else:
                piece_aviable_moves = x.rule(pieces_white,pieces_black)
            return piece_aviable_moves
    return "Not a piece"

def PawnPromotion(piece,row,col,pieces_white,pieces_black):
    blackbackranks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
    whitebackranks = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    
    your_pieces = pieces_white if piece.color == "white" else pieces_black

    if piece.color == "white" and piece.type == "pawn":
        if (row, col) in blackbackranks:
            x = your_pieces.index(piece)
            del your_pieces[x]
            q2w = Queen(color="white",type="queen",moves=0,id="q2w",symbol="♕",pos=[row, col],image=constants.white_queen)
            your_pieces.append(q2w)
            board_table[row][col] = q2w


    elif piece.color == "black" and piece.type == "pawn":
        if (row, col) in whitebackranks:
            x = your_pieces.index(piece)
            del your_pieces[x]
            q2b= Queen(color="black",type="queen",moves=0,id="q2b",symbol="♛",pos=[row, col],image=constants.black_queen)
            your_pieces.append(q2b)
            board_table[row][col] = q2b      

def Takes(pieces_white,pieces_black,piece,take_list_white,take_list_black, previous_pawn_double_move):

    taken_piece = None
    opponent_pieces = pieces_black if piece.color == "white" else pieces_white
    direction = -1 if piece.color == "white" else 1
    if previous_pawn_double_move:
        op_double_pawn = previous_pawn_double_move.get("double_move_pawn")

    # check for regular takes
    for x, op in enumerate(opponent_pieces):

        if op.pos == piece.pos:

            # print(f" Op is {op.type} and piece is {piece.type}")
            taken_piece = op
            
            match op.type:
                case "pawn":
                    if op.color == "white":
                        taken_piece.image = constants.white_pawn_tiny
                    else:
                        taken_piece.image = constants.black_pawn_tiny
                    
                case "rook":
                    if op.color == "white":
                        taken_piece.image = constants.white_rook_tiny
                    else:
                        taken_piece.image = constants.black_rook_tiny
                
                case "knight":
                    if op.color == "white":
                        taken_piece.image = constants.white_knight_tiny
                    else:
                        taken_piece.image = constants.black_knight_tiny
                
                case "bishop":
                    if op.color == "white":
                        taken_piece.image = constants.white_bishop_tiny
                    else:
                        taken_piece.image = constants.black_bishop_tiny
                
                case "queen":
                    if op.color == "white":
                        taken_piece.image = constants.white_queen_tiny
                    else:
                        taken_piece.image = constants.black_queen_tiny

            del opponent_pieces[x]
            board_table[op.pos[0]][op.pos[1]] = piece

            if taken_piece:
                if op.color == "white":
                    take_list_white.append(taken_piece)
                else:
                    take_list_black.append(taken_piece)

            return op

    # check for en passant takes (after regular takes)
    if previous_pawn_double_move:
        if [op_double_pawn.pos[0],op_double_pawn.pos[1]] == [piece.pos[0]-direction,piece.pos[1]] and piece.type == "pawn":
            taken_piece = op_double_pawn            
    
            if op.color == "white":
                taken_piece.image = constants.white_pawn_tiny
            else:
                taken_piece.image = constants.black_pawn_tiny

            opponent_pieces.remove(taken_piece)
            board_table[taken_piece.pos[0]][taken_piece.pos[1]] = "_"

            if taken_piece:
                if taken_piece.color == "white":
                    take_list_white.append(taken_piece)
                else:
                    take_list_black.append(taken_piece)

            return taken_piece

def Castling(black, white, xx, col, new_col, new_row, your_color):

        # check if it moved 2 squares right 
        if (([new_row, new_col] != [xx, (col + 2)]) and
                ([new_row, new_col] != [xx, (col - 2)])):
                return ["not_castling"]

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
                            return ["cancel castling"]
                        break

                if rook:
                    rook_old_pos = rook.pos
                    new_rook_col = col + 1
                    rook.pos = [xx, new_rook_col]
                    rook.moves += 1
                    return ["done castling kingside", rook, rook_old_pos] # return what side castling, the rooks old pos, and the rooks new pos
                
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
                            return ["cancel castling"]
                        break

                if rook:
                    rook_old_pos = rook.pos
                    new_rook_col = col - 1
                    rook.pos = [xx, new_rook_col]
                    rook.moves += 1
                    return ["done castling queenside", rook, rook_old_pos]

        return "cancel castling"

def all_new_moves_opponent_for_check(player, pieces_white, pieces_black):

    # this function just gets all possible take moves for your opponents next move

    all_new_moves_your_color = []
    for i in player: # player = white or black
        if i.type == "pawn":
            all_new_moves_your_color.extend(i.rule_pawn_takes(pieces_white,pieces_black,False))
        else:
            all_new_moves_your_color.extend(i.rule(pieces_white,pieces_black))

    return all_new_moves_your_color

# better version of this function, return as soon as a check is found instead of finding every single possible move first
def all_new_moves_opponent_for_check_test(opp, pieces_white, pieces_black, king_pos):

    for i in opp:

        if i.type == "pawn": 
            if i.rule_pawn_takes(pieces_white,pieces_black,False,king_pos):
                return True
        else:
            if i.rule(pieces_white,pieces_black,king_pos):
                return True

    return False
    
def castling_check(new_col, original_col, new_row, you_sim):
    # updates rooks position if castled
    if new_col > original_col:
            rook_from = [new_row, original_col + 3]
            rook_to   = [new_row, original_col + 1]
    else:
            rook_from = [new_row, original_col - 4]
            rook_to   = [new_row, original_col - 1]
    for p in you_sim:
            if p.pos == rook_from and p.type == "rook":
                p.pos = rook_to
                
                return rook_from, rook_to
    return False, False

def is_your_king_in_check(you, opponent, piece, new_row, new_col, pieces_white, pieces_black, pawn_double_move):
    direction = -1 if piece.color == "white" else 1

    destination_occupant = board_table[new_row][new_col]

    # what gets returned at the end
    is_king_in_check = False
    rook_to, rook_from = False, False

    # track original piece pos 
    original_row = piece.pos[0]
    original_col = piece.pos[1]
    original_pos = piece.pos
    board_table[original_row][original_col] = "_"

    moved_piece = piece
    moved_piece.pos = [new_row,new_col]
    board_table[new_row][new_col] = moved_piece

    # castling, track original rook pos
    king_moved_two = piece.type == "king" and abs(new_col - original_col) == 2
    if king_moved_two:

        # get rooks orignal and end positions to later reset
        rook_from,rook_to = castling_check(new_col=new_col,original_col=original_col,new_row=new_row,you_sim=you) 

        step = 1 if new_col > original_col else -1 # direction king goes, kingside or queenside

        # all squares the king has to go through when castling
        castling_squares = [
            [original_row, original_col],
            [original_row, original_col + step],
            [original_row, original_col + 2 * step],
        ]

        # check if all those squares aren't attacked, if they are then your king is in check and can't castle
        for square in castling_squares:
            if all_new_moves_opponent_for_check_test(
                opp=opponent,
                pieces_white=pieces_white,
                pieces_black=pieces_black,
                king_pos=square
            ):
                is_king_in_check = True
                break

    # if new move is take, temporarily remove the captured piece from opponent
    captured_piece = None
    for piece_op in opponent:
        if piece_op.pos == moved_piece.pos:
            captured_piece = piece_op
            break

    # en passant
    # must be a pawn
    if moved_piece.type == "pawn": # must be a pawn
        if pawn_double_move: # opponent must've just had a double move

            pawn = pawn_double_move.get("double_move_pawn")

            if (pawn.pos == [original_row, original_col+1]
                and (new_row == original_row + direction and new_col - original_col == 1)) or (pawn.pos == [original_row, original_col-1] and (new_row == original_row + direction and new_col - original_col == - 1)):
                if destination_occupant == "_":
                    captured_piece = pawn
                    board_table[captured_piece.pos[0]][captured_piece.pos[1]] = "_"
        
    if captured_piece:
        opponent.remove(captured_piece)


    # find your king and its pos in you sim
    your_king = [piece for piece in you if piece.type == "king"][0]
    king_pos = your_king.pos

    # check if your kings pos is in opp check
    if not is_king_in_check:
        if you == pieces_white:
            is_king_in_check = all_new_moves_opponent_for_check_test(opp=opponent, pieces_white=you, pieces_black=opponent, king_pos=king_pos)
        elif you == pieces_black:
            is_king_in_check = all_new_moves_opponent_for_check_test(opp=opponent, pieces_white=opponent, pieces_black=you, king_pos=king_pos)

    # reset moved piece
    board_table[moved_piece.pos[0]][moved_piece.pos[1]] = "_"
    piece.pos = original_pos 
    board_table[original_pos[0]][original_pos[1]] = piece

    # reset rook if castled
    if rook_to and rook_from:
        for rook in you:
            if rook.pos == rook_to:
                rook.pos = rook_from
                board_table[rook.pos[0]][rook.pos[1]] = rook

    # reset takes if any
    if captured_piece:
        opponent.append(captured_piece)
        board_table[captured_piece.pos[0]][captured_piece.pos[1]] = captured_piece

    return is_king_in_check

def is_opponent_king_in_check(you, opponent, pieces_white, pieces_black):
    
    # checks if you put your opponent into check
    opponent_king = [piece for piece in opponent if piece.type == "king"]

    # incase there isn't an opponent king
    if len(opponent_king) < 1:
        return
    else:
        opponent_king = opponent_king[0]

    king_row = opponent_king.pos[0]
    king_col = opponent_king.pos[1]
    king_pos = [king_row, king_col]

    if king_pos in all_new_moves_opponent_for_check(player=you, pieces_white=pieces_white, pieces_black=pieces_black):
        # print("You cant go here because its a check. Try another move. (3)")
        return True
    else:
        return False

def is_checkmate_opponent(you, opponent,white_pieces,black_pieces):

    if "king" not in [a.type for a in opponent]: return
    
    # opponent kings original position
    kings_original_row, kings_original_col = next(a.pos for a in opponent if a.type == "king")

    # makes list of opponent possible next moves
    opponent_next_moves_passive = []
    for a in opponent:
        if a.type == "pawn":
            next_move_while_in_check = (a.rule(white_pieces,black_pieces,False))
        else:
            next_move_while_in_check = (a.rule(white_pieces,black_pieces))
        for x in next_move_while_in_check:
            opponent_next_moves_passive.append({
                'pos': [x[0], x[1]],
                'id': a.id,
            })

    # for each possible next move, make a board simulation
    # updating sim_opponenent with the theroetical move position
    list_of_trues = []
    for a in opponent_next_moves_passive:  
        
        sim_you = copy.deepcopy(you)
        sim_opponent = copy.deepcopy(opponent)

        sim_row = a["pos"][0]
        sim_col = a["pos"][1]

        # if king castled
        if "king" in a["id"]:
            king_moved_two = abs(sim_col - kings_original_col) == 2 and sim_row == kings_original_row
            if king_moved_two:
                castling_check(new_col=sim_col,original_col=kings_original_col,new_row=sim_row,you_sim=sim_opponent)

        # pos is updated in simulated pieces list
        for x in sim_opponent:
            if x.id == a["id"]:
                x.pos = [sim_row, sim_col]
                break

        # check if one of your pieces was captured and remove it
        captured_piece = None
        for piece in sim_you:
            if piece.pos == [sim_row, sim_col]:
                captured_piece = piece
                break
        if captured_piece:
            sim_you.remove(captured_piece)


        # find the opponents king
        for k in sim_opponent:
            if k.type == "king":
                king_row = k.pos[0] 
                king_col = k.pos[1]

                # if opponent kings pos is in any of your next moves, append a true to list
                if you == white_pieces:
                    if [king_row, king_col] in all_new_moves_opponent_for_check(player=sim_you, pieces_white=sim_you, pieces_black=sim_opponent):
                        list_of_trues.append(True)
                        break
                
                elif you == black_pieces:
                    if [king_row, king_col] in all_new_moves_opponent_for_check(player=sim_you, pieces_white=sim_opponent, pieces_black=sim_you):
                        list_of_trues.append(True)
                        break
                    
    # if the lists length is equal to opponents possible next moves, its checkmate/stalemate, otherwise not
    if len(list_of_trues) == len(opponent_next_moves_passive) and len(opponent_next_moves_passive) > 0:
        # print("checkmate")
        return True
    # print("no checkmate detected")
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
            return False

        attempted_move_2 = input()

        if attempted_move_2 == "cancel":
            return False

        if validate_move(attempted_move_2) == "bad":
            continue

        col, row = int(letter_index[attempted_move_2[0]]) , 8 - int(attempted_move_2[1]) 
    
        if [row,col] in piece_aviable_moves:
            while True:
                for x in all_pieces:
                    if x.id == piece_class.id:

                        check_ = is_your_king_in_check(you=you, opponent=opponent, piece=x, new_row=row, new_col=col, pieces_white=pieces_white,pieces_black=pieces_black,pawn_double_move=False)
                        if check_:
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
                            
                            if result[0] == "not_castling":
                                x.pos = [row,col]
                                x.moves+=1
                            elif result[0] == "cancel castling":
                                return False
                            elif "done castling" in result[0]:
                                x.pos = [row,col]
                                x.moves+=1
                        
                        Takes(pieces_white,pieces_black,x,board.taken_list_white,board.taken_list_black)
                        PawnPromotion(piece=x,row=row,col=col,pieces_white=pieces_white,pieces_black=pieces_black)

                        check_ = is_opponent_king_in_check(you=you, opponent=opponent,pieces_white=pieces_white,pieces_black=pieces_black)
                        if check_:
                            # print(f"Check!")

                            checkmate = is_checkmate_opponent(you=you, opponent=opponent,white_pieces=pieces_white,black_pieces=pieces_black)
                            if checkmate:
                                return "checkmate"
                        else:
                            stalemate = is_checkmate_opponent(you=you, opponent=opponent,white_pieces=pieces_white,black_pieces=pieces_black)
                            if stalemate:
                                return "stalemate"

                        return True
        else:
            print("Piece can't move there, try again.")

if __name__ == "__main__":
    main()