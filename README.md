# Chess by Mark
A two-player chess game built with Python and Pygame. Includes a full graphical interface with click-to-move controls, move highlighting, check/checkmate/stalemate detection, castling, pawn promotion, and en passant. 

<img width="300" height="300" alt="Screenshot 2026-10-01 at 4 31 55 PM" src="https://github.com/user-attachments/assets/60f92d84-bcae-4dde-80f3-bd59c76056d1" />


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
- No draw by repetition or 50-move rule

## Lessons learned
- Dictionary implementation
- Functions and parameters
- Graphical user interface with Pygame
- How to connect multiple files

Link to Shanon paper: https://vision.unipv.it/IA1/ProgrammingaComputerforPlayingChess.pdf
