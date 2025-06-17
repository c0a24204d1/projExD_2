import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = { #移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0), 
    
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    #引数：こうかとんRectまたは爆弾Rect
    # #戻り値：横方向，縦方向の画面内外判定結果
    # #画面内ならTrue，画面外ならFalse
    
    
    yoko, tate = True, True #初期値：画面内
    if rct.left < 0 or WIDTH < rct.right: #横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT <rct.bottom: #縦方向の画面外判定
        tate = False
    return yoko, tate #横方向,　縦方向の画面内判定結果を返す



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のsurfaceを作る(爆弾用)
    pg.draw.circle(bb_img, (250, 0, 0), (10, 10), 10) #赤い円を描く
    bb_img.set_colorkey((0,0,0)) #黒を透明色に設定
    bb_rct = bb_img.get_rect() #爆弾rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)#横座標用
    bb_rct.centery = random.randint(0, HEIGHT)#縦座標用
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectの衝突判定
            print("ゲームオーバー")
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]


        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if k#ey_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出ていたら
            vx *= -1
        if not tate: #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct) #爆弾の線画
        pg.display.update()
        tmr += 1
        clock.tick(50)
    


    
def gameover(screen: pg.Surface) -> None:
    fin_img = pg.Surface((WIDTH,HEIGHT)) #空のsurfceを作る(ブラックアウト)
    pg.draw.rect(fin_img, (0,0,0),pg.Rect(0,0,1600,900)) #四角を線画がする
    fin_img.set_alpha(200) #透明メソッドで半透明にする
    font = pg.font.Font(None, 50) #フォントサイズを設定する
    txt = font.render("Game Over", True, (255, 255, 255)) #ゲームオーバ-と書かれたSurfaceを生成する
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2 #文字の座標を中央に設定する
    ff_img = pg.image.load("fig/8.png")
    ff1_rct = ff_img.get_rect() #画像Surfaceに対応する画像Rectを取得する
    ff2_rct = ff_img.get_rect() #画像Surfaceに対応する画像Rectを取得する
    ff1_rct.center = WIDTH/1.6, HEIGHT/2 #中心座標から右に移動する
    ff2_rct.center = WIDTH/2.7, HEIGHT/2  #中心座標から左に移動する
    screen.blit(fin_img, [0,0])
    screen.blit(txt, txt_rct) #文字surfaceを画面surfaceに転送する
    screen.blit(ff_img, ff1_rct) #右に貼り付ける
    screen.blit(ff_img, ff2_rct) #左に貼り付ける
    pg.display.update()
    time.sleep(5)










    


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
