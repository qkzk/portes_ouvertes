import pgzrun
from pprint import pprint
from random import sample
from time import time

# Globals
TITLE = "   Mine sweeper"

# dimensions
TILE = 30
MAP_WIDTH = 20
MAP_HEIGHT = 14
WIDTH = TILE * MAP_WIDTH
UI_HEIGHT = 60
HEIGHT = TILE * MAP_HEIGHT + UI_HEIGHT

NB_BOMBS = 40


class Color:
    HIDDEN_EVEN = (64, 180, 32)
    HIDDEN_ODD = (90, 200, 48)
    # ZERO_EVEN = (64, 32, 180)
    # ZERO_ODD = (90, 48, 200)
    ZERO_EVEN = (130, 120, 80)
    ZERO_ODD = (150, 148, 100)
    NEIGHBOR_BOMB_EVEN = (130, 120, 80)
    NEIGHBOR_BOMB_ODD = (150, 148, 100)
    BOMB_EVEN = (180, 32, 64)
    BOMB_ODD = (200, 48, 90)
    UI = (24, 75, 10)


def color_number(number):
    '''
    attributes a color to every possible number of surrounding bombs
    '''
    return (int(255/8 * number), 32, int(255 - 255/8*number))


def time_format(t):
    '''
    format the time like 012
    '''
    t = int(t)
    if t >= 999:
        t = 999
    return f"{t:03d}"


class Ui:
    '''
    Class for the Ui.
    Displayed at the top of the screen.
    It shows
        * the number of remaining flags,
        * the elapsed time
        * a colored message if the game is finished
    If the game is over, it can be clicked to start again.
    '''

    def __init__(self, nb_bombs, difficulty="moyen"):
        self.bombs = nb_bombs
        self.flag = 0
        self.difficulty = difficulty
        self.curr_time = time()  # starting time of the game

    def set_curr_time(self):
        '''
        set the current time
        '''
        self.curr_time = time()

    def draw(self, screen, tile_map):
        '''
        clear and redraw the ui
        '''
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, UI_HEIGHT)),
                                Color.UI,)
        self._draw_flags(screen, tile_map)
        self._draw_time(screen, tile_map)
        self._draw_endgame(screen, tile_map)

    def _draw_flags(self, screen, tile_map):
        '''
        Draw the remaining flags
        '''
        screen.draw.text(f"F : {str(tile_map.flag_number)}",
                         topleft=(WIDTH * 0.3,
                                  TILE // 2),
                         color="red", fontsize=40)

    def _draw_time(self, screen, tile_map):
        '''
        draw the elapsed time
        '''
        elapsed_string = time_format(self.curr_time - tile_map.started_time)
        screen.draw.text(f"T : {elapsed_string}",
                         topleft=(WIDTH * 0.5,
                                  TILE // 2),
                         color="yellow", fontsize=40)

    def _draw_endgame(self, screen, tile_map):
        '''
        endgame message ("gg" if won, "you died" otherwize)
        the whole UI can be clicked to start again
        '''
        if tile_map.finished:
            msg = "gg" if tile_map.won else "you died"
            color = "cyan" if tile_map.won else "magenta"
            screen.draw.text(msg,
                             topleft=(WIDTH * 0.05,
                                      TILE // 2),
                             color=color, fontsize=40)
            screen.draw.text('click here to \n play again',
                             topleft=(WIDTH * 0.7,
                                      TILE // 4),
                             color="magenta", fontsize=30)


class Tile:
    '''
    Manage a single tile
    '''

    def __init__(self, x, y, neighbors_bomb,
                 bomb, color='white'):
        self.x = x
        self.y = y
        self.neighbors_bomb = neighbors_bomb
        self.bomb = bomb
        self.color = color
        self.revealed = False
        self.flag = False
        self.incorrect = False

    def draw(self, screen):
        '''
        Draw the tile in alterning color
        and it's content if it must be shown
        '''
        start_height = self.y * TILE + UI_HEIGHT
        screen.draw.filled_rect(
            Rect((self.x * TILE, start_height), (TILE, TILE)),
            self.color)
        if self.revealed and not self.bomb\
                and self.neighbors_bomb != 0 and not self.incorrect:
            self.draw_neighboors(start_height)
        if self.flag and not self.revealed:
            self.draw_flag(start_height)
        if self.bomb and self.revealed:
            self.draw_bomb(start_height)
        if self.incorrect:
            self.draw_incorrect(start_height)

    def draw_neighboors(self, start_height):
        '''
        Draw the number of bombs in neighborhood
        '''
        screen.draw.text(str(self.neighbors_bomb),
                         topleft=(self.x * TILE + 0.25 * TILE,
                                  start_height + 0.25 * TILE),
                         color=color_number(self.neighbors_bomb), alpha=0.8,)

    def draw_flag(self, start_height):
        '''
        Draw an F for the flag
        '''
        screen.draw.text("F",
                         topleft=(self.x * TILE + 0.25 * TILE,
                                  start_height + 0.25 * TILE),
                         color="red", alpha=0.8,)

    def draw_incorrect(self, start_height):
        '''
        Draw an X for the incorrect flag
        '''
        screen.draw.text("X",
                         topleft=(self.x * TILE + 0.25 * TILE,
                                  start_height + 0.25 * TILE),
                         color="red",)

    def draw_bomb(self, start_height):
        '''
        Draw the bomb
        '''
        screen.draw.filled_circle((self.x * TILE + 0.5 * TILE,
                                   start_height + 0.5 * TILE),
                                  int(0.35 * TILE), "black")

    def reveal(self):
        '''
        reveal a tile
        change the attribute (revealed) and the color of the tile
        '''
        self.revealed = True
        if self.bomb:
            self.color = Color.BOMB_EVEN if (
                self.x + self.y) % 2 == 0 else Color.BOMB_ODD
        elif self.neighbors_bomb == 0:
            self.color = Color.ZERO_EVEN if (
                self.x + self.y) % 2 == 0 else Color.ZERO_ODD
        elif self.incorrect:
            self.color = "black"
        else:
            self.color = Color.NEIGHBOR_BOMB_EVEN if (
                self.x + self.y) % 2 == 0 else Color.NEIGHBOR_BOMB_ODD


class TileMap:
    '''
    Manages the tilemap and the game
    '''

    def __init__(self, nb_bombs):
        self.nb_bombs = nb_bombs
        self.tile_map = self._create_tile_map(nb_bombs)
        self.flag_number = nb_bombs
        self.remaining_tiles = MAP_WIDTH * MAP_HEIGHT - nb_bombs
        self.finished = False
        self.won = None
        self.started_time = time()

    def draw(self, screen):
        '''
        draw the whole tile map
        '''
        for i in range(len(self.tile_map)):
            for j in range(len(self.tile_map[0])):
                self.tile_map[i][j].draw(screen)

    def _reveal_all(self):
        '''
        reveal the whole tilemap. used when the player lost
        '''
        for row in self.tile_map:
            for tile in row:
                if tile.flag and not tile.bomb:
                    tile.incorrect = True
                tile.reveal()

    def print_bomb(self):
        '''
        print the tilemap with 1 if there's a bomb and 0 otherwize
        '''
        for j in range(len(self.tile_map[0])):
            for i in range(len(self.tile_map)):
                print(1 if self.tile_map[i][j].bomb else 0, end=' ')
            print()

    def print_neighbors(self):
        '''
        print the tilemap with the number of surrounding bombs
        '''
        for j in range(len(self.tile_map[0])):
            for i in range(len(self.tile_map)):
                print(self.tile_map[i][j].neighbors_bomb, end=' ')
            print()

    def _create_tile_map(self, nb_bombs):
        '''
        creates the tile map.
        '''
        bombs = self._position_bombs(nb_bombs)
        map = []
        for i in range(MAP_WIDTH):
            row = []
            for j in range(MAP_HEIGHT):
                bool_bomp = True if i * MAP_HEIGHT + j in bombs else False
                color = Color.HIDDEN_EVEN if (i+j) % 2 == 0\
                    else Color.HIDDEN_ODD
                row.append(Tile(i, j, None, bool_bomp, color=color))
            map.append(row)
        for i in range(MAP_WIDTH):
            for j in range(MAP_HEIGHT):
                tile = map[i][j]
                tile.neighbors_bomb = self._calculate_neighbors(i, j, map)
        return map

    def _calculate_neighbors(self, i, j, map):
        '''
        calculate the surrounding neighbors
        '''
        neighbors = self._extract_neighbors(i, j, map)
        return sum([1 for neighbor in neighbors if neighbor.bomb])

    def _extract_neighbors(self, i, j, map):
        '''
        extract the surrouning neighbors (cross and corners)
        '''
        neighbors = []
        for k in (-1, 0, 1):
            for l in (-1, 0, 1):
                if ((k != 0 or l != 0) and
                    (0 <= i + k < len(map)) and
                        (0 <= j + l < len(map[0]))):
                    neighbors.append(map[i + k][j + l])
        return neighbors

    def _position_bombs(self, nb_bombs):
        '''
        place the bombs on the tilemap. python is the bomb
        '''
        return sorted(sample(range(MAP_WIDTH * MAP_HEIGHT), nb_bombs))

    def click(self, pos, button):
        '''
        what to do when a tile is clicked
        Left : reveal and explore the surroundings if it's a zero
        Right : toggle a flag on the tile and change the flag counter
        '''
        print("Mouse button", button, "clicked at", pos)
        i, j = self._get_tile(pos)
        print(i, j)
        tile = self.tile_map[i][j]

        if button == mouse.LEFT:
            if not tile.revealed and tile.bomb:
                self._game_over()
                return
            self._explore(i, j)
        if button == mouse.RIGHT:
            delta = 1 if tile.flag else - 1
            self.flag_number += delta
            if self.flag_number <= 0:
                self.flag_number = 0
            tile.flag = not tile.flag

    def _game_over(self):
        '''
        if the game is lost
        '''
        self.finished = True
        self.won = False
        self._reveal_all()

    def check_victory(self):
        '''
        the game is won when remaining_tiles reach 0
        this counter starts at (nb of tiles - nb of bombs).
        It decreases every time a tile is revealed
        The only way it can reaches 0 is if all tiles has been revealed
            and the player is still alive.
        '''
        if self.remaining_tiles == 0:
            self.finished = True
            self.won = True

    def _get_tile(self, pos):
        '''
        get the coords of a tile from the position clicked
        '''
        x, y = pos
        return x//TILE, (y - UI_HEIGHT)//TILE

    def _explore(self, i, j, keep=True):
        '''
        reveal a tile and explore the surrouning
        TODO : problemes avec certains coins...
        TODO : refactorer, séparer en 2 fonctions au moins
        '''
        tile = self.tile_map[i][j]
        tile.reveal()
        self.remaining_tiles -= 1
        if keep:
            cross_tile = []
            for k, l in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= i + k < MAP_WIDTH and 0 <= j + l < MAP_HEIGHT:
                    tile = self.tile_map[i + k][j + l]
                    if not tile.revealed and not tile.bomb:
                        # we stop exploring if a bomb is in the neighborhood
                        if tile.neighbors_bomb == 0:
                            keep = True
                        else:
                            keep = False
                        self._explore(i + k, j + l, keep=keep)
            # explore the corners if we reached a wall
            for k, l in ((-1, -1), (1, 1), (-1, 1), (1, -1)):
                if 0 <= i + k < MAP_WIDTH and 0 <= j + l < MAP_HEIGHT:
                    tile = self.tile_map[i + k][j + l]
                    if not tile.revealed and not tile.bomb:
                        self._explore(i + k, j + l, keep=False)


def draw():
    '''
    called to refresh the screen
    clear and draw elements
    '''
    screen.clear()
    tile_map.draw(screen)
    ui.draw(screen, tile_map)


def on_mouse_down(pos, button):
    '''
    event clic :
    * on the tilemap : reveal
    * on the UI and game is finished : play again
    '''
    x, y = pos
    if y >= UI_HEIGHT:
        tile_map.click(pos, button)
    elif tile_map.finished:
        init_game()


def update():
    '''
    update : 60 times a second
    change the time in the UI
    '''
    if not tile_map.finished:
        ui.set_curr_time()
        tile_map.check_victory()


def init_game():
    '''
    initialize the elements
    '''
    global nb_bombs, tile_map, ui
    nb_bombs = NB_BOMBS
    tile_map = TileMap(nb_bombs)
    ui = Ui(nb_bombs)
    # tile_map.print_bomb()
    # print()
    # tile_map.print_neighbors()

    # randomly choose a 0 tile to begin with
    zeros = [(i, j) for i in range(MAP_WIDTH)
             for j in range(MAP_HEIGHT)
             if tile_map.tile_map[i][j].neighbors_bomb == 0
             and not tile_map.tile_map[i][j].bomb]
    if len(zeros) > 0:
        first_click = sample(zeros, 1)[0]
        tile_map._explore(*first_click)


# game initialisation
# globals
# we have to do it since we'll reset them later from a function
nb_bombs, tile_map, ui = (None, None, None)
init_game()
pgzrun.go()
