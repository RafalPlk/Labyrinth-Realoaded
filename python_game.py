import curses

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
   | ___ \   | |               | |        | |    
   | |_/ /___| | ___   __ _  __| | ___  __| |    
   |    // _ \ |/ _ \ / _` |/ _` |/ _ \/ _` |    
   | |\ \  __/ | (_) | (_| | (_| |  __/ (_| |    
   \_| \_\___|_|\___/ \__,_|\__,_|\___|\__,_|"""



N, S, E, W = 1, 2, 3, 4

dx = {E: 1, W: -1, N: 0, S: 0}
dy = {E: 0, W: 0, N: -1, S: 1}

directions = [N, S, E, W]


# backtracking algorithm
def makeMaze(matrix):
    random.shuffle(directions)
    # todo dopisac


def makeMatrix(height, width, fillValue=1):
    return [fillValue for y in range(height) for x in range(width)]


class MenuWindow():  
    OPTION_LIST = ['Start', 'Quit']

    def __init__(self, appConfig):
        self.appConfig = appConfig
        self.option_index = 0

    def keyboard_handle(self, keypressed):
        if keypressed == curses.KEY_DOWN:
            self.option_index = (self.option_index + 1 + 2) % 2
        elif keypressed == curses.KEY_UP:
            self.option_index = (self.option_index - 1 + 2) % 2
        # You may need to check for newline (aka \n, ^J, ASCII 10) or carriage return (\r, ^M, ASCII 13).
        elif keypressed == curses.KEY_ENTER or keypressed == 10 or keypressed == 13:
            self.appConfig['currentView'] = MenuWindow.OPTION_LIST[self.option_index]

    def update_view(self, screen):
        screen.addstr(0, 0, LOGO)

        for index, option in enumerate(MenuWindow.OPTION_LIST):
            screen.addstr(10 + 2 * index, 10, option, curses.color_pair(self.option_index == index))


class Player:
    def __init__(self, max_x, max_y):
        self.x, self.y = (0, 0) 

    def setPosition(x_position, y_position):
        self.x = x_position
        self.y = y_position

    def getPosition():
        return self.x, self.y

    def attemptToChangePostionBy(x=0, y=0):
        return self.x + x, self.y + y

    def changePostionBy(x=0, y=0):
        self.x, self.y = x, y


class Maze:
    def __init__(self):
        self.maze = makeMaze(makeMatrix(50, 25))

    def isWall(xPosition, yPosition):
        return maze[yPosition][xPosition] == WALL

    def isPath():
        return maze[yPosition][xPosition] == PATH


class GameWindow():
    def __init__(self):
        self.player = Player()
        self.maze = Maze()
    
    def keyboard_handle(self):
        if keypressed == curses.KEY_DOWN:
            self.player.changePostionBy()
        elif keypressed == curses.KEY_UP:
            self.player.stepTop()
        elif keypressed == curses.KEY_LEFT:
            self.player.stepLeft()
        elif keypressed == curses.KEY_RIGHT:
            self.player.stepRight()

    def update_view(self, screen):
        screen.addstr(*self.player.getPosition(), )
        

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
            'difficultLevel': 0,
            'currentView': 'Menu'
        }

        self.dispatcher = {
            'Menu': MenuWindow(self.appConfig),
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
                window.keyboard_handle(keypressed)
                window.update_view(screen)
            else:
                keepLoop = False
                continue


if __name__ == "__main__":
    app = App()
    curses.wrapper(app.main)
