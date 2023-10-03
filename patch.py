import random

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