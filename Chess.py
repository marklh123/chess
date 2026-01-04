# make castling
# detect for checks
# figure out checkmate



def rule_for_pawn(black,white,pawn):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    # basic rule for pawns: 1 up
    row, col_letter = pawn["pos"]
    col = letter_index[col_letter]

    if pawn["color"] == "black":
        direction = 1
    else:
        direction = -1
    # just saying black moves up white moves down the board

    if pawn["move"] == 0:
        new_moves = [(0, direction*1) , (0, direction*2)]
        # if its pawns first move then it can move either 1 or 2 forward
    else:
        new_moves = [(0, direction*1)]
        # if it's not pawns first move then only 1 forward



    new_pos=[]
    for move in new_moves:
        # for loop that goes through possible moves in list new_moves
        delta_col = move[0]
        delta_row = move[1]
        # move[0] is x and move[1] is y of a move (x,y) in list new_moves
        temp_pos = [row + delta_row, col + delta_col]
        new_pos.append(temp_pos)
    # it gets the delta (difference) of col and row and adds that to the pawns current position
    # basically just finds out the next position the pawn can go and puts into list new_pos


    for piece in black + white:
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


    takes = []
    if pawn["color"] == "white":
        opponent_pieces = black
    else:
        opponent_pieces = white
    # defines what color are opponent pieces

    pawn_row, col_letter = pawn["pos"]
    pawn_col = letter_index[col_letter]
    for op in opponent_pieces:
        op_row = op["pos"][0]
        op_col = letter_index[op["pos"][1]]
        # turns col letter to number

        if (([op_row, op_col] == [pawn_row + direction, pawn_col + 1]) or
            ([op_row, op_col] == [pawn_row + direction, pawn_col - 1])):
            print(f'take: {[op_row, op_col]}')
            takes.append([op_row, op_col])

    new_pos.extend(takes)
    # Adds possible take moves to new_pos, need to use extend not append


    # if a pawn gets to back opposite rank, it gets promoted to a queen



    return new_pos

def rule_for_rook(black, white,rook):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


    row, col_letter = rook["pos"]
    col = letter_index[col_letter]

    if rook['color'] == 'black':
        your_color = black
        opponent_color = white

    else:
        your_color = white
        opponent_color = black


    new_pos = []

    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    #down, up, right, left

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

def rule_for_bishop(black,white,bishop):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = bishop["pos"]
    col = letter_index[col_letter]

    if bishop['color'] == 'black':
        your_color = black
        opponent_color = white

    else:
        your_color = white
        opponent_color = black

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

def rule_for_queen(black,white,queen):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = queen["pos"]
    col = letter_index[col_letter]

    if queen['color'] == 'black':
        your_color = black
        opponent_color = white

    else:
        your_color = white
        opponent_color = black

    new_pos = []

    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1),(1,0), (-1,0), (0,1), (0,-1)]
    # first 4 are diagonal directions, last 4 are straight directions

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

def rule_for_king(black,white,king):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


    row, col_letter = king["pos"]
    col = letter_index[col_letter]

    new_moves = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]

    if king["move"] == 0:
        new_moves.extend([(0,2),(0,-2)])

    new_pos = []

    if king["color"] == "white":
        your_color = white
        opponent_color = black

    else:
        your_color = black
        opponent_color = white

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

def rule_for_knight(black,white,knight):
    letter_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    row, col_letter = knight["pos"]
    col = letter_index[col_letter]

    new_moves = [(-2,1),(-2,-1),(2,1),(2,-1),(1,-2),(-1,-2),(1,2),(-1,2)]

    new_pos = []

    if knight["color"] == "white":
        your_color = white
        opponent_color = black

    else:
        your_color = black
        opponent_color = white

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
         "color": "black"},
        {"id": "p2", "type": "pawn", "symbol": "♟", "pos": [1, "b"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p3", "type": "pawn", "symbol": "♟", "pos": [1, "c"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p4", "type": "pawn", "symbol": "♟", "pos": [1, "d"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p5", "type": "pawn", "symbol": "♟", "pos": [1, "e"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p6", "type": "pawn", "symbol": "♟", "pos": [1, "f"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p7", "type": "pawn", "symbol": "♟", "pos": [1, "g"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "p8", "type": "pawn", "symbol": "♟", "pos": [1, "h"], "move": 0, "rule": rule_for_pawn,
         "color": "black"},
        {"id": "r1", "type": "rook", "symbol": "♜", "pos": [0, "a"], "move": 0, "rule": rule_for_rook,
         "color": "black"},
        {"id": "r2", "type": "rook", "symbol": "♜", "pos": [0, "h"], "move": 0, "rule": rule_for_rook,
         "color": "black"},
        {"id": "n1", "type": "knight", "symbol": "♞", "pos": [0, "b"], "move": 0, "rule": rule_for_knight,
         "color": "black"},
        {"id": "n2", "type": "knight", "symbol": "♞", "pos": [0, "g"], "move": 0, "rule": rule_for_knight,
         "color": "black"},
        {"id": "b1", "type": "bishop", "symbol": "♝", "pos": [0, "c"], "move": 0, "rule": rule_for_bishop,
         "color": "black"},
        {"id": "b2", "type": "bishop", "symbol": "♝", "pos": [0, "f"], "move": 0, "rule": rule_for_bishop,
         "color": "black"},
        {"id": "q", "type": "queen", "symbol": "♛", "pos": [0, "d"], "move": 0, "rule": rule_for_queen,
         "color": "black"},
        {"id": "k", "type": "king", "symbol": "♚", "pos": [0, "e"], "move": 0, "rule": rule_for_king, "color": "black"},
    ]

white = [
        {"id": "p1", "type": "pawn", "symbol": "♙", "pos": [6, "a"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p2", "type": "pawn", "symbol": "♙", "pos": [6, "b"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p3", "type": "pawn", "symbol": "♙", "pos": [6, "c"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p4", "type": "pawn", "symbol": "♙", "pos": [6, "d"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p5", "type": "pawn", "symbol": "♙", "pos": [6, "e"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p6", "type": "pawn", "symbol": "♙", "pos": [6, "f"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p7", "type": "pawn", "symbol": "♙", "pos": [6, "g"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "p8", "type": "pawn", "symbol": "♙", "pos": [6, "h"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "r1", "type": "rook", "symbol": "♖", "pos": [7, "a"], "move": 0, "rule": rule_for_rook,
         "color": "white"},
        {"id": "r2", "type": "rook", "symbol": "♖", "pos": [7, "h"], "move": 0, "rule": rule_for_rook,
         "color": "white"},
        {"id": "n1", "type": "knight", "symbol": "♘", "pos": [7, "b"], "move": 0, "rule": rule_for_knight,
         "color": "white"},
        {"id": "n2", "type": "knight", "symbol": "♘", "pos": [7, "g"], "move": 0, "rule": rule_for_knight,
         "color": "white"},
        {"id": "b1", "type": "bishop", "symbol": "♗", "pos": [7, "c"], "move": 0, "rule": rule_for_bishop,
         "color": "white"},
        {"id": "b2", "type": "bishop", "symbol": "♗", "pos": [7, "f"], "move": 0, "rule": rule_for_bishop,
         "color": "white"},
        {"id": "q", "type": "queen", "symbol": "♕", "pos": [7, "d"], "move": 0, "rule": rule_for_queen,
         "color": "white"},
        {"id": "k", "type": "king", "symbol": "♔", "pos": [7, "e"], "move": 0, "rule": rule_for_king, "color": "white"},
    ]


def make_board(figures):
    # make 8x8 empty board
    board = [["_" for _ in range(8)] for _ in range(8)]

    letter_to_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    for fig in figures:
        row, col = fig["pos"]  # example: [1, "a"]
        row_index = row  # the number (0–7)
        col_index = letter_to_index[col]  # convert letter to index
        board[row_index][col_index] = fig["symbol"]

    return board


def the_board_printed(active_player_index, black, white):
    figures = black + white
    board = make_board(figures)  # rebuild the board from current piece positions

    if active_player_index == 0:
        print("    a   b   c   d   e   f   g   h")
        print("   --------------------------------")
        for i, row in enumerate(board):
            row_num = i + 1
            print(f"{row_num} | " + "   ".join(row) + f"  | {row_num}")
            # for i row in enumerate goes through each row and then
            # row num is the row number + 1 because it starts
            # at 0 and then it adds that number to that row
        print("   --------------------------------")
        print("    a   b   c   d   e   f   g   h")
    else:
        print("    a   b   c   d   e   f   g   h")
        print("   --------------------------------")
        for i, row in enumerate(reversed(board)):
            row_num = 8 - i
            print(f"{row_num} | " + "   ".join(row) + f"  | {row_num}")
            # for i row in enumerate goes through each row and then
            # row num is the row number + 1 because it starts
            # at 0 and then it adds that number to that row
        print("   --------------------------------")
        print("    a   b   c   d   e   f   g   h")


def main():
    print()
    print("Hello guys welcome to chess!")
    print()

    player1 = input("White players name: ")
    player2 = input("Black players name: ")
    players = [player1, player2]
    active_player_index = 0

# player selects a piece
# then player chooses a location where to move it
# then based on rule for piece it checks if that move is legal
# if it is then the piece mov

    while True:
        player = players[active_player_index]
        select_piece(player,active_player_index,white,black,the_board_printed)
        active_player_index = (active_player_index + 1) % len(players)

def select_piece(player,active_player_index,white,black,the_board_printed,):
    the_board_printed(active_player_index, black, white)
    while True:
        print()
        col_and_row = input(f"It;s your tur {player}. Choose a column [a-h] and then a row (1-8)")
        if len(col_and_row) != 2:
            print("Character error")
            continue
        col = col_and_row[0]
        if col not in ["a","b","c","d","e","f","g","h"]:
            print(f"This column ({col}) isn't an option. Let's try again.")
            continue
        row = int(col_and_row[1])
        xx = row - 1
        if xx not in [0,1,2,3,4,5,6,7]:
            print(f"This row ({row}) isn't an option. Let's try again.")
            continue

        piece = None

        if active_player_index == 1:
            for p in black:
                if p['pos'] == [xx,col]:
                    piece = p
                    break
        # if its blacks turn it checks blacks pieces and if any position matches with players choice
        # then piece becomes that certain piece on that position


            if piece:
                # if there's a real piece selected
                symbol = piece["symbol"]
                print(f'{player} has selected the piece {symbol} at {p["pos"]}')
                move = make_a_move(piece, None,xx, col)
                if move:
                    return
            else:
                print("Theres no piece in the pos...")



        else: # same thing just for white now
            for w in white:
                if w['pos'] == [xx, col]:
                    piece = w
                    break

            if piece:
                symbol = piece["symbol"]
                print(f'{player} has selected the piece {symbol} at {w["pos"]}')
                move = make_a_move(None,piece,xx,col)
                if move:
                    return
            else:
                print("Theres no piece in the pos...")


def make_a_move(p,w, xx: int, col: str):
    """ Player moves the piece
    p: black piece
    w: white piece
    xx: current row (int) of the piece to move
    col:: current column (string) of the piece to move
    """
    letter_index = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    piece = p or w

    if piece:
        # if there is a real piece selected
        while True:
            print()
            col_and_row = input(f"Choose a column [a-h] to move to and then a row (1-8) to move to: ")
            if len(col_and_row) != 2:
                print("Character error")
                continue
            new_col = col_and_row[0]
            if new_col not in letter_index:
                print("The col isn't available, Try again.")
                continue

            new_row = int(col_and_row[1])-1
            if new_row not in range(8):
                print("Invalid row. Must be a number 1-8. Try again.")
                continue

            print()
            print(letter_index[new_col], new_row)
            print(letter_index[col], xx)
            ################
            # xx,col,piece,new_row, new_col
            # check the move
            ################
            available_pos = piece['rule'](black,white,piece)
            # this is new_pos called into this function
            print(f'available: {available_pos}')
            if len(available_pos) == 0:
                print("This move is not available, try again.")
                return False
            # if new_pos is empty then cancels move and lets player pick different piece
            elif [new_row, letter_index[new_col]] not in available_pos and len(available_pos) != 0:
                print("This exact move is not available, but this piece has other moves, try again.")
                return False

            elif [new_row, letter_index[new_col]] in available_pos:

                if piece["color"] == "white":
                    your_color = white
                    opp_color = black
                else:
                    your_color = black
                    opp_color = white

                if piece['type'] != 'king':
                    print("This is a valid move!")
                    piece['pos'] = [new_row, new_col]
                    piece['move']+=1
                elif piece ['type'] == 'king' and piece['move'] == 0:
                    result = Castling(black, white, piece, letter_index, index_letter,
                                      xx, col, new_col, new_row, your_color)
                    print("ASDASDSADSAD"+result)
                    if result == "not castling":
                        print("This is a valid move!")
                        piece['pos'] = [new_row, new_col]
                        piece['move'] += 1
                    elif result == "cancel castling":
                        print("This move is not castling done right, try again.")
                        return False
                    elif result == "done castling":
                        piece['pos'] = [new_row, new_col]
                        piece['move'] += 1
                PawnPromotion(piece,new_row,new_col,letter_index,col)
                # checks for pawn promotion

                Takes(black,white,piece)
                # checks for takes
                return True


            # if attempted move is a move in new_pos then it allows it
            # pieces position gets updated and move counter goes up by 1

def PawnPromotion(piece,new_row,new_col,letter_index,col):
    blackbackranks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
    whitebackranks = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    # back rank pos for white: (row 7)

    if piece["color"] == "white" and piece["type"] == "pawn":
        if (new_row, letter_index[col]) in blackbackranks:
            print("Ts pawn in back ranks so we gonna make it a queen")
            piece["symbol"] = "♕"
            piece["type"] = "queen"
    elif piece["color"] == "black" and piece["type"] == "pawn":
        if (new_row, letter_index[col]) in whitebackranks:
            print("Ts pawn in back ranks so we gonna make it a queen")
            piece["symbol"] = "♛"
            piece["type"] = "queen"
    # this checks if pawn is in back rank if it is it turns into a queen

def Takes(black,white,piece):
    opponent_pieces = black if piece["color"] == "white" else white
    # makes one of the list of dictionaries the opp pieces depending on what color the piece is

    for op in opponent_pieces:
        # checks through all pieces in opponents pieces
        if op['pos'] == piece['pos']:
            opponent_pieces.remove(op)
            print(f"{op['type']} is gone!")
            break
    # checks if the position has an enemy piece and if so removes it and says that shits gone

def Castling(black,white,piece,letter_index,index_letter,
        xx,col,
        new_col,new_row,your_color):
    # LATER EDIT THIS SO IT CANT HAPPEN DURING CHECK OR IF IT GOES INTO CHECK

        # cant happen if king has already moved before


        print("THIS IS A KING")
        # check if it moved 2 squares right (king-side)


        if (([new_row, letter_index[new_col]] != [xx, (letter_index[col] + 2)]) and
                ([new_row, letter_index[new_col]] != [xx, (letter_index[col] - 2)])):
                return "not_castling"

        #trt to do castling
        if [new_row, letter_index[new_col]] == [xx, (letter_index[col] + 2)]:
            print("Booyahya!")
            targets = [(xx, (letter_index[col] + 1)), (xx, (letter_index[col] + 2))]
            # targets are 2 empty spaces between rook and king king-side
            occupied = [p["pos"] for p in black + white]
            # occupied is all occupied pieces on board for black and white

            if all(t not in occupied for t in targets):
                # If all squares in targets are empty, then do the next step
                rook_col = (letter_index[col]) + 3
                rook = None
                for piece2 in your_color:
                    if (piece2["pos"] == [xx, index_letter[rook_col]]) and (piece2["type"] == "rook"):

                        rook = piece2

                        if piece2["move"] > 0:
                            return "cancel castling"
                        # cant castle if rook has already moved before
                        break

                if rook:
                    # if so then move rook pos

                    print("Ohhhh yeah boy222")
                    new_rook_col = (letter_index[col] + 1)

                    rook["pos"] = [xx, index_letter[new_rook_col]]
                    rook["move"] += 1
                    return "done castling"

        if [new_row, letter_index[new_col]] == [xx, (letter_index[col] - 2)]:

            # checks if king moved 2 squares left (queen-side)
            print("Booyahya #2!")
            targets = [(xx, (letter_index[col] - 1)), (xx, (letter_index[col] - 2)), (xx, (letter_index[col] - 3))]
            # targets are 3 empty spaces between rook and king queen-side
            occupied = [p["pos"] for p in black + white]
            # occupied is all occupied pieces on board for black and white

            if all(t not in occupied for t in targets):
                # If all squares in targets are empty, then do the next step
                rook_col = (letter_index[col]) - 4

                rook = None
                for piece2 in your_color:
                    if (piece2["pos"] == [xx, index_letter[rook_col]]) and (piece2["type"] == "rook"):
                        # checks if one of your rooks are on that position
                        rook = piece2
                        if piece2["move"] > 0:
                            return "cancel castling"
                        break

                if rook:
                    # if so then move rook pos
                    print("Ohhhh yeah boy222")
                    new_rook_col = (letter_index[col] - 1)

                    rook["pos"] = [xx, index_letter[new_rook_col]]
                    rook["move"]+=1
                    return "done castling"

        return "cancel castling"
    # O


if __name__ == '__main__':
    main()