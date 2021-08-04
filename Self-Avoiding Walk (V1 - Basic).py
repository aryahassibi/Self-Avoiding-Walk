import pygame
from random import choice, randint

# it checks to see whether it is even possible to create a self-avoiding path or not
def is_impossible(x, y):
    # If the number of rows and columns are both odd numbers and
    # the starting spot position is a pair of numbers which one of
    # them is an odd number and the other one is an even number.
    if (rows * cols) % 2 == 1 and x % 2 != y % 2:
        return True

    # If the grid dimensions are 1 by X and the starting spot position
    # is not on one end of the grid.
    if rows == 1 and cols > 2 and 0 < x < cols - 1:
        return True
    if cols == 1 and rows > 2 and 0 < y < rows - 1:
        return True
    return False

def find_valid_starting_spot_position():
    # choose the position of the first spot randomly
    x, y = randint(0, cols - 1), randint(0, rows - 1)

    # if it is immposible to create a self-svoiding path with the randomly chosen positions
    # choose another position until it is valid one
    while is_impossible(x, y):
        x, y = randint(0, cols - 1), randint(0, rows - 1)
    return x, y

# used colors
PATH_COLOR = (50, 100, 250)
BG_COLOR = (255, 255, 255)
GRID_COLOR =  (200, 200, 200)
DIRECTION_COLOR = (200, 100, 100)

rows, cols = 5, 5 # Number of rows and cols
grid_size = 40 # Size of each sqaure in the grid
circle_radius = grid_size // 3 # Radius of circles on the path

# width and height of the screen
width, height = cols * grid_size, rows * grid_size
size = [width, height]

# initiate pygame and create window
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Self-Avoiding Walk")
clock = pygame.time.Clock()

# done -> will be set to True when you close the window
done = False

# finished -> will be set to True when you press Space on keyboard to pause the program
# or when the program has found a solution
finished = False

# choose a valid position randomly
first_spot_grid_x, first_spot_grid_y = find_valid_starting_spot_position()

# path -> a list(array) that stores the position of each of the spots on the path
path = [[(first_spot_grid_x + 0.5) * grid_size, (first_spot_grid_y + 0.5) * grid_size]]

# directions -> a list(array) that stores the direction that each spot on the path has taken
directions = []

# option ->  a list(array) that stores the avaiable directions for each spot on the path
options = [[(0, -1), (1, 0), (0, 1), (-1, 0)]]

while not done:
    # clock.tick(fps) sets the FPS of the screen
    # remove the script if you want to SEE SOME SPEEEEEDDDD
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Closed the window
            # done -> is set to True, to end the loop
            # and exit the program
            done = True

        if event.type == pygame.KEYDOWN: # Pressed a key
            if event.key == pygame.K_SPACE: # The pressed key is space
                # The state of finished is fliped
                # restart the program if it is paused or finished
                # pause the program if it is running
                finished = not finished

                # choose a valid position randomly
                first_spot_grid_x, first_spot_grid_y = find_valid_starting_spot_position()

                # reset path, direstions, and options to their intial value
                path = [[(first_spot_grid_x + 0.5) * grid_size, (first_spot_grid_y + 0.5) * grid_size]]
                directions = []
                options = [[(0, -1), (1, 0), (0, 1), (-1, 0)]]

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
            pygame.draw.circle(screen, PATH_COLOR, path[i], circle_radius)
        if len(path) > 1:
            pygame.draw.lines(screen, PATH_COLOR, False, path, 2)

        # Finished? - stop the program if the walk has ended (if a path has been found)
        if len(path) == rows * cols:
            finished = True

        # Stuck? - else if there are no options left for the last spot, then it is stuck
        elif options[-1] == []:
            # Step Back!
            # The last spot position and options is removed from path and options
            options.pop()
            path.pop()
            # remove the direction of the last spot from its options
            options[-1].remove(directions[-1])

            #remove the last spot direction
            directions.pop()

        # Continue. - else, it is neither stuck nor finished, so choose the next spot
        else:
            # Choose a direction randomly
            direction = choice(options[-1])

            # Calculate the postion of the next spot
            next_spot = [path[-1][0] + direction[0] * grid_size, path[-1][1] + direction[1] * grid_size]

            # Check to see if the next_spot is a valid spot
            #   1. It should not be in the path (should not be used before)
            #   2. Its position should be inside the grid
            #      greater than 0 and less than the number of rows/cols
            if not next_spot in path and 0 < next_spot[0] < width and 0 < next_spot[1] < height:
                # Add the next_spot to the path
                path.append(next_spot)

                # Add the randomly chosen direction to directions
                directions.append(direction)

                # Add all of the options to options
                # and remove the direction that it came from, from its options (reverse_direction)
                # e.g. remove up(0, -1) if its direction is down(0, 1)
                # because it cannot go back until it has tried all of the other options
                options.append([(0, -1), (1, 0), (0, 1), (-1, 0)])
                reverse_direction = tuple(element * -1 for element in direction)
                options[-1].remove(reverse_direction)

            # else - the next_spot is not valid
            else:
                # Display the wrong direction that it wants to go
                pygame.draw.line(screen, DIRECTION_COLOR, path[-1], next_spot, 1)
                pygame.draw.circle(screen, DIRECTION_COLOR, next_spot, 5)

                # Remove the wrong direction from the last spot options
                options[-1].remove(direction)

    # Refresh the pygame window to display the path
    pygame.display.flip()


pygame.quit()
