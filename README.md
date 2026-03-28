# Chess by Mark
A two-player chess game built with Python and Pygame. Includes a full graphical interface with click-to-move controls, move highlighting, check/checkmate/stalemate detection, castling, and pawn promotion. 

<img width="300" height="300" alt="Screen Shot 2026-03-28 at 3 41 36 PM" src="https://github.com/user-attachments/assets/48506193-5e54-44e1-acb5-9865587c67d1" />


## Requirements 
- Python 3.10
- Pygame

## Project Structure
- chess_backend.py: main logic
- chess_gui.py: frontend by pygame (run this)
- constants.py: variables
- assets/images/*: piece and board images (pygame)

## Limitations
- Pawn promotion always promotes to queen, no piece choice
- No en passant moves
- No AI opponent, local two-player only
- No draw by repetition or 50-move rule

## Lessons learned
- Dictionary implementation
- Functions and parameters
- Graphical user interface with Pygame
- How to connect multiple files

Link to Shanon paper: https://vision.unipv.it/IA1/ProgrammingaComputerforPlayingChess.pdf
