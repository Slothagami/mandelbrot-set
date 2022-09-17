def mandlebrot(z, c):     return z * z + c
def mandlebrot_4th(z, c): return z * z * z * z + c

def logmap(x, r):         return r * x * (1 - x)