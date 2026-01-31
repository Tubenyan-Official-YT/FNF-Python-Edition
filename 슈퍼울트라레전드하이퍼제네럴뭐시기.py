import time
from turtle import *
from turtleplus import *
import pygame as pg
from easyfile import *
import random as r
from tkinter import filedialog, Tk, Button, Label, messagebox, Entry, Toplevel
from PIL import Image
from pathlib import *

speed=int(input('화살표의 속도를 정하세요. 정수만 입력하세요: '))

sc=setup_screen('프나펑 파이썬판!', '#000000', None, 1600,800)
sc.tracer(0)
sc.update()
cv=sc.getcanvas().winfo_toplevel()
cv.withdraw()
enemyarrows=[]
file=["", "","","","",""] # 파일리스트 만들기
def onbtn(num:int):
    path = filedialog.askopenfilename()
    if path:
        file[num] = path
        messagebox.showinfo('안내', '정상적 업로드 완료!')

def startgame():
    try:
        if all(file):
            global enemyname, fold
            enemyname = Path(file[4]).stem
            fold=Path(file[4]).parent
            for i in range(1, 5):
                p = f"{fold}/{enemyname}{i}.png"
                img = Image.open(p).convert("RGBA").resize((300, 300), Image.LANCZOS)
                img.save(p)
                sc.addshape(p)
            p = f"{fold}/{enemyname}.png"
            img = Image.open(p).convert("RGBA").resize((300, 300), Image.LANCZOS)
            img.save(p)
            sc.addshape(p)
            window.withdraw()
            main()
            window.withdraw()
            cv.deiconify()
    except FileNotFoundError or IndexError:
        messagebox.showerror('오류! 오류! 오류! 파일이 없습니다!', '파일을 찾을 수 없습니다. '
        '\n 파일을 모두 제대로 올려주시길 바랍니다',icon='error')


def on_btn_5():
    messagebox.showinfo('올리기 안내', '올린 한 캐릭터의 모션들이 다 같은 폴더에 위치해야 하며'
    '\n동작 모션 이름은 대기모션이름1, 대기모션이름2.png 이런 형식으로 되어 있어야 합니다.\n'
    '확장자는 png로 해야 합니다. 정상적 업로드 부탁드립니다.')
    path = filedialog.askopenfilename(filetypes=[('PNG 이미지 파일','*.png')])
    if path:
        file[4] = path
        messagebox.showinfo('안내',' 정상적으로 사진업로드가 완료 되었습니다.')

# 저장 파일을 줄바꿈 단위로 나눠 읽기
fi=allread('assets/saves.txt')
fi = fi.split('\n')

def savefile(): # 파일로 곡 저장하기
    e = Entry(window, width=30)
    e.grid(row=4, column=4)
    e.insert(0, "노래 이름 입력")

    def real_save():
        song_name = e.get()
        if all(file[:6]):
            data = f"{song_name} {file[0]} {file[1]} {file[2]} {file[3]} {file[4]} {file[5]}"
            listappend_file('assets/saves.txt', data)
            messagebox.showinfo('안내', f'[{song_name}]을 정상적으로 저장했습니다.')
            e.destroy()
            btn.destroy()
        else:
            messagebox.showerror('에러! 에러!', '파일이 업로드 되지 못했습니다.')
    btn = Button(window, text='확인', command=real_save)
    btn.grid(row=5, column=4)
openernum, n=0,0
def opening():
    global opener, fi
    fi=allread('assets/saves.txt').split('\n')
    opener=Toplevel(window)
    opener.geometry('300x300')
    global openernum
    for i in range(12-len(fi)):
        fi.append('        ')
    try:
        Button(opener, text=f'{fi[0].split(" ")[0]}', command=lambda: fileopener(0)).grid(row=0, column=0)
        Button(opener, text=f'{fi[1].split(" ")[0]}', command=lambda: fileopener(1)).grid(row=0, column=1)
        Button(opener, text=f'{fi[2].split(" ")[0]}', command=lambda: fileopener(2)).grid(row=0, column=2)
        Button(opener, text=f'{fi[3].split(" ")[0]}', command=lambda: fileopener(3)).grid(row=1, column=0)
        Button(opener, text=f'{fi[4].split(" ")[0]}', command=lambda: fileopener(4)).grid(row=1, column=1)
        Button(opener, text=f'{fi[5].split(" ")[0]}', command=lambda: fileopener(5)).grid(row=1, column=2)
        Button(opener, text=f'{fi[6].split(" ")[0]}', command=lambda: fileopener(6)).grid(row=2, column=0)
        Button(opener, text=f'{fi[7].split(" ")[0]}', command=lambda: fileopener(7)).grid(row=2, column=1)
        Button(opener, text=f'{fi[8].split(" ")[0]}', command=lambda: fileopener(8)).grid(row=2, column=2)
        Button(opener, text=f'{fi[9].split(" ")[0]}', command=lambda: fileopener(9)).grid(row=3, column=0)
        Button(opener, text=f'{fi[10].split(" ")[0]}', command=lambda: fileopener(10)).grid(row=3, column=1)
        Button(opener, text=f'{fi[11].split(" ")[0]}', command=lambda: fileopener(11)).grid(row=3, column=2)
    except:
        messagebox.showerror('에러 ! 에러!', '버튼생성불가')
def fileopener(num: int):
    file[0] = fi[num].split(' ')[1]
    file[1] = fi[num].split(' ')[2]
    file[2] = fi[num].split(' ')[3]
    file[3] = fi[num].split(' ')[4]
    file[4] = fi[num].split(' ')[5]
    file[5] = fi[num].split(' ')[6]
    opener.destroy()

status=None
arrow_list=[]
pg.mixer.init()
score=50
miss=0

drawer=turtle()
drawer.hideturtle()
drawer.pencolor('white')
misser=turtle()
misser.hideturtle()
misser.pencolor('white')

lefter=turtle()
downer=turtle()
uper=turtle()
righter=turtle()
lines= {'left':lefter, 'down':downer, 'up':uper, 'right':righter}

leftere=turtle()
downere=turtle()
upere=turtle()
rightere=turtle()
linese= {'left':leftere, 'down':downere, 'up':upere, 'right':rightere}

names = ["downarrow", "downarrowlight", "uparrow", "uparrowlight", "leftarrow",
            "leftarrowlight", "rightarrow", "rightarrowlight", 'bfarm']

for name in names:
        path = f"assets/{name}.png"
        img = Image.open(path)
        target_size = (300, 300) if "bfarm" in name else (80, 80)
        img = img.convert("RGBA").resize(target_size, Image.LANCZOS)
        img.save(path)
        sc.addshape(path)

lefter.shape('assets/leftarrow.png')
downer.shape('assets/downarrow.png')
uper.shape('assets/uparrow.png')
righter.shape('assets/rightarrow.png')

leftere.shape('assets/leftarrow.png')
downere.shape('assets/downarrow.png')
upere.shape('assets/uparrow.png')
rightere.shape('assets/rightarrow.png')

xx=225
for p in lines:
    xx+=75
    lines[p].penup()
    lines[p].goto(xx, 200)

ex=-225
for p in linese:
    ex-=75
    linese[p].penup()
    linese[p].goto(ex, 200)

class Player(turtle):
    def __init__(self):
        super().__init__()
        self.a=''
        self.shape('assets/bfarm.png')
        self.penup()
        self.speed(6)
        self.goto(180, -250)
    def lefti(self): self.left(40); self.right(40); sc.update()
    def righti(self): self.right(40); self.left(40); sc.update()
    def upi(self): self.left(20); self.moveup(40); self.right(20);self.movedown(40);  sc.update()
    def downi(self): self.movedown(40); self.moveup(40); sc.update()
    def update(self):
        if self.a=='left':
            self.lefti()
        if self.a=='up':
            self.upi()
        if self.a=='down':
            self.downi()
        if self.a=='right':
            self.righti()
        else:
            self.shape(f"assets/bfarm.png")

class Arrow(turtle):
    def __init__(self, a:str):
        self.type=a
        super().__init__()
        arrow_list.append(self)
        self.penup()
        shapes = {'left':'leftarrowlight', 'down':'downarrowlight', 'up':'uparrowlight', 'right':'rightarrowlight'}
        self.shape(f'assets/{shapes[a]}.png')
        self.goto(lines[a].xcor(), -200)

    def main(self):
        global miss, score
        self.moveup(speed)
        if self.ycor()>500:
            if self in arrow_list:
                arrow_list.remove(self)
                self.hideturtle()
                miss+=1
                score-=10
                Update_miss()

class EnemyArrow(turtle):
    def __init__(self, a:str):
        self.type=a
        super().__init__()
        enemyarrows.append(self)
        self.penup()
        shapes = {'left':'leftarrow', 'down':'downarrow', 'up':'uparrow', 'right':'rightarrow'}
        self.shape(f'assets/{shapes[a]}.png')
        self.goto(linese[a].xcor(), -200)
    def main(self):
        self.moveup(speed)
        if self in enemyarrows:
            if self.ycor()>235:
                enemyarrows.remove(self)
                self.hideturtle()
                self.clear()

class Enemy(turtle):
    def __init__(self, name, poses_count):
        super().__init__()
        self.penup()
        self.a=None
        self.name, self.poses_count = name, poses_count
        self.is_talking, self.tick = False, 0
        self.goto(0, -30)
        self.shape(f"{fold}/{name}.png")
    def update(self):
        if self.a=='left':
            self.shape(f'{fold}/{self.name}1.png')
        if self.a=='up':
            self.shape(f'{fold}/{self.name}2.png')
        if self.a=='down':
            self.shape(f'{fold}/{self.name}3.png')
        if self.a=='right':
            self.shape(f'{fold}/{self.name}4.png')
        else:
            self.shape(f"{fold}/{self.name}.png")

def Update_score():
    drawer.clear()
    drawer.write(f'현재 점수: {score}점', align='center', font=('맑은 고딕', 20))
def Update_miss():
    misser.clear()
    misser.write(f'현재 틀림: {miss}개', align='center', font=('맑은 고딕', 20))

def main():
    files = allread(file[0], 'utf-8')
    files = files.split('\n')
    efiles = allread(file[5], 'utf-8').split('\n')
    misser.penup()
    misser.goto(0, 300)
    Update_miss()
    texts = ["Ready?", "Set,", "Go!"]
    for txt in texts:
        drawer.clear()
        drawer.write(txt, align='center', font=('Arial', 50, 'bold'))
        end = time.time() + 1
        while time.time() < end: sc.update()
        sc.update()
    drawer.penup()
    drawer.goto(0, 250)
    Update_score()
    pg.mixer.music.load(file[1])
    enemyvocal=pg.mixer.Sound(file[2])
    myvocal=pg.mixer.Sound(file[3])
    global player
    player=Player()

    pico_enemy=Enemy(f'{enemyname}',4)
    enemyvocal.play()
    myvocal.play()
    pg.mixer.music.play()
    starttime=time.time()
    def check():
        if pg.mixer.music.get_busy():
            elapsed = time.time() - starttime
            arrow_type=r.choice(['left', 'right', 'up', 'down'])
            if files:
                if float(files[0]) <= float(format(elapsed, '.1f')):
                    Arrow(arrow_type)
                    files.pop(0)

            if efiles:
                if float(efiles[0]) <= float(format(elapsed, '.1f')):
                    EnemyArrow(arrow_type)
                    efiles.pop(0)
                    pico_enemy.a=arrow_type
                    pico_enemy.update()
            for arrow in arrow_list:
                arrow.main()
            for earrow in enemyarrows:
                earrow.main()
            sc.update()
            sc.ontimer(check, 16)
        else:
            window.deiconify(); cv.withdraw()

    check()
    sc.onkeypress(lambda:hit_check('left'), 'Left')
    sc.onkeypress(lambda:hit_check('down'), 'Down')
    sc.onkeypress(lambda:hit_check('up'), 'Up')
    sc.onkeypress(lambda:hit_check('right'), 'Right')
    sc.onkeypress(lambda:hit_check('left'), 'a')
    sc.onkeypress(lambda:hit_check('down'), 's')
    sc.onkeypress(lambda:hit_check('up'), 'w')
    sc.onkeypress(lambda:hit_check('right'), 'd')
    sc.onscreenclick(lambda x, y: sc.listen())
    # 게임 시작 후 화면을 아무 데나 한 번 클릭하면 키 감지가 살아납니다.
    cv.deiconify()
    cv.focus_force()
    sc.listen()


def hit_check(key):
    print('입력됐음')
    global score
    hit_count = 0  # 이번에 몇 개나 맞췄는지 세기

    for arrow in list(arrow_list):
        if arrow.type == key and arrow.distance(lines[key]) < 120:
            arrow.hideturtle()
            player.a=arrow.type
            player.update()
            if arrow in arrow_list:
                arrow_list.remove(arrow)
            score += 10
            hit_count += 1

    if hit_count > 0:
        Update_score()
        sc.update()

window=Tk()
window.geometry('800x200')
button=Button(window, text='채보 파일 업로드하기',command=lambda:onbtn(0))
button.grid(row=0,column=0)
button2=Button(window, text='반주파일 업로드 하기', command=lambda:onbtn(1))
button2.grid(row=0,column=1)
button3=Button(window, text='상대 보컬 업로드 하기', command=lambda:onbtn(2))
button3.grid(row=0,column=2)
button4=Button(window, text='내 보컬 업로드 하기', command=lambda:onbtn(3))
button4.grid(row=0,column=3)
button5=Button(window, text='적 캐릭터 업로드 하기', command=on_btn_5)
button5.grid(row=0,column=4)
button6 = Button(window, text='적 채보 업로드 하기', command=lambda:onbtn(5))
button6.grid(row=0, column=5)
button6 = Button(window, text='저장하기', command=savefile)
button6.grid(row=0, column=6)
button6 = Button(window, text='저장본 불러오기', command=opening)
button6.grid(row=0, column=7)
starter=Button(window, text='게임시작 하기', command=startgame)
starter.grid(row=3, columnspan=2)

window.mainloop()
window.withdraw()
mainloop()