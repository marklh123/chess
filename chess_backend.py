import constants
import datetime
import json


letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

white_in_check = False
black_in_check = False

file_name = "Chess.txt"
try:
   with open(file_name, "w") as file:
    file.write(f"{datetime.datetime.now()}\n")
except FileExistsError:
   print("That file already exists")

def log_move(piece):
    """

    :param piece:
    :return:
    """
    try:
        with open(file_name, "a") as file:
            json.dump(piece, file, indent=1)
    except FileExistsError:
        print("That file already exists")

def rule_for_pawn_takes(opponent, pawn):
    """
    Find list of possible takes
    :param opponent: black or white
    :param pawn: selected pawn
    :return: takes by the pawn
    """
    if pawn["color"] == "black":
        direction = 1
    else:
        direction = -1

    takes = []

    pawn_row, col_letter = pawn["pos"]
    pawn_col = letter_index[col_letter]
    for op in opponent:
        op_row = op["pos"][0]
        op_col = letter_index[op["pos"][1]]

        if (([op_row, op_col] == [pawn_row + direction, pawn_col + 1]) or
            ([op_row, op_col] == [pawn_row + direction, pawn_col - 1])):
            print(f'take: {[op_row, op_col]}')
            takes.append([op_row, op_col])

    return takes

def rule_for_pawn(you,opponent,pawn):
    # basic rule for pawns: 1 up
    row, col_letter = pawn["pos"]
    col = letter_index[col_letter]

    if pawn["color"] == "black":
        direction = 1
    else:
        direction = -1

    # if its pawns first move then it can move either 1 or 2 forward
    if pawn["move"] == 0:
        new_moves = [(0, direction*1) , (0, direction*2)]
    # if it's not pawns first move then only 1 forward
    else:
        new_moves = [(0, direction*1)]

    # finds out the next position the pawn can go and puts into list new_pos
    new_pos=[]
    for move in new_moves:
        delta_col = move[0]
        delta_row = move[1]
        temp_pos = [row + delta_row, col + delta_col]
        new_pos.append(temp_pos)

    for piece in you + opponent:
        # return new_pos: gives list of positions to the function piece(rule)
        # if theres no moves in new_pos[] it returns an empty list

        row = piece['pos'][0]
        col_letter = piece['pos'][1]
        col = letter_index[col_letter]
        if len(new_pos) == 0:
            break

        if [row, col] == new_pos[0]:
            print(f"first {piece['pos']} is taken, remove forward moves")
            new_pos = []
            # new_pos[0] is if a piece is right in front of the pawn in which the pawn has zero possible moves
            # that is why the list goes empty, the pawn can't move

        if (len(new_pos)>1) and ([row, col] == new_pos[1]):
            print (f'this {piece["pos"]} is taken')
            new_pos.remove([row, col])
            # this is when a piece is 2 places in front of a pawn, gets rid of the 2 space move option
            # can still move 1 forward though

    print(f'available move (before take): {new_pos}')
    takes = rule_for_pawn_takes(opponent, pawn)
    #
    new_pos.extend(takes)
    # Adds possible take moves to new_pos, need to use extend not append
    # if a pawn gets to back opposite rank, it gets promoted to a queen
    return new_pos

def rule_for_rook(you, opponent,rook):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


    row, col_letter = rook["pos"]
    col = letter_index[col_letter]
    #
    your_color = you
    opponent_color = opponent
    #
    new_pos = []
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    #down, up, right, left
    #
    for dr, dc in directions:
        # first iteration is (1,0) so dr = 1 and dc = 0 then (-1,0) so dr = -1 and dc = 0 and so on
        r = row
        c = col

        while True:
            # this loop keeps running until one of the break conditions are met
            r += dr
            # row = row + direction row
            c += dc
            # col = col + direction col
            # keeps adding direction value to rook pos value

            if c < 0 or c > 7:
                break
            if r < 0 or r > 7:
                break
            # if row and col are both smaller than zero and bigger than 7 end loop no moves in new_pos
            # row and col keeps adding direction to it until it becomes too big then breaks here

            if any(p['pos'] == [r, index_letter[c]] for p in your_color):
                break
            #if any pieces position is equal to r,c in your color end loop no moves in new_pos
            #if this condition is met it breaks because that's the exact square that has a piece on it


            if any(p['pos'] == [r, index_letter[c]] for p in opponent_color):
                new_pos.append([r, c])
                break
            # if any pieces position is equal to r,c that's an opponent piece you can take it, but then it breaks

            new_pos.append([r, c])
            # if none of those conditions are met then it's a normal empty square, and it gets added to new_pos

    return new_pos
    # after going through while loop for all directions then all positions are collected and you can return

def rule_for_bishop(you,opponent,bishop):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = bishop["pos"]
    col = letter_index[col_letter]

    your_color = you
    opponent_color = opponent

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

            if any(p['pos'] == [r, index_letter[c]] for p in your_color):
                break


            if any(p['pos'] == [r, index_letter[c]] for p in opponent_color):
                new_pos.append([r, c])
                break

            new_pos.append([r, c])

    return new_pos

def rule_for_queen(you,opponent,queen):
    """
        Find all possible moves for queen
        :param you: your color, black or white
        :param opponent: opponent color, black or white
        :param queen: selected queen
        :return: list of possible moves by the queen
        """

    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = queen["pos"]
    col = letter_index[col_letter]

    your_color = you
    opponent_color = opponent

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

            if any(p['pos'] == [r, index_letter[c]] for p in your_color):
                break

            if any(p['pos'] == [r, index_letter[c]] for p in opponent_color):
                new_pos.append([r, c])
                break

            new_pos.append([r, c])

    return new_pos

def rule_for_king(you,opponent,king):
    """
        Find all possible moves for king
        :param you: your color, black or white
        :param opponent: opponent color, black or white
        :param king: selected king
        :return: list of possible moves by the king
        """

    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


    row, col_letter = king["pos"]
    col = letter_index[col_letter]

    new_moves = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]

    if king["move"] == 0:
        all_pieces = you + opponent
        # occupied_cols are all pieces cols that are in the same row as king
        occupied_cols = [letter_index[p["pos"][1]] for p in all_pieces if p["pos"][0] == row and p is not king]

        # King-side castling: f and g must be empty (col+1 and col+2)
        kingside_clear = (col + 1) not in occupied_cols and (col + 2) not in occupied_cols
        # Queen-side castling: b, c and d must be empty (col-1, col-2, col-3)
        queenside_clear = (col - 1) not in occupied_cols and (col - 2) not in occupied_cols and (
                    col - 3) not in occupied_cols

        if kingside_clear:
            new_moves.append((0, 2))
        if queenside_clear:
            new_moves.append((0, -2))

    new_pos = []

    your_color = you
    opponent_color = opponent

    for move in new_moves:
        temp_row = row + move[0]
        temp_col = col + move[1]
        if temp_row < 0 or temp_row > 7:
            continue
        elif temp_col < 0 or temp_col > 7:
            continue

        if any(p['pos'] == [temp_row,index_letter[temp_col]] for p in your_color):
            continue

        if any(p['pos'] == [temp_row,index_letter[temp_col]] for p in opponent_color):
            new_pos.append([temp_row, temp_col])
            continue

        new_pos.append([temp_row, temp_col])

    return new_pos

def rule_for_knight(you,opponent,knight):
    """
        Find all possible moves for knight
        :param you: your color, black or white
        :param opponent: opponent color, black or white
        :param knight: selected knight
        :return: list of possible moves by the knight
        """

    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = knight["pos"]
    col = letter_index[col_letter]

    new_moves = [(-2,1),(-2,-1),(2,1),(2,-1),(1,-2),(-1,-2),(1,2),(-1,2)]

    new_pos = []

    your_color = you
    opponent_color = opponent

    for move in new_moves:
        temp_row = row + move[0]
        temp_col = col + move[1]
        if temp_row < 0 or temp_row > 7:
            continue
        elif temp_col < 0 or temp_col > 7:
            continue

        if any(p['pos'] == [temp_row, index_letter[temp_col]] for p in your_color):
            continue

        if any(p['pos'] == [temp_row, index_letter[temp_col]] for p in opponent_color):
            new_pos.append([temp_row, temp_col])
            continue

        new_pos.append([temp_row, temp_col])

    # use continue instead of break
    # break → STOP the whole loop
    # continue → SKIP this iteration, keep looping

    return new_pos

black = [
        {"id": "p1", "type": "pawn", "symbol": "♟", "pos": [1, "a"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p2", "type": "pawn", "symbol": "♟", "pos": [1, "b"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p3", "type": "pawn", "symbol": "♟", "pos": [1, "c"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p4", "type": "pawn", "symbol": "♟", "pos": [1, "d"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p5", "type": "pawn", "symbol": "♟", "pos": [1, "e"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p6", "type": "pawn", "symbol": "♟", "pos": [1, "f"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p7", "type": "pawn", "symbol": "♟", "pos": [1, "g"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "p8", "type": "pawn", "symbol": "♟", "pos": [1, "h"], "move": 0, "rule": rule_for_pawn,
         "color": "black", "image": constants.black_pawn},
        {"id": "r1", "type": "rook", "symbol": "♜", "pos": [0, "a"], "move": 0, "rule": rule_for_rook,
         "color": "black", "image": constants.black_rook},
        {"id": "r2", "type": "rook", "symbol": "♜", "pos": [0, "h"], "move": 0, "rule": rule_for_rook,
         "color": "black", "image": constants.black_rook},
        {"id": "n1", "type": "knight", "symbol": "♞", "pos": [0, "b"], "move": 0, "rule": rule_for_knight,
         "color": "black", "image": constants.black_knight},
        {"id": "n2", "type": "knight", "symbol": "♞", "pos": [0, "g"], "move": 0, "rule": rule_for_knight,
         "color": "black", "image": constants.black_knight},
        {"id": "b1", "type": "bishop", "symbol": "♝", "pos": [0, "c"], "move": 0, "rule": rule_for_bishop,
         "color": "black", "image": constants.black_bishop},
        {"id": "b2", "type": "bishop", "symbol": "♝", "pos": [0, "f"], "move": 0, "rule": rule_for_bishop,
         "color": "black", "image": constants.black_bishop},
        {"id": "q", "type": "queen", "symbol": "♛", "pos": [0, "d"], "move": 0, "rule": rule_for_queen,
         "color": "black", "image": constants.black_queen},
        {"id": "k", "type": "king", "symbol": "♚", "pos": [0, "e"], "move": 0, "rule": rule_for_king,
         "color": "black", "image": constants.black_king},
    ]
white = [
        {"id": "p1", "type": "pawn", "symbol": "♙", "pos": [6, "a"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p2", "type": "pawn", "symbol": "♙", "pos": [6, "b"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p3", "type": "pawn", "symbol": "♙", "pos": [6, "c"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p4", "type": "pawn", "symbol": "♙", "pos": [6, "d"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p5", "type": "pawn", "symbol": "♙", "pos": [6, "e"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p6", "type": "pawn", "symbol": "♙", "pos": [6, "f"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p7", "type": "pawn", "symbol": "♙", "pos": [6, "g"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "p8", "type": "pawn", "symbol": "♙", "pos": [6, "h"], "move": 0, "rule": rule_for_pawn,
         "color": "white",  "image": constants.white_pawn},
        {"id": "r1", "type": "rook", "symbol": "♖", "pos": [7, "a"], "move": 0, "rule": rule_for_rook,
         "color": "white",  "image": constants.white_rook},
        {"id": "r2", "type": "rook", "symbol": "♖", "pos": [7, "h"], "move": 0, "rule": rule_for_rook,
         "color": "white",  "image": constants.white_rook},
        {"id": "n1", "type": "knight", "symbol": "♘", "pos": [7, "b"], "move": 0, "rule": rule_for_knight,
         "color": "white",  "image": constants.white_knight},
        {"id": "n2", "type": "knight", "symbol": "♘", "pos": [7, "g"], "move": 0, "rule": rule_for_knight,
         "color": "white",  "image": constants.white_knight},
        {"id": "b1", "type": "bishop", "symbol": "♗", "pos": [7, "c"], "move": 0, "rule": rule_for_bishop,
         "color": "white",  "image": constants.white_bishop},
        {"id": "b2", "type": "bishop", "symbol": "♗", "pos": [7, "f"], "move": 0, "rule": rule_for_bishop,
         "color": "white",  "image": constants.white_bishop},
        {"id": "q", "type": "queen", "symbol": "♕", "pos": [7, "d"], "move": 0, "rule": rule_for_queen,
         "color": "white",  "image": constants.white_queen},
        {"id": "k", "type": "king", "symbol": "♔", "pos": [7, "e"], "move": 0, "rule": rule_for_king,
         "color": "white",  "image": constants.white_king},
    ]


def PawnPromotion(piece,new_row,col):
    """
        Detect if a pawn has reached back rank, promotes to queen if so
        :param piece: selected piece
        :param new_row: moved row, digit 0-7
        :param col: moved col, digit 0-7
         """

    blackbackranks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
    whitebackranks = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]

    if piece["color"] == "white" and piece["type"] == "pawn":
        if (new_row, letter_index[col]) in blackbackranks:
            piece["symbol"] = "♕"
            piece["type"] = "queen"
            piece["image"] = constants.white_queen
            piece["id"] = "qN"
            piece["rule"] = rule_for_queen
    elif piece["color"] == "black" and piece["type"] == "pawn":
        if (new_row, letter_index[col]) in whitebackranks:
            piece["symbol"] = "♛"
            piece["type"] = "queen"
            piece["image"] = constants.black_queen
            piece["id"] = "qN"
            piece["rule"] = rule_for_queen

def Takes(opponent,piece):
    """
        Detects if the moved piece takes an opponents piece
        :param opponent: opponent color, black or white
        :param piece: selected and moved piece
         """

    for op in opponent:
        if op['pos'] == piece['pos']:
            opponent.remove(op)
            break
    # checks if the position has an enemy piece and if so removes it and says that shits gone

def Castling(black, white, letter_index, index_letter,
             xx, col,
             new_col, new_row, your_color):
        """
            Detects if you can castle
            :param black: black pieces, you or opponent
            :param white: white pieces, you or opponent
            :param xx: original row as a digit
            :param col: original colum as a digit
            :param new_col: attempted move column as a digit
            :param new_row: attempted move row as a digit
            :param your_color: black or white
             """

        if (([new_row, letter_index[new_col]] != [xx, (letter_index[col] + 2)]) and
                ([new_row, letter_index[new_col]] != [xx, (letter_index[col] - 2)])):
                return "not_castling"

        # king-side castling
        if [new_row, letter_index[new_col]] == [xx, (letter_index[col] + 2)]:
            targets = [(xx, (letter_index[col] + 1)), (xx, (letter_index[col] + 2))]
            occupied = [p["pos"] for p in black + white]

            # If all squares in targets are empty, then do the next step
            if all(t not in occupied for t in targets):
                rook_col = (letter_index[col]) + 3
                rook = None
                for piece2 in your_color:
                    if (piece2["pos"] == [xx, index_letter[rook_col]]) and (piece2["type"] == "rook"):

                        rook = piece2

                        # cant castle if rook has already moved before
                        if piece2["move"] > 0:
                            return "cancel castling"
                        break

                if rook:
                    new_rook_col = (letter_index[col] + 1)

                    rook["pos"] = [xx, index_letter[new_rook_col]]
                    rook["move"] += 1
                    return "done castling"

        # queen-side
        if [new_row, letter_index[new_col]] == [xx, (letter_index[col] - 2)]:

            targets = [(xx, (letter_index[col] - 1)), (xx, (letter_index[col] - 2)), (xx, (letter_index[col] - 3))]
            occupied = [p["pos"] for p in black + white]

            if all(t not in occupied for t in targets):
                rook_col = (letter_index[col]) - 4

                rook = None
                for piece2 in your_color:
                    if (piece2["pos"] == [xx, index_letter[rook_col]]) and (piece2["type"] == "rook"):
                        rook = piece2
                        if piece2["move"] > 0:
                            return "cancel castling"
                        break

                if rook:
                    new_rook_col = (letter_index[col] - 1)

                    rook["pos"] = [xx, index_letter[new_rook_col]]
                    rook["move"]+=1
                    return "done castling"

        return "cancel castling"

def all_new_moves_opponent_for_check(player, other):
    """
        Gets all possible take moves for your opponents next move
        :param player: your color, black or white
        :param other: opponent color, black or white
        :return: list of all possible moves
    """

    all_new_moves_your_color = []
    for i in player:
        my_rule = i["rule"]
        if i['type'] == 'pawn':
            my_rule = rule_for_pawn_takes
            all_new_moves_your_color.extend(my_rule(other, i))
        else:
            all_new_moves_your_color.extend(my_rule(player, other, i))

    return all_new_moves_your_color

def is_your_king_in_check(you, opponent,
                          piece, new_row, new_col):
    """
    The new move is not valid if it keeps or puts your king in check

    :param you: board pieces for your color, black or white
    :param opponent: board pieces for opponent, black or white
    :param piece: your piece that moved
    :param new_row: your piece new row
    :param new_col: your piece new column
    :return: False if not in check, True if in check
    """

    you_sim = [{"id": p["id"], "type": p["type"], "pos": list(p["pos"]),
                "color": p["color"], "move": p["move"], "rule": p["rule"]} for p in you]


    moved_piece = [x for x in you_sim if x["id"] == piece['id']][0] # gets dictionary of piece that's moving
    moved_piece["pos"] = [new_row, new_col]

    #if new move is take, remove the captured piece from opponent
    opponent_sim = [{"id": p["id"], "type": p["type"], "pos": list(p["pos"]),
                     "color": p["color"], "move": p["move"], "rule": p["rule"]} for p in opponent]
    captured_piece = None
    for piece in opponent_sim:
        if piece["pos"] == moved_piece["pos"]:
            captured_piece = piece
            break
    if captured_piece:
        opponent_sim.remove(captured_piece)


    your_king = [piece for piece in you_sim if piece["type"] == "king"][0]
    king_row = your_king["pos"][0]
    king_col = letter_index[your_king["pos"][1]]
    king_pos = [king_row, king_col]
    if king_pos in all_new_moves_opponent_for_check(opponent_sim, you_sim):
        return True
    else:
        # if king isn't in check next move it can go forward and update the board
        return False

def is_opponent_in_check(you, opponent):
    """ Detect if your move puts opponent in check
        :param you: your color, black or white
        :param opponent: opponent color, black or white
        :return: if opponent is in check, True or False
        """

    opponent_king = [piece for piece in opponent if piece["type"] == "king"][0]
    king_row = opponent_king["pos"][0]
    king_col = letter_index[opponent_king["pos"][1]]
    king_pos = [king_row, king_col]
    print(f"King Position:{king_pos}")
    print(f"All new moves in white: {all_new_moves_opponent_for_check(you, opponent)}")

    if king_pos in all_new_moves_opponent_for_check(you, opponent):
        return True
    else:
        # can go forward and update the board
        return False

def is_opponents_next_moves_0(you, opponent):
    """ Detects if opponent has any possible next moves (used for checkmate and stalemate)
        :param you: your color, black or white
        :param opponent: opponent color, black or white
        :return: if opponent doesn't have any next moves, True or False
        """
    opponent_next_moves_passive = []
    for a in opponent:
        my_rule = a["rule"]
        next_move_while_in_check = (my_rule(opponent, you, a))
        id_for_piece = a["id"]
        for x in next_move_while_in_check:
            opponent_next_moves_passive.append({
                'pos': [x[0], index_letter[x[1]]],
                'id': id_for_piece,
            })

    list_of_trues = []
    for a in opponent_next_moves_passive:  # goes through each of blacks next moves while in check

        sim_you = [{"id": p["id"], "type": p["type"], "pos": list(p["pos"]),
                    "color": p["color"], "move": p["move"], "rule": p["rule"]} for p in you]


        sim_opponent = [{"id": p["id"], "type": p["type"], "pos": list(p["pos"]),
                         "color": p["color"], "move": p["move"], "rule": p["rule"]} for p in opponent]

        # whites simulated move position
        sim_row = a["pos"][0]
        sim_col = a["pos"][1]

        for x in sim_opponent:
            if x["id"] == a["id"]:
                # every other key but pos stays the same, pos is updated
                x["pos"] = [sim_row, sim_col]
                break

        # Check if a piece was captured and remove it
        captured_piece = None
        for sim_black_piece in sim_you:
            if sim_black_piece["pos"] == [sim_row, sim_col]:
                captured_piece = sim_black_piece
                break

        if captured_piece:
            sim_you.remove(captured_piece)

        for k in sim_opponent:
            if k["type"] == "king":
                king_row = k["pos"][0]
                king_col = letter_index[k["pos"][1]]

                if [king_row, king_col] in all_new_moves_opponent_for_check(sim_you, sim_opponent):
                    list_of_trues.append(True)
                break

    # 0 next moves
    if len(list_of_trues) == len(opponent_next_moves_passive) and len(opponent_next_moves_passive) > 0:
        return True

    # >0 next moves
    return False


