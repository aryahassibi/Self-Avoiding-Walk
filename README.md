# Self-Avoiding Walk

A self-avoiding walk is a path from one point to another that never intersects itself. Such paths are usually considered to occur on lattices, so that steps are only allowed in a discrete number of directions and of certain lengths. [Wolfram Mathworld](https://mathworld.wolfram.com/Self-AvoidingWalk.html)

Written in [python](https://www.python.org) (3.7.6), using [pygame library](https://www.pygame.org) (2.0.1)  

<p align="center">
    <b>💡 Press SPACE if you want to create another self-avoiding path or if you want to pause the program.</b>
</p>

I have commented each file as best as I can, so If you want to know more about how each version of my self-avoiding walk works check the python files and read the comments. Now I'm gonna briefly explain the main differences between the versions here.

Ver | Preview  | Description 
:------:|:-------:|------------
1 | ![Self-Avoiding Walk Version 1 GIF](https://user-images.githubusercontent.com/31355913/128322453-8d890b94-6201-4bb3-85e9-bbd530aa102d.gif) | I used three Lists(arrays) to store the properties of each point on the path. All of the spots on the path are stored in ***path***. The direction that a spot takes is stored in the corresponding index of ***directions***. The available options for a post on the path are stored in the corresponding index of ***options***. The program chooses a valid spot randomly to start the path. Then It chooses an available direction randomly and continues until it is stuck. If it is stuck it steps back until it reaches a spot where it can try another direction. The program continues the process until it finds a path that fills the grid.
2 | ![Self-Avoiding Walk Version 2 GIF](https://user-images.githubusercontent.com/31355913/128322721-9569cb7f-ffa2-40b3-bf51-5af8e5f2ab8d.gif) | Instead of storing the properties of each spot in lists I created a class called ***spot*** and stored the position, available options, direction, and other properties of a spot in the class. then I created a 2-dimensional list called ***grid*** and put all of the spots in it. and another 1-dimensional grid called  ***path*** to store the used spot in the path. I used the same algorithm as the first version to find a path.
3 | ![Self-Avoiding Walk Version 3 GIF](https://user-images.githubusercontent.com/31355913/128321482-8b2844ee-0811-47d7-91df-e091a084b917.gif) | For the third version I used the same ***Spot*** class I used in the second version but I changed the algorithm. Instead of going to new spots normally to create a path I used a recursive function to do it.

</br>

## Choosing the first spot randomly
The program chooses the first spot randomly, but then I found out that sometimes it is impossible to create a self-avoiding path. If the number of rows and columns of the grid are odd numbers, and one of the x-coordinate or y-coordinate of the first point is an even number and the other one is an odd number, then it is impossible to create a self-avoiding path. 



Now to prove this draw a grid with an odd number of rows and columns, let's say a 3 x 3 grid. Then color cells or spot that one of the x-coordinate or y-coordinate of them is an even number and the other one is an odd number, like (1, 2) or (3, 2). If you do this then you should be seeing a 3x3 grid with a check pattern, like this | ![3 by 3 grid with check pattern](https://user-images.githubusercontent.com/31355913/128355641-1c06e2cf-c191-48ab-bb67-a03f70590a6f.png)
:-------|:-------:
**In other words you can number the cells/spots like this, and color the even cells (in this case 2, 4, 6, 8)**| ![3 by 3 grid with check pattern](https://user-images.githubusercontent.com/31355913/128355648-67f01410-61bd-4a2d-beb0-37fde44d56e3.png)

1. The length of a path is equal to the number of rows time the number of columns minus 1 (row x cols - 1), so for a 3 by 3 grid the length of a self-avoiding path would be 8. You can also conclude that *the length of the s-a path will be even for a grid with an odd number of rows and cols.*
2. Every step you take on the grid, you either step on an even/black cell from an odd/white cell or vise versa. Therefore your second step will be on a cell with the same color as the cell you started.

Based on these statements (1, 2) in an odd by odd grid if you start on a white cell you will end up on a white cell after getting to the end of your self-avoiding walk and you should end up on a black cell if you start on a black cell, but there is a problem. in an odd by odd grid, the number of black/even cells is always one less than the number of white/odd cells.** Ss stated before the length of the path is n x m - 1, so if you start on a black cell and finish on a black cell it means that you have stepped on ((n x m - 1) / 2) + 1 = (n x m + 1) / 2 = (3 x 3 + 1) / 2 = 5 black cells but there are only (n x m - 1) / 2 = (3 x 3 - 1) / 2 = 4 black cells. So, it is impossible to start on a black cell and finish on a black cell. Therefore, it is impossible to create a self-avoiding path that starts on a black cell(in an (odd x odd) grid).

##
> ** </br>
For a  (n x m)  gird (which n and m are odd numbers) </br>
the number of black cells is equal to (n x m - 1) / 2 </br>
the number of white cells is equal to (n x m + 1) / 2
