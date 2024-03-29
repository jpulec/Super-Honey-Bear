#! /usr/bin/env python

import sys, os
import random

import pygame
from pygame.locals import *

from cutscenes import *
from data import *
from sprites import *
from level import *

def RelRect(actor, camera):
    return Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center
        
    def update(self):
        if self.player.rect.centerx > self.rect.centerx+64:
            self.rect.centerx = self.player.rect.centerx-64
        if self.player.rect.centerx < self.rect.centerx-64:
            self.rect.centerx = self.player.rect.centerx+64
        if self.player.rect.centery > self.rect.centery+64:
            self.rect.centery = self.player.rect.centery-64
        if self.player.rect.centery < self.rect.centery-64:
            self.rect.centery = self.player.rect.centery+64
        self.rect.clamp_ip(self.world)
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))

def save_level(lvl):
    open(filepath("saves/prog.sav"), "w").write(str(lvl))

def get_saved_level():
    try:
        return int(open(filepath("saves/prog.sav")).read())
    except:
        open(filepath("saves/prog.sav"),  "w").write(str(1))
        return 1

class Game(object):

    def __init__(self, screen, continuing=False):

        self.screen = screen
        self.sprites = pygame.sprite.OrderedUpdates()
        self.players = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.OrderedUpdates()
        self.grasss = pygame.sprite.OrderedUpdates()
        self.grays = pygame.sprite.OrderedUpdates()
        self.bricks = pygame.sprite.OrderedUpdates()
        self.movingplatforms = pygame.sprite.OrderedUpdates()
        self.movingplatformtwos = pygame.sprite.OrderedUpdates()
        self.baddies = pygame.sprite.OrderedUpdates()
        self.cannons = pygame.sprite.OrderedUpdates()
        self.feet = pygame.sprite.OrderedUpdates()
        self.firebowsers = pygame.sprite.OrderedUpdates()
        self.feetbig = pygame.sprite.OrderedUpdates()
        self.nomoveplatforms = pygame.sprite.OrderedUpdates()
        self.kisses = pygame.sprite.OrderedUpdates()
        self.boxkisses = pygame.sprite.OrderedUpdates()
        self.explosions = pygame.sprite.OrderedUpdates()
        self.playerdying = pygame.sprite.OrderedUpdates()
        self.bombs = pygame.sprite.OrderedUpdates() # bombs = flagpole
        self.PB = pygame.sprite.OrderedUpdates()
        self.shots = pygame.sprite.OrderedUpdates()
        self.springs = pygame.sprite.OrderedUpdates()
        self.bosses = pygame.sprite.OrderedUpdates()
        self.leaf = pygame.sprite.OrderedUpdates()
        self.hearts = pygame.sprite.OrderedUpdates()
        
        self.levels = ["", "Brashier Park", "Prom", "Brashier Park", "Senior Ball", "Brashier Park", "Door County", "Back of the Trooper", "Brashier Park"]
        self.songs =    [ [""],
                        ["Such Great Heights.mp3"],
                        [""],
                        ["Love Song.ogg"],
                        [""],
                        ["True Love Waits.mp3"],
                        [""],
                        [""],
                        ["Invincible.ogg"],
                        [""]]
        Player.right_images = [load_image("hb1.png"), load_image("hb2.png"), load_image("hb3.png"), load_image("hb4.png"), load_image("hb1.png"), load_image("hb5.png")]
        Platform.images = {"platform-sidewalk.png": load_image("platform-sidewalk.png"), "platform-middle.png": load_image("platform-sidewalk.png")}
        Grass.images = {"grass-1.png": load_image("grass-1.png"), "grass-middle.png": load_image("grass-middle.png")}
        Gray.images = {"gray1.png": load_image("gray1.png"), "gray2.png": load_image("gray2.png")}
        Brick.images = {"brick1.png": load_image("brick1.png"), "brick2.png": load_image("brick2.png")}
        MovingPlatform.image = load_image("moving-platform.png")
        Firebowser.image = load_image("bowser-fireball1.png")
        MovingPlatformtwo.image = load_image("moving-platformlong.png")
        Baddie.left_images1 = [load_image("lock%d.png" % i) for i in range(1, 3)]
        Baddie.left_images2 = [load_image("bheart%d.png" % i) for i in range(1, 3)]
        Baddie.left_images3 = [load_image("squidge%d.png" % i) for i in range(1, 3)]
        Baddie.left_images4 = [load_image("monster-red%d.png" % i) for i in range(1, 3)]
        Cannon.left_images1 = [load_image("cannon%d.png" % i) for i in range(1, 3)]
        Cannon.left_images2 = [load_image("cannonbig%d.png" % i) for i in range(1, 3)]
        Cannon.left_images4 = [load_image("smallcannon%d.png" % i) for i in range(1, 3)]
        BaddieBoom.left_images1 = [load_image("lock2.png"), load_image("lock3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images2 = [load_image("bheart2.png"), load_image("bheart3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images3 = [load_image("squidge2.png"), load_image("squidge3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images4 = [load_image("monster-red2.png"), load_image("monster-red3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        Kiss.images = [load_image("kiss%s.png" % i) for i in range(1, 5)]
        BoxKiss.images = [load_image("kiss%s.png" % i) for i in range(1, 5)]
        KissDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PlayerDie.right_images = [load_image("hbdie.png"), load_image("exp2-1.png"), load_image("exp2-2.png"), load_image("exp2-3.png")]
        Bomb.image = load_image("flagpole.png")
        Bridge.image = load_image("bridge.png")
        BaddieShot.image = load_image("shot.png")
        CannonShot.image = load_image("cannonbullet1.png")
        CannonShotbig.image = load_image("cannonbullet1.png")
        CannonShotsmall.image = load_image("cannonbullet1.png")
        Spring.images = [load_image("spring1.png"), load_image("spring2.png")]
        Logs.image = load_image("wood.png")
        Leaf.images = [load_image("tree-branch-leaf-%s.png" % i) for i in range (1, 6)]
        Can.image = load_image("can.png")
        PB.image = load_image("pb-guitar.png")
        Castle.image = load_image("castle.png")
        Castlebig.image = load_image("castle-big.png")
        Hill.image = load_image("hill.PNG")
        Leaves.image = load_image("leaves-1.png")
        Cloud.image = load_image("cloud.png")
        Cloud2.image = load_image("dobbelclouds.png")
        Platform_Tree.image = load_image("tree-branch.png")
        Platform_Tree_Mid.image = load_image("tree-trunk-middle.png")
        Platform_Tree_lBranch.image = load_image("tree-branch-left.png")
        Platform_Tree_rBranch.image = load_image("tree-branch-right.png")
        Platform_Tree_lRoot.image = load_image("tree-roots-left.png")
        Platform_Tree_rRoot.image = load_image("tree-roots-right.png")
        Platform_Tree_L.image = load_image("tree-trunk-left.png")
        Platform_Tree_R.image = load_image("tree-trunk-right.png")
        Platform_Tree_TopL.image = load_image("tree-top-left.png")
        Platform_Tree_TopR.image = load_image("tree-top-right.png")
        Platform_Tree_TopMid.image = load_image("tree-top-middle.png")
        Boss.left_images = [load_image("bowser1.png"), load_image("bowser2.png"), load_image("bowser3.png")]
        Feet.left_images1 = [load_image("feet%d.png" % i) for i in range(1, 2)] 
        Heart.image = load_image("heart.png")
        Heartdie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        CanBig.image = load_image("can-big.png")
        Fence.image = load_image("fence.png")
        Tree1.image = load_image("tree-1.png")
        Tree2.image = load_image("tree-2.png")
        FeetBig.image = load_image ("feet2.png")
        Grasstexture.image = load_image("grass-texture.png")
        Grass1.image = load_image("grass-1.png")
        Grass2.image = load_image("grass-2.png")
        GrassSprite.image = load_image("grass-texturesprite.png") 
        Wall.image = load_image("wall-1.png")
        Lava.image = load_image("lava.png")
        Chain.image = load_image("chain.png")
        HeartBubble.image = load_image("heartbubble.png")

        Player.groups = self.sprites, self.players
        HeartBubble.groups = self.sprites
        Platform.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass.groups = self.sprites, self.grasss, self.nomoveplatforms
        Brick.groups = self.sprites, self.bricks, self.nomoveplatforms
        Gray.groups = self.sprites, self.grays, self.nomoveplatforms
        MovingPlatform.groups = self.sprites, self.platforms, self.movingplatforms
        MovingPlatformtwo.groups = self.sprites, self.platforms, self.movingplatformtwos
        Baddie.groups = self.sprites, self.baddies
        Cannon.groups = self.sprites, self.cannons, self.platforms
        BaddieBoom.groups = self.sprites
        Kiss.groups = self.sprites, self.kisses
        BoxKiss.groups = self.sprites, self.boxkisses
        KissDie.groups = self.sprites
        Heart.groups = self.sprites, self.hearts
        Heartdie.groups = self.sprites
        PlayerDie.groups = self.sprites, self.playerdying
        Bomb.groups = self.sprites, self.bombs
        BaddieShot.groups = self.sprites, self.shots
        CannonShot.groups = self.sprites, self.shots
        CannonShotbig.groups = self.sprites, self.shots
        CannonShotsmall.groups = self.sprites, self.shots
        Spring.groups = self.sprites, self.springs
        Logs.groups = self.sprites, self.platforms, self.nomoveplatforms
        Can.groups = self.sprites, self.platforms, self.nomoveplatforms
        Leaf.groups = self.sprites, self.leaf, self.platforms
        Platform_Tree.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_Mid.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_lBranch.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_rBranch.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_lRoot.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_rRoot.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_R.groups = self.sprites
        Platform_Tree_L.groups = self.sprites
        Platform_Tree_TopL.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_TopR.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platform_Tree_TopMid.groups = self.sprites, self.platforms, self.nomoveplatforms
        Explosion.groups = self.sprites, self.explosions
        PB.groups = self.sprites, self.PB
        Castle.groups = self.sprites,
        Castlebig.groups = self.sprites,
        Cloud.groups = self.sprites,
        Cloud2.groups = self.sprites,
        Leaves.groups = self.sprites,
        Hill.groups = self.sprites,
        Boss.groups = self.sprites, self.bosses
        Feet.groups = self.sprites, self.feet
        CanBig.groups = self.sprites, self.platforms, self.nomoveplatforms
        Firebowser.groups = self.sprites, self.firebowsers
        Fence.groups = self.sprites
        Tree1.groups = self.sprites
        Tree2.groups = self.sprites
        FeetBig.groups = self.sprites, self.feetbig
        Grasstexture.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass1.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass2.groups = self.sprites, self.platforms, self.nomoveplatforms
        GrassSprite.groups = self.sprites
        Wall.groups = self.sprites
        Lava.groups = self.sprites
        Bridge.groups = self.sprites, self.platforms, self.nomoveplatforms
        Chain.groups = self.sprites,

        self.highscore = 0
        self.score = 0
        self.lives = 3
        self.lvl   = 1
        if continuing:
            self.lvl = get_saved_level()
        self.player = Player((0, 0))
        self.clock = pygame.time.Clock()
        self.bg = load_image("back1.png")
        self.level = Level(self.lvl)
        self.camera = Camera(self.player, self.level.get_size()[0])
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.heart1 = load_image("hb1.png")
        self.heroimg = load_image("hb5.png")
        self.baddie_sound = load_sound("jump2.ogg")
        self.kiss_sound = load_sound("kiss.ogg")
        self.up_sound = load_sound("1up.ogg")
        self.time = 400
        self.running = 1
        self.booming = True
        self.boom_timer = 0
        self.music = self.songs[self.lvl][0]
        self.intro_level()
        self.main_loop()
        
    def end(self):
        self.running = 0
        
    def intro_level(self):
        pygame.mixer.music.fadeout(2000)
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        ren = self.font.render(self.levels[self.lvl], 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Hearts x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)
             
    def next_level(self):
        self.time = 400
        self.booming = True
        self.boom_timer = 0
        #try:
        self.lvl += 1
        self.clear_sprites()
        self.level = Level(self.lvl)
        self.player = Player((0, 0))
        self.camera = Camera(self.player, self.level.get_size()[0])
        save_level(self.lvl)
        self.intro_level()
        self.music = self.songs[self.lvl][0]
        play_music(self.music)
        #except:
        #    if self.lives == 0: # Fix =)
        #        self.lives += 1   
        #    cutscene(self.screen,
        #    ['This was only a test version',
        #     'press enter to end'])
             
        #    self.end()
                            
    def redo_level(self):
        self.booming = False
        self.boom_timer = 0
        self.time = 400
        if self.running:
            self.clear_sprites()
            self.level = Level(self.lvl)
            self.player = Player((0, 0))
            self.camera = Camera(self.player, self.level.get_size()[0])
            self.score -= self.score
            self.highscore = self.highscore

        
    def show_death(self):
        ren = self.font.render("Your Heart was Broken", 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 235))
        pygame.display.flip()
        pygame.time.wait(2500)

    def show_end(self):
        #play_music("goal.ogg")
        HeartBubble((self.player.rect.left + 32, self.player.rect.top))
        for s in self.sprites:
            s.update()    
        pygame.time.wait(7500)
        pygame.display.flip()
        
    def gameover_screen(self):
        stop_music()
        play_music("gameover.ogg")
        cutscene(self.screen, ["Game Over"])
        self.end()

      
    def clear_sprites(self):
        for s in self.sprites:
            pygame.sprite.Sprite.kill(s)

    def main_loop(self):

        while self.running:
            BaddieShot.player = self.player
            CannonShot.player = self.player
            CannonShotbig.player = self.player
            CannonShotsmall.player = self.player
            if not self.running:
                return

            self.boom_timer -= 1

            self.clock.tick(60)
            self.camera.update()
            for s in self.sprites:
                s.update()    
            
            for b in self.PB:
                if self.player.rect.colliderect(b.rect):
                    self.show_end()
                    self.next_level()
                    self.score += 500
                    
            for s in self.shots:
                if not s.rect.colliderect(self.camera.rect):
                    s.kill()
                if s.rect.colliderect(self.player.rect):
                    self.player.hit()
                    s.kill()
            if self.booming and self.boom_timer <= 0:
                self.redo_level()
                
                
            for p in self.platforms:
                p.update()
            self.player.collide(self.springs)
            self.player.collide(self.platforms)

            for g in self.grasss:
                g.update()
            self.player.collide(self.grasss)    
    
            for b in self.bricks:
                b.update()
            self.player.collide(self.bricks)    

            for l in self.grays:
                l.update()
            self.player.collide(self.grays)    
            
            for l in self.leaf:
                l.update()
            self.player.collide(self.leaf)
        
            for m in self.hearts:
                if self.player.rect.colliderect(m.rect):
                    m.kill()
                    Heartdie(m.rect.center)
                    self.score += 5000
                    self.lives += 1
                    self.up_sound.play()
                                    
            for c in self.kisses:
                if self.player.rect.colliderect(c.rect):
                    c.kill()
                    self.kiss_sound.play()
                    KissDie(c.rect.center)
                    self.score += 50
                    
            
                        
            #for p in self.movingplatformtwos:
            #    p.collide(self.players)
            #    for p2 in self.platforms:
            #        if p != p2:
            #            p.collide_with_platforms(p2)

            #for p in self.movingplatforms:
            #    p.collide(self.players)
            #    for p2 in self.platforms:
            #        if p != p2:
            #            p.collide_with_platforms(p2)
        
            for f in self.firebowsers:
                if self.player.rect.colliderect(f.rect):
                    self.player.hit()
#________________________________________________________________________          

            for b in self.baddies:                               # |
                if b.rect.colliderect(self.camera.rect):         # V
                    if b.type == "squidge":
                        if not random.randrange(70):
                            BaddieShot(b.rect.center)
                if b.type != "squidge":
                    b.collide(self.platforms)
                    b.collide(self.movingplatforms)              # Big problem here somewhere,
                    b.collide(self.springs)                      # The enemies is making the game laggy.
                    b.collide(self.cannons)                      # Main problem would be b.collide(self.nomoveplatforms) 
                                                                 # Makes the enemies collide with main platform and for some reason,
                                                                 # that causes alot of problems.
            for c in self.cannons:
                if c.rect.colliderect(self.camera.rect):
                    if c.type == "cannon":
                        if not random.randrange(135):
                            CannonShot(c.rect.center)
                    if c.type != "cannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                    if c.type == "cannonbig":
                        if not random.randrange(120):
                            CannonShotbig(c.rect.center)
                    if c.type != "cannonbig":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)
                    if c.type == "smallcannon":
                         if not random.randrange(145):
                            CannonShotsmall(c.rect.center)
                    if c.type != "smallcannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)    
#_______________________________________________________________________
                        
            for b in self.feet:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()
        
            for r in self.feetbig:
                if self.player.rect.colliderect(r.rect):
                    self.player.hit()
             
            for b in self.bosses:
                if self.player.rect.colliderect(b.rect) and not b.dead:
                    self.player.hit()
                if b.die_time <= 0 and b.dead and not self.explosions:
                    pygamesprite.Sprite.kill(b)
                    self.next_level()
                if b.die_time > 0:
                    for s in self.shots:
                        s.kill()
                    if not random.randrange(4):
                        self.boom_sound.play()
                        
            if self.player.rect.right > self.camera.world.w:
                if not self.bombs and self.lvl < 30:
                    self.next_level()
                else:
                    self.player.rect.right = self.camera.world.w
        
            if self.lvl == 5:
                self.bg = load_image("background-1.png")
                self.music = "castle.ogg"
            else:
                if self.lvl == 6:
                    self.bg = load_image("background-2.png")
                    
            for b in self.baddies:
                if self.player.rect.colliderect(b.rect):
                    if self.player.jump_speed > 0 and \
                        self.player.rect.bottom < b.rect.top+10 and \
                        b.alive():
                        b.kill()
                        self.player.jump_speed = -3
                        self.player.jump_speed = -5
                        self.player.rect.bottom = b.rect.top-1
                        self.score += 100
                        self.baddie_sound.play()
                        BaddieBoom(b.rect.center, b.speed, b.type)
                    else:
                        if b.alive():
                            self.player.hit()

            if self.player.rect.right > self.camera.world.w:
                if not self.bombs and self.lvl < 30:
                    self.next_level()
                else:
                    self.player.rect.right = self.camera.world.w

            if self.player.rect.right > self.camera.world.w:
                self.next_level()

            if self.score > self.highscore:
                self.highscore = self.score

            if self.player.alive():
                self.time -= 0.060
            if self.time <= 0:
                self.player.hit()
                                              
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.end()
                    if e.key == K_z:
                        self.player.jump()     
            if not self.running:
                return
            self.screen.blit(self.bg, ((-self.camera.rect.x/1), 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1), 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1), 0))
            self.camera.draw_sprites(self.screen, self.sprites)
            self.draw_stats()
            for b in self.bosses:
                pygame.draw.rect(self.screen, (255, 0, 0), (170, 64, b.hp*60, 32))
                pygame.draw.rect(self.screen, (0, 0, 0), (170, 64, 300, 32), 1)
            if not self.player.alive() and not self.playerdying:
                if self.lives <= 0:
                    self.gameover_screen()
                else:
                    self.show_death()
                    self.lives -= 1
                    self.redo_level()
            pygame.display.flip()
            if not self.running:
                return

    def draw_stats(self):
        for i in range(self.player.hp):
            self.screen.blit(self.heart1, (16 + i*34, 16))
        self.screen.blit(self.heroimg, (313, 16))
        lives = self.lives
        if lives < 0:
            lives = 0
        ren = self.font.render("Score: %05d" % self.score, 1, (255, 255, 255))
        self.screen.blit(ren, (624-ren.get_width(), 16))
        ren = self.font.render("x%d" % lives, 1, (255, 255, 255))
        self.screen.blit(ren, (315+34, 24))
        ren = self.font.render(self.levels[self.lvl], 1, (255, 255, 255))
        self.screen.blit(ren, (265-ren.get_width(), 16))
        ren = self.font.render("FPS: %d" % self.clock.get_fps(), 1, (255, 255, 255))
        self.screen.blit(ren, (511, 41))
        ren = self.font.render("High:%05d" % self.highscore, 1, (255, 255, 255))
        self.screen.blit(ren, (260-ren.get_width(), 38))
        ren1 = self.font.render("Time: %d" % self.time, 1, (255, 255, 255))
        ren2 = self.font.render("Time: %d" % self.time, 1, Color("#ffffff"))
        self.screen.blit(ren1, (485, 60))
        self.screen.blit(ren2, (485, 60))
