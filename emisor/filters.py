import cv2
import numpy as np
import os

# Función principal para aplicar un filtro a un frame de imagen
def apply_filter(frame, filter_name):
    # Aplica el filtro seleccionado al frame recibido
    if filter_name == "Escala de grises":
        # Convierte la imagen a escala de grises
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_name == "Negativo":
        # Invierte los colores de la imagen
        return cv2.bitwise_not(frame)
    elif filter_name == "Espejo vertical":
        # Invierte la imagen horizontalmente (efecto espejo)
        return cv2.flip(frame, 1)
    elif filter_name == "Espejo horizontal":
        # Invierte la imagen verticalmente
        return cv2.flip(frame, 0)
    elif filter_name == "Desenfoque":
        # Aplica un desenfoque tipo gaussiano personalizado
        kernel = np.array([
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]) / 256.0
        return cv2.filter2D(frame, -1, kernel)
    elif filter_name == "Nitidez":
        # Aplica un filtro de nitidez personalizado
        kernel = np.array([
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, -476, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]) / -256.0
        return cv2.filter2D(frame, -1, kernel)
    elif filter_name == "Bordes":
        # Detecta bordes usando el operador Sobel
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        abs_gx = cv2.convertScaleAbs(gx)
        abs_gy = cv2.convertScaleAbs(gy)
        return cv2.addWeighted(abs_gx, 0.5, abs_gy, 0.5, 0)
    elif filter_name == "Detección de rostros":
        # Dibuja un rectángulo azul alrededor de cada rostro detectado
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame
    elif filter_name == "Bigote":
        # Aplica el filtro de bigote
        return apply_accessory(frame, 'mustache')
    elif filter_name == "Barba":
        # Aplica el filtro de barba
        return apply_accessory(frame, 'beard')
    elif filter_name == "Lentes":
        # Aplica el filtro de lentes
        return apply_accessory(frame, 'glasses')
    elif filter_name == "Sombrero":
        # Aplica el filtro de sombrero
        return apply_accessory(frame, 'hat')
    elif filter_name == "Maquillaje":
        # Aplica el filtro de maquillaje
        return apply_accessory(frame, 'makeup')
    else:
        # Si no se reconoce el filtro, retorna la imagen original
        return frame

# Función para aplicar un accesorio (overlay) sobre la cara detectada
def apply_accessory(frame, accessory_type):
    # Convierte la imagen a escala de grises para la detección de rostros
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Carga el clasificador Haar para detección de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Detecta los rostros en la imagen
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Ruta a la carpeta de imágenes de accesorios
    img_dir = os.path.join(os.path.dirname(__file__), 'img')

    for (x, y, w, h) in faces:
        if accessory_type == 'mustache':
            # Aplica imagen de bigote sobre la cara
            bigote_path = os.path.join(img_dir, 'bigote.png')
            if not os.path.exists(bigote_path):
                continue
            bigote_img = cv2.imread(bigote_path, cv2.IMREAD_UNCHANGED)
            if bigote_img is None or bigote_img.shape[2] != 4:
                continue
            # Calcula tamaño y posición del bigote (debajo de la nariz)
            mustache_w = int(w * 0.7)
            mustache_h = h // 6
            mustache_x = x + (w - mustache_w) // 2
            mustache_y = y + 2 * h // 3
            bigote_resized = cv2.resize(bigote_img, (mustache_w, mustache_h), interpolation=cv2.INTER_AREA)
            # Superpone el bigote en la imagen
            overlay_image_alpha(frame, bigote_resized, mustache_x, mustache_y)
        elif accessory_type == 'beard':
            # Aplica imagen de barba sobre la cara
            barba_path = os.path.join(img_dir, 'barba.png')
            if not os.path.exists(barba_path):
                continue
            barba_img = cv2.imread(barba_path, cv2.IMREAD_UNCHANGED)
            if barba_img is None or barba_img.shape[2] != 4:
                continue
            # Calcula tamaño y posición de la barba (debajo de la boca)
            beard_w = int(w * 0.6)
            beard_h = h // 4
            beard_x = x + (w - beard_w) // 2
            beard_y = y + int(2.75 * h // 3)
            barba_resized = cv2.resize(barba_img, (beard_w, beard_h), interpolation=cv2.INTER_AREA)
            # Superpone la barba en la imagen
            overlay_image_alpha(frame, barba_resized, beard_x, beard_y)
        elif accessory_type == 'hat':
            # Aplica imagen de gorra sobre la cabeza
            gorra_path = os.path.join(img_dir, 'gorra.png')
            if not os.path.exists(gorra_path):
                continue
            gorra_img = cv2.imread(gorra_path, cv2.IMREAD_UNCHANGED)
            if gorra_img is None or gorra_img.shape[2] != 4:
                continue
            # Calcula tamaño y posición de la gorra (encima de la frente)
            hat_w = int(w)
            hat_h = int(h * 0.7)
            gorra_resized = cv2.resize(gorra_img, (hat_w, hat_h), interpolation=cv2.INTER_AREA)
            hat_x = x + (w - hat_w) // 2
            hat_y = max(0, y - hat_h + h // 8)
            # Superpone la gorra en la imagen
            overlay_image_alpha(frame, gorra_resized, hat_x, hat_y)
        elif accessory_type == 'glasses':
            # Aplica imagen de lentes sobre los ojos
            lentes_path = os.path.join(img_dir, 'lentes.png')
            if not os.path.exists(lentes_path):
                continue
            lentes_img = cv2.imread(lentes_path, cv2.IMREAD_UNCHANGED)
            if lentes_img is None or lentes_img.shape[2] != 4:
                continue
            # Calcula tamaño y posición de los lentes (sobre los ojos)
            glasses_w = int(w*0.9)
            glasses_h = int(h*0.4)
            lentes_resized = cv2.resize(lentes_img, (glasses_w, glasses_h), interpolation=cv2.INTER_AREA)
            glasses_x = x + (w - glasses_w) // 2
            glasses_y = y + int(h * 0.3)
            # Superpone los lentes en la imagen
            overlay_image_alpha(frame, lentes_resized, glasses_x, glasses_y)
        elif accessory_type == 'makeup':
            # Aplica maquillaje virtual estilo filtro Instagram
            def apply_region_blend(frame, overlay, mask, alpha):
                # Mezcla suavemente la región del overlay con la imagen base usando la máscara y el alpha
                mask_bool = np.all(mask == (1, 1, 1), axis=2)
                for c in range(3):
                    frame[..., c] = np.where(
                        mask_bool,
                        (overlay[..., c] * alpha + frame[..., c] * (1 - alpha)).astype(np.uint8),
                        frame[..., c]
                    )
            # Colorete en las mejillas (círculos difuminados)
            cheek_radius = w // 11
            cheek_color = (200, 80, 255)
            alpha_cheek = 0.32
            overlay = frame.copy()
            left_cheek_center = (x + w // 3, y + int(h * 0.62))
            right_cheek_center = (x + 2 * w // 3, y + int(h * 0.62))
            cv2.circle(overlay, left_cheek_center, cheek_radius, cheek_color, -1, lineType=cv2.LINE_AA)
            cv2.circle(overlay, right_cheek_center, cheek_radius, cheek_color, -1, lineType=cv2.LINE_AA)
            overlay_blur = cv2.GaussianBlur(overlay, (0, 0), sigmaX=8, sigmaY=8)
            mask = np.zeros_like(frame)
            cv2.circle(mask, left_cheek_center, cheek_radius, (1,1,1), -1, lineType=cv2.LINE_AA)
            cv2.circle(mask, right_cheek_center, cheek_radius, (1,1,1), -1, lineType=cv2.LINE_AA)
            apply_region_blend(frame, overlay_blur, mask, alpha_cheek)
            # Labios pintados (elipse difuminada)
            lip_color = (180, 40, 140)
            alpha_lip = 0.45
            overlay = frame.copy()
            lip_top = (x + w // 2, y + int(h * 0.83))
            lip_w = w // 6
            lip_h = h // 16
            cv2.ellipse(overlay, lip_top, (lip_w, lip_h), 0, 0, 360, lip_color, -1, lineType=cv2.LINE_AA)
            overlay_blur = cv2.GaussianBlur(overlay, (0, 0), sigmaX=4, sigmaY=4)
            mask = np.zeros_like(frame)
            cv2.ellipse(mask, lip_top, (lip_w, lip_h), 0, 0, 360, (1,1,1), -1, lineType=cv2.LINE_AA)
            apply_region_blend(frame, overlay_blur, mask, alpha_lip)
            # Sombra de ojos (elipses difuminadas sobre los ojos)
            eye_color = (220, 120, 255)
            alpha_eye = 0.22
            overlay = frame.copy()
            left_eye_center = (x + w // 3, y + int(h * 0.39))
            right_eye_center = (x + 2 * w // 3, y + int(h * 0.39))
            eye_w = w // 10
            eye_h = h // 18
            cv2.ellipse(overlay, left_eye_center, (eye_w, eye_h), 0, 0, 360, eye_color, -1, lineType=cv2.LINE_AA)
            cv2.ellipse(overlay, right_eye_center, (eye_w, eye_h), 0, 0, 360, eye_color, -1, lineType=cv2.LINE_AA)
            overlay_blur = cv2.GaussianBlur(overlay, (0, 0), sigmaX=5, sigmaY=5)
            mask = np.zeros_like(frame)
            cv2.ellipse(mask, left_eye_center, (eye_w, eye_h), 0, 0, 360, (1,1,1), -1, lineType=cv2.LINE_AA)
            cv2.ellipse(mask, right_eye_center, (eye_w, eye_h), 0, 0, 360, (1,1,1), -1, lineType=cv2.LINE_AA)
            apply_region_blend(frame, overlay_blur, mask, alpha_eye)
            # Iluminador en el puente de la nariz (línea difuminada)
            highlight_color = (255, 255, 255)
            alpha_highlight = 0.18
            overlay = frame.copy()
            nose_x = x + w // 2
            nose_y1 = y + int(h * 0.48)
            nose_y2 = y + int(h * 0.73)
            cv2.line(overlay, (nose_x, nose_y1), (nose_x, nose_y2), highlight_color, w // 32, lineType=cv2.LINE_AA)
            overlay_blur = cv2.GaussianBlur(overlay, (0, 0), sigmaX=4, sigmaY=4)
            mask = np.zeros_like(frame)
            cv2.line(mask, (nose_x, nose_y1), (nose_x, nose_y2), (1, 1, 1), w // 32, lineType=cv2.LINE_AA)
            apply_region_blend(frame, overlay_blur, mask, alpha_highlight)
            # Suavizado de piel en la región de la cara (clonado sin costuras)
            skin = frame[y:y+h, x:x+w].copy()
            skin_blur = cv2.bilateralFilter(skin, d=0, sigmaColor=60, sigmaSpace=18)
            mask_skin = np.zeros((h, w), dtype=np.uint8)
            cv2.ellipse(mask_skin, (w//2, h//2), (w//2-2, h//2-6), 0, 0, 360, 255, -1)
            skin_result = cv2.seamlessClone(skin_blur, skin, mask_skin, (w//2, h//2), cv2.NORMAL_CLONE)
            frame[y:y+h, x:x+w] = cv2.addWeighted(frame[y:y+h, x:x+w], 0.6, skin_result, 0.4, 0)
    return frame

# Superpone una imagen con canal alfa sobre otra imagen base en la posición (x, y)
def overlay_image_alpha(img, img_overlay, x, y):
    overlay_h, overlay_w = img_overlay.shape[:2]
    # Verifica que la superposición no se salga de los límites de la imagen base
    if y + overlay_h > img.shape[0] or x + overlay_w > img.shape[1] or x < 0 or y < 0:
        return
    # Obtiene el canal alfa de la imagen overlay y calcula el fondo
    alpha_overlay = img_overlay[:, :, 3] / 255.0
    alpha_background = 1.0 - alpha_overlay
    # Mezcla cada canal de color usando el canal alfa
    for c in range(0, 3):
        img[y:y+overlay_h, x:x+overlay_w, c] = (
            alpha_overlay * img_overlay[:, :, c] +
            alpha_background * img[y:y+overlay_h, x:x+overlay_w, c]
        )
