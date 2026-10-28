import pygame
import os
from settings import FPS, SCREEN_H, SCREEN_W, PLAYER_MAX_HP, PLAYER_START_Y, PLAYER_START_X, RELOAD_TIME, JUMP_START_COUNT
from assets import load_assets, BASE_DIR
from player import Player
from enemy import Enemy

pygame.init()

assets = load_assets()
player = Player(assets)
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption('Crocodile Hunter')
clock = pygame.time.Clock()
enemies = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)
gameplay = True
label = pygame.font.Font(os.path.join(BASE_DIR,'fonts','Isometra-Regular.ttf'),50)
label_lose = label.render('You dead',False,(0,0,0))
restart_label = label.render('New play!', False, (6,222,2))
restart_label_rect = restart_label.get_rect(topleft=(200,250))
hud_font = pygame.font.Font(os.path.join(BASE_DIR,'fonts','lol'),30)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == enemy_timer and gameplay:
            new_enemies = Enemy(SCREEN_W, 360, assets['crocodile'])
            enemies.append(new_enemies)
    if gameplay:
        keys = pygame.key.get_pressed()
        player.update(keys)
        for bullet in player.bullets:
            bullet.update()

        for i in range(len(player.bullets) -1, -1, -1):
            if player.bullets[i].is_off_screen():
                player.bullets.pop(i)

        for enemy in enemies:
            enemy.update()

        for bullet in player.bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(1)
                    bullet.x = -1000
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.hp -= 1
                enemy.hp = 0
                if player.hp <= 0:
                    gameplay = False

        for i in range(len(enemies) -1, -1, -1):
            if enemies[i].is_dead():
                player.score += 10
                enemies.pop(i)
            elif enemies[i].x < -50:
                enemies.pop(i)
        screen.blit(assets['bg'],(0,0))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in player.bullets:
            bullet.draw(screen)
        if player.is_reloading:
                progress = player.reloading_timer / RELOAD_TIME
                pygame.draw.rect(screen, (100, 100, 100), (player.x, player.y - 10, 50, 5))
                pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y - 10, 50 * progress, 5))
        for i in range(player.hp):
            x = 10 + i * 40
            screen.blit(assets['heart'], (x, 10))
        score_text = hud_font.render(f'Score:{player.score}', False, (255, 255, 255))
        screen.blit(score_text, (SCREEN_W - 200, 10))
        ammo_text = hud_font.render(f'Ammo:{player.ammo}/{player.max_ammo}', False, (255, 255, 255))
        screen.blit(ammo_text, (SCREEN_W - 200, 50))
    else:
        screen.fill((148,18,18))
        screen.blit(label_lose,(200,200))
        screen.blit(restart_label,(200,250))

        mouse = pygame.mouse.get_pos()

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player.x = PLAYER_START_X
            player.y = PLAYER_START_Y
            player.hp = PLAYER_MAX_HP
            enemies.clear()
            player.bullets.clear()
            player.shoot_cooldown = 0
            player.score = 0
            player.is_jump = False
            player.jump_count = JUMP_START_COUNT
            player.anim_count = 0
            player.jump_timer = 0
            player.anim_timer = 0
            player.is_reloading = False
            player.direction = 1
            player.reloading_timer = 0



    pygame.display.update()
    clock.tick(FPS)
pygame.quit()