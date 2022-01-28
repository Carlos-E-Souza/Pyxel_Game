from collections import deque, namedtuple
from random import randint
import pyxel

Point = namedtuple("Point", ["x", "y"])

BACKGRD_COL = 3
WIDTH = 200
HEIGHT = 200
UP = Point(0, -2)
DOWN = Point(0, 2)
RIGHT = Point(2, 0)
LEFT = Point(-2, 0)
START = Point(125, 125)
spawned = True


class Food:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.spawned = state


class Shot:
    def __init__(self, x, y, last):
        self.x = x
        self.y = y
        self.last = last


class App:
    def __init__(self):
        # Inicialize with width and height passed
        pyxel.init(WIDTH, HEIGHT, "SushiCat")
        self.reset()
        pyxel.run(self.update, self.draw)

    # Main functions: reset, update and draw

    def reset(self):
        # Load game assets like images and music
        pyxel.load("SushiCat.pyxres")
        pyxel.playm(0, loop=True)
        self.cat_x = 0
        self.cat_y = 0
        self.cat = deque()
        self.cat.append(Point(100, 100))
        self.cat.append(Point(108, 100))
        self.cat.append(Point(100, 108))
        self.cat.append(Point(108, 108))
        self.direction = RIGHT
        self.death = False
        self.food = Food(100, 100, spawned)
        self.shot = Shot(0, 0, "y")
        self.shot2 = Shot(0, 0, "x")
        self.score = 0

    def update(self):
        if not self.death:
            self.move()
            self.limits()
            self.cat_size()
            self.get_food()
            self.spawn_food()
            self.spawn_shot()
            self.kill()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def draw(self):
        if not self.death:
            pyxel.cls(BACKGRD_COL)
            self.draw_shots()
            self.draw_score()
            self.draw_food()
            self.draw_cat()
        else:
            self.draw_menu()

    def move(self):
        # Checks if buttom was pressed and update coordenates of each part of the cat
        if pyxel.btn(pyxel.KEY_UP):
            for part in range(4):
                new_y = self.cat[part].y + UP.y
                self.cat[part] = self.cat[part]._replace(y=new_y)
        elif pyxel.btn(pyxel.KEY_DOWN):
            for part in range(4):
                new_y = self.cat[part].y + DOWN.y
                self.cat[part] = self.cat[part]._replace(y=new_y)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            for part in range(4):
                new_x = self.cat[part].x + RIGHT.x
                self.cat[part] = self.cat[part]._replace(x=new_x)
            self.direction = RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT):
            for part in range(4):
                new_x = self.cat[part].x + LEFT.x
                self.cat[part] = self.cat[part]._replace(x=new_x)
            self.direction = LEFT

    def cat_size(self):
        # Define range of the images that represent the cat
        self.cat_size_x = []
        self.cat_size_y = []
        for i in range(8):
            self.cat_size_x.append(self.cat_x + i)
            self.cat_size_x.append(self.cat_x - i)
            self.cat_size_y.append(self.cat_y + i)
            self.cat_size_y.append(self.cat_y - i)

    def limits(self):
        # Define limits so the cat can't outrange the screen
        cords_x = []
        cords_y = []
        for i in range(4):
            cords_x.append(self.cat[i].x)
            self.cat_x = int(sum(cords_x)/len(cords_x))
            cords_y.append(self.cat[i].y)
            self.cat_y = int(sum(cords_y)/len(cords_y))

        if (self.cat_x <= 8 or self.cat_x >= 200 or self.cat_y <= 8 or self.cat_y >= 200):
            pyxel.quit()

    def spawn_food(self):
        if self.food.spawned:
            pass
        else:
            self.food.x = randint(10, WIDTH-10)
            self.food.y = randint(10, HEIGHT-10)
            self.food.spawned = True

    def get_food(self):
        if self.food.x in self.cat_size_x and self.food.y in self.cat_size_y:
            self.score += 5
            self.food.spawned = False

    def spawn_shot(self):
        if self.shot.last == "y":
            if self.shot.y < HEIGHT:
                self.shot.y += 4
            else:
                self.shot = Shot(0, randint(10, HEIGHT-10), "x")
        elif self.shot.last == "x":
            if self.shot.x < WIDTH:
                self.shot.x += 4
            else:
                self.shot = Shot(randint(10, WIDTH-10), 0, "y")

        if self.shot2.last == "y":
            if self.shot2.y < HEIGHT:
                self.shot2.y += 4
            else:
                self.shot2 = Shot(0, randint(10, HEIGHT-10), "x")
        elif self.shot2.last == "x":
            if self.shot2.x < WIDTH:
                self.shot2.x += 4
            else:
                self.shot2 = Shot(randint(10, WIDTH-10), 0, "y")

    def kill(self):
        shot_size_x, shot_size_y, shot2_size_x, shot2_size_y = [], [], [], []
        for i in range(2):
            shot_size_x.append(self.shot.x + i)
            shot_size_x.append(self.shot.x - i)
            shot_size_y.append(self.shot.y + i)
            shot_size_y.append(self.shot.y - i)
            shot2_size_x.append(self.shot2.x + i)
            shot2_size_x.append(self.shot2.x - i)
            shot2_size_y.append(self.shot2.y + i)
            shot2_size_y.append(self.shot2.y - i)

        for i in range(4):
            if shot_size_x[i] in self.cat_size_x and shot_size_y[i] in self.cat_size_y:
                self.death = True
            elif shot2_size_x[i] in self.cat_size_x and shot2_size_y[i] in self.cat_size_y:
                self.death = True

    def draw_score(self):
        pyxel.rectb(80, 0, int(len(f"Score:{self.score}")*4.5), 8, 5)
        pyxel.text(81, 1, f"Score:{self.score}", 7)

    def draw_shots(self):
        if self.shot.last == "x":
            pyxel.blt(self.shot.x, self.shot.y, 0, 16, 232, 8, 8, 13)
        else:
            pyxel.blt(self.shot.x, self.shot.y, 0, 24, 232, 8, 8, 13)

        if self.shot2.last == "x":
            pyxel.blt(self.shot2.x, self.shot2.y, 0, 16, 232, 8, 8, 13)
        else:
            pyxel.blt(self.shot2.x, self.shot2.y, 0, 24, 232, 8, 8, 13)

    def draw_food(self):
        if self.food.spawned:
            pyxel.blt(self.food.x, self.food.y, 0, 24, 248, 8, 8, 13)

    def draw_cat(self):
        if self.direction == LEFT:
            pyxel.blt(self.cat[0].x, self.cat[0].y, 0, 0, 240, 8, 8, 13)
            pyxel.blt(self.cat[1].x, self.cat[1].y, 0, 8, 240, 8, 8, 13)
            pyxel.blt(self.cat[2].x, self.cat[2].y, 0, 0, 248, 8, 8, 13)
            pyxel.blt(self.cat[3].x, self.cat[3].y, 0, 8, 248, 8, 8, 13)
        elif self.direction == RIGHT:
            pyxel.blt(self.cat[0].x, self.cat[0].y, 0, 0, 224, 8, 8, 13)
            pyxel.blt(self.cat[1].x, self.cat[1].y, 0, 8, 224, 8, 8, 13)
            pyxel.blt(self.cat[2].x, self.cat[2].y, 0, 0, 232, 8, 8, 13)
            pyxel.blt(self.cat[3].x, self.cat[3].y, 0, 8, 232, 8, 8, 13)

    def draw_menu(self):
        pyxel.cls(8)
        pyxel.text(80, 80, "GAME OVER,", 7)
        pyxel.text(80, 90, f"SCORE:{self.score},", 7)
        pyxel.text(80, 100, "(Q)QUIT,", 7)
        pyxel.text(80, 110, "(R)RESTART", 7)


# pyxel run testes.py
App()
