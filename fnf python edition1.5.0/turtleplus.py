from turtle import *


def setup_screen(title, color=None, image=None, x=200, y=200):
    sc = Screen()
    sc.title(title)
    if color is not None and image is None:
        sc.bgcolor(color)
    elif image is not None:
        sc.bgpic(image)
    sc.setup(x, y)
    return sc

class turtle(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.target = None  # 조준할 대상(보스 등)을 저장할 변수

    # 왼쪽 이동 + 자동 조준
    def movel(self, nom):
        self.setx(self.xcor() - nom)
        if self.target:
            self.setheading(self.towards(self.target.pos()))

    # 오른쪽 이동 + 자동 조준
    def mover(self, nom):
        self.setx(self.xcor() + nom)
        if self.target:
            self.setheading(self.towards(self.target.pos()))

    # 위로 이동 + 자동 조준
    def moveup(self, n):
        self.sety(self.ycor() + n) # forward 대신 sety 사용 (방향 고정 방지)
        if self.target:
            self.setheading(self.towards(self.target.pos()))

    # 아래로 이동 + 자동 조준
    def movedown(self, n):
        self.sety(self.ycor() - n)
        if self.target:
            self.setheading(self.towards(self.target.pos()))