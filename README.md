
# Catchup AI – Alpha-Beta Agent

Catchup is a two-player board game designed by Nick Bentley, played on a hexagonal grid of 61 cells (5 cells per side). The goal is to have the largest group of connected stones when the board is full.

Players take turns placing stones on empty cells. White places only one stone on the very first turn. After that, each player places one or two stones per turn. Stones are never captured or moved.

Catchup's special feature is its catch-up rule. If your opponent's largest group grew on their last turn and is now at least as big as yours, you may place up to three stones on your turn. So the closer you get to winning, the stronger your opponent becomes, and the game is as much about timing as about position.

The game ends when the board is full. The player with the largest group wins. If the largest groups are the same size, the second-largest groups are compared, and so on.

## About this project

This repository contains an AI agent that plays Catchup using **Alpha-Beta search** (minimax with alpha-beta pruning) at a search depth of 2. The catch-up rule is applied inside the search tree, so the agent knows when it or its opponent will get three stones.

**Enhancement:** the search uses *candidate cells*. Instead of trying every empty cell, it only considers empty cells next to an existing stone. This is a form of forward pruning. It greatly reduces the number of moves (in one test position, from 1711 to 91) and makes depth-2 search fast enough to play a full game in time.

**Evaluation function:** a position is scored as
`10 × (my largest group − opponent's largest group) + 1 × (my second-largest group − opponent's second-largest group)`.
The largest group decides the game. The second-largest group is a smaller bonus that matches the tie-break rule.

The project was developed for the Intelligent Search & Games course at Maastricht University.

## Files

- `board.py`: board, neighbors, groups, and scores
- `game.py`: move generation, the catch-up rule, and winner detection
- `alpha_beta_player.py`: evaluation functions and alpha-beta search
- `main.py`: play a game (human vs AI, AI plays either color)
- `experiment.py`: self-play experiments (candidate cells, depth, evaluation)

## How to run

Requires Python 3.10 (no extra packages).

    python main.py

On Windows you can also double-click `run.bat`. The program asks which color the AI plays (W or B).