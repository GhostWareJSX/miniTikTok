import cv2
import numpy as np

def apply_filter(frame, filter_name):
    if filter_name == "Escala de grises":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_name == "Negativo":
        return cv2.bitwise_not(frame)
    elif filter_name == "Espejo vertical":
        return cv2.flip(frame, 1)
    elif filter_name == "Espejo horizontal":
        return cv2.flip(frame, 0)
    elif filter_name == "Desenfoque":
        kernel = np.array([
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]) / 256.0
        return cv2.filter2D(frame, -1, kernel)
    elif filter_name == "Nitidez":
        kernel = np.array([
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, -476, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]) / -256.0
        return cv2.filter2D(frame, -1, kernel)
    elif filter_name == "Bordes":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        abs_gx = cv2.convertScaleAbs(gx)
        abs_gy = cv2.convertScaleAbs(gy)
        return cv2.addWeighted(abs_gx, 0.5, abs_gy, 0.5, 0)
    elif filter_name == "Detección de rostros":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame
    elif filter_name == "Bigote":
        return apply_accessory(frame, 'mustache')
    elif filter_name == "Barba":
        return apply_accessory(frame, 'beard')
    elif filter_name == "Lentes":
        return apply_accessory(frame, 'glasses')
    elif filter_name == "Sombrero":
        return apply_accessory(frame, 'hat')
    elif filter_name == "Maquillaje":
        return apply_accessory(frame, 'makeup')
    else:
        return frame

def apply_accessory(frame, accessory_type):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        if accessory_type == 'mustache':
            # Coordenadas para bigote
            mustache_w = w // 2
            mustache_h = h // 6
            mustache_x = x + w // 4
            mustache_y = y + 2 * h // 3
            cv2.rectangle(frame, (mustache_x, mustache_y), 
                         (mustache_x + mustache_w, mustache_y + mustache_h), 
                         (0, 0, 0), -1)
        elif accessory_type == 'beard':
            # Coordenadas para barba
            beard_w = w
            beard_h = h // 3
            beard_x = x
            beard_y = y + 2 * h // 3
            cv2.rectangle(frame, (beard_x, beard_y), 
                         (beard_x + beard_w, beard_y + beard_h), 
                         (100, 50, 0), -1)
        # Implementar otros accesorios de manera similar
    
    return frame