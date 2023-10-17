
class Matrix:
    def __init__(self, n, m=None):
        # ukoliko je zadan samo n argument, matrica je kvadratna nxn
        self.n = int(n)
        if m == None:
            self.m = int(n)
        else:
            self.m = int(m)
        self.mat  = dict()

    def __setitem__(self, key, value):
        self.mat[key] = value

    def __getitem__(self, key):
        return self.mat.get(key, 0)
    
    def __str__(self):
        s = ""
        for i in range(self.n):
            for j in range(self.m):
                s += str(self[i, j]) + " "
            s += "\n"
        return s