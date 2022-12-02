### インポート
import sys
import time
import copy
import pygame
from pygame.locals import *

### 定数
R_H_SIZE = 20       # ラケット縦サイズ
R_W_SIZE = 100      # ラケット横サイズ
R_B_POS  = 30       # ラケット縦位置
BAL_SIZE = 200       # ボールサイズ
B_X_NUM  = 20       # ブロック横列の数
B_Y_NUM  = 10       # ブロック縦列の数
B_H_SIZE = 20       # ブロック縦サイズ
B_W_SIZE = 45       # ブロック横サイズ
B_TOP    = 30       # ブロック上余白位置
B_LEFT   = 20       # ブロック左余白位置
B_BLANK  = 5        # ブロック間余白
F_RATE   = 120      # フレームレート
K_REPEAT = 20       # キーリピート発生間隔
RKT_SPD  = 35     # ラケット移動速度
BAL_SPD  = 2# ボール移動速度
F_SIZE   = 60       # フォントサイズ
S_TIME   = 2        # START画面時間(秒)
E_TIME   = 4        # CLEAR画面時間(秒)

### 画面定義(X軸,Y軸,横,縦)
SURFACE  = Rect(0, 0, 600, 840) # 画面サイズ

############################
### ラケットクラス
############################
class Racket(pygame.sprite.Sprite):

    ############################
    ### 初期化メソッド
    ############################
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)

        ### ファイル読み込み
        self.image = pygame.image.load(name).convert()

        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (R_W_SIZE, R_H_SIZE))

        ### ラケットオブジェクト生成
        self.rect = self.image.get_rect()

    ############################
    ### ラケット更新
    ############################
    def update(self, racket_pos):

        ### ラケット位置
        self.rect.centerx = racket_pos
        self.rect.centery = SURFACE.bottom - R_B_POS

        ### 画面内に収める
        self.rect.clamp_ip(SURFACE)

    ############################
    ### ラケット描画
    ############################
    def draw(self, surface):
        surface.blit(self.image, self.rect)

############################
### ボールクラス
############################
class Ball(pygame.sprite.Sprite):

    ############################
    ### 初期化メソッド
    ############################
    def __init__(self, name, racket, blocks):
        pygame.sprite.Sprite.__init__(self)

        ### ファイル読み込み
        self.image = pygame.image.load(name).convert_alpha()

        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (BAL_SIZE, BAL_SIZE))

        ### ボールオブジェクト生成
        self.rect = self.image.get_rect()

        self.sp_x = 0               # ボール速度(X軸)
        self.sp_y = 0               # ボール速度(Y軸)
        self.racket = racket        # ラケットを参照
        self.blocks = blocks        # ブロックを参照
        self.update = self.setup    # ゲーム初期状態

    ############################
    ### ゲーム初期状態
    ############################
    def setup(self, surface):

        ### ボール初期位置
        self.rect.centerx = int(SURFACE.width  / 2) + 1
        self.rect.centery = int(SURFACE.height / 3)

        ### ボール速度
        self.sp_x = 0
        self.sp_y = BAL_SPD

        ### 関数代入
        self.update = self.move

    ############################
    ### ボールの挙動
    ############################
    def move(self, surface):
        self.rect.centerx += int(self.sp_x)
        self.rect.centery += int(self.sp_y)

        ### 左壁の反射
        if self.rect.left < SURFACE.left:
            self.rect.left = SURFACE.left
            self.sp_x = -self.sp_x

        ### 右壁の反射
        if self.rect.right > SURFACE.right:
            self.rect.right = SURFACE.right
            self.sp_x = -self.sp_x

        ### 上壁の反射
        if self.rect.top < SURFACE.top:
            self.rect.top = SURFACE.top
            self.sp_y = -self.sp_y

        ### ラケットとボールの接触判定
        if self.rect.colliderect(self.racket.rect):

            ### 接触位置取得
            dist = self.rect.centerx - self.racket.rect.centerx

            ### X軸移動距離設定
            if   dist < 0:
                self.sp_x = -BAL_SPD * (1 + dist / R_W_SIZE/2)
            elif dist > 0:
                self.sp_x =  BAL_SPD * (1 - dist / R_W_SIZE/2)
            else:
                self.sp_x = 0

	        ### Y軸移動
            self.sp_y = -BAL_SPD

        ### ボールを落とした場合
        if self.rect.bottom > SURFACE.bottom:

            ### GAME OVERを表示
            font = pygame.font.Font(None, F_SIZE)
            text = font.render("GAME OVER", True, (255,31,31))
            surface.blit(text, [180,300])

        ### ブロック接触リスト取得(接触したブロックは削除)
        blocks_list = pygame.sprite.spritecollide(self, self.blocks, True)

        ### ブロック接触あり
        if len(blocks_list) > 0:

            ### ボールオブジェクト保存
            ball_rect = copy.copy(self.rect)

            ### 接触ブロックリスト
            for block in blocks_list:

                ### ブロック上に接触した場合
                if block.rect.top > ball_rect.top and block.rect.bottom > ball_rect.bottom and self.sp_y > 0:
                    self.rect.bottom = block.rect.top
                    self.sp_y = -self.sp_y

                ### ブロック下に接触した場合
                if block.rect.top < ball_rect.top and block.rect.bottom < ball_rect.bottom and self.sp_y < 0:
                    self.rect.top = block.rect.bottom
                    self.sp_y = -self.sp_y

                ### ブロック左に接触した場合
                if block.rect.left > ball_rect.left and block.rect.right > ball_rect.right and self.sp_x > 0:
                    self.rect.right = block.rect.left
                    self.sp_x = -self.sp_x

                ### ブロック右に接触した場合
                if block.rect.left < ball_rect.left and block.rect.right < ball_rect.right and self.sp_x < 0:
                    self.rect.left = block.rect.right
                    self.sp_x = -self.sp_x

            ### 残ブロックなし
            if len(self.blocks) == 0:

                ### GAME CLEARを表示
                font = pygame.font.Font(None, F_SIZE)
                text = font.render("GAME CLEAR", True, (63,255,63))
                surface.blit(text, [230,350])
                pygame.display.update()

                ### CLEAR画面時間
                time.sleep(E_TIME)

    ############################
    ### ボール描画
    ############################
    def draw(self, surface):
        surface.blit(self.image, self.rect)

############################
### ブロッククラス
############################
class Block(pygame.sprite.Sprite):

    ############################
    ### 初期化メソッド
    ############################
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)

        ### ファイル読み込み
        self.image = pygame.image.load(name).convert()

        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (B_W_SIZE, B_H_SIZE))

        ### ブロックオブジェクト生成
        self.rect = self.image.get_rect()

        ### ブロック位置設定
        self.rect.left = x * (self.rect.width  + B_BLANK) + B_LEFT
        self.rect.top  = y * (self.rect.height + B_BLANK) + B_TOP

    ############################
    ### ブロック描画
    ############################
    def draw(self, surface):
        surface.blit(self.image, self.rect)

############################
### メイン関数 
############################
def main():

    ### 画面初期化
    pygame.init()
    surface = pygame.display.set_mode(SURFACE.size)

    ### ブロックグループ作成
    blocks = pygame.sprite.Group()
    for x in range(B_X_NUM):        # ブロック横
        for y in range(B_Y_NUM):    # ブロック縦

            ### ブロック作成
            blocks.add(Block("gazo/block.png", x, y))

    ### スプライト作成
    racket = Racket("gazo/racket.png")
    ball   = Ball("gazo/ball.png", racket, blocks)

    ### 時間オブジェクト生成
    clock = pygame.time.Clock()

    ### ラケット初期位置
    racket_pos = int(SURFACE.width / 2)

    ### キーリピート有効
    pygame.key.set_repeat(K_REPEAT)

    ### STARTを表示
    font = pygame.font.Font(None, F_SIZE)
    text = font.render("START", True, (96,96,255))
    surface.fill((0,0,0))
    surface.blit(text, [230,350])
    pygame.display.update()

    ### 一時停止
    time.sleep(S_TIME)

    ### 無限ループ
    while True:

        ### フレームレート設定
        clock.tick(F_RATE)

        ### 背景色設定
        surface.fill((0,0,0))

        ### スプライトを更新
        racket.update(racket_pos)
        ball.update(surface)

        ### スプライトを描画
        racket.draw(surface)
        ball.draw(surface)
        blocks.draw(surface)

        ### 画面更新
        pygame.display.update()

        ### イベント処理
        for event in pygame.event.get():

            ### 終了処理
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

                ### キー操作
                if event.key == K_LEFT:
                    racket_pos -= RKT_SPD
                if event.key == K_RIGHT:
                    racket_pos += RKT_SPD

############################
### 終了関数
############################
def exit():
    pygame.quit()
    sys.exit()

############################
### メイン関数呼び出し
############################
if __name__ == "__main__":

    ### 処理開始
    main()