import random
import pygame as pg
from cons import *
import math
from tkinter import * 
from tkinter import messagebox 

class obj:
    def __init__(self, isspy):
        self.radius = 20
        self.x = random.randint(20, 1900)
        self.y = random.randint(20, 1060)
        self.dx = random.random()*5*math.sqrt(2)
        self.dy = math.sqrt(50-self.dx)
        self.isspy = isspy
        self.isClicked = False
        self.isHovered = False

    def is_hovered(self, mouse_x, mouse_y):
        if math.sqrt(((mouse_x - self.x - 20) ** 2) + ((mouse_y - self.y - 20) ** 2)) < self.radius:
            return True
        else:
            return False

    def detect_collision(self, mlist):
    # 需要预判下一次行动后是否会碰撞
        self.x += self.dx
        self.y += self.dy
        # 碰到屏幕边框要反弹
        if self.x < 0 or self.x > SCREEN_WIDTH-(2*self.radius):
            self.dx *= -1
        if self.y < 0 or self.y > SCREEN_HEIGHT-(2*self.radius):
            self.dy *= -1
        # 小球互相碰撞的时候，根据Brownian运动公式改变他们的速度方向
        for a in mlist:
            for b in mlist:
                if a != b:
                    if math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2)) <= (a.radius + b.radius):
                        brownian_motion(a, b)
        
    def detect_color(self):
        if self.isClicked:
            return pg.Color(0,255,0)
        elif self.isHovered and not self.isClicked:
            return pg.Color(255,0,0)
        else:
            return None



pg.init()
screen = pg.display.set_mode((1920,1080))
SCREEN_WIDTH, SCREEN_HEIGHT = 1920,1080
clock = pg.time.Clock()

#指导语
font = pg.font.Font('HGKT_CNKI.TTF', 40)
text = font.render(u"在接下来出现的笑脸中, 可能会有1-4个间谍, 睁大你的眼睛找到这些间谍", True, (255,255,255))
text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
done = False
screen.blit(text, text_rect)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                done = True

    screen.fill((0, 0, 0))
    # Blit the text.
    screen.blit(text, text_rect)
    pg.display.flip()
    clock.tick(60)

#创建MOT对象并加载图片
spy_num = random.randint(1,4)
face_num = 10 - spy_num
face_list = []
for n in range(face_num):
    f = obj(isspy=False)
    face_list.append(f)
spy_list = []
for n in range(spy_num):
    s = obj(isspy=True)
    spy_list.append(s)
f_img = pg.image.load('face.png')
s_img = pg.image.load('spy.png')
f_img = pg.transform.scale(f_img, (40, 40))
s_img = pg.transform.scale(s_img, (40, 40))

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    # 显示小球们
    for spy in spy_list:
        screen.blit(f_img, (spy.x, spy.y))
    for face in face_list:
        screen.blit(f_img, (face.x, face.y))
    pg.display.flip()
    pg.time.delay(1000)  #等待1000毫秒，然后准备闪烁小球
    # spy小球进行闪烁
    for t in range(5):
        for spy in spy_list:
            screen.blit(f_img, (spy.x, spy.y))
        pg.display.flip()
        pg.time.delay(150)
        for spy in spy_list:
            screen.blit(s_img, (spy.x, spy.y))
        pg.display.flip()
        pg.time.delay(150)

    # 闪烁结束，停500毫秒之后准备运动
    for spy in spy_list:
        screen.blit(f_img, (spy.x, spy.y))
    pg.display.flip()
    pg.time.delay(500)
    done = True

done = False
timer = time.time()
while (time.time()-timer) < 10 and not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    for mot in spy_list + face_list:
        mot.detect_collision(spy_list + face_list)
        screen.blit(f_img, (mot.x, mot.y))

    pg.display.flip()
    clock.tick(60)

# 运动结束，进入选择界面

#弹窗提示一下如何选择
Tk().wm_withdraw() #隐藏Tkinter自己的那个很丑的小窗口
messagebox.showinfo('请用鼠标选择你认为是间谍的对象，按下ENTER确认','请用鼠标选择你认为是间谍的对象，然后按下ENTER以确认选择') 

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                done = True
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for mot in spy_list + face_list:
                    rc = pg.Rect(mot.x, mot.y, 40, 40)
                    if rc.collidepoint(event.pos):
                        mot.isClicked = not mot.isClicked

    mx, my = pg.mouse.get_pos()

    screen.fill((0,0,0))
    for mot in spy_list + face_list:
        if mot.is_hovered(mx, my):
            mot.isHovered = True
        else:
            mot.isHovered = False
        #判断小球应该是什么颜色
        color_flag = mot.detect_color()
        if color_flag is None:
            pass
        else:
            set_color(f_img, color_flag)
        screen.blit(f_img, (mot.x,mot.y))
        f_img = pg.transform.scale(pg.image.load('face.png'), (40, 40))  #初始化f_img以避免对下一个小球的影响
    
    pg.display.flip()
    clock.tick(60)

#判断一下选对了几个间谍
correct = 0
for spy in spy_list:
    if spy.isClicked:
        correct += 1


done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                done = True

    screen.fill((0,0,0))

    # spy小球进行闪烁
    for t in range(5):
        for spy in spy_list:
            screen.blit(f_img, (spy.x, spy.y))
        pg.display.flip()
        pg.time.delay(150)
        for spy in spy_list:
            screen.blit(s_img, (spy.x, spy.y))
        pg.display.flip()
        pg.time.delay(150)

    for spy in spy_list:
        screen.blit(f_img, (spy.x, spy.y))
    pg.display.flip()
    pg.time.delay(500)
    done = True

#弹窗提示一下如何选择
Tk().wm_withdraw() #隐藏Tkinter自己的那个很丑的小窗口
if spy_num == correct:
    bonus = '你真牛逼'
else:
    bonus = '你也太菜了'
text = '总共%i个间谍, 你选对了%i个, %s'%(spy_num,correct,bonus)
messagebox.showinfo('结果',text) 