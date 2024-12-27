# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import random
# from collections import defaultdict
# import heapq

# class TreasureHuntGame:
#     def _init_(self, master):
#         self.master = master
#         self.master.title("Treasure Hunt Game")
        
#         self.rows = 10
#         self.cols = 10
#         self.cell_size = 60
        
#         self.graph = defaultdict(dict)
#         self.treasures = {}
#         self.start = 'A0'
        
#         self.canvas = tk.Canvas(master, width=self.cols*self.cell_size, height=self.rows*self.cell_size)
#         self.canvas.pack()
        
#         self.generate_random_grid()
#         self.draw_grid()
        
#         self.canvas.bind("<Button-1>", self.on_click)
        
#         self.recalculate_button = tk.Button(master, text="Recalculate Path", command=self.recalculate_path)
#         self.recalculate_button.pack()

#         self.robot = None

#     def generate_random_grid(self):
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 node = f"{chr(ord('A') + i)}{j}"
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][right_node] = weight
#                     self.graph[right_node][node] = weight
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][down_node] = weight
#                     self.graph[down_node][node] = weight

#     def draw_grid(self):
#         self.canvas.delete("all")
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 x = j * self.cell_size
#                 y = i * self.cell_size
#                 node = f"{chr(ord('A') + i)}{j}"
                
#                 # Draw node
#                 self.canvas.create_oval(x+5, y+5, x+self.cell_size-5, y+self.cell_size-5, fill="white")
#                 self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2, text=node, font=("Arial", 8))
                
#                 # Draw horizontal edges and weights
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = self.graph[node][right_node]
#                     self.canvas.create_line(x+self.cell_size, y+self.cell_size/2, x+self.cell_size+self.cell_size, y+self.cell_size/2)
#                     self.canvas.create_text(x+self.cell_size+self.cell_size/2, y+self.cell_size/2-10, text=str(weight), font=("Arial", 8), fill="red")
                
#                 # Draw vertical edges and weights
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = self.graph[node][down_node]
#                     self.canvas.create_line(x+self.cell_size/2, y+self.cell_size, x+self.cell_size/2, y+self.cell_size+self.cell_size)
#                     self.canvas.create_text(x+self.cell_size/2+10, y+self.cell_size+self.cell_size/2, text=str(weight), font=("Arial", 8), fill="red")
        
#         # Draw treasures
#         for node, value in self.treasures.items():
#             i = ord(node[0]) - ord('A')
#             j = int(node[1])
#             x = j * self.cell_size
#             y = i * self.cell_size
#             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2+15, text=f"💎{value}", fill="gold", font=("Arial", 10))


#     def on_click(self, event):
#         col = event.x // self.cell_size
#         row = event.y // self.cell_size
#         node = f"{chr(ord('A') + row)}{col}"
        
#         value = simpledialog.askinteger("Add Treasure", f"Enter treasure value for {node}:", minvalue=1)
#         if value is not None:
#             self.treasures[node] = value
#             self.draw_grid()

#     def find_shortest_treasure_route(self):
#         pq = [(0, self.start, [self.start], set(), 0)]
#         visited = {}
#         best_path = (float('inf'), [])

#         while pq:
#             cost, node, path, collected_treasures, collected_value = heapq.heappop(pq)
#             state_key = (node, frozenset(collected_treasures))

#             if state_key in visited and visited[state_key] <= cost:
#                 continue

#             visited[state_key] = cost

#             if node == self.start and len(collected_treasures) == len(self.treasures):
#                 if cost < best_path[0]:
#                     best_path = (cost, path)

#             for next_node, edge_cost in self.graph[node].items():
#                 new_cost = cost + edge_cost
#                 new_collected_treasures = set(collected_treasures)
#                 new_collected_value = collected_value

#                 if next_node in self.treasures and next_node not in new_collected_treasures:
#                     new_collected_treasures.add(next_node)
#                     new_collected_value += self.treasures[next_node]

#                 new_path = path + [next_node]
#                 heapq.heappush(pq, (new_cost, next_node, new_path, new_collected_treasures, new_collected_value))

#         return best_path

#     def recalculate_path(self):
#         cost, path = self.find_shortest_treasure_route()
#         self.draw_grid()  # Redraw the grid to clear previous paths
#         self.animate_path(path)
#         messagebox.showinfo("Path Found", f"Optimal cost: {cost}\nPath: {' -> '.join(path)}")

#     def animate_path(self, path):
#         if self.robot:
#             self.canvas.delete(self.robot)
        
#         start_node = path[0]
#         start_i, start_j = ord(start_node[0]) - ord('A'), int(start_node[1])
#         start_x = start_j * self.cell_size + self.cell_size // 2
#         start_y = start_i * self.cell_size + self.cell_size // 2
        
#         self.robot = self.canvas.create_oval(start_x-10, start_y-10, start_x+10, start_y+10, fill="red")
        
#         def move_robot(path_index):
#             if path_index < len(path):
#                 current_node = path[path_index]
#                 i, j = ord(current_node[0]) - ord('A'), int(current_node[1])
#                 x = j * self.cell_size + self.cell_size // 2
#                 y = i * self.cell_size + self.cell_size // 2
                
#                 self.canvas.coords(self.robot, x-10, y-10, x+10, y+10)
                
#                 if path_index > 0:
#                     prev_node = path[path_index - 1]
#                     prev_i, prev_j = ord(prev_node[0]) - ord('A'), int(prev_node[1])
#                     prev_x = prev_j * self.cell_size + self.cell_size // 2
#                     prev_y = prev_i * self.cell_size + self.cell_size // 2
#                     self.canvas.create_line(prev_x, prev_y, x, y, fill="blue", width=2, arrow=tk.LAST)
                
#                 self.master.after(500, move_robot, path_index + 1)
        
#         move_robot(0)

# def main():
#     root = tk.Tk()
#     game = TreasureHuntGame(root)
#     root.mainloop()

# # if _name_ == "_main_":
# main()

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import random
# from collections import defaultdict
# import heapq

# class TreasureHuntGame:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Treasure Hunt Game")
        
#         self.rows = 10
#         self.cols = 10
#         self.cell_size = 60
        
#         self.graph = defaultdict(dict)
#         self.treasures = {}
#         self.start = 'A0'
        
#         self.canvas = tk.Canvas(master, width=self.cols*self.cell_size, height=self.rows*self.cell_size)
#         self.canvas.pack()
        
#         self.generate_random_grid()
#         self.draw_grid()
        
#         self.canvas.bind("<Button-1>", self.on_click)
        
#         self.recalculate_button = tk.Button(master, text="Recalculate Path", command=self.recalculate_path)
#         self.recalculate_button.pack()

#         self.robot = None

#     def generate_random_grid(self):
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 node = f"{chr(ord('A') + i)}{j}"
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][right_node] = weight
#                     self.graph[right_node][node] = weight
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][down_node] = weight
#                     self.graph[down_node][node] = weight

#     def draw_grid(self):
#         self.canvas.delete("all")
#         # Draw dark background
#         self.canvas.create_rectangle(0, 0, self.cols*self.cell_size, self.rows*self.cell_size, 
#                                    fill="#333333")
        
#         # Draw grid lines
#         for i in range(self.rows + 1):
#             y = i * self.cell_size
#             self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill="#444444")
#         for j in range(self.cols + 1):
#             x = j * self.cell_size
#             self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill="#444444")
            
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 x = j * self.cell_size
#                 y = i * self.cell_size
#                 node = f"{chr(ord('A') + i)}{j}"
                
#                 # Draw white node circles
#                 self.canvas.create_oval(x+5, y+5, x+self.cell_size-5, y+self.cell_size-5, 
#                                      fill="white", outline="#ffffff")
#                 self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2, 
#                                      text=node, font=("Arial", 10))
                
#                 # Draw horizontal edges and weights in red
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = self.graph[node][right_node]
#                     # Draw weight on the grid line
#                     weight_x = x + self.cell_size
#                     weight_y = y + self.cell_size/2
#                     self.canvas.create_text(weight_x, weight_y,
#                                          text=str(weight),
#                                          font=("Arial", 10),
#                                          fill="#ff0000")
                
#                 # Draw vertical edges and weights in red
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = self.graph[node][down_node]
#                     # Draw weight on the grid line
#                     weight_x = x + self.cell_size/2
#                     weight_y = y + self.cell_size
#                     self.canvas.create_text(weight_x, weight_y,
#                                          text=str(weight),
#                                          font=("Arial", 10),
#                                          fill="#ff0000")
                
#         # Draw treasures
#         for node, value in self.treasures.items():
#             i = ord(node[0]) - ord('A')
#             j = int(node[1])
#             x = j * self.cell_size
#             y = i * self.cell_size
#             # Draw treasure with gold background
#             self.canvas.create_oval(x+self.cell_size/2-15, y+self.cell_size/2+5,
#                                  x+self.cell_size/2+15, y+self.cell_size/2+35,
#                                  fill="#FFD700")
#             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2+20,
#                                  text=f"💎{value}",
#                                  font=("Arial", 10))
        
#         # Draw treasures with improved visibility
#         for node, value in self.treasures.items():
#             i = ord(node[0]) - ord('A')
#             j = int(node[1])
#             x = j * self.cell_size
#             y = i * self.cell_size
#             # Draw treasure background
#             self.canvas.create_oval(x+self.cell_size/2-15, y+self.cell_size/2+5,
#                                  x+self.cell_size/2+15, y+self.cell_size/2+35,
#                                  fill="#FFD700", outline="#B8860B")
#             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2+20,
#                                  text=f"💎{value}",
#                                  fill="black",
#                                  font=("Arial", 10, "bold"))

#     def on_click(self, event):
#         col = event.x // self.cell_size
#         row = event.y // self.cell_size
#         node = f"{chr(ord('A') + row)}{col}"
        
#         value = simpledialog.askinteger("Add Treasure", f"Enter treasure value for {node}:", minvalue=1)
#         if value is not None:
#             self.treasures[node] = value
#             self.draw_grid()

#     def find_shortest_treasure_route(self):
#         pq = [(0, self.start, [self.start], set(), 0)]
#         visited = {}
#         best_path = (float('inf'), [])

#         while pq:
#             cost, node, path, collected_treasures, collected_value = heapq.heappop(pq)
#             state_key = (node, frozenset(collected_treasures))

#             if state_key in visited and visited[state_key] <= cost:
#                 continue

#             visited[state_key] = cost

#             if node == self.start and len(collected_treasures) == len(self.treasures):
#                 if cost < best_path[0]:
#                     best_path = (cost, path)

#             for next_node, edge_cost in self.graph[node].items():
#                 new_cost = cost + edge_cost
#                 new_collected_treasures = set(collected_treasures)
#                 new_collected_value = collected_value

#                 if next_node in self.treasures and next_node not in new_collected_treasures:
#                     new_collected_treasures.add(next_node)
#                     new_collected_value += self.treasures[next_node]

#                 new_path = path + [next_node]
#                 heapq.heappush(pq, (new_cost, next_node, new_path, new_collected_treasures, new_collected_value))

#         return best_path

#     def recalculate_path(self):
#         if not self.treasures:
#             messagebox.showinfo("Error", "Please add some treasures first by clicking on nodes!")
#             return
            
#         cost, path = self.find_shortest_treasure_route()
#         self.draw_grid()
#         self.animate_path(path)
#         messagebox.showinfo("Path Found", f"Optimal cost: {cost}\nPath: {' -> '.join(path)}")

#     def animate_path(self, path):
#         if self.robot:
#             self.canvas.delete(self.robot)
        
#         start_node = path[0]
#         start_i, start_j = ord(start_node[0]) - ord('A'), int(start_node[1])
#         start_x = start_j * self.cell_size + self.cell_size // 2
#         start_y = start_i * self.cell_size + self.cell_size // 2
        
#         self.robot = self.canvas.create_oval(start_x-10, start_y-10, start_x+10, start_y+10,
#                                           fill="#FF4444", outline="#CC0000", width=2)
        
#         def move_robot(path_index):
#             if path_index < len(path):
#                 current_node = path[path_index]
#                 i, j = ord(current_node[0]) - ord('A'), int(current_node[1])
#                 x = j * self.cell_size + self.cell_size // 2
#                 y = i * self.cell_size + self.cell_size // 2
                
#                 self.canvas.coords(self.robot, x-10, y-10, x+10, y+10)
                
#                 if path_index > 0:
#                     prev_node = path[path_index - 1]
#                     prev_i, prev_j = ord(prev_node[0]) - ord('A'), int(prev_node[1])
#                     prev_x = prev_j * self.cell_size + self.cell_size // 2
#                     prev_y = prev_i * self.cell_size + self.cell_size // 2
#                     self.canvas.create_line(prev_x, prev_y, x, y,
#                                          fill="#0066CC", width=3,
#                                          arrow=tk.LAST)
                
#                 self.master.after(500, move_robot, path_index + 1)
        
#         move_robot(0)

# def main():
#     root = tk.Tk()
#     game = TreasureHuntGame(root)
#     root.mainloop()

# # if _name_ == "_main_":
# main()


# import itertools
# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import random
# from collections import defaultdict
# import heapq
# from itertools import permutations

# class TreasureHuntGame:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Treasure Hunt Game")
        
#         self.rows = 10
#         self.cols = 10
#         self.cell_size = 60
        
#         self.graph = defaultdict(dict)
#         self.treasures = {}
#         self.start = 'A0'
        
#         self.canvas = tk.Canvas(master, width=self.cols*self.cell_size, height=self.rows*self.cell_size)
#         self.canvas.pack()
        
#         self.generate_random_grid()
#         self.draw_grid()
        
#         self.canvas.bind("<Button-1>", self.on_click)
        
#         self.recalculate_button = tk.Button(master, text="Recalculate Path", command=self.recalculate_path)
#         self.recalculate_button.pack()

#         self.refresh_button = tk.Button(master, text="Refresh Grid", command=self.refresh_grid)
#         self.refresh_button.pack()

#         self.robot = None
    
#     def refresh_grid(self):
#         """Remove treasures and clear any existing path without resetting the edges or weights."""
#         self.treasures = {}  # Clear all treasure values
#         self.robot = None  # Clear any animated robot
#         self.draw_grid()  # Redraw the grid to remove treasures and paths


#     def generate_random_grid(self):
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 node = f"{chr(ord('A') + i)}{j}"
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][right_node] = weight
#                     self.graph[right_node][node] = weight
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = random.randint(1, 20)
#                     self.graph[node][down_node] = weight
#                     self.graph[down_node][node] = weight

#     # def draw_grid(self):
#     #     self.canvas.delete("all")
#     #     for i in range(self.rows):
#     #         for j in range(self.cols):
#     #             x = j * self.cell_size
#     #             y = i * self.cell_size
#     #             node = f"{chr(ord('A') + i)}{j}"
                
#     #             # Draw node
#     #             self.canvas.create_oval(x+8, y+8, x+self.cell_size-5, y+self.cell_size-5, fill="white")
#     #             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2, text=node, font=("Arial", 20))
                
#     #             # Draw horizontal edges and weights
#     #             if j < self.cols - 1:
#     #                 right_node = f"{chr(ord('A') + i)}{j+1}"
#     #                 weight = self.graph[node][right_node]
#     #                 self.canvas.create_line(x+self.cell_size, y+self.cell_size/2, x+self.cell_size+self.cell_size, y+self.cell_size/2)
#     #                 self.canvas.create_text(x+self.cell_size+self.cell_size/2, y+self.cell_size/2, text=str(weight), font=("Arial", 20), fill="red")
                
#     #             # Draw vertical edges and weights
#     #             if i < self.rows - 1:
#     #                 down_node = f"{chr(ord('A') + i + 1)}{j}"
#     #                 weight = self.graph[node][down_node]
#     #                 self.canvas.create_line(x+self.cell_size/2, y+self.cell_size, x+self.cell_size/2, y+self.cell_size+self.cell_size)
#     #                 self.canvas.create_text(x+self.cell_size/2+10, y+self.cell_size+self.cell_size/2, text=str(weight), font=("Arial", 20), fill="red")
        
#     #     # Draw treasures
#     #     for node, value in self.treasures.items():
#     #         i = ord(node[0]) - ord('A')
#     #         j = int(node[1])
#     #         x = j * self.cell_size
#     #         y = i * self.cell_size
#     #         self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2, text=f"💎{value}", fill="red", font=("Times New Roman", 15))
                    
#     def draw_grid(self):
#         self.canvas.delete("all")
#         # Draw dark background
#         self.canvas.create_rectangle(0, 0, self.cols*self.cell_size, self.rows*self.cell_size, 
#                                    fill="#333333")
        
#         # Draw grid lines
#         for i in range(self.rows + 1):
#             y = i * self.cell_size
#             self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill="#444444")
#         for j in range(self.cols + 1):
#             x = j * self.cell_size
#             self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill="#444444")
            
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 x = j * self.cell_size
#                 y = i * self.cell_size
#                 node = f"{chr(ord('A') + i)}{j}"
                
#                 # Draw white node circles
#                 self.canvas.create_oval(x+5, y+5, x+self.cell_size-5, y+self.cell_size-5, 
#                                      fill="white", outline="#ffffff")
#                 self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2, 
#                                      text=node, font=("Arial", 10))
                
#                 # Draw horizontal edges and weights in red
#                 if j < self.cols - 1:
#                     right_node = f"{chr(ord('A') + i)}{j+1}"
#                     weight = self.graph[node][right_node]
#                     # Draw weight on the grid line
#                     weight_x = x + self.cell_size
#                     weight_y = y + self.cell_size/2
#                     self.canvas.create_text(weight_x, weight_y,
#                                          text=str(weight),
#                                          font=("Arial", 10),
#                                          fill="#ff0000")
                
#                 # Draw vertical edges and weights in red
#                 if i < self.rows - 1:
#                     down_node = f"{chr(ord('A') + i + 1)}{j}"
#                     weight = self.graph[node][down_node]
#                     # Draw weight on the grid line
#                     weight_x = x + self.cell_size/2
#                     weight_y = y + self.cell_size
#                     self.canvas.create_text(weight_x, weight_y,
#                                          text=str(weight),
#                                          font=("Arial", 10),
#                                          fill="#ff0000")
                
#         # Draw treasures
#         for node, value in self.treasures.items():
#             i = ord(node[0]) - ord('A')
#             j = int(node[1])
#             x = j * self.cell_size
#             y = i * self.cell_size
#             # Draw treasure with gold background
#             self.canvas.create_oval(x+self.cell_size/2-15, y+self.cell_size/2+5,
#                                  x+self.cell_size/2+15, y+self.cell_size/2+35,
#                                  fill="#FFD700")
#             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2+20,
#                                  text=f"💎{value}",
#                                  font=("Arial", 10))
        
#         # Draw treasures with improved visibility
#         for node, value in self.treasures.items():
#             i = ord(node[0]) - ord('A')
#             j = int(node[1])
#             x = j * self.cell_size
#             y = i * self.cell_size
#             # Draw treasure background
#             self.canvas.create_oval(x+self.cell_size/2-15, y+self.cell_size/2+5,
#                                  x+self.cell_size/2+15, y+self.cell_size/2+35,
#                                  fill="#FFD700", outline="#B8860B")
#             self.canvas.create_text(x+self.cell_size/2, y+self.cell_size/2+20,
#                                  text=f"💎{value}",
#                                  fill="black",
#                                  font=("Arial", 10, "bold"))

    





#     def on_click(self, event):
#         col = event.x // self.cell_size
#         row = event.y // self.cell_size
#         node = f"{chr(ord('A') + row)}{col}"
        
#         value = simpledialog.askinteger("Add Treasure", f"Enter treasure value for {node}:", minvalue=1)
#         if value is not None:
#             self.treasures[node] = value
#             self.draw_grid()
    
    
#     # def find_shortest_path(self, start, end):
#     #     queue = [(start, [start], 0)]
#     #     visited = set()

#     #     while queue:
#     #         (node, path, cost) = queue.pop(0)
#     #         if node not in visited:
#     #             visited.add(node)
#     #             if node == end:
#     #                 return (cost, path)
#     #             for neighbor, weight in self.graph[node].items():
#     #                 if neighbor not in visited:
#     #                     queue.append((neighbor, path + [neighbor], cost + weight))
#     #     return None

#     def find_shortest_path(self, start, end):
#         # Priority queue (min-heap)
#         pq = [(0, start, [start])]  # (cost, node, path)
#         visited = set()

#         while pq:
#             cost, node, path = heapq.heappop(pq)

#             # If we reach the destination node, return the cost and path
#             if node == end:
#                 return (cost, path)

#             # If the node has already been visited, skip it
#             if node in visited:
#                 continue
#             visited.add(node)

#             # Explore the neighbors of the current node
#             for neighbor, weight in self.graph[node].items():
#                 if neighbor not in visited:
#                     # Add the neighbor to the priority queue with updated cost
#                     heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

#         return None
    
#     # def brute_force_shortest_treasure_route(self):
#     #     from itertools import permutations

#     #     # List all treasures
#     #     treasure_locations = list(self.treasures.keys())

#     #     best_cost = float('inf')
#     #     best_path = None

#     #     # Generate all possible orders to visit treasures
#     #     for perm in permutations(treasure_locations):
#     #         # Start from the starting node
#     #         current_path = [self.start]
#     #         current_cost = 0
#     #         valid_path = True

#     #         # Path to the first treasure
#     #         for idx, treasure in enumerate(perm):
#     #             # Calculate shortest path to the treasure
#     #             result = self.find_shortest_path(current_path[-1], treasure)
#     #             if result is None:
#     #                 valid_path = False
#     #                 break

#     #             cost, path = result
#     #             current_cost += cost
#     #             current_path.extend(path[1:])  # Extend without duplicating start node of path

#     #         # After collecting all treasures, find path back to start
#     #         if valid_path:
#     #             result = self.find_shortest_path(current_path[-1], self.start)
#     #             if result is not None:
#     #                 cost, path = result
#     #                 current_cost += cost
#     #                 current_path.extend(path[1:])
#     #             else:
#     #                 valid_path = False

#     #         # If valid path found, update best cost and path
#     #         if valid_path and current_cost < best_cost:
#     #             best_cost = current_cost
#     #             best_path = current_path

#     #     return best_cost, best_path

#     def brute_force_shortest_treasure_route(self):
#         # List all treasures
#         treasure_locations = list(self.treasures.keys())

#         best_cost = float('inf')
#         best_path = None

#         # Generate all possible orders to visit treasures
#         for perm in permutations(treasure_locations):
#             current_path = [self.start]  # Start path at the starting node
#             current_cost = 0
#             valid_path = True

#             # Calculate the path and cost for this permutation of treasures
#             last_node = self.start  # Start from the starting node
#             for treasure in perm:
#                 result = self.find_shortest_path(last_node, treasure)  # Shortest path from last node to current treasure
#                 if result is None:
#                     valid_path = False
#                     break
#                 cost, path = result
#                 current_cost += cost
#                 current_path.extend(path[1:])  # Avoid repeating the last node (last node is already in current_path)
#                 last_node = treasure  # Update the last node after collecting a treasure

#             # After collecting all treasures, find the path back to start
#             if valid_path:
#                 result = self.find_shortest_path(last_node, self.start)  # Shortest path back to start
#                 if result is not None:
#                     cost, path = result
#                     current_cost += cost
#                     current_path.extend(path[1:])
#                 else:
#                     valid_path = False

#             # If valid path found and has a lower cost, update best path and cost
#             if valid_path and current_cost < best_cost:
#                 best_cost = current_cost
#                 best_path = current_path

#         return best_cost, best_path



#     def find_shortest_treasure_route(self):
#         pq = [(0, self.start, [self.start], set(), 0)]
#         visited = {}
#         best_path = (float('inf'), [])

#         while pq:
#             cost, node, path, collected_treasures, collected_value = heapq.heappop(pq)
#             state_key = (node, frozenset(collected_treasures))

#             if state_key in visited and visited[state_key] <= cost:
#                 continue

#             visited[state_key] = cost

#             if node == self.start and len(collected_treasures) == len(self.treasures):
#                 if cost < best_path[0]:
#                     best_path = (cost, path)

#             for next_node, edge_cost in self.graph[node].items():
#                 new_cost = cost + edge_cost
#                 new_collected_treasures = set(collected_treasures)
#                 new_collected_value = collected_value

#                 if next_node in self.treasures and next_node not in new_collected_treasures:
#                     new_collected_treasures.add(next_node)
#                     new_collected_value += self.treasures[next_node]

#                 new_path = path + [next_node]
#                 heapq.heappush(pq, (new_cost, next_node, new_path, new_collected_treasures, new_collected_value))

#         return best_path

#     def recalculate_path(self):
#         use_brute_force = messagebox.askyesno("Algorithm Choice", "Use brute force algorithm?")
        
#         if use_brute_force:
#             cost, path = self.brute_force_shortest_treasure_route()
#         else:
#             cost, path = self.find_shortest_treasure_route()
        
#         self.draw_grid()  # Redraw the grid to clear previous paths
#         self.animate_path(path)
#         messagebox.showinfo("Path Found", f"Optimal cost: {cost}\nPath: {' -> '.join(path)}")

#         # messagebox.showinfo("Path Found", f"Optimal cost: {cost}\nPath: {' -> '.join(path)}")

#     def animate_path(self, path):
#         if self.robot:
#             self.canvas.delete(self.robot)
        
#         start_node = path[0]
#         start_i, start_j = ord(start_node[0]) - ord('A'), int(start_node[1])
#         start_x = start_j * self.cell_size + self.cell_size // 2
#         start_y = start_i * self.cell_size + self.cell_size // 2
        
#         self.robot = self.canvas.create_oval(start_x-10, start_y-10, start_x+10, start_y+10, fill="red")
        
#         def move_robot(path_index):
#             if path_index < len(path):
#                 current_node = path[path_index]
#                 i, j = ord(current_node[0]) - ord('A'), int(current_node[1])
#                 x = j * self.cell_size + self.cell_size // 2
#                 y = i * self.cell_size + self.cell_size // 2
                
#                 self.canvas.coords(self.robot, x-10, y-10, x+10, y+10)
                
#                 if path_index > 0:
#                     prev_node = path[path_index - 1]
#                     prev_i, prev_j = ord(prev_node[0]) - ord('A'), int(prev_node[1])
#                     prev_x = prev_j * self.cell_size + self.cell_size // 2
#                     prev_y = prev_i * self.cell_size + self.cell_size // 2
#                     self.canvas.create_line(prev_x, prev_y, x, y, fill="blue", width=2, arrow=tk.LAST)
                
#                 self.master.after(500, move_robot, path_index + 1)
        
#         move_robot(0)

# def main():
#     root = tk.Tk()
#     game = TreasureHuntGame(root)
#     root.mainloop()

# # if _name_ == "_main_":
# main()


import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from collections import defaultdict
import heapq
from itertools import permutations

class TreasureHuntGame:
    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
        
    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60
        
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'
        
    #     self.canvas = tk.Canvas(master, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=5)  # Place canvas on the grid system
        
    #     # Panel for controls below the canvas
    #     self.controls_frame = tk.Frame(master)
    #     self.controls_frame.grid(row=5, column=0, pady=(10, 20))
        
    #     # Buttons
    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)
        
    #     # Panel to display the shortest path beside the grid
    #     self.path_display = tk.Text(master, width=40, height=25, state=tk.DISABLED, wrap=tk.WORD)
    #     self.path_display.grid(row=0, column=1, padx=10, pady=20, rowspan=5)

    #     self.robot = None
        
    #     self.generate_random_grid()
    #     self.draw_grid()
        
    #     self.canvas.bind("<Button-1>", self.on_click)

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
        
    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60
        
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'
        
    #     self.canvas = tk.Canvas(master, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.grid(row=0, column=1, padx=20, pady=20, rowspan=5)  # Adjusted column for placement of instructions
        
    #     # Instructions Panel
    #     self.instructions_frame = tk.Frame(master, width=200)
    #     self.instructions_frame.grid(row=0, column=0, padx=10, pady=20, sticky=tk.N)

    #     self.instructions_label = tk.Label(
    #         self.instructions_frame, 
    #         text="Instructions:\n\n"
    #              "- Left-click on a cell to add/remove treasures.\n"
    #              "- Click on an edge to update its weight.\n"
    #              "- Use 'Calculate Path' to find the shortest route.\n"
    #              "- Use 'Refresh Grid' to reset treasures.\n\n"
    #              "Legend:\n"
    #              "💎: Treasure\n"
    #              "Red Line: Edge with weight\n"
    #              "Blue Line: Path",
    #         justify=tk.LEFT, 
    #         anchor="w",
    #         wraplength=180
    #     )
    #     self.instructions_label.pack(side=tk.TOP, anchor="w", padx=5)

    #     # Panel for controls below the canvas
    #     self.controls_frame = tk.Frame(master)
    #     self.controls_frame.grid(row=5, column=1, pady=(10, 20))

    #     # Buttons
    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)

    #     # Panel to display the shortest path beside the grid
    #     self.path_display = tk.Text(master, width=40, height=25, state=tk.DISABLED, wrap=tk.WORD)
    #     self.path_display.grid(row=0, column=2, padx=10, pady=20, rowspan=5)

    #     self.robot = None
        
    #     self.generate_random_grid()
    #     self.draw_grid()
        
    #     self.canvas.bind("<Button-1>", self.on_click)

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
        
    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60
        
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'
        
    #     # Instructions Label
    #     self.instructions_label = tk.Label(
    #         master,
    #         text=(
    #             "How to Play:\n"
    #             "- Left-click on a node to add/remove treasures.\n"
    #             "- Left-click on edges to change weights.\n"
    #             "- Use 'Calculate Path' to find the optimal path.\n"
    #             "- Use 'Refresh Grid' to clear treasures and paths."
    #         ),
    #         font=("Arial", 12),
    #         justify=tk.LEFT,
    #         bg="lightblue",
    #         wraplength=600
    #     )
    #     self.instructions_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=20, sticky="n")

    #     # Canvas for grid
    #     self.canvas = tk.Canvas(master, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.grid(row=1, column=0, padx=20, pady=20, rowspan=5)  # Place canvas on the grid system
        
    #     # Panel for controls below the canvas
    #     self.controls_frame = tk.Frame(master)
    #     self.controls_frame.grid(row=6, column=0, pady=(10, 20))
        
    #     # Buttons
    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)
        
    #     # Panel to display the shortest path beside the grid
    #     self.path_display = tk.Text(master, width=40, height=25, state=tk.DISABLED, wrap=tk.WORD)
    #     self.path_display.grid(row=1, column=1, padx=10, pady=20, rowspan=5)

    #     self.robot = None
        
    #     self.generate_random_grid()
    #     self.draw_grid()
        
    #     self.canvas.bind("<Button-1>", self.on_click)

    
    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
    #     self.master.geometry("900x800")  # Set the window size

    #     # Main container for centering content
    #     self.container = tk.Frame(self.master)
    #     self.container.pack(expand=True, fill='both')

    #     # Instructions
    #     self.instructions_label = tk.Label(
    #         self.container,
    #         text=(
    #             "Treasure Hunt Instructions:\n\n"
    #             "• Left-click on a node to add/remove treasures.\n"
    #             "• Left-click on edges to change weights.\n"
    #             "• Press 'Calculate Path' to find the optimal path.\n"
    #             "• Press 'Refresh Grid' to clear treasures and paths."
    #         ),
    #         font=("Arial", 12, "bold"),
    #         justify=tk.LEFT,
    #         wraplength=800
    #     )
    #     self.instructions_label.pack(pady=(10, 20))  # Add padding around instructions

    #     # Game Grid Canvas
    #     self.canvas_frame = tk.Frame(self.container)
    #     self.canvas_frame.pack(pady=(10, 20))  # Add vertical padding

    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60

    #     self.canvas = tk.Canvas(self.canvas_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.pack()

    #     # Buttons for controls
    #     self.controls_frame = tk.Frame(self.container)
    #     self.controls_frame.pack(pady=(10, 20))

    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)

    #     # Display for path and cost
    #     self.path_display = tk.Text(self.container, height=5, width=80, state=tk.DISABLED, wrap='word')
    #     self.path_display.pack(pady=(10, 20))

    #     # Placeholder for logic-related initialization
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'

    #     self.robot = None
    #     self.generate_random_grid()
    #     self.draw_grid()
    #     self.canvas.bind("<Button-1>", self.on_click)

    # def update_path_display(self, cost, path):
    #     # Update the path display widget
    #     self.path_display.config(state=tk.NORMAL)
    #     self.path_display.delete(1.0, tk.END)  # Clear previous content
    #     self.path_display.insert(tk.END, f"Optimal Path Cost: {cost}\nPath: {path}")
    #     self.path_display.config(state=tk.DISABLED)  # Disable editing

    #     # Show a dialog box with the path and cost
    #     messagebox.showinfo("Optimal Path", f"Optimal Path Cost: {cost}\nPath: {path}")

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
    #     self.master.geometry("1200x800")  # Adjust window size to accommodate grid and display

    #     # Main container for centering content
    #     self.container = tk.Frame(self.master)
    #     self.container.pack(expand=True, fill='both')

    #     # Instructions
    #     self.instructions_label = tk.Label(
    #         self.container,
    #         text=(
    #             "Treasure Hunt Instructions:\n\n"
    #             "• Left-click on a node to add/remove treasures.\n"
    #             "• Left-click on edges to change weights.\n"
    #             "• Press 'Calculate Path' to find the optimal path.\n"
    #             "• Press 'Refresh Grid' to clear treasures and paths."
    #         ),
    #         font=("Arial", 12, "bold"),
    #         justify=tk.LEFT,
    #         wraplength=800
    #     )
    #     self.instructions_label.pack(pady=(10, 20))  # Add padding around instructions

    #     # Main grid and display frame
    #     self.grid_display_frame = tk.Frame(self.container)
    #     self.grid_display_frame.pack(pady=(10, 20), fill='both', expand=True)

    #     # Game Grid Canvas
    #     self.canvas_frame = tk.Frame(self.grid_display_frame)
    #     self.canvas_frame.pack(side=tk.LEFT, padx=20)

    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60

    #     self.canvas = tk.Canvas(self.canvas_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.pack()

    #     # Path and cost display
    #     self.path_display_frame = tk.Frame(self.grid_display_frame)
    #     self.path_display_frame.pack(side=tk.LEFT, padx=20, fill='y')

    #     self.path_label = tk.Label(self.path_display_frame, text="Optimal Path and Cost", font=("Arial", 14, "bold"))
    #     self.path_label.pack(pady=(0, 10))

    #     self.path_display = tk.Text(self.path_display_frame, height=15, width=40, state=tk.DISABLED, wrap='word')
    #     self.path_display.pack()

    #     # Buttons for controls
    #     self.controls_frame = tk.Frame(self.container)
    #     self.controls_frame.pack(pady=(10, 20))

    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)

    #     # Placeholder for logic-related initialization
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'

    #     self.robot = None
    #     self.generate_random_grid()
    #     self.draw_grid()
    #     self.canvas.bind("<Button-1>", self.on_click)

    # def update_path_display(self, cost, path):
    #     # Update the path display widget
    #     self.path_display.config(state=tk.NORMAL)
    #     self.path_display.delete(1.0, tk.END)  # Clear previous content
    #     self.path_display.insert(tk.END, f"Optimal Path Cost: {cost}\nPath: {path}")
    #     self.path_display.config(state=tk.DISABLED)  # Disable editing

    #     # Show a dialog box with the path and cost
    #     messagebox.showinfo("Optimal Path", f"Optimal Path Cost: {cost}\nPath: {path}")

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
    #     self.master.geometry("1200x800")  # Fixed window size

    #     # Master grid configuration for center alignment
    #     self.master.grid_rowconfigure(0, weight=1)
    #     self.master.grid_columnconfigure(0, weight=1)

    #     # Main container for all elements
    #     self.container = tk.Frame(self.master)
    #     self.container.grid(row=0, column=0)

    #     # Instructions at the top
    #     self.instructions_label = tk.Label(
    #         self.container,
    #         text=(
    #             "Treasure Hunt Instructions:\n\n"
    #             "• Left-click on a node to add/remove treasures.\n"
    #             "• Left-click on edges to change weights.\n"
    #             "• Press 'Calculate Path' to find the optimal path.\n"
    #             "• Press 'Refresh Grid' to clear treasures and paths."
    #         ),
    #         font=("Arial", 12, "bold"),
    #         justify=tk.LEFT,
    #         wraplength=800
    #     )
    #     self.instructions_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    #     # Main grid frame for the game grid and path display
    #     self.main_frame = tk.Frame(self.container)
    #     self.main_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    #     # Grid display section
    #     self.grid_frame = tk.Frame(self.main_frame)
    #     self.grid_frame.grid(row=0, column=0, padx=(0, 20))

    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60

    #     self.canvas = tk.Canvas(self.grid_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.pack()

    #     # Path and cost display on the right
    #     self.path_display_frame = tk.Frame(self.main_frame)
    #     self.path_display_frame.grid(row=0, column=1, padx=20)

    #     self.path_label = tk.Label(self.path_display_frame, text="Optimal Path and Cost", font=("Arial", 14, "bold"))
    #     self.path_label.pack(pady=(0, 10))

    #     self.path_display = tk.Text(self.path_display_frame, height=15, width=40, state=tk.DISABLED, wrap='word')
    #     self.path_display.pack()

    #     # Buttons for controls at the bottom
    #     self.controls_frame = tk.Frame(self.container)
    #     self.controls_frame.grid(row=2, column=0, columnspan=2, pady=10)

    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)

    #     # Placeholder for logic-related initialization
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'

    #     self.robot = None
    #     self.generate_random_grid()
    #     self.draw_grid()
    #     self.canvas.bind("<Button-1>", self.on_click)

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Treasure Hunt Game")
    #     self.master.geometry("1200x800")  # Fixed window size

    #     # Master grid configuration for center alignment
    #     self.master.grid_rowconfigure(0, weight=1)
    #     self.master.grid_columnconfigure(0, weight=1)

    #     # Main container for all elements (centered)
    #     self.container = tk.Frame(self.master)
    #     self.container.grid(row=0, column=0)

    #     # Instructions at the top
    #     self.instructions_label = tk.Label(
    #         self.container,
    #         text=(
    #             "Treasure Hunt Instructions:\n\n"
    #             "• Left-click on a node to add/remove treasures.\n"
    #             "• Left-click on edges to change weights.\n"
    #             "• Press 'Calculate Path' to find the optimal path.\n"
    #             "• Press 'Refresh Grid' to clear treasures and paths."
    #         ),
    #         font=("Arial", 12, "bold"),
    #         justify=tk.LEFT,
    #         wraplength=800
    #     )
    #     self.instructions_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    #     # Main grid frame for the game grid and path display
    #     self.main_frame = tk.Frame(self.container)
    #     self.main_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    #     # Grid display section
    #     self.grid_frame = tk.Frame(self.main_frame)
    #     self.grid_frame.grid(row=0, column=0, padx=(0, 20))

    #     self.rows = 10
    #     self.cols = 10
    #     self.cell_size = 60

    #     self.canvas = tk.Canvas(self.grid_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
    #     self.canvas.pack()

    #     # Path and cost display on the right (side by side with grid)
    #     self.path_display_frame = tk.Frame(self.main_frame)
    #     self.path_display_frame.grid(row=0, column=1, padx=20)

    #     self.path_label = tk.Label(self.path_display_frame, text="Optimal Path and Cost", font=("Arial", 14, "bold"))
    #     self.path_label.pack(pady=(0, 10))

    #     self.path_display = tk.Text(self.path_display_frame, height=15, width=40, state=tk.DISABLED, wrap='word')
    #     self.path_display.pack()

    #     # Buttons for controls at the bottom (centered under the grid)
    #     self.controls_frame = tk.Frame(self.container)
    #     self.controls_frame.grid(row=2, column=0, columnspan=2, pady=10)

    #     self.recalculate_button = tk.Button(self.controls_frame, text="Calculate Path", command=self.recalculate_path)
    #     self.recalculate_button.pack(side=tk.LEFT, padx=10)

    #     self.refresh_button = tk.Button(self.controls_frame, text="Refresh Grid", command=self.refresh_grid)
    #     self.refresh_button.pack(side=tk.LEFT, padx=10)

    #     # Placeholder for logic-related initialization
    #     self.graph = defaultdict(dict)
    #     self.treasures = {}
    #     self.start = 'A0'

    #     self.robot = None
    #     self.generate_random_grid()
    #     self.draw_grid()
    #     self.canvas.bind("<Button-1>", self.on_click)

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

    # def on_click(self, event):
    #     col = event.x // self.cell_size
    #     row = event.y // self.cell_size
    #     node = f"{chr(ord('A') + row)}{col}"

    #     # Check if there's already a treasure at the clicked node
    #     if node in self.treasures:
    #         # Confirm removal of treasure
    #         remove = messagebox.askyesno("Remove Treasure", f"Remove the treasure at {node}?")
    #         if remove:
    #             del self.treasures[node]  # Remove the treasure
    #             self.draw_grid()  # Redraw the grid
    #         return

    #     # If no treasure exists, allow adding a treasure
    #     value = simpledialog.askinteger("Add Treasure", f"Enter treasure value for {node}:", minvalue=1)
    #     if value is not None:
    #         self.treasures[node] = value
    #         self.draw_grid()
    
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