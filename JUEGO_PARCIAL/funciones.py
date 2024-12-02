from configuracion import *
# Función para cargar puntajes desde el archivo JSON
def cargar_puntajes():
    if os.path.exists(ARCHIVO_PUNTAJES):  # Verifica si el archivo existe
        with open(ARCHIVO_PUNTAJES, "r") as archivo:
            contenido = archivo.read()
            if contenido:  # Verifica si el contenido no está vacío
                return json.loads(contenido)  # Carga los puntajes
    return []# Si el archivo no existe o está vacio, devolver una lista vacia

# Función para guardar un puntaje en el archivo JSON
def guardar_puntaje(nombre, puntos):
    puntajes = cargar_puntajes()
    
    # Verificar si el nombre ya existe
    nombre_existente = False
    for puntaje in puntajes:
        if puntaje["nombre"] == nombre:
            nombre_existente = True
            if puntos > puntaje["puntos"]:
                puntaje["puntos"] = puntos  # Actualizar el puntaje si es mayor
            break

    if not nombre_existente:
        puntajes.append({"nombre": nombre, "puntos": puntos})  # Agregar nuevo puntaje si no existe

    # Mantener solo los 10 mejores puntajes
    puntajes = sorted(puntajes, key=lambda x: x["puntos"], reverse=True)[:10]
    
    with open(ARCHIVO_PUNTAJES, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)

def mostrar_puntajes():
    puntajes = cargar_puntajes()
    pantalla.fill(NEGRO)
    texto_titulo = fuente_titulo.render("Tabla de Puntos", True, BLANCO)
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))
    
    posicion_tabla_puntajes = 200  # Posición inicial para mostrar los puntajes
    for i, puntaje in enumerate(puntajes):
        texto = fuente.render(f"{i + 1}. {puntaje['nombre']}: {puntaje['puntos']}", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, posicion_tabla_puntajes))
        posicion_tabla_puntajes += 50

    texto_volver = fuente.render("Presiona ESC para volver", True, BLANCO)
    pantalla.blit(texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, posicion_tabla_puntajes + 50))
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Volver al menú
                    esperando = False  # Salir del bucle y volver al menú
                    menu_inicio()

######################################################################

def pedir_nombre():
    global nombre_usuario
    pantalla.fill(NEGRO)

    texto_instruccion = fuente_titulo.render("Introduce tu nombre:", True, BLANCO)
    nombre_rect = pygame.Rect(ANCHO // 2 - 150, 400, 300, 50)
    
    # Mensaje de advertencia
    texto_advertencia = fuente.render("Por favor, ingresa un nombre valido", True, ROJO)
    
    pygame.display.flip()
    nombre = ""
    ingresando_nombre = True
    mostrar_advertencia = False
    tiempo_advertencia = 0  # Para controlar el tiempo de la advertencia

    while ingresando_nombre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter para confirmar
                    if nombre:  # Verifica si hay texto ingresado
                        ingresando_nombre = False
                        nombre_usuario = nombre.upper()  # Convertir el nombre a mayusculas
                    else:
                        mostrar_advertencia = True
                        tiempo_advertencia = pygame.time.get_ticks()  # Captura el tiempo actual
                elif event.key == pygame.K_BACKSPACE:  # Borrar con Backspace
                    nombre = nombre[:-1]
                else:  # Agregar caracteres al nombre
                    nombre += event.unicode

        # Dibujar pantalla
        pantalla.fill(NEGRO)
        pantalla.blit(texto_instruccion, (ANCHO // 2 - texto_instruccion.get_width() // 2, 300))
        pygame.draw.rect(pantalla, BLANCO, nombre_rect, 2)
        texto_nombre = fuente.render(nombre, True, BLANCO)
        pantalla.blit(texto_nombre, (nombre_rect.x + 10, nombre_rect.y + 5))
        
        # Mostrar advertencia si no hay nombre
        if mostrar_advertencia:
            pantalla.blit(texto_advertencia, (ANCHO // 2 - texto_advertencia.get_width() // 2, 460))
            # Verificar si han pasado 2 segundos
            if pygame.time.get_ticks() - tiempo_advertencia > 2000:  # 2 segundos
                mostrar_advertencia = False  # Ocultar advertencia después de 2 segundos

        pygame.display.flip()

def pausa():
    pausado = True

    texto_pausa = fuente_titulo.render("Juego en Pausa", True, BLANCO)
    texto_reanudar = fuente.render("Presiona ESC para continuar", True, BLANCO)
    texto_apagar_musica = fuente.render("Presiona X para apagar la música", True, BLANCO)
    texto_prender_musica = fuente.render("Presiona Z para prender la música", True, BLANCO)

    while pausado:
        pantalla.fill(NEGRO) 
        pantalla.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, 150))
        pantalla.blit(texto_reanudar, (ANCHO//2 - texto_reanudar.get_width()//2, 300))
        pantalla.blit(texto_apagar_musica, (ANCHO//2 - texto_apagar_musica.get_width()//2, 400))
        pantalla.blit(texto_prender_musica, (ANCHO//2 - texto_prender_musica.get_width()//2, 500))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Presiona ESCAPE para continuar
                    pausado = False
                if event.key == pygame.K_x:  # Presiona X para apagar la música
                    sonido_fondo.stop()
                if event.key == pygame.K_z: # Presiona Z para prender la música
                    sonido_fondo.play(-1)

def pantalla_game_over():
    pantalla.fill(NEGRO)
    texto_game_over = fuente_titulo.render("GAME OVER", True, BLANCO)
    texto_reiniciar = fuente.render(f"El jugador {nombre_usuario} hizo {puntos} puntos.", True, BLANCO)
    texto_salir = fuente.render("Presiona ESC para salir al menu", True, BLANCO)

    # Dibujar texto de Game Over
    pantalla.blit(texto_game_over, (ANCHO//2 - texto_game_over.get_width()//2, 150))
    pantalla.blit(texto_reiniciar, (ANCHO//2 - texto_reiniciar.get_width()//2, 300))
    pantalla.blit(texto_salir, (ANCHO//2 - texto_salir.get_width()//2, 400))

    pygame.display.flip()

    guardar_puntaje(nombre_usuario, puntos)

    en_game_over = True
    while en_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Presiona Escape para salir
                    en_game_over = False
                    menu_inicio()
                    return

def menu_inicio():
    pantalla.fill(NEGRO)
    texto_titulo = fuente_titulo.render("SPEEDCAR", True, BLANCO)
    texto_jugar = fuente.render("Iniciar Juego", True, BLANCO)
    texto_tabla = fuente.render("Tabla de puntos", True, BLANCO)
    texto_salir = fuente.render("Salir", True, BLANCO)

    # Definir las posiciones y tamaños de los recuadros
    rect_jugar = texto_jugar.get_rect(center=(ANCHO//2, 300))
    rect_tabla = texto_tabla.get_rect(center=(ANCHO//2, 400))
    rect_salir = texto_salir.get_rect(center=(ANCHO//2, 500))

    # Dibujar recuadros alrededor del texto
    pygame.draw.rect(pantalla, BLANCO, rect_jugar.inflate(20, 20), 2)  # Inflate (20, 20) aumenta el tamaño del recuadro (en este caso 20 pixeles de cada lado)
    pygame.draw.rect(pantalla, BLANCO, rect_tabla.inflate(20, 20), 2)
    pygame.draw.rect(pantalla, BLANCO, rect_salir.inflate(20, 20), 2)

    # Dibujar texto
    pantalla.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 150))
    pantalla.blit(texto_jugar, rect_jugar.topleft)
    pantalla.blit(texto_tabla, rect_tabla.topleft)
    pantalla.blit(texto_salir, rect_salir.topleft)

    pygame.display.flip()

    en_menu = True
    while en_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presiona Enter para iniciar el juego
                    en_menu = False
                    pedir_nombre()
                    iniciar_juego()
                if event.key == pygame.K_ESCAPE:  # Presiona Escape para salir
                    pygame.quit()
                    exit()
                if event.key == pygame.K_DOWN:  # Presiona abajo para ver la tabla de puntajes
                    mostrar_puntajes()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rect_jugar.collidepoint(mouse_pos):
                    en_menu = False
                    pedir_nombre()
                    iniciar_juego()
                if rect_tabla.collidepoint(mouse_pos):
                    mostrar_puntajes()  # Mostrar tabla de puntos
                if rect_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

def iniciar_juego():
    global flag_prendido, fondo_y, puntos, jugador, obstaculos

    flag_prendido = True

    # Crear el objeto del jugador
    jugador = Auto(363, 670)
    obstaculos = []
    distancia_minima = 40  # Distancia minima vertical entre obstaculos

    # Generar obstaculos iniciales
    for _ in range(9):
        intentos = 0  # Contador de intentos
        while intentos < 100:  # Límite de intentos
            x_pos = random.choice(carriles_x)
            y_pos = random.randint(10, 500)
            nuevo_obstaculo = Obstaculo(x_pos, y_pos, obstaculos)

            # Verificar que no haya superposición exacta ni cercania vertical
            superpone = False
            for o in obstaculos:
                if (nuevo_obstaculo.obtener_rect().colliderect(o.obtener_rect()) or abs(nuevo_obstaculo.y - o.y) < distancia_minima):
                    superpone = True
                    break

            if not superpone:
                obstaculos.append(nuevo_obstaculo)
                break  # Salir del bucle si se encontro una posicion valida

            intentos += 1  # Incrementar el contador de intentos

    fondo_y = 0
    puntos = 0

    # Reproducir sonido de fondo al iniciar el juego
    sonido_fondo.play(-1)

    reloj = pygame.time.Clock()
    while flag_prendido:
        reloj.tick(FPS)
        puntos += 1  # Incrementar puntos en cada iteracion del bucle principal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_prendido = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Presiona 'P' para pausar el juego
                    pausa()

        # Actualizar posicion del fondo
        fondo_y += 2
        if fondo_y >= ALTO:
            fondo_y = 0

        # Dibujar fondo en la pantalla
        pantalla.blit(fondo_juego, (0, fondo_y - ALTO))
        pantalla.blit(fondo_juego, (0, fondo_y))

        # Dibujar el jugador y los obstáculos
        jugador.dibujar()
        for obstaculo in obstaculos:
            obstaculo.actualizar()
            obstaculo.dibujar()

        # Verificar colisiones entre el jugador y los obstáculos
        jugador_rect = jugador.obtener_rect()
        for obstaculo in obstaculos:
            if jugador_rect.colliderect(obstaculo.obtener_rect()):
                print("Colision detectada! Fin del juego.")
                sonido_colision.play()
                sonido_fondo.stop()  # Detener el sonido de fondo
                pantalla_game_over()
                menu_inicio()
                iniciar_juego()

        # Movimiento del personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and jugador.x > 200:
            jugador.x -= jugador.velocidad
        if keys[pygame.K_RIGHT] and jugador.x < 520:
            jugador.x += jugador.velocidad
        if keys[pygame.K_UP]:
            jugador.y -= jugador.velocidad
        if keys[pygame.K_DOWN]:
            jugador.y += jugador.velocidad

        # Límites de la pantalla para el personaje
        if jugador.x < 200:
            jugador.x = 200
        if jugador.x > 520:
            jugador.x = 520
        if jugador.y < 400:
            jugador.y = 400
        if jugador.y + jugador.alto > ALTO:
            jugador.y = ALTO - jugador.alto

        # Mostrar los puntos en pantalla
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))

        pygame.display.flip()

def play_speedcar():
    menu_inicio()
    iniciar_juego()
    pygame.quit()