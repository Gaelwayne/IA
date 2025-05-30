import cv2
import numpy as np
import tensorflow as tf
from threading import Thread
import queue

class ClasificadorEmocionesTiempoReal:
    def __init__(self, ruta_modelo='clasificador_emociones/modelos/mejor_modelo_emociones.keras'):
        """
        Inicializa el clasificador de emociones en tiempo real
        """
        self.modelo = tf.keras.models.load_model(ruta_modelo)
        self.detector_rostros = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.emociones = ['Enojo', 'Disgusto', 'Miedo', 'Felicidad', 'Neutral', 'Tristeza', 'Sorpresa']
        self.cola_frames = queue.Queue(maxsize=10)
        self.cola_resultados = queue.Queue()
        self.activo = False

    def iniciar_deteccion(self):
        """
        Inicia la detección en tiempo real usando hilos
        """
        print("Iniciando sistema de detección de emociones...")
        self.activo = True
        
        # Iniciar hilos
        Thread(target=self._capturar_video, daemon=True).start()
        Thread(target=self._procesar_frames, daemon=True).start()
        Thread(target=self._mostrar_resultados, daemon=True).start()
        
        print("Sistema iniciado. Presiona 'q' para salir.")

    def _capturar_video(self):
        """
        Captura frames de la cámara
        """
        camara = cv2.VideoCapture(0)
        if not camara.isOpened():
            print("Error: No se pudo acceder a la cámara")
            self.activo = False
            return

        while self.activo:
            ret, frame = camara.read()
            if ret:
                if not self.cola_frames.full():
                    self.cola_frames.put(frame)
            else:
                print("Error al capturar frame")
                break

        camara.release()

    def _procesar_frames(self):
        """
        Procesa los frames para detectar rostros y emociones
        """
        while self.activo:
            if not self.cola_frames.empty():
                frame = self.cola_frames.get()
                frame_procesado = frame.copy()
                
                # Detectar rostros
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rostros = self.detector_rostros.detectMultiScale(
                    gris,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                # Procesar cada rostro
                for (x, y, w, h) in rostros:
                    try:
                        # Extraer y preprocesar rostro
                        rostro = gris[y:y+h, x:x+w]
                        rostro_procesado = cv2.resize(rostro, (48, 48))
                        rostro_procesado = rostro_procesado.astype(np.float32) / 255.0
                        rostro_procesado = np.expand_dims(rostro_procesado, axis=(0, -1))
                        
                        # Predicción
                        predicciones = self.modelo.predict(rostro_procesado, verbose=0)[0]
                        emocion_predicha = np.argmax(predicciones)
                        confianza = predicciones[emocion_predicha]
                        
                        # Dibujar resultados
                        color = (0, 255, 0)
                        cv2.rectangle(frame_procesado, (x, y), (x+w, y+h), color, 2)
                        
                        # Mostrar emoción y confianza
                        texto = f"{self.emociones[emocion_predicha]} ({confianza*100:.1f}%)"
                        cv2.putText(frame_procesado, texto, (x, y-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        
                        # Mostrar gráfico de barras de emociones
                        self._dibujar_grafico_emociones(frame_procesado, predicciones, x+w+10, y, h)
                        
                    except Exception as e:
                        print(f"Error al procesar rostro: {str(e)}")
                
                self.cola_resultados.put(frame_procesado)

    def _dibujar_grafico_emociones(self, frame, predicciones, x, y, altura):
        """
        Dibuja un gráfico de barras con las probabilidades de cada emoción
        """
        ancho_barra = 20
        espacio = 5
        
        for i, (emocion, prob) in enumerate(zip(self.emociones, predicciones)):
            # Color de la barra
            color = (0, int(255 * prob), 0)
            
            # Calcular posición y tamaño de la barra
            x_barra = x + i * (ancho_barra + espacio)
            altura_barra = int(altura * prob)
            y_barra = y + altura - altura_barra
            
            # Dibujar barra
            cv2.rectangle(frame, (x_barra, y_barra), 
                         (x_barra + ancho_barra, y + altura), 
                         color, -1)
            
            # Etiqueta de emoción
            cv2.putText(frame, emocion[:3], (x_barra, y + altura + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def _mostrar_resultados(self):
        """
        Muestra los frames procesados
        """
        while self.activo:
            if not self.cola_resultados.empty():
                frame = self.cola_resultados.get()
                cv2.imshow('Detector de Emociones en Tiempo Real', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.activo = False
                    break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        clasificador = ClasificadorEmocionesTiempoReal()  # ¡Mayúscula en "Clasificador"!
        clasificador.iniciar_deteccion()
    except Exception as e:
        print(f"Error: {str(e)}")  # Sin guion bajo al final