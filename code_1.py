import tkinter as tk

class MazeSolverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Solver")

        self.rows_entry = tk.Entry(master)
        self.rows_entry.grid(row=0, column=0, padx=5, pady=5)
        tk.Label(master, text="Rows:").grid(row=0, column=1, padx=5, pady=5)

        self.cols_entry = tk.Entry(master)
        self.cols_entry.grid(row=1, column=0, padx=5, pady=5)
        tk.Label(master, text="Columns:").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="Create Maze:").grid(row=2, column=0, columnspan=2, pady=5)

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.grid(row=3, column=0, columnspan=2)

        self.start_button = tk.Button(master, text="Start", command=self.create_maze)
        self.start_button.grid(row=4, column=0, pady=10)

        self.solve_button = tk.Button(master, text="Solve", command=self.solve_maze)
        self.solve_button.grid(row=4, column=1, pady=10)

        # Initialize maze variables
        self.rows = 0
        self.cols = 0
        self.cell_size = 0
        self.maze = {}
        self.start_cell = None
        self.end_cell = None
        self.wall_cells = set()

        # Bind events to canvas
        self.canvas.bind("<Button-1>", self.on_cell_click)

    def create_maze(self):
        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())
        self.cell_size = 400 / max(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                self.maze[(i, j)] = {'cell_id': cell_id, 'type': 'empty'}

    def solve_maze(self):
        # self.reset_maze()

        # Find and show the path using DFS
        path = self.dfs(self.start_cell, self.end_cell)

        # Add numbers to the cells in the order they are traversed
        step_count = 1
        for cell in path:
            cell_info = self.maze[cell]
            if cell_info['type'] != 'wall':
                x1, y1, x2, y2 = self.canvas.coords(cell_info['cell_id'])
                cell_center_x = (x1 + x2) / 2
                cell_center_y = (y1 + y2) / 2
                if cell_info['type'] == 'start_cell':
                    self.canvas.itemconfig(cell_info['cell_id'], fill="green")
                elif cell_info['type'] == 'end_cell':
                    self.canvas.itemconfig(cell_info['cell_id'], fill="red")
                else:
                    self.canvas.itemconfig(cell_info['cell_id'], fill="blue")
                self.canvas.create_text(
                    cell_center_x,
                    cell_center_y,
                    text=str(step_count),
                    fill="white"
                )
                step_count += 1

    def dfs(self, start, end):
        stack = [(start, [start])]
        while stack:
            (current_cell, path) = stack.pop()
            for neighbor in self.get_neighbors(current_cell):
                if neighbor not in path and self.maze[neighbor]['type'] != 'wall':
                    if neighbor == end:
                        return path + [neighbor]
                    else:
                        stack.append((neighbor, path + [neighbor]))
        return []

    def get_neighbors(self, cell):
        if cell is None:
            return [] 
        
        row, col = cell

        neighbors = []

        # Check above cell
        if row > 0:
            neighbors.append((row - 1, col))

        # Check below cell
        if row < self.rows - 1:
            neighbors.append((row + 1, col))

        # Check left cell
        if col > 0:
            neighbors.append((row, col - 1))

        # Check right cell
        if col < self.cols - 1:
            neighbors.append((row, col + 1))

        return neighbors

    def on_cell_click(self, event):
        cell = self.get_clicked_cell(event)
        if not self.start_cell:
            self.start_cell = cell
            self.canvas.itemconfig(self.maze[cell]['cell_id'], fill="green")
            self.maze[cell]['type'] = 'start_cell'
        elif not self.end_cell:
            self.end_cell = cell
            self.canvas.itemconfig(self.maze[cell]['cell_id'], fill="red")
            self.maze[cell]['type'] = 'end_cell'
        else:
            if cell not in self.wall_cells:
                self.wall_cells.add(cell)
                self.canvas.itemconfig(self.maze[cell]['cell_id'], fill="black")
                self.maze[cell]['type'] = 'wall'

    def get_clicked_cell(self, event):
        x, y = event.x, event.y
        row = int(y / self.cell_size)
        col = int(x / self.cell_size)
        return row, col

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()
