import pygame
import random

ANCHO = 758
ALTO = 757
FPS = 60

pygame.display.set_caption("SPEEDCAR")
pantalla = pygame.display.set_mode((ANCHO, ALTO))
fondo_juego = pygame.image.load("JUEGO_PARCIAL/fondo_juego.png")
fondo_juego_rect = fondo_juego.get_rect()

class Auto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.imagen = pygame.image.load("JUEGO_PARCIAL/PERSONAJE/auto.png")
        self.ancho, self.alto = self.imagen.get_size()  # Ajustar a las dimensiones reales de la imagen

    def dibujar(self):
        "Dibuja el auto en la pantalla"
        pantalla.blit(self.imagen, (self.x, self.y))

    def obtener_rect(self):
        "Devuelve el rectángulo de colisión del auto"
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)




