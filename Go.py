from graphics import *
from random import randint

gravity = .3


def collision(p1, p2, pt):
    return p1.x < pt.x < p2.x and p1.y < pt.y < p2.y


def obj_collision(p1, p2, c1, c2):
    return collision(p1, p2, c1) or collision(p1, p2, c2)


class Brick(Rectangle):
    def __init__(self, pt):
        self.p1 = Point(pt.x-5, pt.y-5)
        self.p2 = Point(pt.x+5, pt.y+5)
        super().__init__(self.p1, self.p2)
        self.velocity = randint(0, 30) / 10
        self.setFill('red')
        self.scoreval = 10


class Bonus(Brick):
    def __init__(self, pt):
        super().__init__(pt)
        self.setFill('green')
        self.scoreval = 30


class Player(Rectangle):
    def __init__(self, pt):
        self.p1 = Point(pt.x - 25, pt.y - 10)
        self.p2 = Point(pt.x + 25, pt.y + 10)
        super().__init__(self.p1, self.p2)
        self.setFill('blue')
        self.score = 0


class Game:
    def __init__(self):
        self.width = 400
        self.height = 300
        self.win = GraphWin("go", self.width, self.height)
        self.bricks = []
        self.player = Player(Point(200, 260))
        self.player.draw(self.win)
        self.scoreboard = Text(Point(30, 290), f"Score: {self.player.score}")
        self.scoreboard.draw(self.win)
        for _ in range(2):
            brick = Brick(Point(randint(20, 380), -10))
            self.bricks.append(brick)
            brick.draw(self.win)
        brick = Bonus(Point(randint(20, 380), -10))
        self.bricks.append(brick)
        brick.draw(self.win)

    def brick_move(self):
        for brick in self.bricks:
            brick.move(0, brick.velocity)
            brick.velocity += gravity
            if obj_collision(self.player.p1, self.player.p2,
                             brick.p1, brick.p2):
                self.player.score += brick.scoreval
                self.replace_brick(brick)
                self.scoreboard.setText(f"Score: {self.player.score}")
            if brick.getCenter().y > self.height:
                self.player.score -= brick.scoreval
                self.replace_brick(brick)
                self.scoreboard.setText(f"Score: {self.player.score}")

    def replace_brick(self, brick):
        brick.undraw()
        self.bricks.remove(brick)
        if type(brick) == Brick:
            new_brick = Brick(Point(randint(20, 380), -10))
            new_brick.draw(self.win)
            self.bricks.append(new_brick)
        elif type(brick) == Bonus:
            new_brick = Bonus(Point(randint(20, 380), -10))
            new_brick.draw(self.win)
            self.bricks.append(new_brick)

    def player_move(self, key):
        xpos = self.player.getCenter().x
        if key == 'Left' and 20 < xpos:
            self.player.move(-20, 0)
        elif key == 'Right' and xpos < self.width - 20:
            self.player.move(20, 0)
        elif key == 'Up' and 40 < xpos:
            self.player.move(-50, 0)
        elif key == 'Down' and xpos < self.width - 40:
            self.player.move(50, 0)

    def game_loop(self):
        while True:
            self.brick_move()
            k = self.win.checkKey()
            if k:
                self.player_move(k)


if __name__ == '__main__':
    game = Game()
    game.game_loop()

