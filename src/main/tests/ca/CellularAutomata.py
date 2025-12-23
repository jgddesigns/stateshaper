import time
import random
import os
from core import Stateshaper



class CellularAutomata:



    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __init__(self):
        self.WIDTH = 80
        self.HEIGHT = 30
        self.SEED = 42

        # Symbols
        self.WATER = "~"
        self.LAND  = "."
        self.HILL  = "^"
        self.MOUNT = "▲"

        self.rng = random.Random(self.SEED)



    def run(self, fill=0.45, smooth_steps=6):
        self.clear()
        mask = self.generate_world_mask(fill=fill, smooth_steps=smooth_steps)
        elev = self.add_elevation(mask)
        self.render(elev)


    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def make_noise(self, fill=0.45):
        return [
            [1 if self.rng.random() < fill else 0 for _ in range(self.WIDTH)]
            for _ in range(self.HEIGHT)
        ]

    def neighbors(self, grid, x, y):
        c = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= self.WIDTH or ny >= self.HEIGHT:
                    c += 1  # treat edges as solid
                else:
                    c += grid[ny][nx]
        return c

    def step(self, grid):
        new = [[0] * self.WIDTH for _ in range(self.HEIGHT)]
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                n = self.neighbors(grid, x, y)
                if grid[y][x] == 1:
                    new[y][x] = 1 if n >= 4 else 0
                else:
                    new[y][x] = 1 if n >= 5 else 0
        return new

    def generate_world_mask(self, fill=0.45, smooth_steps=6):
        grid = self.make_noise(fill=fill)
        for _ in range(smooth_steps):
            grid = self.step(grid)
        return grid

    def add_elevation(self, mask):
        elev = [[0] * self.WIDTH for _ in range(self.HEIGHT)]
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if mask[y][x]:
                    elev[y][x] = self.rng.randint(1, 100)
        return elev

    def render(self, elev):
        for y in range(self.HEIGHT):
            row = []
            for x in range(self.WIDTH):
                h = elev[y][x]
                if h == 0:
                    row.append(self.WATER)
                elif h < 40:
                    row.append(self.LAND)
                elif h < 75:
                    row.append(self.HILL)
                else:
                    row.append(self.MOUNT)
            print("".join(row))







    def define_stateshaper(self):

        self.engine = Stateshaper([111, 222, 543, 235, 67], [0, 1])
