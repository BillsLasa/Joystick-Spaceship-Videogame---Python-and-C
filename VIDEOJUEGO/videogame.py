import serial	#Librería para Comunicación Serial
import time		#Esperar un tiempo
import sys		#Para transformar de bytes a decimal y cerrar ventana de pygame
import pygame	#Librería para crear videojuegos 
from pygame.locals import *	#Importar ciertas funciones o variables de pygame
import random   #Libréría para valores aleatorios


################################################################################
#PROPIEDADES BÁSICAS DEL JUEGO
################################################################################
#VENTANA
global anchoVentana
global altoVentana
global tamanoVentana 						#TAMAÑO DE LA VENTANA
global colorFondoVentana 					#COLOR DE LA VENTANA DE FONDO
anchoVentana = 800
altoVentana = 600
tamanoVentana = (anchoVentana,altoVentana)
colorFondoVentana = (0,0,0)

#NAVE
global colorColisionNave							#COLOR DE LA COLISIÓN DE LA NAVE - ROJO
global posXNave										#POSICIÓN INICIAL X DE LA COLISIÓN DE LA NAVE
global posYNave 									#POSICIÓN INICIAL Y DE LA COLISIÓN DE LA NAVE
global anchoNave 									#ANCHO DE LA COLISIÓN DE LA NAVE
global altoNave 									#ALTO DE LA COLISIÓN DE LA NAVE
colorColisionNave = (193,59,59)					
posXNave = 360									
posYNave = 400									
anchoNave = 80									
altoNave = 80									

#ACCIONES NAVE
global velocidadXNave 
global velocidadYNave 
velocidadXNave = 0
velocidadYNave = 0

#ESTRELLAS
global randomXEstrellas
global randomYEstrellas
global coordenadasEstrellasInicial
global colorEstrellas
global velocidadEstrellas

randomXEstrellas = 0	#POSICIÓN RANDOM EN X DE LAS ESTRELLAS DE FONDO
randomYEstrellas = 0 	#POSICIÓN RANDOM EN Y DE LAS ESTRELLAS DE FONDO
coordenadasEstrellasInicial = []	#COORDENADAS INICIALES DE LAS ESTRELLAS
colorEstrellas = (255,255,255)
velocidadEstrellas = 1

#METEORITOS
global randomXMeteoritos
global randomYMeteoritos
global coordenadasMeteoritosInicial
global colorMeteoritos
global velocidadMeteoritos
global anchoMeteorito 									#ANCHO DE LA COLISIÓN DEL METEORITO
global altoMeteorito 									#ALTO DE LA COLISIÓN DEL METEORITO
global numeroMeteorito

randomXMeteoritos = 0	#POSICIÓN RANDOM EN X DE LOS METEORITOS
randomYMeteoritos = 0 	#POSICIÓN RANDOM EN Y DE LOS METEORITOS
coordenadasMeteoritosInicial = []	#COORDENADAS INICIALES DE LOS METEORITOS
colorMeteoritos = (59,140,193)
velocidadMeteoritos = []
anchoMeteorito = 80
altoMeteorito  = 80
numeroMeteorito = 0

#BALA
global posXBala
global posYBala
global colorBala
global velocidadBala	
global anchoBala
global altoBala
global lanzarBala
global numeroBalas
global colisionBala
global yaHayBala
global numeroBalas
global balasParaEliminar

posXBala = 0	#POSICIÓN EN X DE LA BALA
posYBala = []	#POSICIÓN EN X DE LA BALA

colorBala = (40,60,230)
velocidadBala = 20		#VELOCIDAD EN Y DE LA BALA

anchoBala = 14
altoBala  = 30

lanzarBala = 0
numeroBalas = 0
colisionBala = []
yaHayBala = 0
balasParaEliminar = []


#VIDA Y PUNTAJE
global numeroVidas
global posInicioVida
global numeroPuntaje

numeroVidas = 3
numeroPuntaje = 0

#VARIABLES PARA ACCIONES
global botonEstado
global botonPresionado
global pantalla
global pantallaMenuPrincipal
global pantallaOpciones
global pantallaGameOver
global joystickDecena
global joystickUnidad

botonEstado = 0			#INDICA QUE BOTÓN SE HA PRESIONADO Y VELOCIDAD DEL JOYSTICK 
						# 0: SIN ACCIÓN; 1: START; 2: SELECT; 3: ARRIBA; 4: ABAJO
						# ab: a representa velocidad en X, b representa velocidad en Y
pantalla = 0			#INDICA EN QUE PANTALLA ESTAMOS
						# 0: MENU PRINCIPAL; 1: JUEGO; 2: OPCIONES; 3: GAME OVER
pantallaMenuPrincipal = 0	#INDICA EN QUE MODO ESTÁS POSICIONADO DEL MENÚ PRINCIPAL
							# 0: INICIAR; 1: SALIR
pantallaOpciones = 0	#INDICA EN QUE MODO ESTÁS POSICIONADO DE OPCIONES
						# 0: REANUDAR; 1: SALIR 
botonPresionado = 0		#INDICA SI SE HA PRESIONADO EL BOTÓN O NO, (ESTO PARA EVITAR QUE POR PRESIONAR UNA VEZ, LA ACCIÓN OCURRA VARIAS VECES)
						# 0: NO SE HA PRESIONADO; 1: SÍ SE HA PRESIONADO
pantallaGameOver = 0	#INDICA EN QUE MODO ESTÁS POSICIONADO EN GAME OVER
						# 0: REINICIAR; 1: SALIR
################################################################################
#PROCEDIMIENTOS PREVIOS
################################################################################
#Hallar las coordenadas iniciales aleatorias de estrellas
def coordenadasEstrellas():
	for i in range(60):
		randomXEstrellas = random.randint(0,anchoVentana)
		randomYEstrellas = random.randint(0,altoVentana)
		coordenadasEstrellasInicial.append([randomXEstrellas,randomYEstrellas])	#Agregar a la lista las coordenadas de uns estrella

#Hallar las coordenadas iniciales aleatorias de meteoritos
def coordenadasMeteoritos():
	global velocidadMeteoritos
	global tipoMeteorito
	tipoMeteorito = []

	for j in range(10):
		randomXMeteoritos = random.randint(0,anchoVentana)
		randomYMeteoritos = random.randint((altoVentana/3)-400,0)
		velocidadMeteoritos.append(random.randint(3,6))
		tipoMeteorito.append(random.randint(0,2))
		coordenadasMeteoritosInicial.append([randomXMeteoritos,randomYMeteoritos])	#Agregar a la lista las coordenadas de un meteorito


################################################################################
#PROCEDIMIENTOS REPETITIVOS
################################################################################
def obtenerEventosMando():
	#estadoVideojuego = serial.Serial('COM4', baudrate = 9600, bytesize=8, parity='N', stopbits=1)
	#time.sleep(2)
	botonEstado = 0
	
	print ("ESPERANDO COMUNICACIÓN")
	estadoVideojuego = serial.Serial('COM8', baudrate = 9600, bytesize=8, parity='N', stopbits=1)
	bait = estadoVideojuego.read()
	botonEstado = int.from_bytes(bait, byteorder = sys.byteorder)
	print(botonEstado)

	#try:
	#	print ("ESPERANDO COMUNICACIÓN")
	#	estadoVideojuego = serial.Serial('COM4', baudrate = 9600, bytesize=8, parity='N', stopbits=1)
	#	bait = estadoVideojuego.read()
	#	botonEstado = int.from_bytes(bait, byteorder = sys.byteorder)
	#	print(botonEstado)
	#except:
	#	pass

	return botonEstado

################################################################################
#ELEMENTOS DEL JUEGO
################################################################################
def estrellas():
	global velocidadEstrellas

	for coordStar in coordenadasEstrellasInicial:
		pygame.draw.circle(ventana,colorEstrellas,coordStar,2)
		coordStar[1] += velocidadEstrellas	#BAJAR EN Y EN UNA UNIDAD
		#CONDICIÓN PARA REINICIAR LA ESTRELLA DESDE EL PRINCIPIO EN Y
		if(coordStar[1] > altoVentana):
			coordStar[1] = 0

def meteoritos():
	global velocidadMeteoritos
	global numeroMeteorito
	global colisionMeteorito
	global tipoMeteorito
	global numeroTipoMeteorito
	global meteoritoSprite1
	global meteoritoSprite2
	global meteoritoSprite3
	colisionMeteorito = []
	numeroColision = 0
	numeroTipoMeteorito = 0

	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	meteoritoSprite1 = pygame.image.load("imagenes/meteorito.png").convert_alpha()		#IMAGEN METEORITO
	meteoritoSprite2 = pygame.image.load("imagenes/meteorito2.png").convert_alpha()		#IMAGEN METEORITO
	meteoritoSprite3 = pygame.image.load("imagenes/meteorito3.png").convert_alpha()		#IMAGEN METEORITO

	for coordMeteor in coordenadasMeteoritosInicial:
		colisionMeteorito.append(pygame.Rect(coordMeteor[0],coordMeteor[1],anchoMeteorito,altoMeteorito))	#Colisión nave
		#pygame.draw.rect(ventana,colorMeteoritos,colisionMeteorito[numeroColision])	#Colisión nave
		if(tipoMeteorito[numeroTipoMeteorito] == 0):
			ventana.blit(meteoritoSprite1, [coordMeteor[0],coordMeteor[1]]) ##MOSTRAR METEORITOS 
		if(tipoMeteorito[numeroTipoMeteorito] == 1):
			ventana.blit(meteoritoSprite2, [coordMeteor[0],coordMeteor[1]]) ##MOSTRAR METEORITOS 
		if(tipoMeteorito[numeroTipoMeteorito] == 2):
			ventana.blit(meteoritoSprite3, [coordMeteor[0],coordMeteor[1]]) ##MOSTRAR METEORITOS 

		#VELOCIDAD
		coordMeteor[1] += velocidadMeteoritos[numeroMeteorito]	#BAJAR EN Y EN UNA UNIDAD
		#CONDICIÓN PARA REINICIAR LA ESTRELLA DESDE EL PRINCIPIO EN Y
		if(coordMeteor[1] > altoVentana):
			coordMeteor[1] = random.randint((altoVentana/3)-400,0)
			#El meteorito inicia en algún valor random del ancho
			coordMeteor[0] = random.randint(0,anchoVentana)
		#PARA IR AL SIGUIENTE METEORITO
		if(numeroMeteorito == 9):
			numeroMeteorito = 0
		else:
			numeroMeteorito+=1
		#PARA IR AL SIGUIENTE METEORITO
		if(numeroTipoMeteorito == 9):
			numeroTipoMeteorito = 0
		else:
			numeroTipoMeteorito+=1

		numeroColision += 1


def bala():
	global posXBala
	global posYBala
	global velocidadBala
	global lanzarBalaInicio
	global numeroBalas
	global colisionBala
	global yaHayBala
	global balasParaEliminar
	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	balaSprite = pygame.image.load("imagenes/bala.png").convert_alpha()		#IMAGEN METEORITO

	################################################################################
	#CARGAR SONIDOS
	################################################################################
	salidaBalaSound = pygame.mixer.Sound("sonidos/lanzarBala.wav")

	################################################################################
	#LÓGICA
	################################################################################
	if(lanzarBala == 1):
		numeroBalas += 1	#Aumentar la cantidad de balas

	if(numeroBalas > 0):
		print("YA HAY BALA")
		yaHayBala = 1
	else:
		yaHayBala = 0

	posXBala = posXNave + 33	#Posición X en la parte central de la nave

	#POSICIÓN INICIAL DE LA BALA
	if(lanzarBalaInicio == 1):
		posYBala.append(posYNave)	#Posición Y inicial de la Bala
		colisionBala.append(pygame.Rect(posXBala,posYBala[numeroBalas-1],anchoBala,altoBala))	#Colisión Bala
		salidaBalaSound.play()
		lanzarBalaInicio = 0

	#PONER COLISIONES Y SPRITE DE LA BALA
	for m in range(numeroBalas):
		#COLISIÓN DE LA BALA
		posYBala[m] -= velocidadBala
		colisionBala[m] = pygame.Rect(posXBala,posYBala[m],anchoBala,altoBala)
		#pygame.draw.rect(ventana,colorBala,colisionBala[m])	#Colisión Bala
		ventana.blit(balaSprite, [posXBala,posYBala[m]-5]) ##MOSTRAR BALA

		#REDUCIR NUMERO DE BALAS, SI YA SALIÓ FUERA DE LA PANTALLA CREANDO UNA LISTA DE BALAS POR ELIMINAR
		if(posYBala[m] < -200):
			balasParaEliminar.append(m)
		
	#ELIMINAR TODAS LAS BALAS FUERA DE LA PANTALLA		
	for n in range(len(balasParaEliminar)):
		colisionBala.pop(balasParaEliminar[n])	#ELIMINAR LA COLISIÓN QUE HA SALIDO FUERA DE PANTALLA
		posYBala.pop(balasParaEliminar[n])		#ELIMINAR LA POSICIÓN DE LA BALA m
	
	numeroBalas = numeroBalas - len(balasParaEliminar)
	balasParaEliminar = []


def vida():
	global numeroVidas
	global posInicioVida

	posInicioVida = (40,20)
	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	corazon = pygame.image.load("imagenes/corazon.png").convert_alpha()		#IMAGEN METEORITO

	if(numeroVidas == 0):
		pantalla = 3

	#INICIAR POSICIÓN DE LOS CORAZONES
	for t in range(numeroVidas):
		ventana.blit(corazon, [posInicioVida[0]+30*t, posInicioVida[1]]) ##MOSTRAR BALA

def puntaje():
	global numeroPuntaje

	################################################################################
	#CARGAR FUENTES
	################################################################################
	alturaLetra = 20
	fuentePuntaje = pygame.font.SysFont("Arial Black",alturaLetra)
	textPuntaje = str(numeroPuntaje).zfill(6)

	textPuntajeCompleto = fuentePuntaje.render(textPuntaje,0,(255,255,255))
	ventana.blit(textPuntajeCompleto, [650, 20]) ##MOSTRAR BALA
################################################################################
#PANTALLAS O MENÚ
################################################################################
def menuPrincipal():
	global pantallaMenuPrincipal
	global botonPresionado
	global pantalla
	global botonEstado
	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	#IMÁGENES MENÚ PRINCIPAL
	mpIniciar = pygame.image.load("imagenes/menuPrincipal_Iniciar.png").convert()	#MENÚ PRINCIPAL - INICIAR
	mpSalir   = pygame.image.load("imagenes/menuPrincipal_Salir.png").convert()		#MENÚ PRINCIPAL - SALIR

	################################################################################
	#CARGAR SONIDOS
	################################################################################
	irIniciar = pygame.mixer.Sound("sonidos/aceptarMenu.wav")
	cambiarMenu = pygame.mixer.Sound("sonidos/cambiarMenu.wav")
	################################################################################
	#COLOCAR IMÁGENES
	################################################################################
	#FONDO
	if(pantallaMenuPrincipal == 0):
		ventana.blit(mpIniciar, [0,0])	#Colorear el fondo de la ventana

	if(pantallaMenuPrincipal == 1):
		ventana.blit(mpSalir, [0,0])	#Colorear el fondo de la ventana

	################################################################################
	#ACCIONES SEGÚN BOTÓN PRESIONADO
	################################################################################
	#CONSIDERAR QUE RECIÉN CUANDO SE SOLTÓ EL BOTÓN, SE PUEDE VOLVER A ACCIONAR LO DE 3 O 4 EN BOTÓN PRESIONADO
	#Ningún botón presionado ni Joystick
	if(botonEstado == 0):
		botonPresionado = 0

	#BAJAR EN EL MENÚ - BOTÓN ABAJO
	if(botonEstado == 4 and botonPresionado == 0):
		if(pantallaMenuPrincipal == 1):
			pantallaMenuPrincipal = 0
		else:
			pantallaMenuPrincipal += 1
		botonPresionado = 1

		cambiarMenu.play()
	#SUBIR EN EL MENÚ - BOTÓN ARRIBA
	elif(botonEstado == 3 and botonPresionado == 0):
		if(pantallaMenuPrincipal == 0):
			pantallaMenuPrincipal = 1
		else:
			pantallaMenuPrincipal -= 1
		botonPresionado = 1

		cambiarMenu.play()

	#SI SE PRESIONA START
	if(botonEstado == 1 and botonPresionado == 0):
		#EN INICIAR, IR A LA PANTALLA DE JUEGO (1)
		if(pantallaMenuPrincipal == 0):
			pantalla = 1
			irIniciar.play()
		#EN SALIR, SALIR DEL JUEGO
		if(pantallaMenuPrincipal == 1):
			pygame.quit()
			sys.exit()
		botonPresionado = 1

############################################
def juego():
	global botonEstado
	global posXNave
	global posYNave
	global velocidadXNave
	global velocidadYNave
	global velocidadEstrellas
	global velocidadMeteoritos
	global pantalla 
	global numeroMeteorito
	global colisionNave
	global colisionMeteorito
	global siColisiono
	global lanzarBala
	global lanzarBalaInicio
	global botonPresionado
	global yaHayBala
	global coordenadasMeteoritosInicial
	global numeroBalas
	global posYBala
	global colisionBala
	global balasParaEliminar
	global joystickDecena
	global joystickUnidad

	global numeroVidas
	global numeroPuntaje

	siColisiono = 0
	velocidadEstrellas = 1

	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	naveSprite = pygame.image.load("imagenes/nave.png").convert_alpha()		#MENÚ PRINCIPAL - SALIR

	################################################################################
	#CARGAR SONIDOS
	################################################################################
	choqueNave = pygame.mixer.Sound("sonidos/choqueNave.wav")
	choqueBala = pygame.mixer.Sound("sonidos/choqueBala.wav")

	irSelect = pygame.mixer.Sound("sonidos/aceptarMenu.wav")
	################################################################################
	#ACCIONES SEGÚN BOTÓN PRESIONADO
	################################################################################
	#Ningún botón presionado ni Joystick
	if(botonEstado == 0):
		velocidadXNave = 0
		velocidadYNave = 0
		botonPresionado = 0	#INDICAR QUE YA SE DEJÓ DE PRESIONAR BOTÓN

	#Botón ARRIBA
	if(botonEstado == 3):
		velocidadYNave = -10

	#Botón ABAJO
	if(botonEstado == 4):
		velocidadYNave = 10

	#Botón SELECT
	if(botonEstado == 2):
		velocidadEstrellas = 0
		velocidadXNave = 0
		velocidadYNave = 0
		pantalla = 2
		botonPresionado = 1

		irSelect.play()

	#Botón START
	if(botonEstado == 1 and botonPresionado == 0):
		lanzarBala = 1
		lanzarBalaInicio = 1
		botonPresionado = 1

	#Joystick
	#Se aseguran 2 cifras
	if(botonEstado > 10):
		joystickDecena = int(botonEstado/10)
		joystickUnidad = botonEstado%10

		#OBTENER VELOCIDAD EN X POR JOYSTICK
		if(joystickDecena == 1):
			velocidadXNave = 20
		elif(joystickDecena == 2): 
			velocidadXNave = 10
		elif(joystickDecena == 3): 
			velocidadXNave = 5
		elif(joystickDecena == 4): 
			velocidadXNave = 0
		elif(joystickDecena == 5): 
			velocidadXNave = -5
		elif(joystickDecena == 6): 
			velocidadXNave = -10
		elif(joystickDecena == 7): 
			velocidadXNave = -20

		#OBTENER VELOCIDAD EN Y POR JOYSTICK
		if(joystickUnidad == 1):
			velocidadYNave = 20
		elif(joystickUnidad == 2): 
			velocidadYNave = 10
		elif(joystickUnidad == 3): 
			velocidadYNave = 5
		elif(joystickUnidad == 4): 
			velocidadYNave = 0
		elif(joystickUnidad == 5): 
			velocidadYNave = -5
		elif(joystickUnidad == 6): 
			velocidadYNave = -10
		elif(joystickUnidad == 7): 
			velocidadYNave = -20

	#VELOCIDAD EN CERO CUANDO ESTÁ EN LOS LÍMITES
	#if(posXNave >)
	#Colocar Colisión según velocidad
	posXNave += velocidadXNave
	posYNave += velocidadYNave

	################################################################################
	#ZONA DE DIBUJO, COLOREO Y CREACIÓN DE COLISIONES
	################################################################################
	#FONDO
	ventana.fill(colorFondoVentana)	#Colorear el fondo de la ventana
	estrellas()	#Dibujar estrellas

	#NAVE
	colisionNave = pygame.Rect(posXNave,posYNave,anchoNave,altoNave)	#Colisión nave
	ventana.blit(naveSprite, [posXNave-20,posYNave-20]) ##MOSTRAR NAVE
	#pygame.draw.rect(ventana,colorColisionNave,colisionNave)	#Colisión nave

	#METEORITOS
	meteoritos() #Dibujar Meteoritos

	if(lanzarBala == 1):
		bala()
		lanzarBala = 0

	if(yaHayBala == 1):
		bala()

	#SISTEMA DE VIDA Y PUNTAJE
	vida()
	puntaje()
	################################################################################
	#ACCIONES POR COLISIONES
	################################################################################
	#CHOQUE NAVE - METEORITO: ELIMINAR METEORITO Y GENERAR OTRO MUY ARRIBA DE LA PANTALLA
	for k in range(10): 
		if(colisionNave.colliderect(colisionMeteorito[k])):
			colisionMeteorito.pop(k)	#ELIMINAR LA COLISIÓN QUE HA CHOCADO
			coordenadasMeteoritosInicial[k][0] = random.randint(0,anchoVentana)
			coordenadasMeteoritosInicial[k][1] = random.randint((altoVentana/3)-400,0)
			nuevaColision = pygame.Rect(coordenadasMeteoritosInicial[k][0],coordenadasMeteoritosInicial[k][1],anchoMeteorito,altoMeteorito)
			colisionMeteorito.insert(k,nuevaColision)	

			choqueNave.play()
			#QUITA VIDA POR CHOQUE
			numeroVidas -= 1

	#CHOQUE BALA - METEORITO: ELIMINAR METEORITO Y GENERAR OTRO MUY ARRIBA DE LA PANTALLA, Y ELIMINAR BALA
	for p in range(len(colisionBala)):
		for q in range(len(colisionMeteorito)):
			if(colisionMeteorito[q].colliderect(colisionBala[p])):
				#ELIMINAR Y REEMPLAZA METEORITO
				colisionMeteorito.pop(q)	#ELIMINAR LA COLISIÓN QUE HA CHOCADO
				coordenadasMeteoritosInicial[q][0] = random.randint(0,anchoVentana)
				coordenadasMeteoritosInicial[q][1] = random.randint((altoVentana/3)-400,0)
				nuevaColision = pygame.Rect(coordenadasMeteoritosInicial[q][0],coordenadasMeteoritosInicial[q][1],anchoMeteorito,altoMeteorito)
				colisionMeteorito.insert(q,nuevaColision)

				#REDUCIR NUMERO DE BALAS, SI CHOCÓ
				balasParaEliminar.append(p)

				choqueBala.play()

				#AUMENTAR PUNTAJE
				numeroPuntaje += 10
				
	#ELIMINAR TODAS LAS BALAS QUE HAN CHOCADO	
	for r in range(len(balasParaEliminar)):
		colisionBala.pop(balasParaEliminar[r])	#ELIMINAR LA COLISIÓN QUE HA SALIDO FUERA DE PANTALLA
		posYBala.pop(balasParaEliminar[r])		#ELIMINAR LA POSICIÓN DE LA BALA m
		
			
	numeroBalas = numeroBalas - len(balasParaEliminar)
	balasParaEliminar = []

############################################
def opciones():
	global pantallaOpciones
	global botonPresionado
	global pantalla
	global botonEstado
	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	#IMÁGENES MENÚ PRINCIPAL
	oReanudar = pygame.image.load("imagenes/opciones_Reanudar.png").convert()	#MENÚ PRINCIPAL - INICIAR
	oSalir    = pygame.image.load("imagenes/opciones_Salir.png").convert()		#MENÚ PRINCIPAL - SALIR

	################################################################################
	#CARGAR SONIDOS
	################################################################################
	cambiarSelect = pygame.mixer.Sound("sonidos/cambiarMenu.wav")
	irReanudar = pygame.mixer.Sound("sonidos/aceptarMenu.wav")
	################################################################################
	#COLOCAR IMÁGENES
	################################################################################
	#FONDO
	if(pantallaOpciones == 0):
		ventana.blit(oReanudar, [100,150])	#Colorear el fondo de la ventana

	if(pantallaOpciones == 1):
		ventana.blit(oSalir, [100,150])	#Colorear el fondo de la ventana

	################################################################################
	#ACCIONES SEGÚN BOTÓN PRESIONADO
	################################################################################
	#CONSIDERAR QUE RECIÉN CUANDO SE SOLTÓ EL BOTÓN, SE PUEDE VOLVER A ACCIONAR LO DE 3 O 4 EN BOTÓN PRESIONADO
	#Ningún botón presionado ni Joystick
	if(botonEstado == 0):
		botonPresionado = 0

	#BAJAR EN OPCIONES - BOTÓN ABAJO
	if(botonEstado == 4 and botonPresionado == 0):
		if(pantallaOpciones == 1):
			pantallaOpciones = 0
		else:
			pantallaOpciones += 1
		botonPresionado = 1

		cambiarSelect.play()
	#SUBIR EN EL MENÚ - BOTÓN ARRIBA
	elif(botonEstado == 3 and botonPresionado == 0):
		if(pantallaOpciones == 0):
			pantallaOpciones = 1
		else:
			pantallaOpciones -= 1
		botonPresionado = 1

		cambiarSelect.play()

	#SI SE PRESIONA START
	if(botonEstado == 1 and botonPresionado == 0):
		#EN INICIAR, IR A LA PANTALLA DE JUEGO (1)
		if(pantallaOpciones == 0):
			pantalla = 1
			irReanudar.play()
		#EN SALIR, SALIR DEL JUEGO
		if(pantallaOpciones == 1):
			pygame.quit()
			sys.exit()
		botonPresionado = 1

############################################
def gameOver():
	global pantallaGameOver
	global botonPresionado
	global pantalla
	global numeroVidas
	global botonEstado
	global colisionMeteorito 
	global colisionBala
	global velocidadMeteoritos 
	global velocidadEstrellas
	global coordenadasMeteoritosInicial
	global coordenadasEstrellasInicial 
	global tipoMeteorito
	global posXNave
	global posYNave
	global numeroPuntaje
	################################################################################
	#CARGAR IMÁGENES
	################################################################################
	#IMÁGENES MENÚ PRINCIPAL
	goReiniciar = pygame.image.load("imagenes/gameOver_Reiniciar.png").convert()	#MENÚ PRINCIPAL - INICIAR
	goSalir   = pygame.image.load("imagenes/gameOver_Salir.png").convert()		#MENÚ PRINCIPAL - SALIR

	################################################################################
	#CARGAR SONIDOS
	################################################################################
	irReiniciar = pygame.mixer.Sound("sonidos/aceptarMenu.wav")
	cambiarGameOver = pygame.mixer.Sound("sonidos/cambiarMenu.wav")
	################################################################################
	#COLOCAR IMÁGENES
	################################################################################
	#FONDO
	if(pantallaGameOver == 0):
		ventana.blit(goReiniciar, [0,0])	#Colorear el fondo de la ventana

	if(pantallaGameOver == 1):
		ventana.blit(goSalir, [0,0])	#Colorear el fondo de la ventana

	################################################################################
	#ACCIONES SEGÚN BOTÓN PRESIONADO
	################################################################################
	#CONSIDERAR QUE RECIÉN CUANDO SE SOLTÓ EL BOTÓN, SE PUEDE VOLVER A ACCIONAR LO DE 3 O 4 EN BOTÓN PRESIONADO
	#Ningún botón presionado ni Joystick
	if(botonEstado == 0):
		botonPresionado = 0

	#BAJAR EN EL MENÚ - BOTÓN ABAJO
	if(botonEstado == 4 and botonPresionado == 0):
		if(pantallaGameOver == 1):
			pantallaGameOver = 0
		else:
			pantallaGameOver += 1
		botonPresionado = 1

		cambiarGameOver.play()
	#SUBIR EN EL MENÚ - BOTÓN ARRIBA
	elif(botonEstado == 3 and botonPresionado == 0):
		if(pantallaGameOver == 0):
			pantallaGameOver = 1
		else:
			pantallaGameOver -= 1
		botonPresionado = 1

		cambiarGameOver.play()

	#SI SE PRESIONA START
	if(botonEstado == 1 and botonPresionado == 0):
		#EN INICIAR, IR A LA PANTALLA DE JUEGO (1)
		if(pantallaGameOver == 0):
			pantalla = 1
			irReiniciar.play()
			numeroVidas = 3
			numeroPuntaje = 0
			colisionMeteorito = []
			colisionBala = []
			velocidadMeteoritos = []
			velocidadEstrellas = []
			coordenadasMeteoritosInicial = []
			coordenadasEstrellasInicial = []
			tipoMeteorito = []
			#Ejecutar procedimientos previos
			coordenadasEstrellas()	#Obtener las coordenadas iniciales de las estrellas
			coordenadasMeteoritos()	#Obtener las coordenadas iniciales de los meteoritos
			posXNave = 360									
			posYNave = 400
		#EN SALIR, SALIR DEL JUEGO
		if(pantallaGameOver == 1):
			pygame.quit()
			sys.exit()

		botonPresionado = 1

################################################################################
#JUEGO
################################################################################
pygame.init()	#Iniciar librería de Pygame
ventana = pygame.display.set_mode(tamanoVentana)	#Establecer una ventana
clock = pygame.time.Clock()	#Reloj para definir FPS



#Ejecutar procedimientos previos
coordenadasEstrellas()	#Obtener las coordenadas iniciales de las estrellas
coordenadasMeteoritos()	#Obtener las coordenadas iniciales de los meteoritos
while True:
	#PARA PODER CERRAR CON EL BOTÓN X DE LA VENTANA
	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()

	################################################################################
	#LÓGICA
	################################################################################
	#OBTENER DEL PIC16F877 (COM4) QUE BOTÓN SE HA PRESIONADO Y VELOCIDAD DEL JOYSTICK
	botonEstado = obtenerEventosMando()

	################################################################################
	#PANTALLAS
	################################################################################
	if(numeroVidas == 0):
		pantalla = 3
		if(pantalla == 3):
			gameOver()
	else:
		if(pantalla == 0):
			menuPrincipal()
		if(pantalla == 1):
			juego()
		if(pantalla == 2):
			opciones()

	#ACTUALIZAR VENTANAS
	pygame.display.update()	
	#DEFINIR FPS		
	clock.tick(60)			