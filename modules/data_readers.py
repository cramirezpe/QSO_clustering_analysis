from pathlib import Path
import numpy as np

class AbacusOut:
    def __init__(self, path):
        self.path = Path
        self.npoles = dict()
        try:
            r, _0, _2, _4 = np.loadtxt(path, unpack=True)
            self.npoles[0] = _0 
            self.npoles[2] = _2
            self.npoles[4] = _4
        except ValueError:
            r, _0 = np.loadtxt(path, unpack=True)
            self.npoles[0] = _0
            self.npoles[2] = np.zeros_like(_0)
            self.npoles[4] = np.zeros_like(_0)
        
        self.r = r
        self.savg = r

    def compute_npole(self, n):
        return self.npoles[n]

class eBossOut:
    def __init__(self, file):
        self.file = file
        _s, _xi0, _xi2, _xi4 = np.loadtxt(self.file, unpack=True)
        self.r = _s
        self.poles = {0: _xi0, 2: _xi2, 4: _xi4}
    
    def compute_npole(self, pole):
        return self.poles[pole]

    def __str__(self):
        return self.label    