import sprite_engine
import random
import animated_sprite

def load(sprite_engin):
    ratio = 3	
    sprite_engin.load_sound("sounds/Colt45.wav")
    sprite_engin.load_music("music/zoolrave.mod")

    #blue team
    animated_sprite.flag(animated_sprite.team1, sprite_engin, 2*82*ratio+32+30,(300-62)*ratio) 
    spawn1 = sprite_engine.spawn(sprite_engin, 2*82*ratio+32,(300-62)*ratio, 1)
    spawn2 = sprite_engine.spawn(sprite_engin, 82*ratio,(500-62)*ratio, -1)
    animated_sprite.team1.spawns = [spawn1,spawn2]
    #red team
    animated_sprite.flag(animated_sprite.team2, sprite_engin, 175*ratio,(223*8-62)*ratio) 
    spawn3 = sprite_engine.spawn(sprite_engin, 100*ratio, (223*8-62)*ratio, 1)
    spawn4 = sprite_engine.spawn(sprite_engin, 250*ratio, (223*8-62)*ratio, 1)
    animated_sprite.team2.spawns = [spawn3,spawn4]
       
    wallimage = "pics/wall.blue.tga"
    floorimage = "pics/floor.red.tga"

    
    
    sprite_engin.respawns = [spawn1,spawn2,spawn3,spawn4]
    
    wall1 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall1.rect.top = 0
    wall1.rect.left = 0
    wall2 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall2.rect.top = 222*ratio
    wall2.rect.left = 0
    wall3 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall3.rect.top = 222*2*ratio
    wall3.rect.left = 0
    wall4 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall4.rect.top = 223*3*ratio
    wall4.rect.left = 0
    wall5 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall5.rect.top = 223*4*ratio
    wall5.rect.left = 0
    wall6 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall6.rect.top = 223*5*ratio
    wall6.rect.left = 0
    wall7 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall7.rect.top = 223*6*ratio
    wall7.rect.left = 0
    wall8 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall8.rect.top = 223*7*ratio
    wall8.rect.left = 0

    wall9 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall9.rect.top = 760*ratio
    wall9.rect.centerx = (32+2*82)*ratio
    wall10 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall10.rect.top = 223*ratio + 760*ratio
    wall10.rect.centerx = (32+2*82)*ratio


    wall11 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall11.rect.top = 0
    wall11.rect.left = (32+4*82)*ratio
    wall12 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall12.rect.top = 223*ratio
    wall12.rect.left = (32+4*82)*ratio
    wall13 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall13.rect.top = 223*2*ratio
    wall13.rect.left = (32+4*82)*ratio
    wall14 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall14.rect.top = 223*3*ratio
    wall14.rect.left = (32+4*82)*ratio
    wall15 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall15.rect.top = 223*4*ratio
    wall15.rect.left = (32+4*82)*ratio
    wall16 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall16.rect.top = 223*5*ratio
    wall16.rect.left = (32+4*82)*ratio
    wall17 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall17.rect.top = 223*6*ratio
    wall17.rect.left = (32+4*82)*ratio
    wall18 = sprite_engine.simplesprite(sprite_engin,wallimage)
    wall18.rect.top = 223*7*ratio
    wall18.rect.left = (32+4*82)*ratio
    
    floor1 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor1.rect.left = 32*ratio

    floor2 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor2.rect.left = (32+82)*ratio

    floor3 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor3.rect.left = (32+2*82)*ratio

    floor4 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor4.rect.left = (32+3*82)*ratio

    floor5 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor5.rect.left = 32*ratio
    floor5.rect.top = 500*ratio
    floor6 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor6.rect.left = 80*ratio
    floor6.rect.top = 500*ratio

    floor7 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor7.rect.right = (32+4*82)*ratio
    floor7.rect.top = 615*ratio
    floor8 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor8.rect.right = (4*82-18)*ratio
    floor8.rect.top = 615*ratio

    floor9 = sprite_engine.simplesprite(sprite_engin,floorimage) #moving floor
    floor9.rect.centerx = (32+2*82)*ratio
    floor9.rect.top = 710*ratio

    floor10 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor10.rect.left = 32*ratio
    floor10.rect.top = 890*ratio

    floor11 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor11.rect.right = (32+4*82)*ratio
    floor11.rect.top = 1100*ratio

    floor12 = sprite_engine.simplesprite(sprite_engin,floorimage) #moving floor
    floor12.rect.centerx = (32+2*82)*ratio
    floor12.rect.top = 223*2*ratio + 760*ratio

    floor13 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor13.rect.left = 32*ratio
    floor13.rect.top = 1350*ratio
    floor14 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor14.rect.left = 70*ratio
    floor14.rect.top = 1350*ratio

    floor15 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor15.rect.right = (32+4*82)*ratio
    floor15.rect.top = 1350*ratio
    floor16 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor16.rect.right = (4*82-8)*ratio
    floor16.rect.top = 1350*ratio

    floor17 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor17.rect.centerx = (32+2*82)*ratio
    floor17.rect.top = 1550*ratio
    
    floor21 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor21.rect.left = 32*ratio
    floor21.rect.bottom = 223*8*ratio

    floor22 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor22.rect.left = (32+82)*ratio
    floor22.rect.bottom = 223*8*ratio

    floor23 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor23.rect.left = (32+2*82)*ratio
    floor23.rect.bottom = 223*8*ratio

    floor24 = sprite_engine.simplesprite(sprite_engin,floorimage)
    floor24.rect.left = (32+3*82)*ratio
    floor24.rect.bottom = 223*8*ratio

    floorflag = sprite_engine.simplesprite(sprite_engin,floorimage)
    floorflag.rect.centerx = (32+2*82)*ratio
    floorflag.rect.bottom = 300*ratio


