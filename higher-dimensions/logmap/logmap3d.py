import matplotlib.pyplot as plt

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')

startPop    = .5
removeNoise = True
layerDetail = 40

prec  = 60
zprec = prec
rprec = prec

zrange = [-2, 2]
rrange = [-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]

xs, ys, zs = [], [], []

r = complex(rrange[0], zrange[0])
for _ in range(zprec):
    for _ in range(rprec):
        pop = startPop

        if removeNoise:
            for _ in range(200):
                pop = r * pop * (1 - pop)

        for _ in range(layerDetail):
            pop = r * pop * (1 - pop)

            xs.append(r.real)
            ys.append(pop)
            zs.append(r.imag)

        r += rspan / rprec
    r -= r.real - rrange[0]
    r += complex(0, zspan / zprec)

ax.scatter(xs, ys, zs, s = .05)
plt.ylim([-2, 2])
plt.show()
