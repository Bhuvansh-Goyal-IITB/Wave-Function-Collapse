from PIL import Image
import numpy as np
from collections import Counter
from itertools import chain
import random
import pygame
import time
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Classes
class Patch:
    def __init__(self, pos, num_patterns):
        self.pos = pos
        self.possible_ids = set(i for i in range(num_patterns))
        self.collapsed = False

    @property
    def entropy(self):
        if self.collapsed:
            return 0
        return len(self.possible_ids) + ((random.random() - 0.5) / 5)
        
    def collapse(self, weights):
        weights = tuple(weights[id] for id in self.possible_ids)
        
        id_choice = random.choices(list(self.possible_ids), weights=weights, k=1)
        
        self.possible_ids = {*id_choice}
        self.collapsed = True

# Functions
def initialize_wave(width, height, num_patterns):
    wave = [[None for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            wave[y][x] = Patch((x, y), num_patterns)

    return wave

def create_adjacency(patterns):
    adjacency = tuple(tuple(set() for _ in range(4)) for _ in range(len(patterns)))

    for i, this_pattern in enumerate(patterns):
        for j, other_pattern in enumerate(patterns):
            if [[val for x, val in enumerate(row[1:])] for y, row in enumerate(this_pattern)] == [[val for x, val in enumerate(row[:-1])] for y, row in enumerate(other_pattern)]:
                adjacency[i][1].add(j)
                adjacency[j][3].add(i)
            if [[val for x, val in enumerate(row)] for y, row in enumerate(this_pattern[:-1])] == [[val for x, val in enumerate(row)] for y, row in enumerate(other_pattern[1:])]:
                adjacency[i][0].add(j)
                adjacency[j][2].add(i)

    return adjacency

def get_all_patterns(data, size):
    width, height = len(data[0]), len(data)
    all = list()
    
    for y in range(len(data)):
        for x in range(len(data[0])):
        
            flattned_pattern = list()
            
            for j in range(size):
                for i in range(size):
                    flattned_pattern.append(data[(y+j)%height][(x+i)%width])
            
            pattern = tuple(tuple(flattned_pattern[x + y * size] for x in range(size)) for y in range(size))
            
            all.append(pattern)
            
            rot_90 = tuple(tuple(tuple(val) for x, val in enumerate(row)) for y, row in enumerate(np.rot90(np.array(pattern)).tolist()))
            all.append(rot_90)
            
            rot_180 = tuple(tuple(tuple(val) for x, val in enumerate(row)) for y, row in enumerate(np.rot90(np.rot90(np.array(pattern))).tolist()))
            all.append(rot_180)
            
            rot_270 = tuple(tuple(tuple(val) for x, val in enumerate(row)) for y, row in enumerate(np.rot90(np.rot90(np.rot90(np.array(pattern)))).tolist()))
            all.append(rot_270)

            h_flip = tuple(tuple(tuple(val) for x, val in enumerate(row)) for y, row in enumerate(np.array(pattern)[:, ::-1]))
            all.append(h_flip)
            
            v_flip = tuple(tuple(tuple(val) for x, val in enumerate(row)) for y, row in enumerate(np.array(pattern)[::-1, :]))
            all.append(v_flip)

    return all

def find_least_entropy(wave):
    min_pos = None
    min_entropy = None
    for y, row in enumerate(wave):
        for x, patch in enumerate(row):
            if patch.entropy == 0:
                continue
            if min_entropy == None or min_entropy > patch.entropy:
                min_pos = (x, y)
                min_entropy = patch.entropy
    
    return min_pos

def propogate(wave, pos, adjacency):
    queue = [pos]

    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))

    while len(queue) > 0:
        current = queue.pop(0)
        for i in range(4):
            nx, ny = current[0] + directions[i][0], current[1] + directions[i][1]
            if nx < 0 or nx > len(wave[0]) - 1 or ny < 0 or ny > len(wave) - 1:
                continue
            
            neighbour =  wave[ny][nx]
            possible = set.union(*[adjacency[id][i] for id in wave[current[1]][current[0]].possible_ids])
       
            if not neighbour.possible_ids.issubset(possible):
                intersection = neighbour.possible_ids & possible

                if not intersection:
                    return False
                
                neighbour.possible_ids = intersection
                
                queue.append((nx, ny))
        
    return True
            
# Implimentation
img = Image.open("samples/Town.png")
data = [[tuple(img.getdata())[x + y * img.width] for x in range(img.width)] for y in range(img.height)]

all_patterns = get_all_patterns(data, 3)

c = Counter(all_patterns)
frequencies = tuple(c.values())
patterns = tuple(c.keys())
num_patterns = len(patterns)

adjacencies = create_adjacency(patterns)

WIDTH, HEIGHT = 80, 80

wave = initialize_wave(WIDTH, HEIGHT, num_patterns)

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

pixel_w = 10
success = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("#222222")

    while not success:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        min_pos = find_least_entropy(wave)
        if min_pos == None:
            print("Success")
            success = True
            break

        wave[min_pos[1]][min_pos[0]].collapse(frequencies)
        if propogate(wave, min_pos, adjacencies):
            for y, row in enumerate(wave):
                for x, patch in enumerate(row):
                    if len(patch.possible_ids) > 1:
                        continue
                    pattern_id = list(patch.possible_ids)[0]
                    color = patterns[pattern_id][0][0]

                    pygame.draw.rect(screen, color, pygame.Rect((x * pixel_w, y * pixel_w), (pixel_w, pixel_w)))
            pygame.display.flip()
            clock.tick(0)
            continue
        else:
            print("Fail")
            wave = initialize_wave(WIDTH, HEIGHT, num_patterns)
            break
    
    for y, row in enumerate(wave):
        for x, patch in enumerate(row):
            if len(patch.possible_ids) > 1:
                continue
            pattern_id = list(patch.possible_ids)[0]
            color = patterns[pattern_id][0][0]

            pygame.draw.rect(screen, color, pygame.Rect((x * pixel_w, y * pixel_w), (pixel_w, pixel_w)))
            
    pygame.display.flip()
    clock.tick(60)
    # for y, row in enumerate(wave):
    #     for x, patch in enumerate(row):    
    #         print(patch.possible_ids, end=" ")
    #     print("")  

