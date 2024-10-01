import time
from collections import deque


def find_end(row, row_index):
    """Finds the exit of the maze.

    Args:
    row (list): The last row of the maze.
    row_index (int): The index of the last row.

    Returns:
    tuple: The coordinates of the exit cell.
    """
    # Searches final row for exit
    for i in range(0, len(row)):
        if row[i] == '-':
            return row_index - 1, i


def create_graph(maze):
    """Creates a graph of the maze.

    Args:
    maze (list): The maze to create a graph of.

    Returns:
    graph (dict): A dictionary of the nodes of the graph
    and the directions of their connections.
    """
    graph = {}
    maze_height = len(maze)
    maze_width = len(maze[0])
    # For each row
    for row_index in range(0, len(maze)):
        row = maze[row_index]
        # For each cell
        for column_index in range(0, len(row)):
            cell = row[column_index]
            if cell == '-':
                coords = (row_index, column_index)
                # Check for connections in cardinal directions to determine if node
                cardinals = [False, False, False, False]  # NESW
                openings = 0
                # North
                try:
                    if maze[row_index - 1][column_index] == '-':
                        cardinals[0] = True
                        openings += 1
                except IndexError:
                    pass
                # East
                try:
                    if maze[row_index][column_index + 1] == '-':
                        cardinals[1] = True
                        openings += 1
                except IndexError:
                    pass
                # South
                try:
                    if maze[row_index + 1][column_index] == '-':
                        cardinals[2] = True
                        openings += 1
                except IndexError:
                    pass
                # West
                try:
                    if maze[row_index][column_index - 1] == '-':
                        cardinals[3] = True
                        openings += 1
                except IndexError:
                    pass

                # If it only has 2 opposite openings it's not a node
                if openings != 2 or (not (cardinals[0] & cardinals[2]) and not (cardinals[1] & cardinals[3])):
                    graph[coords] = cardinals

    # Attach nodes
    for node in graph:
        # Connecting north node
        # If there is a node north
        if graph.get(node)[0]:
            # For each possible cell north of the node
            for i in range(1, maze_height):
                node_attempt = (node[0] - i, node[1])
                # If a node exists
                if graph.get(node_attempt) is not None:
                    # Store the new node as the north connection
                    graph[node][0] = node_attempt
                    break
        # Connecting south node
        if graph.get(node)[2]:
            for i in range(1, maze_height):
                node_attempt = (node[0] + i, node[1])
                if graph.get(node_attempt) is not None:
                    graph[node][2] = node_attempt
                    break
        # Connecting east node
        if graph.get(node)[1]:
            for i in range(1, maze_width):
                node_attempt = (node[0], node[1] + i)
                if graph.get(node_attempt) is not None:
                    graph[node][1] = node_attempt
                    break
        # Connecting west node
        if graph.get(node)[3]:
            for i in range(1, maze_width):
                node_attempt = (node[0], node[1] - i)
                if graph.get(node_attempt) is not None:
                    graph[node][3] = node_attempt
                    break
    return graph


def start_end_points(maze):
    """Finds the entrance and exit points of the maze.

    Args:
    maze (list): The maze to find the entrance and exit of.

    Returns:
    cells (tuple): The coordinates of the entrance and exit respectively."""
    # Find starting cell
    for i in range(0, len(maze[0])):
        if maze[0][i] == '-':
            start_cell = (0, i)
            break
    # Calls find_end on the last row of the maze
    end_cell = find_end(maze[-1], len(maze))

    return start_cell, end_cell


def depth_first_search(maze):
    """Performs depth first search on the maze.

    Args:
    maze (list): The maze to perform depth first search on.

    Returns:
    final_path (dict): A dictionary of the cells in the solution's path and the cells they came from.
    number of nodes (int): The number of nodes visited to find the solution.
    """
    # Setup graph
    graph = create_graph(maze)
    start_cell, end_cell = start_end_points(maze)

    # Push starting cell to frontier and explored
    explored = deque()
    frontier = deque()
    explored.append(start_cell)
    frontier.append(start_cell)
    dfs_path = {}

    # Repeat until frontier is empty or end is found
    while len(frontier) > 0:
        current_cell = frontier.pop()

        # If end of maze is found end
        if current_cell == end_cell:
            break

        # For each cardinal direction find possible child cells with priority in a south west direction.
        search_order = [0, 1, 3, 2]  # N -> E -> W -> S
        for i in search_order:
            if graph.get(current_cell)[i]:
                child_cell = graph.get(current_cell)[i]

                # If already visited skip
                if child_cell in explored:
                    continue

                # Push child cell to explored and frontier
                explored.append(child_cell)
                frontier.append(child_cell)

                # Add to path
                dfs_path[child_cell] = current_cell

    # Removes excess cells dfs visited but aren't in final solution
    final_path = {end_cell: end_cell}
    while end_cell != start_cell:
        final_path[dfs_path[end_cell]] = end_cell
        end_cell = dfs_path[end_cell]

    return final_path, len(dfs_path)


def setup(maze_path):
    """Reads the maze from a txt file and makes it easier to compute with.

    Args:
    maze_path (str): The path to the maze txt file.

    Returns:
    maze (list): The maze as a list of strings representing the rows.
    """
    # Get maze from txt file
    with open(maze_path) as f:
        maze = f.readlines()

    # Remove whitespace and new line characters
    for i in range(0, len(maze)):
        if i != len(maze) - 1:
            maze[i] = maze[i][:-1].replace(' ', '')
        else:
            maze[i] = maze[i].replace(' ', '')

    return maze


def breadth_first_search(maze):
    """Performs breadth first search on the maze.

    Args:
    maze (list): The maze to perform breadth first search on.

    Returns:
    final_path (dict): A dictionary of the cells in the solution's path and the cells they came from.
    number of nodes (int): The number of nodes visited to find the solution.
    """
    # Setup
    start_cell, end_cell = start_end_points(maze)
    graph = create_graph(maze)
    frontier = deque()
    explored = deque()
    frontier.append(start_cell)
    explored.append(start_cell)
    bfs_path = {}

    # Repeat until frontier is empty or end is found
    while len(frontier) > 0:
        # First in first out to prevent depth first search
        current_cell = frontier.popleft()

        # If end of maze is found end also
        if current_cell == end_cell:
            break

        # For each cardinal direction find possible child cells
        for i in range(0, 4):
            if graph.get(current_cell)[i]:
                child_cell = graph.get(current_cell)[i]

                # If already visited skip
                if child_cell in explored:
                    continue

                # Push child cell to explored and frontier
                explored.append(child_cell)
                frontier.append(child_cell)

                # Add to path
                bfs_path[child_cell] = current_cell

    # Formatting path
    final_path = {end_cell: end_cell}
    while end_cell != start_cell:
        final_path[bfs_path[end_cell]] = end_cell
        end_cell = bfs_path[end_cell]

    return final_path, len(bfs_path)


def visualise(maze_path, solution):
    """Displays the solution on the maze.

    Args:
    maze_path (str): The path to the maze txt file.
    solution (dict): The solution to the maze.
    """

    # Calculate intermediary points
    points = [solution[0]]
    for i in range(0, len(solution) - 1):
        # Find current and next cell
        row = solution[i][0]
        column = solution[i][1]
        next_row = solution[i + 1][0]
        next_column = solution[i + 1][1]

        # Calculate difference between current and next cell
        row_difference = next_row - row
        column_difference = next_column - column

        # Increments through rows adding points to list
        if row_difference != 0:
            if row_difference < 0:
                stride = -1
            else:
                stride = 1
            for i in range(1, row_difference + 1, stride):
                points.append(((row + i), column))

        # Increments through columns adding points to list
        if column_difference != 0:
            if column_difference < 0:
                stride = -1
            else:
                stride = +1
            for i in range(1, column_difference + 1, stride):
                points.append((row, (column + i)))

    # Get maze from txt file
    with open(maze_path) as f:
        maze = f.readlines()

    # Replaces spaces where the solution is with x's
    for row, column in points:
        row_list = list(maze[row])
        row_list[column * 2] = 'x'
        maze[row] = row_list

    # Prints maze
    for i in maze:
        for j in i:
            print(j, end='')


def main():
    '''Main function to run the program.'''
    # User terminal input
    print("Welcome to the maze solver!")
    print("Mazes are currently stored in \mazes")
    print("For access to the included mazes enter (E)asy, (M)edium, (L)arge or (V)large")
    print("Otherwise enter your own path")
    path = input("Enter the path to the maze: ")
    if path == 'E':
        path = 'mazes/maze-Easy.txt'
    elif path == 'M':
        path = 'mazes/maze-Medium.txt'
    elif path == 'L':
        path = 'mazes/maze-Large.txt'
    elif path == 'V':
        path = 'mazes/maze-VLarge.txt'
    print("Available search algorithms are: depth first search(D) and breadth first search(B)")
    while True:
        search_algorithm = input("Enter D for dfs and B for bfs: ")
        if search_algorithm == 'D' or search_algorithm == 'B':
            break

    if search_algorithm == 'D':
        returns = depth_first_search(setup(path))
    elif search_algorithm == 'B':
        returns = breadth_first_search(setup(path))


    # Get start time
    start_time = time.time()

    # Available included mazes

    #path = 'mazes/maze-Easy.txt'
    #path = 'mazes/maze-Medium.txt'
    #path = 'mazes/maze-Large.txt'
    #path = 'mazes/maze-VLarge.txt'

    # Available search algorithms

    #returns = depth_first_search(setup(path))
    #returns = breadth_first_search(setup(path))

    # Format solution
    solution = list(returns[0])
    solution.reverse()
    nodes_visited = returns[1]
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Nodes visited = ", nodes_visited)
    # Calculate steps
    steps = 1
    for i in range(0, len(solution) - 1):
        steps += abs(solution[i + 1][0] - solution[i][0]) + abs(solution[i + 1][1] - solution[i][1])
    print("Steps in final path = ", steps)
    print("The final solution: ", solution)
    visualise(path, solution)


main()
print()
input("Press enter to exit")