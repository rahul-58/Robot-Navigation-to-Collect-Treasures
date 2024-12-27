import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from collections import defaultdict
import heapq
from itertools import permutations

class TreasureHuntGame:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Treasure Hunt Game")
        self.master.geometry("1200x800")  # Fixed window size

        # Master grid configuration for centering everything
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=4)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=4)
        self.master.grid_columnconfigure(2, weight=1)

        # Instructions on the left (centered vertically and horizontally within column 0)
        self.instructions_label = tk.Label(
            self.master,
            text=(
                "Treasure Hunt Instructions:\n\n"
                "• Left-click on a node to add/remove treasures.\n"
                "• Left-click on edges to change weights.\n"
                "• Press 'Calculate Path' to find the optimal path.\n"
                "• Press 'Refresh Grid' to clear treasures and paths."
            ),
            font=("Arial", 12, "bold"),
            justify=tk.LEFT,
            wraplength=300
        )
        self.instructions_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", rowspan=2)

        # Main container for the grid and buttons (centered vertically and horizontally within column 1)
        self.main_frame = tk.Frame(self.master)
        self.main_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew", rowspan=1)

        # Grid display section (centered vertically and horizontally within column 1)
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.grid(row=0, column=0, padx=(0, 20))

        self.rows = 10
        self.cols = 10
        self.cell_size = 60

        self.canvas = tk.Canvas(self.grid_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        # Path and cost display on the right (centered vertically and horizontally within column 2)
        self.path_display_frame = tk.Frame(self.master)
        self.path_display_frame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

        self.path_label = tk.Label(self.path_display_frame, text="Optimal Path and Cost", font=("Arial", 14, "bold"))
        self.path_label.pack(pady=(20, 20))

        self.path_display = tk.Text(self.path_display_frame, height=15, width=40, state=tk.DISABLED, wrap='word')
        self.path_display.pack()

        # Buttons for controls at the bottom (centered below the grid)
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.grid(row=1, column=0, pady=10)

        self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
        self.recalculate_button.pack(side=tk.LEFT, padx=10)

        self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        # Placeholder for logic-related initialization
        self.graph = defaultdict(dict)
        self.treasures = {}
        self.start = 'A0'

        self.robot = None
        self.generate_random_grid()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)


    def update_path_display(self, cost, path):
        # Update the path display widget
        self.path_display.config(state=tk.NORMAL)
        self.path_display.delete(1.0, tk.END)  # Clear previous content
        self.path_display.insert(tk.END, f"Optimal Path Cost: {cost}\nPath: {path}")
        self.path_display.config(state=tk.DISABLED)  # Disable editing

        # Show a dialog box with the path and cost
        messagebox.showinfo("Optimal Path", f"Optimal Path Cost: {cost}\nPath: {path}")

    def refresh_grid(self):
        """Remove treasures and clear any existing path without resetting the edges or weights."""
        self.treasures = {}  # Clear all treasure values
        self.robot = None  # Clear any animated robot
        self.clear_path_display()  # Clear the path display
        self.draw_grid()  # Redraw the grid to remove treasures and paths

    def clear_path_display(self):
        """Clear the path display beside the grid."""
        self.path_display.config(state=tk.NORMAL)
        self.path_display.delete(1.0, tk.END)
        self.path_display.config(state=tk.DISABLED)

    def update_path_display(self, cost, path):
        """Display the path and cost beside the grid."""
        self.path_display.config(state=tk.NORMAL)
        self.path_display.delete(1.0, tk.END)
        self.path_display.insert(tk.END, f"Optimal Cost: {cost}\n")
        self.path_display.insert(tk.END, "Path:\n")
        self.path_display.insert(tk.END, " -> ".join(path))
        self.path_display.config(state=tk.DISABLED)

    def generate_random_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                node = f"{chr(ord('A') + i)}{j}"
                if j < self.cols - 1:
                    right_node = f"{chr(ord('A') + i)}{j+1}"
                    weight = random.randint(1, 20)
                    self.graph[node][right_node] = weight
                    self.graph[right_node][node] = weight
                if i < self.rows - 1:
                    down_node = f"{chr(ord('A') + i + 1)}{j}"
                    weight = random.randint(1, 20)
                    self.graph[node][down_node] = weight
                    self.graph[down_node][node] = weight

    def draw_grid(self):
        self.canvas.delete("all")
        # Draw dark background
        self.canvas.create_rectangle(0, 0, self.cols * self.cell_size, self.rows * self.cell_size, fill="#333333")

        # Draw grid lines
        for i in range(self.rows + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill="#444444")
        for j in range(self.cols + 1):
            x = j * self.cell_size
            self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill="#444444")

        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.cell_size
                y = i * self.cell_size
                node = f"{chr(ord('A') + i)}{j}"

                # Draw node circles with white fill
                self.canvas.create_oval(
                    x + 10, y + 10, x + self.cell_size - 10, y + self.cell_size - 10,
                    fill="white", outline="#ffffff"
                )
                self.canvas.create_text(
                    x + self.cell_size / 2, y + self.cell_size / 2,
                    text=node, font=("Arial", 10)
                )

                # Draw horizontal edges and weights
                if j < self.cols - 1:
                    right_node = f"{chr(ord('A') + i)}{j + 1}"
                    weight = self.graph[node][right_node]
                    self.canvas.create_line(
                        x + self.cell_size - 10, y + self.cell_size / 2,
                        x + self.cell_size + 10, y + self.cell_size / 2,
                        fill="red", width=2
                    )
                    self.canvas.create_text(
                        x + self.cell_size, y + self.cell_size / 2 - 10,
                        text=str(weight), font=("Arial", 10), fill="yellow"
                    )

                # Draw vertical edges and weights
                if i < self.rows - 1:
                    down_node = f"{chr(ord('A') + i + 1)}{j}"
                    weight = self.graph[node][down_node]
                    self.canvas.create_line(
                        x + self.cell_size / 2, y + self.cell_size - 10,
                        x + self.cell_size / 2, y + self.cell_size + 10,
                        fill="red", width=2
                    )
                    self.canvas.create_text(
                        x + self.cell_size / 2 + 10, y + self.cell_size,
                        text=str(weight), font=("Arial", 10), fill="yellow"
                    )

        # Draw treasures
        for node, value in self.treasures.items():
            i = ord(node[0]) - ord('A')
            j = int(node[1])
            x = j * self.cell_size
            y = i * self.cell_size
            self.canvas.create_oval(
                x + self.cell_size / 2 - 15, y + self.cell_size / 2 - 15,
                x + self.cell_size / 2 + 15, y + self.cell_size / 2 + 15,
                fill="#FFD700", outline="#B8860B"
            )
            self.canvas.create_text(
                x + self.cell_size / 2, y + self.cell_size / 2,
                text=f"💎{value}", fill="black", font=("Arial", 12, "bold")
            )
    
    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        node = f"{chr(ord('A') + row)}{col}"

        clicked_x = event.x
        clicked_y = event.y
        cell_center_x = col * self.cell_size + self.cell_size // 2
        cell_center_y = row * self.cell_size + self.cell_size // 2

        # Prioritize detecting edge clicks before detecting nodes
        for dx, dy, neighbor_offset in [(1, 0, (0, 1)), (0, 1, (1, 0))]:  # Horizontal and Vertical edges
            neighbor_i = row + neighbor_offset[0]
            neighbor_j = col + neighbor_offset[1]
            if 0 <= neighbor_i < self.rows and 0 <= neighbor_j < self.cols:
                neighbor_node = f"{chr(ord('A') + neighbor_i)}{neighbor_j}"

                if dx == 1:  # Horizontal edge
                    edge_start_x = col * self.cell_size + self.cell_size
                    edge_start_y = row * self.cell_size + self.cell_size // 2
                    if abs(clicked_x - edge_start_x) < self.cell_size // 4 and abs(clicked_y - edge_start_y) < self.cell_size // 4:
                        self.update_edge_weight(node, neighbor_node)
                        return

                if dy == 1:  # Vertical edge
                    edge_start_x = col * self.cell_size + self.cell_size // 2
                    edge_start_y = row * self.cell_size + self.cell_size
                    if abs(clicked_x - edge_start_x) < self.cell_size // 4 and abs(clicked_y - edge_start_y) < self.cell_size // 4:
                        self.update_edge_weight(node, neighbor_node)
                        return

        # Detect clicking on a node for treasures
        if abs(clicked_x - cell_center_x) < self.cell_size // 3 and abs(clicked_y - cell_center_y) < self.cell_size // 3:
            # Treasure toggle functionality
            if node in self.treasures:
                remove = messagebox.askyesno("Remove Treasure", f"Remove the treasure at {node}?")
                if remove:
                    del self.treasures[node]
                    self.draw_grid()
                return

            value = simpledialog.askinteger("Add Treasure", f"Enter treasure value for {node}:", minvalue=1)
            if value is not None:
                self.treasures[node] = value
                self.draw_grid()
    
    def update_edge_weight(self, node1, node2):
        """Prompt the user to update the weight of the edge between two nodes."""
        new_weight = simpledialog.askinteger(
            "Update Edge Weight",
            f"Enter new weight for edge {node1} -> {node2}:",
            minvalue=1
        )
        if new_weight is not None:
            self.graph[node1][node2] = new_weight
            self.graph[node2][node1] = new_weight
            self.draw_grid()
            # self.recalculate_path()

    
    def find_shortest_path(self, start, end):
        # Priority queue (min-heap)
        pq = [(0, start, [start])]  # (cost, node, path)
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            # If we reach the destination node, return the cost and path
            if node == end:
                return (cost, path)

            # If the node has already been visited, skip it
            if node in visited:
                continue
            visited.add(node)

            # Explore the neighbors of the current node
            for neighbor, weight in self.graph[node].items():
                if neighbor not in visited:
                    # Add the neighbor to the priority queue with updated cost
                    heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

        return None

    def find_shortest_treasure_route(self):
        pq = [(0, self.start, [self.start], set(), 0)]
        visited = {}
        best_path = (float('inf'), [])

        while pq:
            cost, node, path, collected_treasures, collected_value = heapq.heappop(pq)
            state_key = (node, frozenset(collected_treasures))

            if state_key in visited and visited[state_key] <= cost:
                continue

            visited[state_key] = cost

            if node == self.start and len(collected_treasures) == len(self.treasures):
                if cost < best_path[0]:
                    best_path = (cost, path)

            for next_node, edge_cost in self.graph[node].items():
                new_cost = cost + edge_cost
                new_collected_treasures = set(collected_treasures)
                new_collected_value = collected_value

                if next_node in self.treasures and next_node not in new_collected_treasures:
                    new_collected_treasures.add(next_node)
                    new_collected_value += self.treasures[next_node]

                new_path = path + [next_node]
                heapq.heappush(pq, (new_cost, next_node, new_path, new_collected_treasures, new_collected_value))

        return best_path
    
    def recalculate_path(self):
        use_brute_force = messagebox.askyesno("Algorithm Choice", "Use brute force algorithm?")
        
        if use_brute_force:
            cost, path = self.brute_force_shortest_treasure_route()
        else:
            cost, path = self.find_shortest_treasure_route()
        
        self.update_path_display(cost, path)
        self.animate_path(path)
    
    def brute_force_shortest_treasure_route(self):
        # List all treasures
        treasure_locations = list(self.treasures.keys())

        best_cost = float('inf')
        best_path = None

        # Generate all possible orders to visit treasures
        for perm in permutations(treasure_locations):
            current_path = [self.start]  # Start path at the starting node
            current_cost = 0
            valid_path = True

            # Calculate the path and cost for this permutation of treasures
            last_node = self.start  # Start from the starting node
            for treasure in perm:
                result = self.find_shortest_path(last_node, treasure)  # Shortest path from last node to current treasure
                if result is None:
                    valid_path = False
                    break
                cost, path = result
                current_cost += cost
                current_path.extend(path[1:])  # Avoid repeating the last node (last node is already in current_path)
                last_node = treasure  # Update the last node after collecting a treasure

            # After collecting all treasures, find the path back to start
            if valid_path:
                result = self.find_shortest_path(last_node, self.start)  # Shortest path back to start
                if result is not None:
                    cost, path = result
                    current_cost += cost
                    current_path.extend(path[1:])
                else:
                    valid_path = False

            # If valid path found and has a lower cost, update best path and cost
            if valid_path and current_cost < best_cost:
                best_cost = current_cost
                best_path = current_path

        return best_cost, best_path

    def animate_path(self, path):
        if self.robot:
            self.canvas.delete(self.robot)
        start_node = path[0]
        start_i, start_j = ord(start_node[0]) - ord('A'), int(start_node[1])
        start_x = start_j * self.cell_size + self.cell_size // 2
        start_y = start_i * self.cell_size + self.cell_size // 2
        self.robot = self.canvas.create_oval(start_x-10, start_y-10, start_x+10, start_y+10, fill="red")
        def move_robot(path_index):
            if path_index < len(path):
                current_node = path[path_index]
                i, j = ord(current_node[0]) - ord('A'), int(current_node[1])
                x = j * self.cell_size + self.cell_size // 2
                y = i * self.cell_size + self.cell_size // 2
                self.canvas.coords(self.robot, x-10, y-10, x+10, y+10)
                if path_index > 0:
                    prev_node = path[path_index - 1]
                    prev_i, prev_j = ord(prev_node[0]) - ord('A'), int(prev_node[1])
                    prev_x = prev_j * self.cell_size + self.cell_size // 2
                    prev_y = prev_i * self.cell_size + self.cell_size // 2
                    self.canvas.create_line(prev_x, prev_y, x, y, fill="blue", width=2, arrow=tk.LAST)
                self.master.after(500, move_robot, path_index + 1)
        move_robot(0)

def main():
    root = tk.Tk()
    game = TreasureHuntGame(root)
    root.mainloop()

main()