import pygame
import random

ANCHO = 758
ALTO = 757
FPS = 60

pygame.display.set_caption("SPEEDCAR")
pantalla = pygame.display.set_mode((ANCHO, ALTO))
fondo_juego = pygame.image.load("JUEGO_PARCIAL/fondo_juego.png")
fondo_juego_rect = fondo_juego.get_rect()

class Obstaculo:
    def __init__(self, x, y, obstaculos):
        self.x = x
        self.y = y
        self.velocidad = 1
        self.obstaculos = obstaculos
        self.imagen_enemigo = self.obtener_imagen_obstaculo()
        self.ancho, self.alto = self.imagen_enemigo.get_size()  # Ajustar a las dimensiones reales de la imagen
        self.escalar_imagen()  # Escalar la imagen al tamaño deseado

    
    def dibujar(self):
        "Dibuja el obstáculo en la pantalla"
        pantalla.blit(self.imagen_enemigo, (self.x, self.y))

    
    def actualizar(self):
        "Actualiza la posición del obstáculo"
        self.y += self.velocidad
        if self.y > ALTO:
            self.y = random.randint(-75, -50)  # Evitar superposiciones iniciales
            nueva_x = random.choice([280, 356, 435, 500, 205])
            superpone = True
            while superpone:
                superpone = False
                for obstaculo in self.obstaculos:
                    if obstaculo != self and self.obtener_rect(nueva_x).colliderect(obstaculo.obtener_rect()):
                        superpone = True
                        nueva_x = random.choice([280, 356, 435, 500, 205])
                        break
            self.x = nueva_x
            print(f"Obstáculo reaparece en x: {self.x}, y: {self.y}")
            self.imagen_enemigo = self.obtener_imagen_obstaculo()
            self.escalar_imagen()  # Escalar la nueva imagen

    
    def obtener_imagen_obstaculo(self):
        "Devuelve una imagen aleatoria de obstáculo"
        enemigos_imagenes = [
            pygame.image.load("JUEGO_PARCIAL/PERSONAJE/auto_esquiva.png"),
            pygame.image.load("JUEGO_PARCIAL/PERSONAJE/barrera.png"),
            pygame.image.load("JUEGO_PARCIAL/PERSONAJE/barril.png")
        ]
        imagen = random.choice(enemigos_imagenes)
        return imagen

    
    def escalar_imagen(self):
        "Escala la imagen del obstáculo a su doble tamaño"
        self.ancho = self.imagen_enemigo.get_width() * 2
        self.alto = self.imagen_enemigo.get_height() * 2
        self.imagen_enemigo = pygame.transform.scale(self.imagen_enemigo, (self.ancho, self.alto))

    def obtener_rect(self, x=None):
        "Devuelve el rectángulo de colisión del obstáculo"
        if x is None:
            x = self.x
        return pygame.Rect(x, self.y, self.ancho, self.alto)