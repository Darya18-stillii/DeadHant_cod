
import  pygame
from settings import CROCODILE_SPEED,CROCODILE_HP

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.hp = CROCODILE_HP
        self.speed = CROCODILE_SPEED
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def take_damage(self, dmg):
        self.hp -= dmg

    def is_dead(self):
        return self.hp <= 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

