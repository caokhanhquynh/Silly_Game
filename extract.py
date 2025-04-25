from PIL import Image

gif = Image.open("giphy.gif")

for frame in range(gif.n_frames):
    gif.seek(frame)
    gif.save(f"frame_{frame}.png")
