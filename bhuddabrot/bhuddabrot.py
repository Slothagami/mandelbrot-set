import numpy as np 
from PIL import Image

from multiprocessing import Pool

width, height = 1000, 650#1500, 975#1000, 650
density = 2000 

screen_ratio = width / height

counts = np.zeros((height, width))

# Mandelbrot Loop
plot_range = 1

def bhuddabrot(depth):
    maximum = 0
    for x in np.linspace(-2, 2, density):
        for y in np.linspace(-2, 2, density):
            path = []
            # z = complex(x * screen_ratio, y)

            # Random point
            rx, ry = (np.random.rand(2) * 4) - 2
            z = complex(rx, ry)

            c = z 

            for _ in range(depth):
                if abs(z) > 2: break

                z = z**2 + c 
                path.append(z)

            if abs(z) > 2:
                for point in path:
                    # Plot z if point escaped
                    point_x = int( (point.real/screen_ratio + plot_range) / (2 * plot_range) * width  )
                    point_y = int( (point.imag              + plot_range) / (2 * plot_range) * height )

                    if 0 < point_x < width:
                        if 0 < point_y < height:
                            counts[point_y, point_x] += 1

                            # Update Max
                            count = counts[point_y, point_x] 
                            if count > maximum: maximum = count

    # normalize image
    image = counts / maximum * 255
    image = image.astype("uint8")
    return image


if __name__ == "__main__":
    # Calculate Color Channels
    with Pool() as pool:
        results = pool.map(bhuddabrot, (200, 1500, 3000))

    # r = bhuddabrot(100)
    # print("Red Channel Finished")
    # g = bhuddabrot(900)
    # print("Green Channel Finished")
    # b = bhuddabrot(2000)
    # print("Blue Channel Finished")

    # image = np.stack((r, g, b), 2)
    image = np.stack(results, 2)
    image = Image.fromarray(image)
    image.save("bhuddabrot/bhuddabrot.png")
