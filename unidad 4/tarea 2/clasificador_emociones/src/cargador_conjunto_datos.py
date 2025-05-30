import os
import cv2
import numpy as np
from tqdm import tqdm
import tensorflow as tf

class CargadorDatos:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base
        self.emociones = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        
    def cargar_conjunto_datos(self):
        """
        Carga train/test directamente desde las carpetas del FER2013.
        """
        X_train, y_train = self._cargar_imagenes(os.path.join(self.ruta_base, 'train'))
        X_test, y_test = self._cargar_imagenes(os.path.join(self.ruta_base, 'test'))
        
        # Convertir a arrays numpy y one-hot encoding
        X_train = np.array(X_train).reshape(-1, 48, 48, 1)
        y_train = tf.keras.utils.to_categorical(y_train, num_classes=7)
        X_test = np.array(X_test).reshape(-1, 48, 48, 1)
        y_test = tf.keras.utils.to_categorical(y_test, num_classes=7)
        
        print("\nFormas de los conjuntos:")
        print(f"Train: {X_train.shape}, {y_train.shape}")
        print(f"Test: {X_test.shape}, {y_test.shape}")
        
        return X_train, y_train, X_test, y_test
    
    def _cargar_imagenes(self, ruta_conjunto):
        """
        Carga imágenes desde un directorio (train o test).
        """
        datos, etiquetas = [], []
        for idx, emocion in enumerate(self.emociones):
            ruta_emocion = os.path.join(ruta_conjunto, emocion)
            print(f"\nCargando {ruta_emocion}...")
            
            for img_name in tqdm(os.listdir(ruta_emocion)):
                try:
                    img_path = os.path.join(ruta_emocion, img_name)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        img = img.astype(np.float32) / 255.0  # Normalizar
                        datos.append(img)
                        etiquetas.append(idx)
                except Exception as e:
                    print(f"Error al cargar {img_path}: {str(e)}")
        
        return datos, etiquetas

if __name__ == "__main__":
    cargador = CargadorDatos('clasificador_emociones/datos')
    X_train, y_train, X_test, y_test = cargador.cargar_conjunto_datos()