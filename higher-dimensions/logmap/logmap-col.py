import matplotlib.pyplot as plt

pop = .5
r = 3.8
pops = []

for _ in range(200):
    pop = r * pop * (1 - pop)
    pops.append(pop)

plt.plot(pops)
plt.show()