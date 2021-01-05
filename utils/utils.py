import random

# bottom left: 0 0
def convert_gridworld_coords(coords):
    # 800 x 960
    # 48 x 40 (rows x cols)
    # [0, 0] -> [0, 960]
    # [47, 39] -> [800, 0]
    # [0, 39] -> [800, 960]
    # [47, 0] -> [0, 0]

    # [row, col]
    row = coords[0]
    col = coords[1]

    y = 960 - row*20
    x = (col+1)*20

    # [0, 0] -> [20, 960]
    # [47, 39] -> [800, 20]
    # [0, 39] -> [800, 960]
    # [47, 0] -> [20, 20]

    return [x, y]

"""
    position : [row, col]
    limits   : [row, col]
    returns  : [min_x_index, max_x_index, ...]
"""
def get_visible_grid_slice(position, gridworld_limits):
    slice = [position[0] - 2, position[0] + 2, position[1] - 2, position[1] + 2]

    if slice[0] < 0:
        slice[0] = 0

    if slice[1] >= gridworld_limits[0]:
        slice[1] = gridworld_limits[0]-1

    if slice[2] < 0:
        slice[2] = 0

    if slice[3] >= gridworld_limits[1]:
        slice[3] = gridworld_limits[1]-1

    return slice

"""
    gridworld_old: the whole matrix
    terminal_pos: [x, y]
"""
def sweep(gridworld_old, position, terminal_pos, transition_reward, terminal_transition_reward):

    slice = get_visible_grid_slice(position, [len(gridworld_old), len(gridworld_old[0])])

    gridworld_new = gridworld_old.copy()

    i = slice[0]
    ii = slice[2]

    best_next_coords = 'None'

    while i <= slice[1]:     # row
        while ii <= slice[3]:    # col

            if [i, ii] == terminal_pos:  # terminal state
                gridworld_new[i][ii] = 0    # expected reward from terminal state is zero
                ii += 1
                continue
            elif position == terminal_pos:
                return [gridworld_new, best_next_coords]

            max_adj_val = get_max_adj_val(gridworld_old, i, ii, terminal_pos, terminal_transition_reward, transition_reward)
            gridworld_new[i][ii] = max_adj_val[0]

            if [i, ii] == position:
                best_next_coords = max_adj_val[1]

            ii += 1

        ii = slice[2]
        i += 1
    # sweep complete
    return [gridworld_new, best_next_coords]

def get_max_adj_val(gridworld, i, ii, terminal_pos, terminal_transition_reward, transition_reward):
    adjacent_coords = [
        [i - 1, ii],  # up
        [i, ii + 1],  # right
        [i + 1, ii],  # down
        [i, ii - 1]  # left
    ]

    # transitioning outside the bounds of the gridworld will leave position unchanged
    if i == 0:
        adjacent_coords[0][0] = i
    elif i == len(gridworld) - 1:
        adjacent_coords[2][0] = i

    if ii == 0:
        adjacent_coords[3][1] = ii
    elif ii == len(gridworld[0]) - 1:
        adjacent_coords[1][1] = ii

    adjacent_vals = []
    for coord in adjacent_coords:
        if coord == terminal_pos:
            adjacent_vals.append(terminal_transition_reward + transition_reward + gridworld[coord[0], coord[1]])
        else:
            adjacent_vals.append(transition_reward + gridworld[coord[0], coord[1]])

    max_adjacent_val = max(adjacent_vals)
    max_adjacent_coords = [k for k, x in enumerate(adjacent_vals) if x == max_adjacent_val] # find the indices of all max vals
    best_coords = adjacent_coords[random.choice(max_adjacent_coords)]

    return [max_adjacent_val, best_coords]

def center_img(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

