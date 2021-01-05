import numpy as np
from utils import utils
import random
import pyglet

pyglet.resource.path = ['resources/']
pyglet.resource.reindex()

tile_img = pyglet.resource.image("tile_img.png")
utils.center_img(tile_img)

cheese_img = pyglet.resource.image("cheese_img.png")
utils.center_img(cheese_img)

mouse_img = pyglet.resource.image("mouse_img.png")
utils.center_img(mouse_img)

game_window = pyglet.window.Window(820, 1000, caption="Mouse and Cheese!", visible=False)
game_window.set_location(900, 40)
tile_batch = pyglet.graphics.Batch()

tiles = [pyglet.sprite.Sprite(img=tile_img, batch=tile_batch, subpixel=False, x=0, y=0) for i in range(25)]
cheese = pyglet.sprite.Sprite(img=cheese_img, subpixel=False, x=800, y=20)
mouse = pyglet.sprite.Sprite(img=mouse_img, subpixel=False, x=800, y=20)
text_label = pyglet.text.Label(x=350, y=980)

gridworld_old = np.zeros((48, 40))
# the coordinates are flipped, x are the rows, same for y
position = [random.randrange(0, 46), random.randrange(0, 38)]
cheese_pos = [47, 39]
transition_reward = -1
terminal_transition_reward = 300

games_to_simulate = 500
game_num = 0
paths = {str(game_num): []}
replaying_game_num = 0
replaying_pos_num = 0

def run_sim():
    global gridworld_old
    global position
    global game_num

    paths[str(game_num)].append(position)

    gridworld_old, position = utils.sweep(gridworld_old, position, cheese_pos, transition_reward,
                                          terminal_transition_reward)

    if position == 'None':
        paths[str(game_num)].append(position)
        game_num += 1
        paths[str(game_num)] = []
        position = [random.randrange(0, 46), random.randrange(0, 38)]


def update(dt):
    global paths
    global replaying_game_num
    global gridworld_old
    global replaying_pos_num

    current_game = paths[str(replaying_game_num)]

    # current replay ended
    if replaying_pos_num >= len(current_game)-1:
        replaying_pos_num = 0
        replaying_game_num += 5
        if replaying_game_num >= game_num:   # replay the last one forever
            replaying_game_num = game_num-1
        current_game = paths[str(replaying_game_num)]

    position = current_game[replaying_pos_num]
    replaying_pos_num += 1

    text_label.text = "Game number: " + str(replaying_game_num)

    visible_tiles = utils.get_visible_grid_slice(position, [len(gridworld_old), len(gridworld_old[0])])

    x_coords = [visible_tiles[0] + x for x in range(visible_tiles[1] - visible_tiles[0] + 1)]
    y_coords = [visible_tiles[2] + y for y in range(visible_tiles[3] - visible_tiles[2] + 1)]
    visible_coords = []

    for x in x_coords:
        for y in y_coords:
            visible_coords.append([x, y])

    for i in range(len(tiles)):
        if i >= len(visible_coords):
            tiles[i].x, tiles[i].y = utils.convert_gridworld_coords(visible_coords[-1])
            continue
        tiles[i].x, tiles[i].y = utils.convert_gridworld_coords(visible_coords[i])

    mouse.x, mouse.y = utils.convert_gridworld_coords(position)



@game_window.event
def on_draw():
    game_window.clear()
    tile_batch.draw()
    cheese.draw()
    mouse.draw()
    text_label.draw()

while game_num < games_to_simulate:
    print("Running game #: " + str(game_num))
    run_sim()


game_window.set_visible()
pyglet.clock.schedule_interval(update, 1/240.0)
pyglet.app.run()


