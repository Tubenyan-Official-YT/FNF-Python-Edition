import time
from turtle import *
from turtleplus import *
import pygame as pg
from easyfile import *
import random as r
from tkinter import filedialog, Tk, Button, Label, messagebox, Entry, Toplevel
from PIL import Image
from pathlib import *
from threading import Thread
# ---------------------------------------------------------------------------------------
speed=int(input('화살표의 속도를 정하세요. 정수만 입력하세요: '))
pico_enemy=None
is_running=False
cur_llx, cur_lly, cur_urx, cur_ury = -800, -400, 800, 400
file=["", "","","","","",""]
enemyarrows=[]
# ------------ ------------------------ -------------------------------------------------
sc=setup_screen('프나펑 파이썬판!', '#000000', None, 1600,800)
sc.tracer(0)
sc.update()
cv=sc.getcanvas().winfo_toplevel()
cv.withdraw()
# ㅗ ------- 스크린 설정 ---------------------------------------------------
# ㅜ ----- 파일 올리기 설정 -----
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
            if file[6]:
                bg_img = Image.open(file[6]).convert("RGBA").resize((1600, 800), Image.LANCZOS)
                bg_img.save(file[6])
                sc.bgpic(file[6])
            window.withdraw()
            main()
            window.withdraw()
            cv.deiconify()
    except (FileNotFoundError, IndexError):
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

# ㅜ ------ 파일 저장하고 불러오기 설정 ----------
def savefile(): # 파일로 곡 저장하기
    e = Entry(window, width=30)
    e.grid(row=4, column=4)
    e.insert(0, "노래 이름 입력")

    def real_save():
        song_name = e.get()
        if all(file[:7]):
            f0 = f"assets/data/{Path(file[0]).name}"
            f1 = f"assets/data/{Path(file[1]).name}"
            f2 = f"assets/data/{Path(file[2]).name}"
            f3 = f"assets/data/{Path(file[3]).name}"
            f4 = f"assets/data/{Path(file[4]).name}"
            f5 = f"assets/data/{Path(file[5]).name}"
            f6 = f"assets/data/{Path(file[6]).name}"
            data = f"{song_name}|{f0}|{f1}|{f2}|{f3}|{f4}|{f5}|{f6}"
            listappend_file('assets/saves.txt',data,'utf-8')
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
        Button(opener, text=f'{fi[0].split("|")[0]}', command=lambda: fileopener(0)).grid(row=0, column=0)
        Button(opener, text=f'{fi[1].split("|")[0]}', command=lambda: fileopener(1)).grid(row=0, column=1)
        Button(opener, text=f'{fi[2].split("|")[0]}', command=lambda: fileopener(2)).grid(row=0, column=2)
        Button(opener, text=f'{fi[3].split("|")[0]}', command=lambda: fileopener(3)).grid(row=1, column=0)
        Button(opener, text=f'{fi[4].split("|")[0]}', command=lambda: fileopener(4)).grid(row=1, column=1)
        Button(opener, text=f'{fi[5].split("|")[0]}', command=lambda: fileopener(5)).grid(row=1, column=2)
        Button(opener, text=f'{fi[6].split("|")[0]}', command=lambda: fileopener(6)).grid(row=2, column=0)
        Button(opener, text=f'{fi[7].split("|")[0]}', command=lambda: fileopener(7)).grid(row=2, column=1)
        Button(opener, text=f'{fi[8].split("|")[0]}', command=lambda: fileopener(8)).grid(row=2, column=2)
        Button(opener, text=f'{fi[9].split("|")[0]}', command=lambda: fileopener(9)).grid(row=3, column=0)
        Button(opener, text=f'{fi[10].split("|")[0]}', command=lambda: fileopener(10)).grid(row=3, column=1)
        Button(opener, text=f'{fi[11].split("|")[0]}', command=lambda: fileopener(11)).grid(row=3, column=2)
    except:
        messagebox.showerror('에러 ! 에러!', '버튼생성불가')
def fileopener(num: int):
    try:
        file[0] = fi[num].split('|')[1]
        file[1] = fi[num].split('|')[2]
        file[2] = fi[num].split('|')[3]
        file[3] = fi[num].split('|')[4]
        file[4] = fi[num].split('|')[5]
        file[5] = fi[num].split('|')[6]
        file[6] = fi[num].split('|')[7]
        opener.destroy()
    except:
        messagebox.showwarning('에러! 에러!', '파일이 없으니까 열 수 없습니다')

# ㅜ ----- 변수 설정 2 -----
status=False
arrow_list=[]
score=50
miss=0
# ㅜ ----- 음악 재생기 초기화 -----
pg.mixer.init()

# ㅜ ----- 점수쓰는 터틀 만들기 -----
drawer=turtle()
drawer.hideturtle()
drawer.pencolor('white')
misser=turtle()
misser.hideturtle()
misser.pencolor('white')

# ㅜ ----- 화살표 판정선 터틀 설정하기(플레이어) -----
lefter=turtle()
downer=turtle()
uper=turtle()
righter=turtle()
lines= {'left':lefter, 'down':downer, 'up':uper, 'right':righter} # 하나하나에 대응하는 딕셔너리

leftere=turtle()
downere=turtle()
upere=turtle()
rightere=turtle()
linese= {'left':leftere, 'down':downere, 'up':upere, 'right':rightere}

# ㅜ ----- 이미지 추가 / 설정
names = ["downarrow", "downarrowlight", "uparrow", "uparrowlight",
         "leftarrow", "leftarrowlight", "rightarrow", "rightarrowlight",
         "bfarm", "death_left", "death_down", "death_up", "death_right"] # 여기에 이미지 추가
# 참고: ( 적 사진은 따로 리사이징 함. )
for name in names:
    path = f"assets/{name}.png"
    try:
        img = Image.open(path)
        # bfarm(나의 1인칭 캐릭터)만 300x300, 나머지는 전부 80x80으로 리사이징
        target_size = (300, 300) if "bfarm" in name else (80, 80)
        img = img.convert("RGBA").resize(target_size, Image.LANCZOS)
        img.save(path)
        sc.addshape(path)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {path}")
# ㅜ ----- 판정선 모양을 이미지로 설정하기
lefter.shape('assets/leftarrow.png')
downer.shape('assets/downarrow.png')
uper.shape('assets/uparrow.png')
righter.shape('assets/rightarrow.png')
# ㅜ ----- 적 판정선 모양을 이미지로 설정하기
leftere.shape('assets/leftarrow.png')
downere.shape('assets/downarrow.png')
upere.shape('assets/uparrow.png')
rightere.shape('assets/rightarrow.png')

# ㅜ ----- 판정선 터틀들을 올바른 위치로 옮겨주기
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

# ㅜ ----- 판정 글자용 터틀 설정 -----
judge_writer = turtle()
judge_writer.hideturtle()
judge_writer.penup()
judge_writer.speed(0)
judge_writer.goto(0, 100)
sc.update()

# ㅜ ----- 판정 글자 보이기 함수 -----
def show_judgment(text, color):
    judge_writer.clear()
    judge_writer.pencolor(color)
    judge_writer.write(text, align='center', font=('Arial', 40, 'bold'))
    sc.ontimer(judge_writer.clear, 500)

# ㅜ 플레이어를 설정하는 클래스 -----
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

# ㅜ 화살표를 설정하는 클래스 -----
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

# ㅜ ----- 적 화살표를 설정하는 클래스 -----
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

# ㅜ ----- 즉사 화살표를 설정 -----
class Deatharrow(turtle):
    def __init__(self, a:str):
        self.type=a
        super().__init__()
        arrow_list.append(self)
        self.penup()
        shapes = {'left':'death_left', 'down':'death_down', 'up':'death_up', 'right':'death_right'}
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

# ㅜ ----- 적을 설정함.
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

# ㅜ ----- 점수와 미스를 업데이트 하는 함수 생성 -----
def Update_score():
    drawer.clear()
    drawer.write(f'현재 점수: {score}점', align='center', font=('맑은 고딕', 20))
    if score < 0:
        bf_GOJA_transform()
def Update_miss():
    misser.clear()
    misser.write(f'현재 틀림: {miss}개', align='center', font=('맑은 고딕', 20))

# ㅜ ----- 판정함수 설정 -----
is_left, is_down, is_up, is_right = False, False, False, False
# ㅗ ----- 판정함수 설정 -----

# 눌렸을 때 실행할 함수 만들기
def press_left():
    global is_left
    if not is_left:
        is_left = True
        hit_check('left')
def press_down():
    global is_down
    if not is_down:
        is_down = True
        hit_check('down')
def press_up():
    global is_up
    if not is_up:
        is_up = True
        hit_check('up')
def press_right():
    global is_right
    if not is_right:
        is_right = True
        hit_check('right')
# ㅜ ----- 뗏을 때 실행할 함수 만들기
def release_left():
    global is_left
    is_left = False
def release_down():
    global is_down
    is_down = False
def release_up():
    global is_up
    is_up = False
def release_right():
    global is_right
    is_right = False

# ㅜ ----- 보프가 랩배틀에서 져서 고오자아로 변신하는 장면 / 상태 설정 -----
def bf_GOJA_transform():
    global status
    if status != True:
        status=True
        sc.bgcolor('black')
        pg.mixer.stop()
        lefter.hideturtle()
        downer.hideturtle()
        uper.hideturtle()
        righter.hideturtle()
        leftere.hideturtle()
        downere.hideturtle()
        upere.hideturtle()
        rightere.hideturtle()
        if isinstance(pico_enemy, Turtle):
            pico_enemy.shape('assets/bf_killed.png')
            pico_enemy.goto(0,0)

player=Player() # 플레이어 만들기

# ㅜ ----- 카메라 키우기/옮기기 설정 -----
def set_camera(target=''):
    global is_running, cur_lly, cur_urx, cur_llx, cur_ury
    llx, lly, urx, ury = cur_llx, cur_lly, cur_urx, cur_ury

    if target == 'player': # 카메라 타겟이 플레이어 일때
        t_llx, t_lly, t_urx, t_ury = -500, -350, 1100, 450 # 목표 변수를 설정
        line_x, line_y = +12, +2 # 판정선이 움직일 거리
    elif target == 'enemy': # 카메라 타겟이 적일 때
        t_llx, t_lly, t_urx, t_ury = -1100, -350, 500, 450 # 목표 변수를 설정
        line_x, line_y = -12, +2 # 판정선이 움직일 거리
    else: # 중간으로 이동할 때(최초 상태)
        t_llx, t_lly, t_urx, t_ury = -800, -400, 800, 400 # 목표 변수를 설정(원래 비율 상태)
        lines_x=300
        for i in lines: # 판정선 이동
            lines[i].goto(lines_x, 200)
            lines_x += 75
        lines_x=-300
        for i in linese: # 판정선 이동
            linese[i].goto(lines_x, 200)
            lines_x -= 75
        sc.update()
        line_x, line_y = 0,0 # 판정선 이동량 설정 X, 순간이동을 하기 때문

    for i in range(1, 26): # 26회에 나누어 이동
        now_llx = llx + (t_llx - llx) * (i / 26) # 가야할 거리를 26으로 나눈 값을 계속하여 추가
        now_lly = lly + (t_lly - lly) * (i / 26) # ''
        now_urx = urx + (t_urx - urx) * (i / 26) # ''
        now_ury = ury + (t_ury - ury) * (i / 26) # ''
        if line_x != 0 or line_y != 0: # 판정선이 갈 거리가 0 이 아니다, 즉 노멀 상태를 해야하는 것이 아니라면
            for p in lines: # 우리편 화살표 이동
                lines[p].goto(lines[p].xcor() + line_x /26, lines[p].ycor() + line_y /26)
            for p in linese: #우리편 화살표 이동
                linese[p].goto(linese[p].xcor() + line_x/26, linese[p].ycor() + line_y/26)
        sc.setworldcoordinates(now_llx, now_lly, now_urx, now_ury) # 월드의 카메라를 변수와 동기화
        sc.update() # 이거 안하면 뒤에서만 열심히 하고 증거 없어서 상 못받는 꼴임
        time.sleep(0.005) # 이거 안하면 렉걸려서 컴퓨터 폭발해서 지구 날라감 ㅋㅋㅋ
    cur_llx, cur_lly, cur_urx, cur_ury = t_llx, t_lly, t_urx, t_ury
    is_running=False # 애니메이션이 끝났으면 끝났다고 보고하기

# ㅜ ----- 적에게 카메라를 들이대는 코드
# 참고: ( 굳이 따로 분리해내는 이유는 threading을 사용해서 렉을 줄이기 위한 노력의 일환이다 )
def setenemy():
    global is_running
    if is_running == False:
        is_running = True
        Thread(target=set_camera, args=('enemy',),daemon=True).start()
    else:
        return
# ㅜ ----- 플레이어에게 카메라를 들이대는 코드
def setplayer():
    global is_running
    if is_running == False:
        is_running = True
        Thread(target=set_camera, args=('player',), daemon=True).start()
    else:
        return
# ㅜ ----- 중간에 카메라를 들이대는 코드
def setnormal():
    global is_running
    if is_running == False:
        is_running = True
        Thread(target=set_camera, daemon=True).start()
    else:
        return
# ---------------------- 실질적 프로그램 시작 ------------------------------------------------------------------
def main():
    # ㅜ ----- 플레이어 설정
    player.goto(180, -250)
    player.shape('assets/bfarm.png')
    player.showturtle()
    # ㅜ ----- 줄바꿈으로 구분된 채보 리스트를 만들기(아직 문자열)
    raw = allread(file[0], 'utf-8').splitlines()
    eraw = allread(file[5], 'utf-8').splitlines()

    # ㅜ ----- 리스트 컴프리헨션을 이용하여 즉사노트와 일반노트가 부호로 구분된 리스트 새로 생성하기
    temp=[-float(i[1:]) if i.startswith('k') else float(i) for i in raw if i.strip()]
    etemp=[float(i) for i in eraw if i.strip()]

    # ㅜ ----- 실제 파일 검사에 사용할 리스트 만들기
    global files, efiles
    files=temp; efiles = etemp
    # ㅜ ----- 미스 카운터 설정
    misser.penup()
    misser.goto(0, 300)
    Update_miss()
    # ㅜ 레디 , 셋 , 고 만들기
    texts = ["Ready?", "Set,", "Go!"]
    for txt in texts:
        drawer.clear()
        drawer.write(txt, align='center', font=('Arial', 50, 'bold'))
        end = time.time() + 1
        while time.time() < end: sc.update()
        sc.update()
    # ㅜ ----- 점수 카운터 설정
    drawer.penup()
    drawer.goto(0, 250)
    Update_score()
    pg.mixer.music.load(file[1])

    # ㅜ ----- 적 / 플레이어 보컬 설정
    global enemyvocal, myvocal
    enemyvocal=pg.mixer.Sound(file[2])
    myvocal=pg.mixer.Sound(file[3])

    # ㅜ ----- 적 터틀이 있으면 적을 생성하고 아니라면 설정만 하기
    global pico_enemy
    if not isinstance(pico_enemy, Enemy):
        pico_enemy=Enemy(f'{enemyname}',4)
    else:
        pico_enemy.goto(0, -30)
        pico_enemy.shape(f"{fold}/{enemyname}.png")
        pico_enemy.showturtle()

    # ㅜ ----- 시작시간을 재고, 소리 3개 모두 재생하기
    enemyvocal.play()
    myvocal.play()
    pg.mixer.music.play()
    starttime=time.time()

    # ㅜ ----- 부활 만들기
    def press_enter():
        global status, files, efiles, starttime, score, miss
        if status == True:
            status=False
            score = 50
            miss = 0
            Update_score()
            Update_miss()
            lefter.showturtle()
            downer.showturtle()
            uper.showturtle()
            righter.showturtle()
            leftere.showturtle()
            downere.showturtle()
            upere.showturtle()
            rightere.showturtle()
            for a in arrow_list: a.hideturtle()
            for ea in enemyarrows: ea.hideturtle()
            arrow_list.clear()
            enemyarrows.clear()
            if isinstance(pico_enemy, Turtle):
                pico_enemy.shape(f"{fold}/{enemyname}.png")
                pico_enemy.goto(0, -30)
            if file[6]:
                sc.bgpic(file[6])
            else:
                sc.bgcolor('black')
            main()
    # ㅜ ----- 키 눌렀을때 이벤트 설정
    def setup_keys():
        sc.listen()
        # 방향키
        sc.onkeypress(press_left, 'Left')
        sc.onkeyrelease(release_left, 'Left')
        sc.onkeypress(press_down, 'Down')
        sc.onkeyrelease(release_down, 'Down')
        sc.onkeypress(press_up, 'Up')
        sc.onkeyrelease(release_up, 'Up')
        sc.onkeypress(press_right, 'Right')
        sc.onkeyrelease(release_right, 'Right')

        # WASD
        sc.onkeypress(press_up, 'w')
        sc.onkeyrelease(release_up, 'w')
        sc.onkeypress(press_left, 'a')
        sc.onkeyrelease(release_left, 'a')
        sc.onkeypress(press_down, 's')
        sc.onkeyrelease(release_down, 's')
        sc.onkeypress(press_right, 'd')
        sc.onkeyrelease(release_right, 'd');  sc.onkeypress(press_enter, 'Return')
    # ㅜ ----- 판정함수 만들기
    def check():
        if status == True:
            return # 죽었을때는 사용하지 않음

        if pg.mixer.music.get_busy(): # 음악이 재생 중일때
            elapsed = time.time() - starttime
            arrow_type=r.choice(['left', 'right', 'up', 'down']) # 랜덤 화살표
            if files and efiles: # 둘이서 할 때
                if abs(files[0]) < elapsed and efiles[0] < elapsed: # 구분된 채보 타이밍이 절댓값이 0보다 크면
                    setnormal()
                    Arrow(arrow_type)
                    EnemyArrow(arrow_type)
                    files.pop(0)
                    efiles.pop(0)
                    pico_enemy.a = arrow_type
                    pico_enemy.update()
            elif files: # 플레이어만 할때
                if abs(files[0]) <= elapsed:
                    val = files.pop(0)  # 일단 꺼내고 나서 비교
                    setplayer()
                    if val > 0:
                        Arrow(arrow_type)
                    else:
                        Deatharrow(arrow_type)
            elif efiles: # 적만 할 때
                if efiles[0] <= elapsed:
                    setenemy()
                    EnemyArrow(arrow_type)
                    efiles.pop(0)
                    pico_enemy.a=arrow_type
                    pico_enemy.update()
            if not efiles and not files: # 채보가 없을 때
                setnormal()
            for arrow in arrow_list: # 화살표가 있을 때
                arrow.main()
            for earrow in enemyarrows: # 적 화살표가 있을 때
                earrow.main()
            sc.update()
            sc.ontimer(check, 30)

        else: # 음악이 재생되지 않으면 창 닫기
            window.deiconify(); cv.withdraw()

    check() # ontimer 루프 돌리기
    setup_keys() # 키 설정 돌리기
    sc.onscreenclick(lambda x, y: sc.listen())
    # 게임 시작해서 클릭하면 키 감지 살아남.
    cv.deiconify()
    cv.focus_force() # 말들어 임마 찰싹
    sc.listen()

# ㅜ ----- 판정 체크
def hit_check(key):
    print('입력됐음') # 판정이 안될때 키보드 문제를 체크하기 위한 도구
    global score
    hit_count = 0  # 이번에 몇 개나 맞췄는지 세기
    # ㅜ ----- 화살표가 있으면
    for arrow in list(arrow_list)[:37]:
        dist=arrow.distance(lines[key]) # 화살표의 판정선에 대한 거리
        if isinstance(arrow, Deatharrow): # 화살표가 즉사노트면
            if arrow.type == key and dist < 120:
                show_judgment('You died lol', 'white')
                arrow.hideturtle()
                player.a=arrow.type
                player.update()
                if arrow in arrow_list:
                    arrow_list.remove(arrow)
                    sc.turtles().remove(arrow)
                bf_GOJA_transform()
                break
        # ㅜ ----- 화살표가 일반이면
        if isinstance(arrow, Arrow):
            dist = arrow.distance(lines[key])
            if arrow.type == key and dist <= 50: # 거리가 50보다 작게 잘 맞히면
                show_judgment('Sick~!', 'red')
                arrow.hideturtle()
                player.a = arrow.type # 플레이어 모션 바꾸기
                player.update()
                if arrow in arrow_list:
                    arrow_list.remove(arrow)
                    sc.turtles().remove(arrow)
                score += 50
                hit_count += 1
                break
            elif arrow.type == key and 50 <= dist < 120: # good 판정
                show_judgment('GOOD!', 'green')
                arrow.hideturtle()
                player.a = arrow.type
                player.update()
                if arrow in arrow_list:
                    arrow_list.remove(arrow)
                    sc.turtles().remove(arrow)
                score += 10
                hit_count += 1
                break
            elif arrow.type == key and 120 <= dist < 165: # bad 판정
                show_judgment('bad', 'gray')
                arrow.hideturtle()
                player.a = arrow.type
                player.update()
                if arrow in arrow_list:
                    arrow_list.remove(arrow)
                    sc.turtles().remove(arrow)
                score += 2
                break
            elif arrow.type == key and 165 <= dist <= 200: # shit 판정
                show_judgment('SHiT', 'brown')
                arrow.hideturtle()
                player.a = arrow.type
                player.update()
                if arrow in arrow_list:
                    arrow_list.remove(arrow)
                    sc.turtles().remove(arrow)
                score -= 5
                break

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
button7 = Button(window, text='저장하기', command=savefile)
button7.grid(row=0, column=6)
button8 = Button(window, text='저장본 불러오기', command=opening)
button8.grid(row=0, column=7)
starter=Button(window, text='게임시작 하기', command=startgame)
starter.grid(row=3, columnspan=2)
starter=Button(window, text='배경 불러오기', command=lambda:onbtn(6))
starter.grid(row=3, columnspan=8)

window.mainloop()
window.withdraw()
mainloop()

# Ⓒ all rights reserved. 2026 / 02 / 06. Fri.