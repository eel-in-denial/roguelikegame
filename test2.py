import pyglet
import os
from PIL import Image


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "foundation_tiles/drylands", '8-drylands_portal.png')  # adjust folder/filename
output_path1 = os.path.join(script_dir, "scaledImages", 'sandHex.png')  # adjust folder/filename
output_path2 = os.path.join(script_dir, "scaledImages", 'sandHexSmall.png')  # adjust folder/filename

# pil_img = Image.open(image_path)
# pil_img = pil_img.resize((238,207), Image.LANCZOS)
# pil_img.save(output_path1)
pil_img = Image.open(image_path)
pil_img = pil_img.resize((119,103), Image.LANCZOS)
pil_img.save(output_path2)

image = pyglet.image.load(output_path1)

window = pyglet.window.Window(width=1400, height=700)

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()

