Treasure Hunt Game

Overview
This repository contains the Treasure Hunt Game, a grid-based interactive game implemented using Python's Tkinter library. Players can set treasures, adjust edge weights, and calculate the optimal path for collecting all treasures with minimal cost. The game supports both brute force and heuristic-based algorithms for pathfinding.

Features

Interactive Grid:
Click on nodes to add or remove treasures.
Click on edges to modify their weights.

Pathfinding:
Calculate the optimal treasure-collecting path using either:
A heuristic algorithm.
A brute force approach (evaluates all permutations of treasure paths).

Visualization:
View the grid with treasures, edges, and weights.
Animated robot follows the calculated path.

Customization:
Randomized grid generation.
Flexible grid size and edge weights.

Requirements

Python 3.8+
Tkinter (bundled with most Python distributions)

Installation

Clone the repository:
git clone https://github.com/your-username/treasure-hunt-game.git
cd treasure-hunt-game

Run the script:
python treasure_hunt_game.py

How to Play

Grid Basics:
The grid is a 10x10 matrix where nodes represent points connected by weighted edges.
Treasures can be placed at nodes, and their values determine the priority of collection.
Adding/Removing Treasures:

Left-click on a node:
If empty, a dialog prompts for the treasure value.
If occupied, a confirmation dialog allows treasure removal.

Updating Edge Weights:
Left-click near an edge to modify its weight.

Calculating the Path:
Press Calculate Path to find the optimal path for collecting all treasures.
Choose between brute force or heuristic algorithms when prompted.

Resetting the Grid:
Press Refresh Grid to clear all treasures and reset the display.

Algorithms

1. Heuristic Algorithm
Uses a priority queue to find the shortest path while collecting treasures.
Balances performance and accuracy for larger grids.

2. Brute Force Algorithm
Evaluates all permutations of treasure paths to find the most cost-efficient route.
Suitable for smaller grids due to exponential complexity.

Code Structure

Grid Setup:
Randomly generates nodes, edges, and weights during initialization.

Pathfinding:
find_shortest_path(): Calculates the shortest path between two nodes using Dijkstra's algorithm.
find_shortest_treasure_route(): Finds the optimal treasure-collecting path using the heuristic approach.
brute_force_shortest_treasure_route(): Exhaustively evaluates all possible treasure-collecting paths.

User Interaction:
on_click(): Handles mouse clicks to add treasures or modify edge weights.
recalculate_path(): Triggers the pathfinding algorithms based on user input.

Visualization:
Draws the grid, treasures, and paths dynamically.
Animates the robot's movement along the calculated path.

Future Enhancements
Add more algorithms for pathfinding.
Support larger grid sizes with dynamic scaling.
Introduce additional game mechanics like obstacles or multiple robots.

Author
Rahul Reddy 
Connect on LinkedIn
