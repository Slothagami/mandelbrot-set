import os 
import imageio

os.chdir(os.path.dirname(__file__))
wdir = "./renders/4D-Render/frames/"

frames = os.listdir(wdir)
frames.sort(key=lambda x: int(x.split(".")[-2].split("-")[-1]))
details = frames[0].split("-FRAME-")[0]

frameData = []
for frame in frames:
    frameData.append(imageio.imread(wdir + frame))
imageio.mimsave(f'./renders/4D-Render/{details}.gif', frameData)