import curses
import random
import json
import time
from curses import wrapper

player_banks = [0,0,0]

playboard_start_addr = [ 
    (5,32),
    (7,30),
    (9,30),
    (11,32)]

used_letter_dict = {
    "A": (8 ,3),
    "B": (8 ,4),
    "C": (8 ,5),
    "D": (8 ,6),
    "E": (8 ,7),
    "F": (9 ,3),
    "G": (9 ,4),
    "H": (9 ,5),
    "I": (9 ,6),
    "J": (9 ,7),
    "K": (10,3),
    "L": (10,4),
    "M": (10,5),
    "N": (10,6),
    "O": (10,7),
    "P": (11,3),
    "Q": (11,4),
    "R": (11,5),
    "S": (11,6),
    "T": (11,7),
    "U": (12,3),
    "V": (12,4),
    "W": (12,5),
    "X": (12,6),
    "Y": (12,7),
    "Z": (13,3)
    }

def clear_used_letters():
    stdscr.addstr(used_letter_dict["A"][0], used_letter_dict["A"][1], " ")
    stdscr.addstr(used_letter_dict["B"][0], used_letter_dict["B"][1], " ")
    stdscr.addstr(used_letter_dict["C"][0], used_letter_dict["C"][1], " ")
    stdscr.addstr(used_letter_dict["D"][0], used_letter_dict["D"][1], " ")
    stdscr.addstr(used_letter_dict["E"][0], used_letter_dict["E"][1], " ")
    stdscr.addstr(used_letter_dict["F"][0], used_letter_dict["F"][1], " ")
    stdscr.addstr(used_letter_dict["G"][0], used_letter_dict["G"][1], " ")
    stdscr.addstr(used_letter_dict["H"][0], used_letter_dict["H"][1], " ")
    stdscr.addstr(used_letter_dict["I"][0], used_letter_dict["I"][1], " ")
    stdscr.addstr(used_letter_dict["J"][0], used_letter_dict["J"][1], " ")
    stdscr.addstr(used_letter_dict["K"][0], used_letter_dict["K"][1], " ")
    stdscr.addstr(used_letter_dict["L"][0], used_letter_dict["L"][1], " ")
    stdscr.addstr(used_letter_dict["M"][0], used_letter_dict["M"][1], " ")
    stdscr.addstr(used_letter_dict["N"][0], used_letter_dict["N"][1], " ")
    stdscr.addstr(used_letter_dict["O"][0], used_letter_dict["O"][1], " ")
    stdscr.addstr(used_letter_dict["P"][0], used_letter_dict["P"][1], " ")
    stdscr.addstr(used_letter_dict["Q"][0], used_letter_dict["Q"][1], " ")
    stdscr.addstr(used_letter_dict["R"][0], used_letter_dict["R"][1], " ")
    stdscr.addstr(used_letter_dict["S"][0], used_letter_dict["S"][1], " ")
    stdscr.addstr(used_letter_dict["T"][0], used_letter_dict["T"][1], " ")
    stdscr.addstr(used_letter_dict["U"][0], used_letter_dict["U"][1], " ")
    stdscr.addstr(used_letter_dict["V"][0], used_letter_dict["V"][1], " ")
    stdscr.addstr(used_letter_dict["W"][0], used_letter_dict["W"][1], " ")
    stdscr.addstr(used_letter_dict["X"][0], used_letter_dict["X"][1], " ")
    stdscr.addstr(used_letter_dict["Y"][0], used_letter_dict["Y"][1], " ")
    stdscr.addstr(used_letter_dict["Z"][0], used_letter_dict["Z"][1], " ")
    stdscr.refresh()

def clear_dollar_amnts():
    stdscr.addstr(19,4, "      ") 
    stdscr.addstr(19,38, "      ") 
    stdscr.addstr(19,70, "      ") 
    stdscr.refresh()

def clear_category():
    stdscr.addstr(14, 36, "                ")
    stdscr.refresh()

def clear_spin():
    stdscr.addstr(6,66, "        ")
    stdscr.refresh()

def populate_init_board(ull, puzzle_entry):
    puzzle = puzzle_entry["puzzle"]
    category = puzzle_entry["category"]

    stdscr.addstr(14,39, category)
    stdscr.refresh()
    time.sleep(1)
    split_puz = puzzle.split(" ")
    boardlines = []
    cur_boardline = ""
    cur_boardline_len = 0
    for entry in split_puz:
        if ( (len(boardlines) == 0) or (len(boardlines) == 3) ):
            max_line_len = 12
        else:
            max_line_len = 14

        if ( cur_boardline_len + len(entry) + 1 <= max_line_len ):
            cur_boardline += entry
            cur_boardline += " "
            cur_boardline_len += len(entry)
        else:
            boardlines.append(cur_boardline[:-1])
            cur_boardline = str(entry) + " "
            cur_boardline_len = len(entry)
    boardlines.append(cur_boardline[:-1])


    clear_playing_board()
    populate_board(boardlines, ull)
    stdscr.addstr(23,0, "Press Right to spin       ") 
    stdscr.addstr(24,0, "Press Left to buy a vowel ") 
    stdscr.addstr(25,0, "Press Down to solve       ") 
    stdscr.refresh()
    return boardlines


def populate_board(boardlines, used_letter_list):
    starting_addr = (5,30)
    col_offset = 0
    row_offset = 0
    line_idx = 0
    time.sleep(1)
    for line in boardlines:
        if line_idx == 1 or line_idx == 2:
            col_offset = -2
        else:
            col_offset = 0

        for char in line:
            if char in ["&", "!", ",", ".", "?", " ", "-"]:
                stdscr.addstr(starting_addr[0]+row_offset, starting_addr[1]+col_offset, char)
            elif char in used_letter_list:
                stdscr.addstr(starting_addr[0]+row_offset, starting_addr[1]+col_offset, char)
            else:
                stdscr.addstr(starting_addr[0]+row_offset, starting_addr[1]+col_offset, u"\u25A0")
            col_offset += 2
        row_offset += 2
        line_idx +=1

    stdscr.addstr(19,4, "{}".format(player_banks[0])) 
    stdscr.addstr(19,38, "{}".format(player_banks[1])) 
    stdscr.addstr(19,70, "{}".format(player_banks[2]))

    for used_letter in used_letter_list:
       stdscr.addstr(used_letter_dict[used_letter][0], used_letter_dict[used_letter][1], used_letter) 
    stdscr.refresh()
    


def clear_playing_board():
    stdscr.addstr(5,30, " ")
    stdscr.addstr(5,32, " ")
    stdscr.addstr(5,34, " ")
    stdscr.addstr(5,36, " ")
    stdscr.addstr(5,38, " ")
    stdscr.addstr(5,40, " ")
    stdscr.addstr(5,42, " ")
    stdscr.addstr(5,44, " ")
    stdscr.addstr(5,46, " ")
    stdscr.addstr(5,48, " ")
    stdscr.addstr(5,50, " ")
    stdscr.addstr(5,52, " ")

    stdscr.addstr(7,28, " ")
    stdscr.addstr(7,30, " ")
    stdscr.addstr(7,32, " ")
    stdscr.addstr(7,34, " ")
    stdscr.addstr(7,36, " ")
    stdscr.addstr(7,38, " ")
    stdscr.addstr(7,40, " ")
    stdscr.addstr(7,42, " ")
    stdscr.addstr(7,44, " ")
    stdscr.addstr(7,46, " ")
    stdscr.addstr(7,48, " ")
    stdscr.addstr(7,50, " ")
    stdscr.addstr(7,52, " ")
    stdscr.addstr(7,54, " ")

    stdscr.addstr(9,28, " ")
    stdscr.addstr(9,30, " ")
    stdscr.addstr(9,32, " ")
    stdscr.addstr(9,34, " ")
    stdscr.addstr(9,36, " ")
    stdscr.addstr(9,38, " ")
    stdscr.addstr(9,40, " ")
    stdscr.addstr(9,42, " ")
    stdscr.addstr(9,44, " ")
    stdscr.addstr(9,46, " ")
    stdscr.addstr(9,48, " ")
    stdscr.addstr(9,50, " ")
    stdscr.addstr(9,52, " ")
    stdscr.addstr(9,54, " ")

    stdscr.addstr(11,30, " ")
    stdscr.addstr(11,32, " ")
    stdscr.addstr(11,34, " ")
    stdscr.addstr(11,36, " ")
    stdscr.addstr(11,38, " ")
    stdscr.addstr(11,40, " ")
    stdscr.addstr(11,42, " ")
    stdscr.addstr(11,44, " ")
    stdscr.addstr(11,46, " ")
    stdscr.addstr(11,48, " ")
    stdscr.addstr(11,50, " ")
    stdscr.addstr(11,52, " ")

    stdscr.refresh()

            
def update_current_player_index(idx):
    stdscr.addstr(21,7, str(idx))
    stdscr.refresh()
    

def advance_current_player(cur_player_idx):
    if cur_player_idx == 0:
        player_idx = 1
    elif cur_player_idx == 1:
        player_idx = 2
    else:
        player_idx = 0
    update_current_player_index(player_idx)
    return player_idx

def spin(cur_player_idx, puzzle, boardlines, ull):
    wheel_options = [500, 550, 600, 650, 700, 800, 850, 900, 1000, 2500, 3500, 5000]
    wheel_idx = random.randrange(0, 11,1)
    money_up_for_grabs = wheel_options[wheel_idx]
    clear_spin()
    stdscr.addstr(6,66, "{}".format(wheel_options[wheel_idx]))
    stdscr.refresh()
    time.sleep(1)
    consonant_req()
    ch = stdscr.getch()
    return test_puzzle_for_consonant(str(chr(ch)).upper(), cur_player_idx, puzzle, money_up_for_grabs, boardlines, ull)

def clear_workspace():
    stdscr.addstr(23, 0, " "*80)
    stdscr.addstr(24, 0, " "*80)
    stdscr.addstr(25, 0, " "*80)
    stdscr.addstr(26, 0, " "*80)
    stdscr.addstr(27, 0, " "*80)
    stdscr.addstr(28, 0, " "*80)
    stdscr.addstr(29, 0, " "*80)
    stdscr.refresh()

def consonant_req():
    clear_workspace()
    stdscr.addstr(23, 0, "Type a consonant: ")
    stdscr.refresh()

def vowel_req():
    clear_workspace()
    stdscr.addstr(23, 0, "Type a vowel: ")
    stdscr.refresh()

def turn_instructions():
    time.sleep(1)
    clear_workspace()
    stdscr.addstr(24,0, "Press Right to spin       ") 
    stdscr.addstr(25,0, "Press Left to buy a vowel ") 
    stdscr.addstr(26,0, "Press Down to solve       ") 
    stdscr.refresh()


def find_num_char_in_string(ch, string):
    x = [i for i, letter in enumerate(string) if letter == ch]
    return len(x)
        
def test_puzzle_for_consonant(character, cur_player_idx, puzzle, money_up_for_grabs, boardlines, ull):
    if ( character in ["A", "E", "I", "O", "U"]):
        stdscr.addstr(23, 0, "Sorry, {} is a vowel, not a consonant. Next player's turn".format(character)) 
        cur_player_idx = advance_current_player(cur_player_idx)
        turn_instructions()
    elif character in ull:
        stdscr.addstr(23, 0, "Sorry, {} has already been called. Next player's turn".format(character)) 
        cur_player_idx = advance_current_player(cur_player_idx)
        populate_board(boardlines, ull)
        turn_instructions()
    elif not (character in puzzle):
        cur_player_idx = advance_current_player(cur_player_idx)
        ull.append(character)
        populate_board(boardlines, ull)
        stdscr.addstr(23, 0, "Sorry, no {}. Next player's turn".format(character)) 
        turn_instructions()
    else:
        ull.append(character)
        player_banks[cur_player_idx] += money_up_for_grabs*find_num_char_in_string(character, puzzle)
        clear_workspace()
        stdscr.addstr(23, 0, "{} {}s!".format(find_num_char_in_string(character, puzzle), character)) 
        populate_board(boardlines, ull) 
        turn_instructions()
    stdscr.refresh()
    return cur_player_idx
    

def buy_a_vowel(cur_player_idx, puzzle, boardlines, ull):
    #test is player bank contains more than 250, if not, they forfeit their turn 
    if player_banks[cur_player_idx] < 250:
        clear_workspace()
        stdscr.addstr(23, 0, "Sorry, player {}, you do not have enough money to buy a vowel ($250). Next player's turn".format(cur_player_idx)) 
        cur_player_idx = advance_current_player(cur_player_idx)
        populate_board(boardlines, ull) 
    else:
        clear_workspace()
        vowel_req()
        ch = stdscr.getch()
        player_banks[cur_player_idx] -= 250
        test_puzzle_for_vowel(str(chr(ch)).upper(), cur_player_idx, puzzle, boardlines, ull)
    turn_instructions()
    stdscr.refresh()
    return cur_player_idx


def test_puzzle_for_vowel(character, cur_player_idx, puzzle, boardlines, ull):
    if ( character not in ["A", "E", "I", "O", "U"]):
        clear_workspace()
        stdscr.addstr(23, 0, "Sorry, {} is not a vowel. Next player's turn".format(character)) 
        cur_player_idx = advance_current_player(cur_player_idx)
    elif character in ull:
        clear_workspace()
        stdscr.addstr(23, 0, "Sorry, {} has already been called. Next player's turn".format(character)) 
        cur_player_idx = advance_current_player(cur_player_idx)
        populate_board(boardlines, ull)
    elif not (character in puzzle):
        cur_player_idx = advance_current_player(cur_player_idx)
        ull.append(character)
        populate_board(boardlines, ull)
        clear_workspace()
        stdscr.addstr(23, 0, "Sorry, no {}. Next player's turn".format(character)) 
    else:
        ull.append(character)
        clear_workspace()
        stdscr.addstr(23, 0, "{} {}s!".format(find_num_char_in_string(character, puzzle), character)) 
        time.sleep(3)
        populate_board(boardlines, ull) 
    return cur_player_idx

def solve_attempt(cur_player_idx, puzzle):
    clear_workspace()
    stdscr.addstr(23, 0, "Type your solve attempt and submit with Enter Key:") 
    stdscr.addstr(24, 0, "")
    test_bytes = stdscr.getstr(24, 0, len(puzzle)) 
    test_string = ""
    for byt in test_bytes:
        test_string += str(chr(byt))
    if test_string == puzzle:
        clear_workspace()
        stdscr.addstr(23, 0, "CONGRATULATIONS PLAYER {}! YOU WON ${} !!!".format(cur_player_idx, player_banks[cur_player_idx])) 
        stdscr.addstr(24, 0, " Press Ctrl+C to exit and play again ")
        stdscr.refresh()
        time.sleep(5)
        player_idx = cur_player_idx
        success = 1
    else:
        clear_workspace()
        stdscr.addstr(23, 0, "Unfortunately, '{}' is not the correct solution. Play continues to the next player.".format(test_string)) 
        stdscr.addstr(24, 0, "")
        stdscr.refresh()
        time.sleep(5)
        player_idx = advance_current_player(cur_player_idx)
        success = 0
    return player_idx, success


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0,0,"Assuming 3 players: Rolling to determine who goes first:")    
    stdscr.refresh()
    player_priorities = [random.randrange(1,100,1), random.randrange(1,100,1), random.randrange(1,100,1)]
    max_idx = 0
    max_val = 0
    for x in range(len(player_priorities)):
        stdscr.addstr(x+1,0,"Player {}: {}".format(x, player_priorities[x]))
        stdscr.refresh()
        if player_priorities[x] > max_val :
            max_val = player_priorities[x]
            max_idx = x

    stdscr.addstr(4,0,"Player {} goes first".format(max_idx))
    cur_player_idx = max_idx

    ch = stdscr.getch()
    if (ch == curses.KEY_RIGHT):
        stdscr.clear()
        with open("board.txt", "r") as rfile:
            lines = rfile.readlines()

        line_idx = 0
        for line in lines:
            stdscr.addstr(line_idx, 0, line)
            line_idx += 1

    clear_used_letters()
    clear_dollar_amnts()
    clear_category()
    clear_spin()

    with open("puzzle_list.json", "r") as rfile:
        puzzle_entries = json.load(rfile)

    #choose a random puzzle index
    #ensure its round does not contain "^"
    # if not, this is our puzzle and break
    while (True):
        rand_puzzle_index = random.randrange(0, 1970, 1)
        puzzle_entry = puzzle_entries["season_40"][rand_puzzle_index]
        if not ("^" in puzzle_entry["round"]):
            break;
    puzzle = puzzle_entry["puzzle"]
    category = puzzle_entry["category"]

    used_letters_list = []
    boardlines = populate_init_board(used_letters_list, puzzle_entry)
    update_current_player_index(cur_player_idx)

    while ( True ):
        ch = stdscr.getch()
        if ( ch == curses.KEY_RIGHT ):
            cur_player_idx = spin(cur_player_idx, puzzle, boardlines, used_letters_list)
        elif ( ch == curses.KEY_LEFT ):
            cur_player_idx = buy_a_vowel(cur_player_idx, puzzle, boardlines, used_letters_list)
        else :
            cur_player_idx, success = solve_attempt(cur_player_idx, puzzle)
            if ( success ):
                break


if __name__ == '__main__':
    stdscr = curses.initscr()
    stdscr.keypad(True)
    main(stdscr)
