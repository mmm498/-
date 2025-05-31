import pygame
from pygame.locals import *
import sys
import random
from itertools import cycle

SCREENWIDTH = 822
SCREENHEIGHT = 199
FPS = 30

# 游戏状态常量
START_SCREEN = 0
COUNTDOWN = 1
GAMEPLAY = 2
GAME_OVER = 3

# 初始化pygame
pygame.init()
pygame.font.init()

# 设置中文字体
font = pygame.font.SysFont("SimHei", 36)
title_font = pygame.font.SysFont("SimHei", 48)


# 定义一个移动地图类
class MyMap:
    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:  # 小于-790说明地图已经完全移动完毕
            self.x = 800  # 给地图一个新的坐标点
        else:
            self.x -= 5  # 5个像素向左移动

    # 更新地图
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))


# 背景音乐按钮
class Music_Button:
    is_open = True  # 背景乐音的标记

    def __init__(self):
        self.open_img = pygame.image.load('image/btn_open.png').convert_alpha()
        self.close_img = pygame.image.load('image/btn_close.png').convert_alpha()
        self.bg_music = pygame.mixer.Sound('audio/bg_music.wav')  # 加载背景音乐
        self.bg_music.play(-1)  # 循环播放背景音乐

    # 判断鼠标是否在按钮的范围内
    def is_select(self):
        # 获取鼠标的坐标
        point_x, point_y = pygame.mouse.get_pos()
        w, h = self.open_img.get_size()  # 获取按钮图片的大小
        # 判断鼠标是否在按钮范围内
        in_x = point_x > 20 and point_x < 20 + w
        in_y = point_y > 20 and point_y < 20 + h
        return in_x and in_y

    def toggle_music(self):
        if self.is_open:
            self.bg_music.stop()
            self.is_open = False
        else:
            self.bg_music.play(-1)
            self.is_open = True


# 玛丽类
class Marie:
    def __init__(self):
        # 初始化小玛丽矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False  # 跳跃的状态
        self.jumpHeight = 130  # 跳跃的高度
        self.lowest_y = 140  # 最低坐标
        self.jumpValue = 0  # 跳跃增变量
        # 小玛丽动图索引
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])
        # 加载小玛丽图片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure2.png").convert_alpha(),
            pygame.image.load("image/adventure3.png").convert_alpha(),
        )
        self.jump_audio = pygame.mixer.Sound('audio/jump.wav')  # 跳音效
        self.rect.size = self.adventure_img[0].get_size()
        self.x = 50  # 绘制小玛丽的X坐标
        self.y = self.lowest_y  # 绘制小玛丽的Y坐标
        self.rect.topleft = (self.x, self.y)

    # 跳状态
    def jump(self):
        if not self.jumpState:  # 只有不在跳跃状态时才能起跳
            self.jumpState = True
            self.jump_audio.play()


    # 玛丽移动
    def move(self):
        if self.jumpState:  # 当起跳的时候
            if self.rect.y >= self.lowest_y:  # 如果站在地上
                self.jumpValue = -5  # 以5个像素值向上移动
            if self.rect.y <= self.lowest_y - self.jumpHeight:  # 小玛丽到达顶部回落
                self.jumpValue = 5  # 以5个像素值向下移动
            self.rect.y += self.jumpValue  # 通过循环改变玛丽的Y坐标
            if self.rect.y >= self.lowest_y:  # 如果小玛丽回到地面
                self.rect.y = self.lowest_y  # 确保不会超出地面
                self.jumpState = False  # 关闭跳跃状态



    # 绘制小玛丽
    def draw_marie(self):
        # 匹配小玛丽动图
        marieIndex = next(self.marieIndexGen)
        # 绘制小玛丽
        SCREEN.blit(self.adventure_img[marieIndex], (self.x, self.rect.y))


# 障碍物类
class Obstacle:
    score = 1  # 分数
    move = 5  # 移动距离
    obstacle_y = 150  # 障碍物y坐标

    def __init__(self):
        # 初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 加载障碍物图片
        self.missile = pygame.image.load("image/missile.png").convert_alpha()
        self.pipe = pygame.image.load("image/pipe.png").convert_alpha()
        # 加载分数图片
        self.numbers = (
            pygame.image.load('image/0.png').convert_alpha(),
            pygame.image.load('image/1.png').convert_alpha(),
            pygame.image.load('image/2.png').convert_alpha(),
            pygame.image.load('image/3.png').convert_alpha(),
            pygame.image.load('image/4.png').convert_alpha(),
            pygame.image.load('image/5.png').convert_alpha(),
            pygame.image.load('image/6.png').convert_alpha(),
            pygame.image.load('image/7.png').convert_alpha(),
            pygame.image.load('image/8.png').convert_alpha(),
            pygame.image.load('image/9.png').convert_alpha()
        )
        # 加载加分音效
        self.score_audio = pygame.mixer.Sound('audio/score.wav')  # 加分
        # 0和1随机数
        r = random.randint(0, 1)
        if r == 0:  # 如果随机数为0显示导弹障碍物相反显示管道
            self.image = self.missile  # 显示导弹障碍
            self.move = 15  # 移动速度加快
            self.obstacle_y = 100  # 导弹坐标在天上
        else:
            self.image = self.pipe  # 显示管道障碍
        # 根据障碍物位图的宽高来设置矩形
        self.rect.size = self.image.get_size()
        # 获取位图宽高
        self.width, self.height = self.rect.size
        # 障碍物绘制坐标
        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x, self.y)

    # 障碍物移动
    def obstacle_move(self):
        self.rect.x -= self.move

    # 绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 获取分数
    def getScore(self):
        tmp = self.score
        if tmp == 1:
            self.score_audio.play()  # 播放加分音乐
        self.score = 0  # 确保只加一次分
        return tmp

    # 显示分数
    def showScore(self, score):
        # 获取得分数字
        self.scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # 要显示的所有数字的总宽度
        for digit in self.scoreDigits:
            # 获取积分图片的宽度
            totalWidth += self.numbers[digit].get_width()
        # 分数横向位置
        Xoffset = (SCREENWIDTH - (totalWidth + 30))
        for digit in self.scoreDigits:
            # 绘制分数
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            # 随着数字增加改变位置
            Xoffset += self.numbers[digit].get_width()


# 显示开始界面
def show_start_screen(music_button):
    # 加载开始界面背景
    start_bg = pygame.image.load("image/start_bg.png").convert_alpha()

    # 创建开始按钮
    start_button = pygame.Rect(SCREENWIDTH // 2 - 100, SCREENHEIGHT // 2 + 50, 200, 50)

    btn_img = music_button.open_img if music_button.is_open else music_button.close_img

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                # 检查音乐按钮
                if music_button.is_select():
                    music_button.toggle_music()
                    btn_img = music_button.open_img if music_button.is_open else music_button.close_img

                # 检查开始按钮
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    return

            # 响应键盘按键开始游戏
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

        # 绘制开始界面
        SCREEN.blit(start_bg, (0, 0))

        # 绘制开始按钮
        button_color = (0, 200, 0) if start_button.collidepoint(pygame.mouse.get_pos()) else (0, 150, 0)
        pygame.draw.rect(SCREEN, button_color, start_button, border_radius=10)
        button_text = font.render("开始游戏", True, (255, 255, 255))
        SCREEN.blit(button_text, button_text.get_rect(center=start_button.center))

        # 绘制音乐按钮
        SCREEN.blit(btn_img, (20, 20))

        # 更新显示
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# 显示倒计时
def show_countdown():
    countdown_font = pygame.font.SysFont("SimHei", 72)
    countdown_texts = ["3", "2", "1", "GO!"]

    # 加载倒计时音效
    try:
        countdown_sounds = [
            pygame.mixer.Sound('audio/countdown_3.wav'),
            pygame.mixer.Sound('audio/countdown_2.wav'),
            pygame.mixer.Sound('audio/countdown_1.wav'),
            pygame.mixer.Sound('audio/go.wav')
        ]
    except FileNotFoundError:
        # 如果音效文件不存在，使用空列表
        countdown_sounds = [None] * 4

    for i, text in enumerate(countdown_texts):
        # 播放音效（如果有）
        if countdown_sounds[i]:
            countdown_sounds[i].play()

        # 绘制倒计时文本
        text_surface = countdown_font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))

        # 清空屏幕并绘制背景和玛丽
        SCREEN.fill((0, 0, 0))
        bg1.map_update()
        bg2.map_update()
        marie.draw_marie()
        SCREEN.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.time.delay(1000)  # 延迟1秒

        # 处理事件以保持响应
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


# 显示游戏结束界面
def show_game_over(score):
    # 加载并放大游戏结束图片
    original_over_img = pygame.image.load('image/gameover.png').convert_alpha()
    over_img = pygame.transform.scale(original_over_img,
                                      (int(original_over_img.get_width() * 1.5),
                                       int(original_over_img.get_height() * 1.5)))

    img_y = (SCREENHEIGHT - over_img.get_height()) // 2 - 30  # 微调位置

    # 创建重新开始按钮（与开始界面按钮垂直位置一致）
    restart_button = pygame.Rect(
        SCREENWIDTH // 2 - 100,  # 水平居中
        SCREENHEIGHT // 2 + 50,  # 与开始按钮Y坐标一致
        200, 50
    )

    # 创建更小的分数字体
    small_font = pygame.font.SysFont("SimHei", 28)  # 原36减小为28

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    return

            if event.type == KEYDOWN and event.key == K_SPACE:
                return

        SCREEN.fill((0, 0, 0))

        # 绘制背景和障碍物
        bg1.map_update()
        bg2.map_update()
        for obstacle in obstacles:
            obstacle.draw_obstacle()

        marie.draw_marie()

        # 绘制Game Over图片
        SCREEN.blit(over_img, ((SCREENWIDTH - over_img.get_width()) // 2, img_y))

        # 绘制调整后的最终得分
        score_text = small_font.render(f"最终得分: {score}", True, (0, 0, 0))  # 使用小号字体
        score_rect = score_text.get_rect(center=(SCREENWIDTH // 2, img_y + over_img.get_height() + 20))  # 下移20像素
        SCREEN.blit(score_text, score_rect)

        # 绘制重新开始按钮
        button_color = (200, 0, 0) if restart_button.collidepoint(pygame.mouse.get_pos()) else (150, 0, 0)
        pygame.draw.rect(SCREEN, button_color, restart_button, border_radius=10)
        button_text = font.render("重新开始", True, (255, 255, 255))
        SCREEN.blit(button_text, button_text.get_rect(center=restart_button.center))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
# 主游戏函数
def mainGame():
    global SCREEN, FPSCLOCK, bg1, bg2, marie, obstacles

    # 初始化pygame
    pygame.init()

    # 创建窗口和时钟
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('玛丽冒险')

    # 创建音乐按钮
    music_button = Music_Button()

    while True:
        # 显示开始界面
        show_start_screen(music_button)

        # 创建地图对象
        bg1 = MyMap(0, 0)
        bg2 = MyMap(800, 0)

        # 创建小玛丽对象
        marie = Marie()

        # 初始化游戏变量
        score = 0
        addObstacleTimer = 0
        obstacles = []
        game_over = False

        # 显示倒计时
        show_countdown()

        # 游戏主循环
        while not game_over:
            # 处理事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    # 检查音乐按钮
                    if music_button.is_select():
                        music_button.toggle_music()

                # 空格键控制跳跃
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if marie.rect.y >= marie.lowest_y:  # 如果小玛丽在地面上
                        marie.jump()

            # 更新地图
            bg1.map_update()
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()

            # 更新小玛丽
            marie.move()
            marie.draw_marie()

            # 添加障碍物
            addObstacleTimer += 20
            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    obstacle = Obstacle()
                    obstacles.append(obstacle)
                addObstacleTimer = 0

            # 更新障碍物
            for obstacle in obstacles[:]:
                obstacle.obstacle_move()
                obstacle.draw_obstacle()

                # 检查碰撞
                if pygame.sprite.collide_rect(marie, obstacle):
                    game_over = True
                    music_button.bg_music.stop()

                # 检查是否获得分数
                if (obstacle.rect.x + obstacle.rect.width) < marie.rect.x and obstacle.score > 0:
                    score += obstacle.getScore()

                # 移除超出屏幕的障碍物
                if obstacle.rect.x < -obstacle.rect.width:
                    obstacles.remove(obstacle)

            # 显示分数
            if obstacles:
                obstacles[0].showScore(score)

            # 绘制音乐按钮
            btn_img = music_button.open_img if music_button.is_open else music_button.close_img
            SCREEN.blit(btn_img, (20, 20))

            # 更新显示
            pygame.display.update()
            FPSCLOCK.tick(FPS)

        # 游戏结束，显示游戏结束界面
        show_game_over(score)


if __name__ == '__main__':
    mainGame()