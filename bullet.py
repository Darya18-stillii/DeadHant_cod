import pygame


from settings import  BULLET_SPEED, SCREEN_W

class Bullet:
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = BULLET_SPEED
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x

    def is_off_screen(self):
        return self.x < 0 or self.x > SCREEN_W

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
