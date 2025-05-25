
import cv2
import os
import numpy as np

# Ruta de entrada y salida
input_dir = r'C:\Users\gaeli\Downloads\dataset_emociones\test\angry'
output_dir = r'C:\Users\gaeli\Downloads\dataset_emociones\test\preprocesadas'
os.makedirs(output_dir, exist_ok=True)

# Transformaciones
angles = [-10, 0, 10]
brillo_factors = [0.8, 1.0, 1.2]
target_size = (48, 48)

def ajustar_brillo(img, factor):
    return np.clip(img * factor, 0, 255).astype(np.uint8)

def rotar_img(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    return cv2.warpAffine(img, M, (w, h))

for filename in os.listdir(input_dir):
    img_path = os.path.join(input_dir, filename)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    img = cv2.resize(img, target_size)

    for angle in angles:
        rotated = rotar_img(img, angle)
        for factor in brillo_factors:
            bright = ajustar_brillo(rotated, factor)
            name = f"{os.path.splitext(filename)[0]}_rot{angle}_b{factor:.1f}.png"
            cv2.imwrite(os.path.join(output_dir, name), bright)
