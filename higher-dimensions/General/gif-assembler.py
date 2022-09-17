import os 
import imageio

os.chdir(os.path.dirname(__file__))
wdir = "./renders/frames/"

gifName = "Mandlebrot-n3000-s400-spinY"

frames = os.listdir(wdir)
frames.sort(key=lambda x: int(x.split(".")[0]))

frameData = []
for frame in frames:
    frameData.append(imageio.imread(wdir + frame))
imageio.mimsave(f'./renders/{gifName}.gif', frameData, fps=8)