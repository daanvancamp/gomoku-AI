# Gomoku-AI

A sophisticated implementation of the Gomoku (Five in a Row) game with artificial intelligence and webcam support for physical game boards. The updated recognition system is integrated into this project, while the original version can be found at: https://github.com/daanvancamp/five_in_a_row_recognition

## Development Timeline

### June 2024
- Initiated webcam support integration

### July 2024
- **Optimized neural network by switching from Adam to SGD optimizer**
- **Fixed exploration phase bug during training by implementing random move selection after 30 attempts (occurs ~0.1% of the time)**
- Modernized GUI interface
- Enhanced function stability through exception handling
- Eliminated duplicate functions in filereader.py
- **Implemented dynamic learning rate adjustment (0.9999x decrease per training round) for more refined pattern recognition**
- **Added model overruling system for critical game situations:**
  - Prevents losses from opponent's four-in-a-row with open end
  - Blocks three-in-a-row with two open ends
  - Optimizes move selection through valid cell filtering
  - Features GUI toggle and detailed move logging
- Added board hover effects for improved user experience
- Implemented human vs DVC-AI training mode
- Highlighted AI's latest move in red
- **Enabled multiple model training capability**
- Added webcam recognition toggle
- Integrated situation loading into gameplay
- Converted file-based globals to true global variables
- Expanded test scenarios database

### August 2024
- Restructured codebase with three distinct game functions
- **Implemented per-player overruling options**
- **Added crash prevention through option hiding**
- Split game function into runreplay, rungame, and runtraining
- **Released version 0.1**
- Added music toggle feature
- Optimized code structure (reduced gomoku.py by 200 lines)
- **Fixed critical gameplay exploit involving edge-to-center strategy**
- **Major stability improvements to prevent GUI crashes**
- **Released version 1.0**
- Enhanced UI with grayed-out elements
- Added model statistics module
- **Released version 1.1**
- Expanded model statistics
- Fixed model deletion crashes
- **Released version 1.2**
- Integrated Pygame window into fullscreen Tkinter interface
- **Released version 1.3**
- Added optional training graphs
- Implemented various stability improvements
- **Released version 1.4**
- Integrated webcam recognition system
- Restructured GUI and recognition modules
- Implemented fullscreen menu system
- **Concluded initial design phase**

### September-December 2024 and Beyond
- **Complete codebase redesign using MVC architecture**
- Enhanced feature restoration
- Implemented new fullscreen interface
- Perfected webcam recognition under proper lighting conditions

## Current Status
No known issues at present.

## Developers
- Daan Van Camp
- Wim Nevelsteen
