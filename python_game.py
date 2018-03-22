import curses
import random
import time
import datetime
# app = {
#     'menu': {
#         'option_index': 0,
#     },
#     'difficult_level_chooser': {
#         'option_index': 0,
#     },
#     'game': {
#         'czas': None,
#         'labirynt': None,
#         'player': {
#             'x': 0,
#             'y': 0
#          },
#         'key': None,
#         'przeciwnicy': None
#     },
#     'menu2': {
#         'option_index': 0,
#     },
#     'is_active': True,
#     'current_window': 'menu',
#     'key_pressed': None,
#     'screen': None
# }

WALL = 1
PATH = 0

LOGO = """
 _           _     _                  _   _      
| |         | |   (_)                | | | |     
| |     __ _| |__  _ _ __ _   _ _ __ | |_| |__   
| |    / _` | '_ \| | '__| | | | '_ \| __| '_ \  
| |___| (_| | |_) | | |  | |_| | | | | |_| | | | 
\_____/\__,_|_.__/|_|_|   \__, |_| |_|\__|_| |_| 
                           __/ |                 
                          |___/                  
   ______     _                 _          _     
   | ___ \   | |               | |        | |TM.
   | |_/ /___| | ___   __ _  __| | ___  __| |    
   |    // _ \ |/ _ \ / _` |/ _` |/ _ \/ _` |    
   | |\ \  __/ | (_) | (_| | (_| |  __/ (_| |    
   \_| \_\___|_|\___/ \__,_|\__,_|\___|\__,_|"""


N, S, E, W = 1, 2, 3, 4

dx = {E: 1, W: -1, N: 0, S: 0}
dy = {E: 0, W: 0, N: -1, S: 1}

directions = [N, S, E, W]

# wyrzuc
WIDTH = 50
HEIGHT = 25

NEIGHBORS = { 
    N: [(0, 1), (0, -1), (-1, 0)],
    S: [(0, 1), (0, -1), (1, 0)],
    E: [(0, 1), (-1, 0), (1, 0)],
    W: [(0, -1), (-1, 0), (1, 0)],
}


def isNeighborsCellAreEmpty(matrix, direction, y, x):
    return any([not matrix[y + dy][x + dx] for dy, dx in NEIGHBORS[direction]])


def fillMaze(matrix, y, x):
    random.shuffle(directions)

    for direction in directions:
        matrix[y][x] = 0

        new_y = y + dy[direction]
        new_x = x + dx[direction]

        if 0 < new_x < WIDTH - 1 and 0 < new_y < HEIGHT - 1:
            if isNeighborsCellAreEmpty(matrix, direction, new_y, new_x,):
                continue
            
            fillMaze(matrix, new_y, new_x)


# backtracking algorithm
def makeMaze(matrix):
    fillMaze(matrix, len(matrix) - 1, len(matrix[0]) - 2)
    return matrix


def makeMatrix(height, width, fillValue=1):
    return [[fillValue for y in range(height)] for x in range(width)]

class Key:
    def __init__(self, xPosition, yPosition):
        self.x = xPosition
        self.y = yPosition
        self.visible = True

    def getPosition(self):
        return self.x, self.y

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def draw(self, screen):
        screen.addstr(self.y, self.x, " k"[self.visible])


class Player:
    def __init__(self, xPosition, yPosition):
        self.x = xPosition
        self.y = yPosition
        self.lastPosition = [self.x, self.y]

    def getPosition(self):
        return self.x, self.y

    def restorePosition(self):
        self.x, self.y = self.lastPosition

    def changePostionBy(self, x=0, y=0):
        self.lastPosition = [self.x, self.y]
        self.x += x 
        self.y += y

    def draw(self, screen):
        screen.addstr(self.y, self.x, "x")


class Maze:
    def __init__(self):
        self.maze = makeMaze(makeMatrix(50, 25))
        self.height = len(self.maze)
        self.width = len(self.maze[0])

    def isWall(self, xPosition, yPosition):
        return self.maze[yPosition][xPosition] == WALL

    def openPassage(self):
        self.maze[self.height - 1][self.width - 2] = PATH

    def closePassage(self):
        self.maze[self.height - 1][self.width - 2] = WALL

    def getPassagePostion(self):
            return self.height - 1, self.width - 2

    def getRandomPosition(self):
        avaiblePositions = [(x, y) for y, row in enumerate(self.maze) for x, element in enumerate(row) if not self.maze[y][x]]
        return random.choice(avaiblePositions)

    def draw(self, screen, fogOfWarPosition):
        x, y = fogOfWarPosition
        
        for j in range(HEIGHT):
            screen.addstr(j, 0, " █"[self.maze[j][0]]) 
            screen.addstr(j, WIDTH-1, " █"[self.maze[j][WIDTH-1]]) 
   
        for i in range(WIDTH):
            screen.addstr(0, i, " █"[self.maze[0][i]]) 
            screen.addstr(HEIGHT-1, i, " █"[self.maze[HEIGHT-1][i]]) 

        for j in range(y-4, y+5): 
            for i in range(x-8, x+9):
                if 0 < j < self.height and 0 < i < self.width:
                    screen.addstr(j, i, " █"[self.maze[j][i]]) 


class Timer():
    def __init__(self, timer):
        self.timer = timer
        self.last_time = datetime.datetime.now()
        
    def draw(self, screen):
        mins, secs = divmod(self.timer, 60)
        timeformat = 'Pozostały czas: {:02d}:{:02d}'.format(mins, secs)
        screen.addstr(0, 51, timeformat)

        if (datetime.datetime.now() - self.last_time).total_seconds() > 1:
            self.last_time = datetime.datetime.now()
            self.timer -= 1

    def isTimeout(self):
        return not self.timer
        

class MenuWindow():  
    OPTION_LIST = ['Start', 'Quit']

    def __init__(self, appConfig):
        self.appConfig = appConfig
        self.option_index = 0

    def keyboardHandle(self, keypressed):
        if keypressed == curses.KEY_DOWN:
            self.option_index = (self.option_index + 1 + 2) % 2
        elif keypressed == curses.KEY_UP:
            self.option_index = (self.option_index - 1 + 2) % 2
        elif keypressed == curses.KEY_ENTER or keypressed == 10 or keypressed == 13:
            self.appConfig['currentView'] = MenuWindow.OPTION_LIST[self.option_index]

    def updateView(self, screen):
        screen.addstr(0, 0, LOGO)

        for index, option in enumerate(MenuWindow.OPTION_LIST):
            screen.addstr(20 + 2 * index, 20, option, curses.color_pair(self.option_index == index))


class GameWindow():
    def __init__(self, appConfig):
        self.appConfig = appConfig
        self.maze = Maze()
        self.player = Player(*self.maze.getRandomPosition())
        self.key = Key(*self.maze.getRandomPosition())
        self.timer = Timer(240)

        self.maze.closePassage()
        
    def keyboardHandle(self, keypressed):
        if keypressed == curses.KEY_DOWN:
            self.player.changePostionBy(y=1)
        elif keypressed == curses.KEY_UP:
            self.player.changePostionBy(y=-1)
        elif keypressed == curses.KEY_LEFT:
            self.player.changePostionBy(x=-1)
        elif keypressed == curses.KEY_RIGHT:
            self.player.changePostionBy(x=1)
        elif keypressed == ord('q'):
            self.appConfig['currentView'] = 'Menu'
    
    def preprocess(self):
        if self.maze.isWall(*self.player.getPosition()):
            self.player.restorePosition()

        if self.key.getPosition() == self.player.getPosition():
            self.key.hide()
            self.maze.openPassage()

        if self.timer.isTimeout():
            self.appConfig['currentView'] = 'Menu'

    def updateView(self, screen):
        self.preprocess()

        self.maze.draw(screen, self.player.getPosition())
        self.timer.draw(screen)
        self.key.draw(screen)
        self.player.draw(screen)

     
class End():
    def __init__(self):
        pass
    
    def keyboard_handle(self):
        pass

    def update_view(self):
        pass


class App:
    def __init__(self):
        self.appConfig = {
            'currentView': 'Menu',
            'keyFound': False
        }

        self.dispatcher = {
            'Menu': MenuWindow(self.appConfig),
            'Start': GameWindow(self.appConfig),
            'Quit': None
        }

    def main(self, screen):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(0)

        screen.timeout(100)

        keepLoop = True
        while keepLoop:
            keypressed = screen.getch()
            window = self.dispatcher[self.appConfig['currentView']]

            if window:
                screen.clear()
                window.keyboardHandle(keypressed)
                window.updateView(screen)
            else:
                keepLoop = False
                continue


if __name__ == "__main__":
    app = App()

    try:
        curses.wrapper(app.main)
    except KeyboardInterrupt:
        exit()
