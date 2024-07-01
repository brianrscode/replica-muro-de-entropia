"""
Este código trata de simular un poco el funcionamiento del muro de entropía.
A través de este muro, se puede generar una llave de cifrado para cada cuadro de video.

En este caso, es tiene un video del cual cada cierto tiempo toma el frame que esté
en ese momento y genera una llave de cifrado a partir de los pixeles de ese frame.
"""

import cv2
import numpy as np
import hashlib


def generar_llave_de_cifrado_desde_frame(frame) -> str:
    """Función para generar la llave de cifrado desde un cuadro de video"""
    # imagen_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir imagen a escala de grises
    pixeles = np.array(frame).flatten()  # Crear una nueva matriz con los pixeles de la imagen
    clave_str = "".join(map(str, pixeles))  # Unir todos los pixeles en una cadena de texto
    llave = hashlib.sha256(clave_str.encode()).hexdigest()  # Generar la llave de cifrado

    return llave


def procesar_video(ruta_video: str, intervalo_segundos: int = 5):
    """Función principal para procesar el video"""
    try:
        cap = cv2.VideoCapture(ruta_video)
        if not cap.isOpened():
            raise ValueError("No se puede abrir el video.")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        intervalo = intervalo_segundos * fps
        contador_cuadros = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("frame", frame)  # Mostrar el cuadro de video

            if contador_cuadros % intervalo == 0:  # Generar la llave de cifrado cada 5 segundos
                llave = generar_llave_de_cifrado_desde_frame(frame)
                print(llave)

            if cv2.waitKey(24) & 0xFF == ord('q'):
                break

            contador_cuadros += 1

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error al procesar el video: {e}")


# Ejecución del procesamiento de video
procesar_video("./videos/lamparaLava.mp4")
