import pygame
from random import choice, randint

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
# 2. Spot.reset()
#   - resets self.options, self.direction, self.is_in_path to their initial values
#     and makes the spot reusable.
#
# 3. Spot.is_stuck()
#   - returns True if there no options left for the spot and it is stuck
#   - returns False otherwise
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
        if (rows * cols) % 2 == 1 and grid_x % 2 != grid_y % 2:
            return True
        if rows == 1 and cols > 2 and 0 < grid_x < cols - 1:
            return True
        if cols == 1 and rows > 2 and 0 < grid_y < rows - 1:
            return True
        return False

    @staticmethod
    def find_valid_starting_spot_position():
        # choose the position of the first spot randomly
        x, y = randint(0, cols - 1), randint(0, rows - 1)

        # if it is immposible to create a self-svoiding path with the randomly chosen positions
        # choose another position until it is valid one
        while Spot.is_impossible(x, y):
            x, y = randint(0, cols - 1), randint(0, rows - 1)
        return x, y


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
pygame.display.set_caption("Self-Avoiding Walk")
clock = pygame.time.Clock()

# done will be set to True when you close the window
done = False

# finished will be set to True when you press Space on keyboard
# to pause the program or when the program has found a solution
finished = False

# grid -> a two dimentional list(array) that each elemnt is a Spot
grid = []
for r in range(rows):
    grid_row = []
    for c in range(cols):
        grid_row.append(Spot(c, r))
    grid.append(grid_row)

# choose a valid position randomly
first_spot_grid_x, first_spot_grid_y = Spot.find_valid_starting_spot_position()

# path -> a list(array) that stores a copy of each Spot that is in the path
path = [grid[first_spot_grid_y][first_spot_grid_x]]
path[-1].is_in_path = True

while not done:
    # clock.tick(fps) sets the FPS of the screen
    # remove the script if you want to SEE SOME SPEEEEEDDDD
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Closed the window
            # done -> is set to True, to end the loop
            # and exit the program
            done = True

        if event.type == pygame.KEYDOWN:  # Pressed a key
            if event.key == pygame.K_SPACE: # The pressed key is space
                # The state of finished is fliped
                # restart the program if it is paused or finished
                # pause the program if it is running
                finished = not finished

                # Reset every Spot in grid to make the grid resuable
                for r in range(rows):
                    for c in range(cols):
                        grid[r][c].reset()

                # choose a valid position randomly
                first_spot_grid_x, first_spot_grid_y = Spot.find_valid_starting_spot_position()

                # Choose the first spot randomly
                path = [grid[first_spot_grid_y][first_spot_grid_x]]
                path[-1].is_in_path = True

    # Run/resume the program if it is not finished
    if not finished:
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

        # Finished? - stop the program if the walk has ended (if apath has been found)
        # if the length of the path is equal to the number of spots on the grid
        # a path has been found
        if len(path) == rows * cols:
            finished = True

        # Stuck?
        elif path[-1].is_stuck():
            # Step Back!
            # The last Spot is reseted and removed from path
            path[-1].reset()
            path.pop()

            # remove the direction of the last spot from its options
            path[-1].options.remove(path[-1].direction)

        # Continue. - else, it is neither stuck nor finished, so choose the next spot
        else:
            # Choose a direction randomly
            direction = choice(path[-1].options)

            # Calculate the postion of the next spot
            next_spot = [path[-1].grid_x + direction[0], path[-1].grid_y + direction[1]]

            # Check to see if the next_spot is a valid spot
            #   1. It should not be in the path (should not be used before)
            #   2. Its position should be inside the grid
            #      greater than 0 and less than the number of rows/columns
            if 0 <= next_spot[1] < rows and 0 <= next_spot[0] < cols and not grid[next_spot[1]][next_spot[0]].is_in_path:
                # set the direction for the last spot
                path[-1].direction = direction

                # Add the new spot to path
                path.append(grid[next_spot[1]][next_spot[0]])
                path[-1].is_in_path = True

                # Remove the direction that it came from, from its options (reverse_direction)
                # e.g. remove up(0, -1) if its direction is down(0, 1)
                # because it cannot go back until it has tried all of the other options
                reverse_direction = tuple(element * -1 for element in direction)
                path[-1].options.remove(reverse_direction)

            # else - the next_spot is not valid
            else:
                # Display the wrong direction that it wants to go
                pygame.draw.line(screen, DIRECTION_COLOR, Spot(next_spot[0],next_spot[1]).position, path[-1].position, 1)
                pygame.draw.circle(screen, DIRECTION_COLOR, Spot(next_spot[0],next_spot[1]).position, 5)
                # Remove the wrong direction from the last spot options
                path[-1].options.remove(direction)

    # Refresh the pygame window to display the path
    pygame.display.flip()

pygame.quit()
