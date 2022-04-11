import random
import pygame as pg
import time
import sys

'''Цвета'''
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (0, 255, 255)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)


class Area():
    '''Прямоугольник'''

    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        '''Создание прямоугольника'''
        self.rect = pg.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        '''Изменение цвета'''
        self.fill_color = new_color

    def fill(self):
        '''Отрисовка прямоугольника'''
        pg.draw.rect(window, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        '''Обводка прямоугольника'''
        pg.draw.rect(window, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        '''Проверяет кликнули ли мышкой на область прямоугольника'''
        return self.rect.collidepoint(x, y)


class Label(Area):
    '''Надпись'''

    def set_text(self, txt, fsize=12, txt_color=BLACK):
        '''Инициализируем шрифт и надпись'''
        self.font = pg.font.SysFont('algerian', fsize)
        self.image = self.font.render(txt, True, txt_color)

    def draw(self, shift_x, shift_y):
        '''Отрисовка надписи на прямоугольнике'''
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def draw_cards(self, shift_x=0, shift_y=0):
        '''Отрисовка обводки прямоугольника'''
        self.fill()
        self.outline(BLUE, 5)
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


pg.init()
window = pg.display.set_mode((500, 500))
pg.display.set_caption('FastClicker')
window.fill(LIGHT_BLUE)
clock = pg.time.Clock()
cards = []
num_cards = 4
x = 70

is_pause = False
wait = 0
wait1 = None
points = 0
play = True
first_time_win = True


# Создание счётчиков
time_text = Label(0, 0, 50, 50, LIGHT_BLUE)
time_text.set_text('Time:', 20, DARK_BLUE)
time_text.draw(20, 20)

timer = Label(50, 55, 50, 40, LIGHT_BLUE)
timer.set_text('0', 20, DARK_BLUE)
timer.draw(0, 0)

score_text = Label(380, 0, 50, 50, LIGHT_BLUE)
score_text.set_text('Count:', 20, DARK_BLUE)
score_text.draw(20, 20)

score = Label(430, 55, 50, 40, LIGHT_BLUE)
score.set_text('0', 20, DARK_BLUE)
score.draw(0, 0)

# Создание конечного фона

lose = Label(0, 0, 500, 500, RED)
lose.set_text('Time is out !!!', 30, DARK_BLUE)
win = Label(0, 0, 500, 500, GREEN)
win.set_text('You are win !!!', 30, DARK_BLUE)
result_time = Label(90, 230, 250, 250, GREEN)

# Создание карточек
for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 5)
    new_card.set_text('CLICK', 15)
    cards.append(new_card)
    x += 100

start_time = time.time()
cur_time = start_time

while play:

    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if len(cards) != 0:
                for i in range(num_cards):
                    if cards[i].collidepoint(x, y):
                        if i + 1 == click:
                            cards[i].color(GREEN)
                            points += 1
                        else:
                            cards[i].color(RED)
                            points -= 1
                        cards[i].fill()
                        score.set_text(str(points), 20, DARK_BLUE)
                        score.draw(0, 0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # это пауза
                if is_pause:
                    is_pause = False
                else:
                    is_pause = True

    if not is_pause:
        if wait1 == None:
            if wait == 0:
                wait = 15
                click = random.randint(1, num_cards)
                for i in range(num_cards):
                    if i + 1 == click:
                        cards[i].color(YELLOW)
                        cards[i].draw_cards(10, 40)
                    else:
                        cards[i].color(YELLOW)
                        cards[i].fill()
                        cards[i].outline(BLUE, 5)
            else:
                wait -= 1

    # Проигрыш
        new_time = time.time()
        if new_time - start_time >= 11:
            if wait1 == None:
                cards.clear()
                wait1 = 25
                lose.draw(110, 180)
            else:
                wait1 -= 1
            if wait1 == 0:
                play = False

    # Изменение показаний игрового таймера
        if wait1 == None:
            if int(new_time) - int(cur_time) == 1:
                timer.set_text(str(int(new_time - start_time)), 20, DARK_BLUE)
                timer.draw(0, 0)
                cur_time = new_time

        # Выигрыш
        if points >= 5:
            if first_time_win:
                result_time.set_text('Your gameplay time: ' +
                                     str(int(new_time - start_time)), 25, DARK_BLUE)
                first_time_win = False
                cards.clear()
            if wait1 == None:
                wait1 = 50
                win.draw(110, 180)
                result_time.draw(0, 0)
            else:
                wait1 -= 1
            if wait1 == 0:
                play = False

    clock.tick(20)
    pg.display.update()
