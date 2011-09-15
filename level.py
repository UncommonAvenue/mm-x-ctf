import sprite_engine
import random


def load(sprite_engin):
    ratio = 3	
    sprite_engin.load_sound("sounds/Colt45.wav")
    sprite_engin.load_music("music/zoolrave.mod")
   
    color = 'blue'

   
    wallimage = "pics/wall." + color + ".tga"
    floorimage = "pics/floor." + color + ".tga"

    spawn1 = sprite_engine.spawn(sprite_engin, 32*ratio,(600-62)*ratio, 1)
    spawn2 = sprite_engine.spawn(sprite_engin, 100*ratio, (600-62)*ratio, 1)
    spawn3 = sprite_engine.spawn(sprite_engin, 432*ratio, (600-62)*ratio, -1)
    spawn4 = sprite_engine.spawn(sprite_engin, 250*ratio, (600-62)*ratio, 1)
    spawnratio = sprite_engine.spawn(sprite_engin, 650*ratio, (600-62)*ratio, -1)
    spawn6 = sprite_engine.spawn(sprite_engin, 750*ratio, (600-62)*ratio, -1)
    spawn7 = sprite_engine.spawn(sprite_engin, 360*ratio, (600-62)*ratio, 1)
    sprite_engin.respawns = [spawn1, spawn2, spawn3, spawn4, spawnratio, spawn6,spawn7 ]
    
    wall1 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall1.rect.left = 0
    wall2 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall2.rect.top = 223*ratio
    wall2.rect.left = 0
    wall3 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall3.rect.top = 223*2*ratio
    wall3.rect.left = 0

    wall4 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wallratio = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall6 = sprite_engine.simplesprite(sprite_engin,wallimage)


    wall4.rect.right = 800*ratio

    wallratio.rect.right = 800*ratio

    wall6.rect.right = 800*ratio


    wallratio.rect.top = 223*ratio
    wall6.rect.top = 223*2*ratio

    floor1 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor1.rect.left = 32*ratio

    floor2 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor2.rect.left = (32+82)*ratio

    floor3 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor3.rect.left = (32+2*82)*ratio

    floor4 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor4.rect.left = (32+3*82)*ratio

    floorratio = sprite_engine.simplesprite(sprite_engin,floorimage)
    floorratio.rect.left = (32+4*82)*ratio

    floor6 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor6.rect.left = (32+ratio*82)*ratio

    floor7 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor7.rect.left = (32+6*82)*ratio

    floor8 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor8.rect.left = (32+7*82)*ratio

    floor9 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor9.rect.left = (32+8*82)*ratio



    floor11 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor11.rect.left = 32*ratio
    floor11.rect.bottom = 600*ratio

    floor12 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor12.rect.left = (32+82)*ratio
    floor12.rect.bottom = 600*ratio

    floor13 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor13.rect.left = (32+2*82)*ratio
    floor13.rect.bottom = 600*ratio

    floor14 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor14.rect.left = (32+3*82)*ratio
    floor14.rect.bottom = 600*ratio

    floor1ratio = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor1ratio.rect.left = (32+4*82)*ratio
    floor1ratio.rect.bottom = 600*ratio

    floor16 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor16.rect.left = (32+5*82)*ratio
    floor16.rect.bottom = 600*ratio

    floor17 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor17.rect.left = (32+6*82)*ratio
    floor17.rect.bottom = 600*ratio

    floor18 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor18.rect.left = (32+7*82)*ratio
    floor18.rect.bottom = 600*ratio

    floor19 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor19.rect.left = (32+8*82)*ratio
    floor19.rect.bottom = 600*ratio

    floor19 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor19.rect.left = 300*ratio
    floor19.rect.bottom = 400*ratio




