#インポート
import sys
import time
import copy
import pygame 
from pygame.locals import * 

##定数
R_H_SIZE = 10  #ラケット縦サイズ
R_W_SIZE = 100 #ラケット横サイズ
R_B_POS = 30 #ラケット縦位置
BAL_SIZE = 18 #ボールサイズ
B_X_NUM = 10 #ブロック横列の数
B_Y_NUM = 5 #ブロック縦列の数
B_H_SIZE = 15 #ブロック縦サイズ
B_W_SIZE = 35 #ブロック横サイズ
B_TOP = 50 #ブロック上余白位置
B_LEFT = 10 #ブロック左余白位置
B_BLANK = 3 #ブロック間余白
F_RATE = 60 #フレームワーク
K_REPEAT = 20 #キーリピート発生感覚
RKT_SPD = 10 #ラケット移動速度
BAL_SPD = 10 #ボール移動速度
F_SIZE = 60 #フォントサイズ
S_TIME = 2 #START画面時間(秒)
E_TIME = 4 #CLEAR画面時間(秒)

#画面定義(X軸,Y軸,横,縦)
SURFACE = Rect(0, 0, 400, 640) #画面サイズ

##ラケットクラス
class Racket(pygame.sprite.Sprite):
  #初期化メソッド
  def __init__(self, name):
    pygame.sprite.Sprite.__init(self)
    #ファイル読み込み
    self.image = pygame = pygame.image.load(name).convert()
    #画像サイズ変更
    self.image = pygame.transform.scale(self.image, (R_W_SIZE, R_H_SIZE))
    ##ラケットオブジェクト生成
    self.rect = self.image.get_rect()
  #ラケット更新
  
  def update (self, racket_pos):
    #ラケット位置
    self.rect.centerx = racket_pos
    self.rect.centery = SURFACE.bottom - R_B_POS
    
    #画面内に収める
    self.rect.clamp_ip(SURFACE)
    
  #ラケット描画
  def draw(self, surface):
    surface.blit(self.image, self.rect)