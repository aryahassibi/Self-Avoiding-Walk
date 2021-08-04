import pygame
from random import choice, randint

# Used colors
PATH_COLOR = (50, 100, 250)
BG_COLOR = (255, 255, 255)
GRID_COLOR =  (200, 200, 200)
DIRECTION_COLOR = (200, 100, 100)

rows, cols = 5, 5 # Number of rows and cols
grid_size = 40 # Size of each sqaure in the grid
circle_radius = grid_size // 3 # Radius of circles on the path

# width and height of the screen
width, height = cols * grid_size, rows * grid_size
size = (width, height)

# initiate pygame and create window
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Self-Avoiding Walk V3")

# done will be set to True when you close the window
done = False

# finished will be set to True when the program has found a self-avoiding path
finished = False


# Spot(grid_x, grid_y) takes two inputs which are the position of the spot
# based on the grid rows and columns.
# grid_x ranges from 0 to cols -- grid_y ranges from 0 to rows
#
# 1. __init__(self, grid_x, grid_y)
#   - self.x and self.y -> the spot's exact position on the window
#     ( calculated based on grid_x, grid_y, grid_size)
#   - self.options -> the available options for the spot
#   - self.direction ->  stores the randomly chosen direction for this spot
#   - self.is_in_path -> is set to True when the spot is used in the path
#
# 2. Spot.reset(self)
#   - resets self.options, self.direction, self.is_in_path to their initial values
#     and makes the spot reusable.
#
# 3. Spot.is_stuck(self)
#   - returns True if there no options left for the spot and it is stuck
#   - returns False otherwise
#
# 4. Spot.is_impossible(grid_x, grid_y)  -  static function
#   - it checks to see whether it is even possible to create a self-avoiding path or not
#   - When is it impossible?
#       1. If the number of rows and columns are both odd numbers and
#         the starting spot position is a pair of numbers which one of
#         them is an odd number and the other one is an even number
#       2. If the grid dimensions are 1 by X and the starting spot position
#          is not on one end of the grid.
#          this is possible    -> ◽️◽️◽️◽️◽️◽️◽️◽️◼️
#          this is impossible  -> ◽️◽️◽️◽️◽️◽️◼️◽️◽️
#   - function returns True if it is impossible and returns False
#     if it is possible to find a self-avoiding path
#
# 5. Spot.find_valid_starting_spot_position()  -  static function
#   - It chooses the position of the first spot randomly
#   - if it is immposible to create a self-svoiding path with the randomly chosen positions
#     it chooses another position until it is a valid one
#
# 6. Spot.path_finder(grid_x, grid_y)  -  static function
#   - path_finder a static function that is recursive
#   - it will find a self-avoiding path and puts it in the path list
#   - then you can draw path and see it

class Spot:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.x = (grid_x + 0.5) * grid_size
        self.y = (grid_y + 0.5) * grid_size
        self.position = (self.x, self.y)

        self.options = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.direction = 0
        # up, right , down , left

        self.is_in_path = False

    def reset(self):
        self.options = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.direction = 0
        self.is_in_path = False

    def is_stuck(self):
        if self.options == []:
            return True
        return False

    @staticmethod
    def is_impossible(grid_x, grid_y):
        # Check to see if no spot has been added to the path
        # and grid_x, grid_y is the position of the first Spot of the path
        if len(path) == 0:
            if (rows * cols) % 2 == 1 and grid_x % 2 != grid_y % 2:
                return True
            if rows == 1 and cols > 2 and 0 < grid_x < cols - 1:
                return True
            if cols == 1 and rows > 2 and 0 < grid_y < rows - 1:
                return True
        return False

    @staticmethod
    def find_valid_starting_spot_position():
        x, y = randint(0, cols - 1), randint(0, rows - 1)
        while Spot.is_impossible(x, y):
            x, y = randint(0, cols - 1), randint(0, rows - 1)
        return x, y

    @staticmethod
    def path_finder(grid_x, grid_y):
        global grid, path, finished

        # check to see if the position(grid_x, grid_y) of the spot is valid:
        #   1. grid_x and grid_y are valid positions on the grid
        #      greater than 0 and less than the number of rows/columns
        #   2. spot(grid_x, grid_y) has not been used in the path before
        if 0 <= grid_y < rows and 0 <= grid_x < cols and not grid[grid_y][grid_x].is_in_path:
            # grid_x and grid_y are valid, so let's call the grid[grid_y][grid_x], current_spot
            current_spot = grid[grid_y][grid_x]

            # add the spot to the path
            current_spot.is_in_path = True
            path.append(current_spot)

            # Remove the direction that it came from, from its options (reverse_direction)
            # e.g. remove up(0, -1) if its direction is down(0, 1)
            # because it cannot go back until it has tried all of the other options
            # except for the first spot - which can go any direction
            if len(path) > 1:
                reverse_direction = tuple(element * -1 for element in path[-2].direction)
                current_spot.options.remove(reverse_direction)

            # if the length of the path is equal to the number of spots on the grid_
            # a path has been found -> set finished to True
            # return True, to come out of the recursive function
            if len(path) == rows * cols:
                finished = True
                return True

            # try all of the possible direction for current spot until it is stuck
            while not current_spot.is_stuck():
                # Choose a direction randomly
                direction = choice(current_spot.options)

                # set the direction for the current spot
                current_spot.direction = direction

                # call the function and give it the next spot position
                # store the return of the function in next_spot
                next_spot = Spot.path_finder(current_spot.grid_x + direction[0], current_spot.grid_y + direction[1])

                # the function returned False so the direction it take was not good
                # and it is better to remove it from its options
                if next_spot == False:
                    current_spot.options.remove(direction)

            # if the current spot has no where to go but a path has not been found yet
            if current_spot.is_stuck() and not finished:
                # reset the current spot to make it reusable
                # remove the last spot in the path
                # return False, go back and try another direction
                path[-1].reset()
                path.pop()
                return False

        # grid_x and grid_y are not valid
        # return False to go back and try another direction
        return False


# grid -> a two dimentional list(array) that each elemnt is a Spot
grid = []
for r in range(rows):
    grid_row = []
    for c in range(cols):
        grid_row.append(Spot(c, r))
    grid.append(grid_row)

# path -> a list(array) that stores a copy of each Spot that is in the path
# The first spot in the path is chosen randomly
path = []

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Closed the window
            # done -> is set to True, to end the loop
            # and exit the program
            done = True

        if event.type == pygame.KEYDOWN:  # Pressed a key
            if event.key == pygame.K_SPACE: # The pressed key is space
                # The state of finished is set to False to restart the function
                finished = False

                # make path empty, so that the program can create another path
                path = []

                # Reset every Spot in grid to make the grid resuable
                for r in range(rows):
                    for c in range(cols):
                        grid[r][c].reset()

    # finished will be set to True when the function finds a path
    # and it is False by default
    if not finished:
        # choose a valid position randomly
        first_spot_grid_x, first_spot_grid_y = Spot.find_valid_starting_spot_position()

        # call the recursive function to find a path
        # path_finder pushes every spot into the path list
        a = Spot.path_finder(first_spot_grid_x, first_spot_grid_y)

        # resize pygame window, set its height width to their initial values
        # in case the screen was resized to show "impossible text"
        screen = pygame.display.set_mode(size)

        # Set background color
        screen.fill(BG_COLOR)

        # Draw grid lines
        for r in range(1, rows):
            pygame.draw.line(screen, GRID_COLOR, [0, r * grid_size], [width,r * grid_size])
        for c in range(1, cols):
            pygame.draw.line(screen, GRID_COLOR, [c * grid_size, 0], [c * grid_size,height])

        # Draw path
        for i in range(len(path)):
            pygame.draw.circle(screen, PATH_COLOR, path[i].position, circle_radius)
            if i > 0:
                pygame.draw.line(screen, PATH_COLOR, path[i - 1].position, path[i].position, 2)

        # Refresh the pygame window to display the path
        pygame.display.flip()

pygame.quit()
