import pyglet
from pyglet.window import mouse
from pyglet.window import key
from PIL import Image
import os


window = pyglet.window.Window()


# Directory the script itself is in
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'hex.png')

pil_img = Image.open(file_path)
pil_img = pil_img.resize((32, 32), Image.LANCZOS)
pil_img.save(os.path.join(script_dir, 'cursor_32.png'))

image = pyglet.image.load(os.path.join(script_dir, 'cursor_32.png'))
cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
window.set_mouse_cursor(cursor)

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

image = pyglet.resource.image('hex.png')

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')

@window.event
def on_mouse_motion(x, y, dx, dy):
    print(x,y)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.ENTER:
        print('The enter key was pressed.')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

pyglet.app.run(1/120)



event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)