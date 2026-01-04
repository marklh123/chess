
from Chess import (
                    Castling, PawnPromotion, Takes,
                    rule_for_pawn, rule_for_king,
                    rule_for_rook, rule_for_queen,
                    rule_for_knight,
                    the_board_printed
                   )

board_template= {
    (0,"a"):False,(0,"b"): False,(0,"c"): False,(0,"d"): False,(0,"e"): False,(0,"f"): False,(0,"g"): False,(0,"h"): False,
    (1,"a"):False,(1,"b"): False,(1,"c"): False,(1,"d"): False,(1,"e"): False,(1,"f"): False,(1,"g"): False,(1,"h"): False,
    (2, "a"): False, (2, "b"): False, (2, "c"): False, (2, "d"): False, (2, "e"): False, (2, "f"): False, (2, "g"): False,
    (2, "h"): False,
    (3,"a"):False,(3,"b"): False,(3,"c"): False,(3,"d"): False,(3,"e"): False,(3,"f"): False,(3,"g"): False,(3,"h"): False,
    (4, "a"): False, (4, "b"): False, (4, "c"): False, (4, "d"): False, (4, "e"): False, (4, "f"): False, (4, "g"): False,
    (4, "h"): False,
    (5, "a"): False, (5, "b"): False, (5, "c"): False, (5, "d"): False, (5, "e"): False, (5, "f"): False, (5, "g"): False,
    (5, "h"): False,
    (6, "a"): False, (6, "b"): False, (6, "c"): False, (6, "d"): False, (6, "e"): False, (6, "f"): False, (6, "g"): False,
    (6, "h"): False,
    (7, "a"): False, (7, "b"): False, (7, "c"): False, (7, "d"): False, (7, "e"): False, (7, "f"): False, (7, "g"): False,
    (7, "h"): False
}

test_scenario_1 = {
    "black": [
            {"id": "p1", "type": "pawn", "symbol": "♟", "pos": [1, "a"], "move": 0, "rule": rule_for_pawn,
             "color": "black", "results":[]},
            {"id": "p2", "type": "pawn", "symbol": "♟", "pos": [1, "b"], "move": 0, "rule": rule_for_pawn,
             "color": "black"},
            {"id": "p3", "type": "pawn", "symbol": "♟", "pos": [1, "g"], "move": 0, "rule": rule_for_pawn,
             "color": "black"},
            {"id": "p4", "type": "pawn", "symbol": "♟", "pos": [6, "g"], "move": 0, "rule": rule_for_pawn,
             "color": "black"},
            {"id": "p5", "type": "pawn", "symbol": "♟", "pos": [4, "g"], "move": 0, "rule": rule_for_pawn,
             "color": "black"},
            {"id": "k", "type": "king", "symbol": "♚", "pos": [0, "e"], "move": 0, "rule": rule_for_king, "color": "black"},
            {"id": "r1", "type": "rook", "symbol": "♜", "pos": [0, "a"], "move": 0, "rule": rule_for_rook,
             "color": "black"},
            {"id": "r2", "type": "rook", "symbol": "♜", "pos": [0, "h"], "move": 0, "rule": rule_for_rook,
             "color": "black"},
            {"id": "r3", "type": "rook", "symbol": "♜", "pos": [1, "e"], "move": 0, "rule": rule_for_rook,
             "color": "black"},
            {"id": "n1", "type": "knight", "symbol": "♞", "pos": [2, "c"], "move": 0, "rule": rule_for_knight,
             "color": "black"},
            {"id": "n2", "type": "knight", "symbol": "♞", "pos": [6, "f"], "move": 0, "rule": rule_for_knight,
             "color": "black"},
    ],
    "white": [
        {"id": "p1", "type": "pawn", "symbol": "♙", "pos": [2, "a"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        { "id": "p2", "type": "pawn", "symbol": "♙", "pos": [2, "h"], "move": 0, "rule": rule_for_pawn,
         "color": "white"},
        {"id": "r2", "type": "rook", "symbol": "♖", "pos": [7, "h"], "move": 0, "rule": rule_for_rook,
         "color": "white"},
        {"id": "q", "type": "queen", "symbol": "♕", "pos": [7, "d"], "move": 0, "rule": rule_for_queen,
         "color": "white"},
        {"id": "n2", "type": "knight", "symbol": "♘", "pos": [7, "g"], "move": 0, "rule": rule_for_knight,
         "color": "white"},
        {"id": "k", "type": "king", "symbol": "♔", "pos": [7, "e"], "move": 0, "rule": rule_for_king, "color": "white"},
    ],

    "black_results":
        {
            "p1": {},
            "p2": {(2, "b"): True, (3, "b"): True, (2, "a"): True},
            "p3": {(2, "g"): True, (3, "g"): True, (2, "h"): True},
            "p4": {(7, "h"): True},
            "p5": {(5, "g"): True},
            "k": {(0, "d"): True,(1, "d"): True,(1, "e"): True,(1, "f"): True,(0, "f"): True,
                  (0, "c"): "pass",(0, "g"): "pass",},
            "r1": {(0, "b"): True,(0, "c"): True,(0, "d"): True},
            "r2": {(0, "g"): True,(0, "f"): True, (1, "h"): True, (2, "h"): True},
            "r3": {(1, "c"): True,(1, "d"): True, (1, "f"): True,
                   (2, "e"): True,(3, "e"): True,(4, "e"): True,(5, "e"): True, (6, "e"): True, (7, "e"): True},
            "n1": {(0, "b"):True, (3, "a"):True,(4, "b"):True,(4, "d"):True,(0, "d"):True, (3,"e"):True},
            "n2": {(4,"e"):True,(7,"d"):True,(5,"d"):True, (5,"h"):True, (7,"h"):True}
        }
}

def run_the_rules(piece,  cur_row: int, cur_col: str,
                          new_row:int, new_col: str,
                          black, white):
    """ Player moves the piece
    piece: selected  piece
    cur_row: current row (int) of the piece to move
    cur_col:: current column (string) of the piece to move

    Returns: True if move is good, False if move is not good
    """
    letter_index = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    index_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    if piece:
        # if there is a real piece selected
            #print()
            #print(letter_index[new_col], new_row)
            #print(letter_index[cur_col], cur_row)
            ################
            # xx,col,piece,new_row, new_col
            # check the move
            ################
            available_pos = piece['rule'](black,white,piece)
            # this is new_pos called into this function
            print(f'available====: {available_pos}')
            if len(available_pos) == 0:
                #print("This move is not available, try again.")
                return False
            # if new_pos is empty then cancels move and lets player pick different piece
            elif [new_row, letter_index[new_col]] not in available_pos and len(available_pos) != 0:
                #print("This exact move is not available, but this piece has other moves, try again.")
                return False

            elif [new_row, letter_index[new_col]] in available_pos:
                if piece["color"] == "white":
                    your_color = white
                    opp_color = black
                else:
                    your_color = black
                    opp_color = white

                if piece['type'] != 'king':
                    print(f"This is a valid move! {new_row}, {new_col}")
                    #piece['pos'] = [new_row, new_col]
                    #piece['move']+=1
                elif piece ['type'] == 'king' and piece['move'] == 0:
                    result = Castling(black, white, piece, letter_index, index_letter,
                                      cur_row, cur_col, new_col, new_row, your_color)
                    #print("ASDASDSADSAD"+result)
                    if result == "not castling":
                        print("This is a valid move!")
                        #piece['pos'] = [new_row, new_col]
                        #piece['move'] += 1
                    elif result == "cancel castling":
                        #print("This move is not castling done right, try again.")
                        return False
                    elif result == "done castling":
                        print ("This is a valid move")
                        #piece['pos'] = [new_row, new_col]
                        #piece['move'] += 1
                #PawnPromotion(piece,new_row,new_col,letter_index,cur_col)
                # checks for pawn promotion
                #Takes(black,white,piece)
                # checks for takes
                return True

def driver():
    """
    Runs the tests
    Select a piece, get the current position,
    for each pos in board check if rules match the truth
    :return:
    """
    for piece in test_scenario_1["black"]:
        print (f'testing piece: {piece["id"]}')
        cur_row, cur_col = piece["pos"]
        #
        expected_results = test_scenario_1["black_results"]
        piece_id = piece["id"]
        board = board_template.copy()
        board.update(expected_results[piece_id])
        fix_me = []
        for pos, value in board.items():
            new_row, new_col = pos
            truth = value
            if truth == "pass":
                #jump over this move as in case of castling
                continue
            result = run_the_rules(piece,
                                   cur_row, cur_col,
                                   new_row, new_col,
                                   black=test_scenario_1["black"],
                                   white=test_scenario_1["white"])
            if result != truth:
                fix_me.append(f'({piece_id}: {cur_row}, {cur_col}) -> ({new_row}, {new_col}): {result} vs {truth}')
            #assert result == truth
        print ("======= errors start =======")
        for e in fix_me:
            print (e)
        print("======= errors ends =======")

if __name__ == '__main__':
    driver()
    the_board_printed(0, test_scenario_1["black"], test_scenario_1["white"])