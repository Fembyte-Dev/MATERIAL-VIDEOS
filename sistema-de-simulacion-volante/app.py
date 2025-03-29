import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
from pygame.locals import *

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar Pygame para la visualización del volante
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulador de Volante")

# Variables para el volante y velocidad
volante_angulo = 0
velocidad = 0
max_velocidad = 100
ultimo_tiempo_parpadeo = 0
boca_abierta = False

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Función para dibujar el volante
def dibujar_volante(angulo):
    screen.fill(NEGRO)
    
    # Dibujar el volante (círculo con rotación)
    centro = (width // 2, height // 2)
    radio = 150
    
    pygame.draw.circle(screen, BLANCO, centro, radio, 5)
    pygame.draw.circle(screen, BLANCO, centro, 10)
    
    # Dibujar las líneas del volante
    for i in range(0, 360, 45):
        angulo_rad = np.radians(i + angulo)
        x1 = centro[0] + (radio - 20) * np.cos(angulo_rad)
        y1 = centro[1] + (radio - 20) * np.sin(angulo_rad)
        x2 = centro[0] + radio * np.cos(angulo_rad)
        y2 = centro[1] + radio * np.sin(angulo_rad)
        pygame.draw.line(screen, BLANCO, (x1, y1), (x2, y2), 5)
    
    # Dibujar el velocímetro
    fuente = pygame.font.SysFont('Arial', 30)
    texto_velocidad = fuente.render(f"Velocidad: {velocidad} km/h", True, BLANCO)
    screen.blit(texto_velocidad, (50, 50))
    
    # Dibujar instrucciones
    fuente_peq = pygame.font.SysFont('Arial', 16)
    instrucciones = [
        "Instrucciones:",
        "- Mueve las manos como si giraras un volante",
        "- Parpadea para aumentar velocidad (+10 km/h)",
        "- Abre la boca para reducir velocidad (-10 km/h)"
    ]
    
    for i, texto in enumerate(instrucciones):
        texto_render = fuente_peq.render(texto, True, BLANCO)
        screen.blit(texto_render, (50, height - 100 + i * 20))

# Función para detectar parpadeo
def detectar_parpadeo(landmarks_rostro):
    # Puntos para los ojos (índices según Face Mesh)
    # Ojo izquierdo
    punto_sup_izq = landmarks_rostro[159]
    punto_inf_izq = landmarks_rostro[145]
    # Ojo derecho
    punto_sup_der = landmarks_rostro[386]
    punto_inf_der = landmarks_rostro[374]
    
    # Calcular distancia vertical para cada ojo
    dist_izq = np.sqrt((punto_sup_izq.x - punto_inf_izq.x)**2 + (punto_sup_izq.y - punto_inf_izq.y)**2)
    dist_der = np.sqrt((punto_sup_der.x - punto_inf_der.x)**2 + (punto_sup_der.y - punto_inf_der.y)**2)
    
    # Umbral para determinar parpadeo
    return dist_izq < 0.02 and dist_der < 0.02

# Función para detectar boca abierta
def detectar_boca_abierta(landmarks_rostro):
    # Puntos para la boca (índices según Face Mesh)
    punto_sup = landmarks_rostro[13]
    punto_inf = landmarks_rostro[14]
    
    # Calcular distancia vertical
    dist = np.sqrt((punto_sup.x - punto_inf.x)**2 + (punto_sup.y - punto_inf.y)**2)
    
    # Umbral para determinar boca abierta
    return dist > 0.1

# Capturar video de la cámara
cap = cv2.VideoCapture(0)

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Voltear el frame horizontalmente para un efecto espejo
    frame = cv2.flip(frame, 1)
    
    # Convertir el frame a RGB para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar las manos
    resultados_manos = hands.process(frame_rgb)
    
    # Procesar el rostro
    resultados_rostro = face_mesh.process(frame_rgb)
    
    # Detectar gestos faciales
    if resultados_rostro.multi_face_landmarks:
        for landmarks_rostro in resultados_rostro.multi_face_landmarks:
            # Detectar parpadeo
            if detectar_parpadeo(landmarks_rostro.landmark):
                tiempo_actual = time.time()
                if tiempo_actual - ultimo_tiempo_parpadeo > 0.5:  # Evitar detección múltiple
                    velocidad = min(velocidad + 10, max_velocidad)
                    ultimo_tiempo_parpadeo = tiempo_actual
            
            # Detectar boca abierta
            nueva_boca_abierta = detectar_boca_abierta(landmarks_rostro.landmark)
            if nueva_boca_abierta and not boca_abierta:
                velocidad = max(velocidad - 10, 0)
            boca_abierta = nueva_boca_abierta
    
    # Detectar movimiento del volante
    if resultados_manos.multi_hand_landmarks:
        for hand_landmarks in resultados_manos.multi_hand_landmarks:
            # Obtener coordenadas de la muñeca y el dedo medio
            muneca = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            dedo_medio = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            
            # Calcular ángulo basado en la posición relativa
            dx = dedo_medio.x - muneca.x
            volante_angulo = dx * 90  # Escalar a un rango de -90 a 90 grados
            
            # Dibujar landmarks de la mano en el frame
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Mostrar el frame de la cámara
    frame = cv2.resize(frame, (400, 300))
    frame_pyg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pyg = np.rot90(frame_pyg)
    frame_pyg = pygame.surfarray.make_surface(frame_pyg)
    
    # Dibujar en Pygame
    dibujar_volante(volante_angulo)
    screen.blit(frame_pyg, (width - 410, height - 310))
    
    pygame.display.flip()
    
    # Manejar eventos de Pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
hands.close()
face_mesh.close()
pygame.quit()