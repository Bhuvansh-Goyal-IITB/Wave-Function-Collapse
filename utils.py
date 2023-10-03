import numpy as np


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
