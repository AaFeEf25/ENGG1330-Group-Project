# ENGG1330-Group-Project
The University of Hong Kong - ENGG1330 Project - Group E1-1 - Made by Ahmed Aafeef Ayman, Cai Yichen, Gu Kin Kwan, He Yujie, Khiami Jad &amp; Zhang Zhechuan


Code Breaker: The Terminal Challenge
====================================

Welcome to Code Breaker: The Terminal Challenge! This is a terminal-based game suite featuring multiple mini-games designed to test your problem-solving skills. The game is built using Python’s curses library, which enables an interactive and visually engaging experience directly in the terminal.

Table of Contents
-----------------
- Features
- Installation
- How to Run
- Game Mechanics
    - Main Menu
    - Mini-Games
- Controls
- Technical Overview
- Troubleshooting

Features
--------
- Engaging Gameplay: Choose from a variety of mini-games, each designed to be challenging and fun.
- Typing Effects and ASCII Art: Visual effects add atmosphere and immersion to the gameplay.
- Score Tracking: Track your score across different levels and games.
- User-Friendly Interface: Simple navigation through menus and games, suitable for both new and experienced players.

Installation
------------
To run this game, you'll need Python 3 and the curses library. The curses library is typically included with Python on Linux and macOS, but it may require additional installation on Windows.

For Windows:
1. Install Python 3. You can download it from https://www.python.org/downloads/.
2. Install the windows-curses package to support curses:
   pip install windows-curses

For Linux/macOS:
1. Ensure Python 3 is installed. It usually comes pre-installed on most Linux and macOS systems.
2. No additional setup is required for curses.

For EdStem:
1. Install the folder in a Ed Workspace
2. Open the terminal
3. Run the game by inserting the following command: "python {directory of main game file}"

How to Run
----------
Once the prerequisites are installed, follow these steps to run the game:

1. Clone this repository or download the game files.
2. Open a terminal in the directory containing the game files.
3. Run the game using the following command:
   python main.py

The game should start, displaying the main menu. Use the arrow keys to navigate, and press Enter to select options.

Game Mechanics
--------------
Main Menu
---------
The main menu provides three options:

1. Start Game: Begin a series of mini-games.
2. Instructions: View instructions on how to play the game.
3. Quit: Exit the game.

Mini-Games
----------
After selecting "Start Game," you’ll progress through a series of mini-games. Here’s an overview of each:

1. Scramble: Unscramble letters to guess a word.
2. Password Guessing: Guess a 3-digit code to unlock the gate.
3. Number Guessing: Guess a number between 1 and 100.
4. Memory Game: Match pairs of numbers in a memory-style game.
5. Hangman: Guess a hidden word letter by letter.
6. Sliding Block Puzzle: Arrange numbers in order by moving blocks around a 3x2 grid.

Each game contributes to the overall score, which is displayed at the end of the series.

Controls
--------
- Arrow Keys: Navigate through the main menu and other options.
- Enter: Select a highlighted menu item.
- Typing: Input text-based answers in games like Hangman, Scramble, and Password Guessing.
- W/A/S/D: Move blocks in the Sliding Block Puzzle.
- 'quit': Type 'quit' during a game to return to the main menu.

Technical Overview
------------------
The game is built using Python’s curses library, which allows for creating text-based user interfaces in the terminal.

Code Structure
--------------
- safe_addstr and safe_move: Functions to handle adding text and moving the cursor safely within the terminal bounds.
- Typing Effect (printslow): Provides a typing animation for added visual interest.
- Game Loop (maingame): Manages the overall gameplay flow, advancing from one mini-game to the next based on player progress.
- Score Tracking: A global playerscore variable keeps track of the player’s score across all mini-games.

Color Customization
-------------------
The game utilizes curses.init_pair to set up color schemes, enhancing the UI and distinguishing different text elements (e.g., errors in red, success in green).

Troubleshooting
---------------
- Text Overflow or Cut-off: If some text does not display correctly, try resizing your terminal window or maximizing it.
- Curses Error on Windows: Make sure to install windows-curses by running pip install windows-curses.
- Terminal Size Issues: The game checks for a minimum terminal size. If the terminal window is too small, a message will prompt you to resize.


Enjoy playing Code Breaker: The Terminal Challenge! Test your skills, solve puzzles, and break through the virtual gates to victory!
