import matplotlib.pyplot as plt

startPop = .5
xs, ys = [], []
removeNoise = True

precision = 9000
rRange = [-2, 4.15]
rSpan = rRange[1] - rRange[0]

r = complex(rRange[0], 0)
for _ in range(precision):
    pop = startPop

    if removeNoise:
        for _ in range(200):
            pop = r * pop * (1 - pop)

    for _ in range(50):
        pop = r * pop * (1 - pop)

        xs.append(r.real)
        ys.append(pop)

    r += rSpan / precision

plt.scatter(xs, ys, .01)
plt.ylim([-.5, 1.3])
plt.show()
