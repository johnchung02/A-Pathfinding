from time import sleep
import numpy as np
import pygame

class Node:
    def __init__(self, coordinate=None, parentNode=None):
        self.coordinate = coordinate
        self.parentNode = parentNode
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coordinate == other.coordinate
        return False

def createChildrenNodes(node, grid):
    childrenNodes = []
    
    offsets = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),         (0, 1),
               (1, -1), (1, 0), (1, 1)]
    
    for dx, dy in offsets:
        x = node.coordinate[0] + dx
        y = node.coordinate[1] + dy
        
        if x > (len(grid) - 1) or x < 0 or y > (len(grid[0]) - 1) or y < 0:
            continue
        
        if grid[x][y] == 1:
            continue
        
        childNode = Node((x,y), node)
        childrenNodes.append(childNode)

    return childrenNodes

def diagonalDistance(start, end):
    dx = abs(start[0] - end[0])
    dy = abs(start[1] - end[1])
    
    h = 1 * (dx + dy) + (np.sqrt(2) - 2 * 1) * min(dx, dy)
    return h

def returnPath(node):
    path = []
    current = node
    while current is not None:
        path.append(current.coordinate)
        current = current.parentNode
    
    return path[::-1]

def createGrid(width, length):
    probabilities = [0.8, 0.2]

    grid = np.random.choice([0, 1], size=(length, width), p=probabilities)
            
    return grid

def aStar(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 2:
                start = (i,j)
            elif grid[i][j] == 3:
                end = (i,j)
    
    openList = []
    closedList = []
    
    startNode = Node(start, None)
    startNode.g = startNode.h = startNode.f = 0
    
    openList.append(startNode)

    outIter = 0
    maxIter = 10000

    while len(openList) > 0:
        outIter += 1
        if outIter > maxIter:
            print("tooo many")
            return openList
        
        
        currentNode = min(openList, key=lambda obj: obj.f)
        
        openList.remove(currentNode)
        closedList.append(currentNode)
        
        if currentNode.coordinate == end:
            print("goal reached!")
            return returnPath(currentNode)
            
        childrenNodes = createChildrenNodes(currentNode, grid)
        for child in childrenNodes:
            restart = False
            
            for closedNode in closedList:
                if closedNode.coordinate == child.coordinate:
                    #continue to beginning of for loop (for child in childrenNodes:)
                    restart = True
                    break
                
            child.g = currentNode.g + diagonalDistance((child.coordinate[0], child.coordinate[1]), (currentNode.coordinate[0], currentNode.coordinate[1]))
            child.h = diagonalDistance((child.coordinate[0], child.coordinate[1]), (end[0], end[1]))
            child.f = child.g + child.h
                    
            for openNode in openList:
                if child.coordinate == openNode.coordinate and child.g > openNode.g:
                    restart = True
                    break
            
            if restart:
                continue
            
            openList.append(child)
                    
    return None

def updateScreen(grid):
    window.fill((255, 255, 255))
    
    for i in range(0, 10):
        for j in range(0, 10):
            if grid[i][j] == 1:
                pygame.draw.rect(window, (0,0,0), (j*100,i*100,100,100), width=0)
            elif grid[i][j] == 2:
                pygame.draw.rect(window, (0,255,0), (j*100,i*100,100,100), width=0)
            elif grid[i][j] == 3:
                pygame.draw.rect(window, (255,0,0), (j*100,i*100,100,100), width=0)
            elif grid[i][j] == 4:
                pygame.draw.rect(window, (0,0,255), (j*100,i*100,100,100), width=0)
            pygame.draw.rect(window, (0,0,0), (j*100,i*100,100,100), width=1)

    pygame.display.update()

pygame.init()

width = 1200
height = 1000

grid = np.zeros((10,10))

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding Window")
updateScreen(grid)

done = False
while not done:
    makeObstalce = True
    while makeObstalce:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] > 1000:
                    makeObstalce = False
                    continue
                
                grid[mouse[1]//100][mouse[0]//100] = 1
                
                updateScreen(grid)
        mouse = pygame.mouse.get_pos()

    choosed = 0
    makeStart = True
    while makeStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] > 1000 and choosed == 1:
                    grid = tempGrid.copy()
                    makeStart = False
                    continue
                
                elif mouse[0] < 1000:
                    tempGrid = grid.copy()
                    tempGrid[mouse[1]//100][mouse[0]//100] = 2
                    choosed = 1
                
                updateScreen(tempGrid)
        mouse = pygame.mouse.get_pos()

    choosed = 0
    makeGoal = True
    while makeGoal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] > 1000 and choosed == 1:
                    grid = tempGrid.copy()
                    makeGoal = False
                    continue
                
                elif mouse[0] < 1000:
                    tempGrid = grid.copy()
                    tempGrid[mouse[1]//100][mouse[0]//100] = 3
                    choosed = 1
                
                updateScreen(tempGrid)
        mouse = pygame.mouse.get_pos()

    path = aStar(grid)
    for i in range(len(path)):
        grid[path[i][0]][path[i][1]] = 4
        updateScreen(grid)
        sleep(0.1)

    for event in pygame.event.get(): #quit when user closes window
        if event.type == pygame.QUIT:
            done = True