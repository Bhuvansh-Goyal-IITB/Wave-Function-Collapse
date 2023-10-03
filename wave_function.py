from patch import Patch
from utils import *
from collections import Counter
from PIL import Image

class Wave:
    def __init__(self, imgUrl, kernel_size, width, height):
        img = Image.open(imgUrl)
        data = [[tuple(img.getdata())[x + y * img.width] for x in range(img.width)] for y in range(img.height)]
        
        all_patterns = get_all_patterns(data, kernel_size)

        c = Counter(all_patterns)
        self.frequencies = tuple(c.values())
        self.patterns = tuple(c.keys())
        self.num_patterns = len(self.patterns)

        self.adjacencies = create_adjacency(self.patterns)

        self.width = width
        self.height = height

        self.wave = [[None for _ in range(width)] for _ in range(height)]
        self.initialize_wave(width, height)

    def reset_wave(self):
        self.wave = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.initialize_wave(self.width, self.height)

    def initialize_wave(self, width, height):
        for y in range(height):
            for x in range(width):
                self.wave[y][x] = Patch((x, y), self.num_patterns)
        
    def find_least_entropy(self):
        min_pos = None
        min_entropy = None
        for y, row in enumerate(self.wave):
            for x, patch in enumerate(row):
                if patch.entropy == 0:
                    continue
                if min_entropy == None or min_entropy > patch.entropy:
                    min_pos = (x, y)
                    min_entropy = patch.entropy
        
        return min_pos
    
    def collapse(self, x, y):
        self.wave[y][x].collapse(self.frequencies)
        
    def propogate(self, pos):
        queue = [pos]

        directions = ((0, -1), (1, 0), (0, 1), (-1, 0))

        while len(queue) > 0:
            current = queue.pop(0)
            for i in range(4):
                nx, ny = current[0] + directions[i][0], current[1] + directions[i][1]
                if nx < 0 or nx > len(self.wave[0]) - 1 or ny < 0 or ny > len(self.wave) - 1:
                    continue
                
                neighbour =  self.wave[ny][nx]
                possible = set.union(*[self.adjacencies[id][i] for id in self.wave[current[1]][current[0]].possible_ids])
        
                if not neighbour.possible_ids.issubset(possible):
                    intersection = neighbour.possible_ids & possible

                    if not intersection:
                        return False
                    
                    neighbour.possible_ids = intersection
                    
                    queue.append((nx, ny))
            
        return True