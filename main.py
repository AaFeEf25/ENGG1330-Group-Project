# by jad
import random
import time
import curses

playerscore = 0


def safe_addstr(stdscr, y, x, text, color_pair=1):
    """
    Adds a string to the screen at the specified coordinates with the given color pair.
    """
    try:
        max_y, max_x = stdscr.getmaxyx()
        if y < max_y and x < max_x:
            # shorten text if it exceeds the screen width
            if x + len(text) > max_x:
                text = text[:max_x - x]
            stdscr.addstr(y, x, text, curses.color_pair(color_pair))
    except curses.error:
        pass


def safe_move(stdscr, y, x):
    """
    Moves the cursor to the specified coordinates.
    """
    try:
        max_y, max_x = stdscr.getmaxyx()
        if y < max_y and x < max_x:
            stdscr.move(y, x)
    except curses.error:
        pass


def printslow(text, stdscr, y, x, color_pair=1):
    """
    Prints text to the screen one character at a time with a slight delay to create a typing effect (like hackers).
    """
    try:
        for i, char in enumerate(text):
            safe_addstr(stdscr, y, x + i, char, color_pair)
            stdscr.refresh()
            time.sleep(0.02)
    except curses.error:
        pass


def printasciigate(stdscr):
    """
    Displays an ASCII art gate indicating level completion.
    """
    try:
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))  # background color
        gateart = [
            "========================",
            "|        GATE          |",
            "|      UNLOCKED        |",
            "========================"
        ]
        max_y, max_x = stdscr.getmaxyx()
        start_y = (max_y - len(gateart)) // 2
        for i, line in enumerate(gateart):
            x_position = (max_x - len(line)) // 2
            safe_addstr(stdscr, start_y + i, x_position, line, 5)
        stdscr.refresh()
        time.sleep(2)
    except curses.error:
        pass  # ignore the error





def ensure_minimum_terminal_size(stdscr, min_rows, min_cols):
    """
    Ensures that the terminal window meets the minimum size requirements (different for each game).
    """
    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < min_rows or max_x < min_cols:
            stdscr.clear()
            safe_addstr(stdscr, 0, 0,
                        f"The terminal window is too small ({max_x}x{max_y}).",
                        color_pair=3)
            safe_addstr(stdscr, 1, 0,
                        f"Please resize it to at least {min_cols} columns "
                        f"and {min_rows} rows.", color_pair=3)
            safe_addstr(stdscr, 3, 0,
                        "After resizing, press any key to continue...",
                        color_pair=3)
            stdscr.refresh()
            stdscr.getch()
        else:
            break


def main_menu(stdscr):
    """
    Displays the main menu and handles user navigation.
    """
    curses.curs_set(0)  # Hide cursor

    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text color
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Selected menu item color
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Error messages color
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Additonal Color 
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success messages color
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # User input color

    # Set the background color for the entire screen
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.refresh()

    # Ensure the terminal size is above the minimum before proceeding
    ensure_minimum_terminal_size(stdscr, 24, 80)

    current_row = 0
    menu = ["Start Game", "Instructions", "Quit"]

    def print_menu(stdscr, selected_row):
        """
        Prints the main menu.
        """
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))  # set background color
        max_y, max_x = stdscr.getmaxyx()
        title = '''
         ▗▄▄▖ ▗▄▖ ▗▄▄▄ ▗▄▄▄▖    ▗▄▄▖ ▗▄▄▖ ▗▄▄▄▖ ▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▄▄▖ 
        ▐▌   ▐▌ ▐▌▐▌  █▐▌       ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌▗▞▘▐▌   ▐▌ ▐▌
        ▐▌   ▐▌ ▐▌▐▌  █▐▛▀▀▘    ▐▛▀▚▖▐▛▀▚▖▐▛▀▀▘▐▛▀▜▌▐▛▚▖ ▐▛▀▀▘▐▛▀▚▖
        ▝▚▄▄▖▝▚▄▞▘▐▙▄▄▀▐▙▄▄▖    ▐▙▄▞▘▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌
        '''
        title_lines = title.strip('\n').split('\n')
        for idx, line in enumerate(title_lines):
            safe_addstr(stdscr, 2 + idx, (max_x - len(line)) // 2, line, 5)
        for idx, row in enumerate(menu):
            x = (max_x - len(row)) // 2
            y = (max_y // 2) - len(menu) + idx * 2
            if idx == selected_row:
                safe_addstr(stdscr, y, x, row, 2)  # Highlight selected menu item
            else:
                safe_addstr(stdscr, y, x, row, 1)  # Default menu items
        stdscr.refresh()

    print_menu(stdscr, current_row)

    while True: # Handles navigation of main menu
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            ensure_minimum_terminal_size(stdscr, 24, 80)
            print_menu(stdscr, current_row)
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            print_menu(stdscr, current_row)
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
            print_menu(stdscr, current_row)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if current_row == 0:
                maingame(stdscr)
                print_menu(stdscr, current_row)
            elif current_row == 1:
                show_instructions(stdscr)
                print_menu(stdscr, current_row)
            elif current_row == 2:
                break
        else:
            pass  # Ignore other keys


def show_instructions(stdscr):
    """
    Displays game instructions to the player.
    """
    ensure_minimum_terminal_size(stdscr, 24, 80)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Sets background color
    instructions = [
        "Welcome to Code Breaker!",
        "You will be presented with a series of challenges to unlock code gates.",
        "You can type 'quit' at any input prompt to exit to the main menu.",
        "Navigate through the challenges and see how high you can score!",
        "Press any key to return to the main menu."
    ]

    max_y, max_x = stdscr.getmaxyx()
    for idx, line in enumerate(instructions):
        y = (max_y // 2 - len(instructions) // 2) + idx
        x = (max_x - len(line)) // 2
        safe_addstr(stdscr, y, x, line, 4)  # Use yellow color for instructions
    stdscr.refresh()
    stdscr.getch()


def get_user_input(stdscr, prompt_y, prompt_x, prompt_text, color_pair):
    """
    Prompts the user for input and returns the entered string.
    """
    curses.noecho()
    safe_move(stdscr, prompt_y, 0)
    stdscr.clrtoeol()  # Clear the line
    safe_addstr(stdscr, prompt_y, prompt_x, prompt_text, color_pair)
    stdscr.refresh()
    input_str = ''
    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            return None  # Continue to redraw
        elif c in [10, 13]:  # Enter key
            break
        elif c in [127, curses.KEY_BACKSPACE, curses.KEY_DC]:  # Backspace/Delete
            if len(input_str) > 0:
                input_str = input_str[:-1]
                y, x = stdscr.getyx()
                safe_move(stdscr, y, x - 1)
                stdscr.delch()
        else:
            try:
                input_char = chr(c)
                input_str += input_char
                safe_addstr(stdscr, stdscr.getyx()[0], stdscr.getyx()[1], input_char, 6)  
                stdscr.refresh()
            except curses.error:
                continue  # Ignore errors caused by window resizing (It will automatically reset anyways)
    return input_str.strip()


# by Aafeef
def scramble(stdscr):
    """
    Scramble game where the player must unscramble a given word.
    """
    ensure_minimum_terminal_size(stdscr, 10, 40)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    printslow("Scramble Game", stdscr, 1, 0, color_pair=1)
    printslow("Unscramble the letters to guess the correct word.",
              stdscr, 2, 0, color_pair=1)
    printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)

    word_file = "words.txt"
    try:
        with open(word_file, 'r') as f:
            WORDS = f.read().splitlines()
    except FileNotFoundError:
        WORDS = ["python", "hangman", "programming", "development",
                 "computer", "science"]  # Default words
        printslow("words.txt not found. Using default word list.", stdscr, 4, 0, 3)  # Red for error

    if not WORDS:
        WORDS = ["python", "hangman", "programming", "development",
                 "computer", "science"]  # Fallback if "words.txt" is doesnt display properly

    answer = random.choice(WORDS)
    scrambled = ''.join(random.sample(answer, len(answer)))

    printslow(f"Scrambled word: {scrambled}", stdscr, 5, 0, color_pair=2)  # Green for scrambled word

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 10 or max_x < 40:
            ensure_minimum_terminal_size(stdscr, 10, 40)
            stdscr.clear()
            stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
            printslow("Scramble Game", stdscr, 1, 0, color_pair=1)
            printslow("Unscramble the letters to guess the correct word.",
                      stdscr, 2, 0, color_pair=1)
            printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)
            printslow(f"Scrambled word: {scrambled}", stdscr, 5, 0, color_pair=2)
            continue
        try:
            user_input = get_user_input(stdscr, 7, 0, "Your guess: ", 4)
            if user_input is None:
                continue  # Handle resize
            if user_input.lower() == 'quit':
                return False  # Exit to main menu
            if user_input.lower() == answer.lower():
                printslow("Correct! The gate unlocks...", stdscr, 9, 0, color_pair=5)  # Green for success
                stdscr.refresh()
                time.sleep(2)
                printasciigate(stdscr)
                return True

            else:
                safe_addstr(stdscr, 9, 0, "Incorrect. Try again.", 3)  # Red for error
                global playerscore
                playerscore -= 5
                safe_move(stdscr, 7, len("Your guess: "))
                stdscr.clrtoeol()
        except curses.error:
            continue


def passwordguessing(stdscr):
    """
    Password guessing game where the player must crack a 3-digit password.
    """
    ensure_minimum_terminal_size(stdscr, 15, 60)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    printslow("Password Guessing Game", stdscr, 1, 0, color_pair=1)
    printslow("Crack the 3-digit password to unlock the gate.",
              stdscr, 2, 0, color_pair=1)
    printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)

    code_digits = [str(random.randint(1, 9)) for _ in range(3)]
    code = ''.join(code_digits)
    code_hint = ["*", "*", "*"]

    def check_guess(guess, code_hint):
        """
        Provides feedback on each digit of the guess.
        """
        feedback_y = 10
        for i, char in enumerate(guess):
            safe_move(stdscr, feedback_y + i, 0)
            stdscr.clrtoeol()
            if char == code[i]:
                code_hint[i] = char
                printslow(f"{char} is in the right position!", stdscr,
                          feedback_y + i, 0, color_pair=2)  # Green
            elif char in code:
                printslow(f"{char} is in the password but in the wrong position!", stdscr, feedback_y + i, 0,
                          color_pair=4)  # Yellow
            else:
                printslow(f"{char} is not in the password!", stdscr, feedback_y + i, 0, color_pair=3)  # Red
        return ''.join(code_hint)

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 15 or max_x < 60:
            ensure_minimum_terminal_size(stdscr, 15, 60)
            stdscr.clear()
            stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
            printslow("Password Guessing Game", stdscr, 1, 0, color_pair=1)
            printslow("Crack the 3-digit password to unlock the gate.",
                      stdscr, 2, 0, color_pair=1)
            printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)
            continue
        try:
            user_input = get_user_input(stdscr, 5, 0, "Enter your 3-digit guess: ", 4)
            if user_input is None:
                continue  # Handle resize 
            if user_input.lower() == 'quit':
                return False

            if user_input.isdigit() and len(user_input) == 3:
                if user_input == code:
                    safe_addstr(stdscr, 13, 0, "Password Correct! The gate unlocks...", 5)  # Green
                    stdscr.refresh()
                    printasciigate(stdscr)
                    return True
                else:
                    code_display = check_guess(user_input, code_hint)
                    safe_addstr(stdscr, 14, 0, f"Incorrect password! Try again! Known password so far: {code_display}",
                                3)  # Red
                    global playerscore
                    playerscore -= 5
            else:
                safe_addstr(stdscr, 6, 0, "Please enter a valid 3-digit number.", 3)  # Red
        except curses.error:
            continue


def numberguessing(stdscr):
    """
    Number guessing game where the player must guess a number between 1 and 100.
    """
    ensure_minimum_terminal_size(stdscr, 10, 40)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    printslow("Number Guessing Game", stdscr, 1, 0, color_pair=1)
    printslow("Guess a number between 1 and 100 to unlock the gate.",
              stdscr, 2, 0, color_pair=1)
    printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)

    answer = random.randint(1, 100)

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 10 or max_x < 40:
            ensure_minimum_terminal_size(stdscr, 10, 40)
            stdscr.clear()
            stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
            printslow("Number Guessing Game", stdscr, 1, 0, color_pair=1)
            printslow("Guess a number between 1 and 100 to unlock the gate.",
                      stdscr, 2, 0, color_pair=1)
            printslow("Type 'quit' to exit to the main menu.", stdscr, 3, 0, color_pair=1)
            continue
        try:
            user_input = get_user_input(stdscr, 5, 0, "Enter your guess: ", 4)
            if user_input is None:
                continue  # Handle resize
            if user_input.lower() == 'quit':
                return False

            if not user_input.isdigit():
                safe_addstr(stdscr, 7, 0, "Please enter a valid number.", 3)  # Red
                continue
            guess = int(user_input)
            if guess == answer:
                stdscr.clear()
                stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
                printslow("Correct! The gate unlocks...", stdscr, 8, 0, 5)  # Green
                printasciigate(stdscr)
                return True
            elif guess < answer:
                safe_addstr(stdscr, 7, 0, "Too low! Try again.", 3)  # Red

            else:
                safe_addstr(stdscr, 7, 0, "Too high! Try again.", 3)  # Red

        except curses.error:
            continue


# by Aafeef
def memorygame(stdscr):
    """
    Memory puzzle game where the player must match pairs of numbers.
    """

    def create_deck(): #creates a deck of card from (1-6) with all values repeated. So the list will be [1,2,3,4,5,6,1,2,3,4,5,6].
        deck = list(range(1, 7)) * 2
        random.shuffle(deck)
        return deck

    def display_board(stdscr, board, revealed): #this function prints the board
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
        safe_addstr(stdscr, 1, 0, "Memory Puzzle Game", 1)
        safe_addstr(stdscr, 2, 0, "Match pairs of numbers to unlock the gate.", 1)
        safe_addstr(stdscr, 3, 0, "Type 'quit' at any prompt to exit to the main menu.", 1)
        safe_addstr(stdscr, 5, 0, "Board:", 1)
        for i in range(3):
            row = ''
            for j in range(4):
                index = i * 4 + j
                if revealed[index]:
                    row += f"[{board[index]}] "
                else:
                    row += "[ ] "
            safe_addstr(stdscr, 6 + i, 0, row, 1)
        stdscr.refresh()

    def check_win(revealed): #check if all the elements in the revealed list is true
        return all(revealed)

    ensure_minimum_terminal_size(stdscr, 18, 40)
    board = create_deck()
    revealed = [False] * 12 # A list of 12 False, representing whether the card is revealed.

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 18 or max_x < 40:
            ensure_minimum_terminal_size(stdscr, 18, 40)
            continue
        try: #error handling
            display_board(stdscr, board, revealed)
            user_input1 = get_user_input(stdscr, 10, 0, "Choose the first card (1-12): ", 4)
            if user_input1 is None:
                continue  # Handle resize
            if user_input1.lower() == 'quit':
                return False

            user_input2 = get_user_input(stdscr, 11, 0, "Choose the second card (1-12): ", 4)
            if user_input2 is None:
                continue  # Handle resize
            if user_input2.lower() == 'quit':
                return False

            if not (user_input1.isdigit() and user_input2.isdigit()):
                safe_addstr(stdscr, 13, 0, "Invalid input! Please enter numbers between 1 and 12.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
                continue
            first_choice = int(user_input1) - 1
            second_choice = int(user_input2) - 1
            if first_choice < 0 or first_choice >= 12 or \
                    second_choice < 0 or second_choice >= 12:
                safe_addstr(stdscr, 13, 0, "Invalid card numbers! Choose between 1 and 12.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
                continue
            if first_choice == second_choice: 
                safe_addstr(stdscr, 13, 0, "You chose the same card twice. Try again.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
                continue
            if revealed[first_choice] or revealed[second_choice]:
                safe_addstr(stdscr, 13, 0, "One of the selected cards is already revealed. Try again.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
                continue
            revealed[first_choice] = True
            revealed[second_choice] = True
            display_board(stdscr, board, revealed)
            time.sleep(1)
            if board[first_choice] != board[second_choice]: #Checks whether the card matches 
                safe_addstr(stdscr, 13, 0, "No match! Cards will be hidden again.", 3)  # Red
                global playerscore
                playerscore -= 5
                stdscr.refresh()
                time.sleep(2)
                revealed[first_choice] = False
                revealed[second_choice] = False
            else:
                safe_addstr(stdscr, 13, 0, "It's a match!", 5)  # Green
                stdscr.refresh()
                time.sleep(2)
            if check_win(revealed):
                display_board(stdscr, board, revealed)
                safe_addstr(stdscr, 15, 0, "Congratulations! You've matched all pairs. The gate unlocks...", 5)  # Green
                stdscr.refresh()
                time.sleep(2)
                printasciigate(stdscr)
                return True
        except curses.error:
            continue

def hangman(stdscr):
    """
    Hangman game where the player must guess the hidden word one letter at a time.
    """

    def choose_word():
        words = ["python", "hangman", "programming", "development",
                 "computer", "science"]
        return random.choice(words)

    def display_hangman(stdscr, tries):
        stages = [
            """
               -----
               |   |
               |   O
               |  /|\\
               |  / \\
               -
            """,
            """
               -----
               |   |
               |   O
               |  /|\\
               |  /
               -
            """,
            """
               -----
               |   |
               |   O
               |  /|
               |
               -
            """,
            """
               -----
               |   |
               |   O
               |   |
               |
               -
            """,
            """
               -----
               |   |
               |   O
               |
               |
               -
            """,
            """
               -----
               |   |
               |
               |
               |
               -
            """,
            """
               -----
               |
               |
               |
               |
               -
            """
        ]
        hangman_drawing = stages[tries]
        lines = hangman_drawing.strip('\n').split('\n')
        for idx, line in enumerate(lines):
            safe_addstr(stdscr, 5 + idx, 0, line, 1)  # White text for hangman drawing
        stdscr.refresh()

    ensure_minimum_terminal_size(stdscr, 20, 60)
    word = choose_word()
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    word_completion = "_" * len(word)

    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    safe_addstr(stdscr, 1, 0, "Welcome to Hangman!", 1)
    safe_addstr(stdscr, 2, 0, "Try to guess the word, one letter at a time, or guess the full word.", 1)
    safe_addstr(stdscr, 3, 0, "Type 'quit' to exit to the main menu.", 1)
    display_hangman(stdscr, tries)
    safe_addstr(stdscr, 12, 0, f"{word_completion}", 2)  # Green for word completion
    stdscr.refresh()

    while not guessed and tries > 0:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 20 or max_x < 60:
            ensure_minimum_terminal_size(stdscr, 20, 60)
            stdscr.clear()
            stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
            safe_addstr(stdscr, 1, 0, "Welcome to Hangman!", 1)
            safe_addstr(stdscr, 2, 0, "Try to guess the word, one letter at a time, or guess the full word.", 1)
            safe_addstr(stdscr, 3, 0, "Type 'quit' to exit to the main menu.", 1)
            display_hangman(stdscr, tries)
            safe_addstr(stdscr, 12, 0, f"{word_completion}", 2)
            stdscr.refresh()
            continue
        try:
            user_input = get_user_input(stdscr, 14, 0, "Please guess a letter or word: ", 4)
            if user_input is None:
                continue  # Handle resize
            if user_input.lower() == 'quit':
                return False
            if len(user_input) == 1 and user_input.isalpha():
                if user_input in guessed_letters:
                    stdscr.move(16, 0)
                    stdscr.clrtoeol()  # Clear line 16 before writing
                    safe_addstr(stdscr, 16, 0, "You already guessed that letter.", 3)  # Red
                elif user_input not in word:
                    stdscr.move(16, 0)
                    stdscr.clrtoeol()  # Clear line 16 before writing
                    safe_addstr(stdscr, 16, 0, f"{user_input} is not in the word.", 3)  # Red
                    tries -= 1
                    guessed_letters.append(user_input)
                else:
                    stdscr.move(16, 0)
                    stdscr.clrtoeol()  # Clear line 16 before writing
                    safe_addstr(stdscr, 16, 0, f"Good job! {user_input} is in the word.", 5)  # Green
                    guessed_letters.append(user_input)
                    word_completion = "".join([letter if letter in guessed_letters else "_" for letter in word])
                    if "_" not in word_completion:
                        guessed = True
            elif len(user_input) == len(word) and user_input.isalpha():
                if user_input in guessed_words:
                    stdscr.move(16, 0)
                    stdscr.clrtoeol()  # Clear line 16 before writing
                    safe_addstr(stdscr, 16, 0, "You already guessed that word.", 3)  # Red
                elif user_input != word:
                    stdscr.move(16, 0)
                    stdscr.clrtoeol()  # Clear line 16 before writing
                    safe_addstr(stdscr, 16, 0, f"{user_input} is not the correct word.", 3)  # Red
                    tries -= 1
                    guessed_words.append(user_input)
                else:
                    guessed = True
                    word_completion = word
            else:
                stdscr.move(16, 0)
                stdscr.clrtoeol()  # Clear line 16 before writing
                safe_addstr(stdscr, 16, 0, "Invalid input. Please try again.", 3)  # Red
            stdscr.refresh()
            display_hangman(stdscr, tries)
            safe_addstr(stdscr, 12, 0, f"{word_completion}", 2)
            stdscr.refresh()
        except curses.error:
            continue
    if guessed:
        stdscr.move(18, 0)
        stdscr.clrtoeol()  # Clear line 18 before writing
        safe_addstr(stdscr, 18, 0, "Congratulations! You've guessed the word. The gate unlocks...", 5)  # Green
        stdscr.refresh()
        time.sleep(2)
        printasciigate(stdscr)
        return True
    else:
        stdscr.move(18, 0)
        stdscr.clrtoeol()  # clears line 18 before writing
        safe_addstr(stdscr, 18, 0, f"Sorry, you ran out of tries. The word was '{word}'.", 3)  # Red
        global playerscore
        playerscore -= 30 # decreases player's scores after losing
        stdscr.refresh()
        time.sleep(3)
        return True


def slidingblock(stdscr):
    """
    Sliding block puzzle game where the player must arrange numbers in order.
    """

    def count_inversions(tiles):
        inversion_count = 0
        tile_list = [tile for tile in tiles if tile != 0]
        for i in range(len(tile_list)):
            for j in range(i + 1, len(tile_list)):
                if tile_list[i] > tile_list[j]:
                    inversion_count += 1
        return inversion_count

    def shuffle_board():
        while True:
            tiles = [1, 2, 3, 4, 5, 0]
            random.shuffle(tiles)
            if count_inversions(tiles) % 2 == 0:
                row1 = tiles[:3]
                row2 = tiles[3:]
                return [row1, row2]

    def display_board(stdscr, board):
        safe_addstr(stdscr, 5, 0, '+-----+-----+-----+', 1)
        for i, row in enumerate(board):
            row_text = f'|{row[0] if row[0] != 0 else " ":^5}|{row[1] if row[1] != 0 else " ":^5}|{row[2] if row[2] != 0 else " ":^5}|'
            safe_addstr(stdscr, 6 + i * 2, 0, row_text, 1)
            safe_addstr(stdscr, 7 + i * 2, 0, '+-----+-----+-----+', 1)
        stdscr.refresh()

    def check_win(board):
        correct_board = [[1, 2, 3], [4, 5, 0]]
        return board == correct_board

    def find_empty_space(board):
        for i in range(2):
            for j in range(3):
                if board[i][j] == 0:
                    return i, j

    def is_valid_move(empty_pos, move):
        empty_x, empty_y = empty_pos
        move_x, move_y = move
        return 0 <= empty_x + move_x < 2 and 0 <= empty_y + move_y < 3

    def move_block(board, empty_pos, move):
        empty_x, empty_y = empty_pos
        move_x, move_y = move
        new_x, new_y = empty_x + move_x, empty_y + move_y
        board[empty_x][empty_y], board[new_x][new_y] = board[new_x][new_y], board[empty_x][empty_y]

    ensure_minimum_terminal_size(stdscr, 15, 40)
    board = shuffle_board()
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    safe_addstr(stdscr, 0, 0, "Sliding Block Puzzle", 1)
    safe_addstr(stdscr, 1, 0, "Arrange the numbers in order by moving the empty space.", 1)
    safe_addstr(stdscr, 2, 0, "Use W/A/S/D to move blocks up, left, down, and right.", 1)
    safe_addstr(stdscr, 3, 0, "Type 'R' to resign from the puzzle.", 1)
    safe_addstr(stdscr, 4, 0, "Type 'quit' to exit to the main menu.", 1)
    stdscr.refresh()

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 15 or max_x < 40:
            ensure_minimum_terminal_size(stdscr, 15, 40)
            stdscr.clear()
            stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
            safe_addstr(stdscr, 0, 0, "Sliding Block Puzzle", 1)
            safe_addstr(stdscr, 1, 0, "Arrange the numbers in order by moving the empty space.", 1)
            safe_addstr(stdscr, 2, 0, "Use W/A/S/D to move blocks up, left, down, and right.", 1)
            safe_addstr(stdscr, 3, 0, "Type 'R' to resign from the puzzle.", 1)
            safe_addstr(stdscr, 4, 0, "Type 'quit' to exit to the main menu.", 1)
            stdscr.refresh()
            continue
        try:
            display_board(stdscr, board)
            if check_win(board):
                safe_addstr(stdscr, 12, 0, "Congratulations! You solved the puzzle. The gate unlocks...", 5)  # Green
                stdscr.refresh()
                time.sleep(2)
                printasciigate(stdscr)
                return True
            user_input = get_user_input(stdscr, 10, 0, "Enter your move (W/A/S/D) or R to resign: ", 4)
            if user_input is None:
                continue  # Handle resize
            if user_input.lower() == 'quit':
                return False
            if user_input.upper() == 'R':
                global playerscore
                playerscore -= 30 # decreases player's scores after losing
                safe_addstr(stdscr, 12, 0, "You resigned.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
                break
            moves = {'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1)}
            if user_input.upper() in moves:
                empty_pos = find_empty_space(board)
                if is_valid_move(empty_pos, moves[user_input.upper()]):
                    move_block(board, empty_pos, moves[user_input.upper()])
                else:
                    safe_addstr(stdscr, 12, 0, "Invalid move. Try again!", 3)  # Red
                    stdscr.refresh()
                    time.sleep(2)
            else:
                safe_addstr(stdscr, 12, 0, "Invalid input. Please enter W/A/S/D or R.", 3)  # Red
                stdscr.refresh()
                time.sleep(2)
        except curses.error:
            continue


def maingame(stdscr):
    """
    Main game loop that navigates through different puzzle levels.
    """
    global playerscore
    playerscore = 100  # Score at the start of the game
    level = 1
    puzzles = [scramble, passwordguessing, numberguessing, memorygame, hangman, slidingblock]

    ensure_minimum_terminal_size(stdscr, 24, 80)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set the background color
    printslow("Welcome to Code Breaker: The Terminal Challenge!", stdscr, 0, 0, 5)  # Green
    printslow("You are a hacker attempting to bypass a series of virtual code gates.", stdscr, 1, 0, 5)  # Green

    while level <= len(puzzles):
        printslow(f"Level {level} - Get ready for the next challenge!", stdscr, 3, 0, 4)  # Yellow
        puzzle_solved = puzzles[level - 1](stdscr)
        if puzzle_solved:
            level += 1
            playerscore += 10
            if level > len(puzzles):
                continue
            while True:
                prompt_text = "Do you want to continue (Y/N)? "
                stdscr.clear()
                stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
                safe_addstr(stdscr, 10, 0, prompt_text, 1)  # White
                stdscr.refresh()
                curses.echo()
                curses.curs_set(1)
                try:
                    response_bytes = stdscr.getstr().decode().strip().lower()
                except UnicodeDecodeError:
                    response_bytes = ''
                curses.noecho()
                curses.curs_set(0)
                if response_bytes == 'y':
                    break
                elif response_bytes == 'n':
                    return
                else:
                    safe_addstr(stdscr, 11, 0, "Invalid input. Please enter 'y' or 'n'.", 3)  # Red
                    stdscr.refresh()
        else:
            break

    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color
    printslow("Thank you for playing Code Breaker: The Terminal Challenge!", stdscr, 2, 0, 5)  # Green
    printslow(f"Your Final Score: {playerscore}", stdscr, 3, 0, 2)  # Green
    stdscr.refresh()
    time.sleep(3)


if __name__ == "__main__":
    curses.wrapper(main_menu)

