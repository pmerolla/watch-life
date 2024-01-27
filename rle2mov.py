
import numpy as np
import os
from PIL import Image
import re


def load_rle(file_path):
  with open(file_path, 'r') as f:
    rle_string = f.read()
  return rle_string


def rle_to_array(rle):
    lines = rle.strip().split('\n')

    # Extract the dimensions
    x_line = next((line for line in lines if line.startswith('x =')), '')
    match = re.search(r'x\s*=\s*(\d+),\s*y\s*=\s*(\d+)', x_line)
    if not match:
        raise ValueError("Invalid RLE header. Dimensions not found.")

    width, height = map(int, match.groups())

    array = np.zeros((height, width), dtype=int)

    # Process the RLE data
    data = ''.join(line for line in lines if not line.startswith('#') and not line.startswith('x ='))
    y, x = 0, 0
    for match in re.finditer(r'(\d*)(b|o|\$)', data):
        count_str, cell = match.groups()
        count = int(count_str) if count_str else 1

        if cell == 'b':
            x += count
        elif cell == 'o':
            array[y, x:x+count] = 1
            x += count
        elif cell == '$':
            y += count
            x = 0

    return array


def advance_game_of_life_state(grid):
    # Determine the size of the grid
    rows, cols = grid.shape

    # Create a new grid for the next state
    new_grid = np.zeros((rows, cols), dtype=int)

    # Iterate over each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Count the live neighbors
            live_neighbors = np.sum(grid[max(0, row-1):min(rows, row+2), max(0, col-1):min(cols, col+2)]) - grid[row, col]

            # Apply the rules of the game
            if grid[row, col] == 1 and live_neighbors < 2:
                new_grid[row, col] = 0 # Die: underpopulation
            elif grid[row, col] == 1 and (live_neighbors == 2 or live_neighbors == 3):
                new_grid[row, col] = 1 # Live
            elif grid[row, col] == 1 and live_neighbors > 3:
                new_grid[row, col] = 0 # Die: overpopulation
            elif grid[row, col] == 0 and live_neighbors == 3:
                new_grid[row, col] = 1 # Become live: reproduction

    return new_grid


def advance_game_of_life_state_optimized(grid):
    # Create an output grid initialized to zero
    new_grid = np.zeros_like(grid)

    # Iterate over the 8 possible directions for neighbors
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue # Skip the center cell

            # Shift the grid in the direction and add to the count
            shifted_grid = np.roll(grid, shift=(dx, dy), axis=(0, 1))
            new_grid += shifted_grid

    # Apply the Game of Life rules using boolean logic
    new_grid = ((new_grid == 3) | ((grid == 1) & (new_grid == 2))).astype(int)

    return new_grid


def save_game_state_to_image(grid, file_path):
    # Convert the game state to an image (255 for alive cells, 0 for dead cells)
    img = Image.fromarray(np.uint8(grid * 255), 'L')
    
    # Save the image
    img.save(file_path)


watch_rle = load_rle("watch.rle")
watch_np = rle_to_array(watch_rle)

UPSCALE_FLAG = True

mod = 8
sim_time = 60 * 12 * mod
save_dir = "strikes_12_8x"

#### Note this setting simulates 12hr, took some time on my MBP :-)
# mod = 8 ** 4
# sim_time = 60 * 60 * 60 * 12 + 6000
# save_dir = "round_the_clock"

idx = 0
for k in range(sim_time):
    watch_np = advance_game_of_life_state_optimized(watch_np)
    if (k % mod==0):
        if UPSCALE_FLAG:
            # Lazy man's 2x2 upscale
            upscale = np.zeros((watch_np.shape[0] * 2, watch_np.shape[1] * 2), dtype=int)
            upscale[0::2, 0::2] = watch_np
            upscale[0::2, 1::2] = watch_np
            upscale[1::2, 0::2] = watch_np
            upscale[1::2, 1::2] = watch_np
            save_game_state_to_image(upscale, f"{save_dir}/{save_dir}_{idx}.png")
        else:
            save_game_state_to_image(watch_np, f"{save_dir}/{save_dir}_{idx}.png")
        idx = idx + 1

