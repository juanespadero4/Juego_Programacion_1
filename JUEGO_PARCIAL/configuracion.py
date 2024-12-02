import pygame
import os
import json
from jugador import *
from obstaculo import *

pygame.init()
pygame.mixer.init()

ANCHO = 758
ALTO = 757
FPS = 60

carriles_x = [280, 356, 435, 500, 205]
pygame.display.set_caption("SPEEDCAR")
icono = pygame.image.load("Juego_Programacion_1/JUEGO_PARCIAL/PERSONAJE/auto_icono2.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode((ANCHO, ALTO))
fondo_juego = pygame.image.load("Juego_Programacion_1/JUEGO_PARCIAL/fondo_juego.png")
fondo_juego_rect = fondo_juego.get_rect()
fuente = pygame.font.Font("Juego_Programacion_1/JUEGO_PARCIAL/FUENTE/game_over.ttf", 60)  # Fuente para mostrar los puntos
fuente_titulo = pygame.font.Font("Juego_Programacion_1/JUEGO_PARCIAL/FUENTE/game_over.ttf", 100)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)  

# Cargar archivos de sonidos
sonido_fondo = pygame.mixer.Sound("Juego_Programacion_1/JUEGO_PARCIAL/SONIDOS/sonido_fondo.mp3")
sonido_colision = pygame.mixer.Sound("Juego_Programacion_1/JUEGO_PARCIAL/SONIDOS/game_over.mp3")

nombre_usuario = ""  # Variable para almacenar el nombre del usuario

######################################################################
ARCHIVO_PUNTAJES = "Juego_Programacion_1/JUEGO_PARCIAL/puntaje_jugadores.json"

