# README - Proyecto Final de Inteligencia Artificial: Reconocimiento de Emociones Faciales

## Descripción del Proyecto
Este proyecto tiene como objetivo desarrollar un sistema de reconocimiento de emociones humanas a partir de imágenes faciales utilizando una red neuronal convolucional (CNN). El sistema puede funcionar en tiempo real con la cámara web o con videos, y está entrenado para identificar siete emociones principales: enojo, disgusto, miedo, felicidad, neutral, tristeza y sorpresa.

## Integrantes del Equipo
- Abraham Gael Herrera Quiñones
- Juan Eduardo Garcia Noriz

## Carrera
Ingeniería en Sistemas Computacionales

## Materia
Inteligencia Artificial

## Profesor
Zuriel Dathan Mora Felix

## Horario
Grupo: 09:00-10:00

## Estructura del Proyecto
El sistema se compone de las siguientes partes principales:

1. **Cargador de Datos**:
   - Lee las imágenes de entrenamiento y prueba.
   - Normaliza las imágenes (escala de grises y ajuste de brillo).
   - Las imágenes están etiquetadas con las siete emociones.

2. **Arquitectura de la Red Neuronal**:
   - Utiliza una CNN con tres bloques principales para extraer características.
   - Incluye capas para evitar sobreajuste (`BatchNormalization` y `Dropout`).
   - La salida es un porcentaje de probabilidad para cada emoción.

3. **Entrenamiento del Modelo**:
   - Se detiene automáticamente si el modelo deja de mejorar.
   - Guarda el mejor modelo obtenido durante el proceso.
   - Usa técnicas de aumento de datos (rotación y volteo de imágenes) para mejorar la precisión.

4. **Pruebas en Tiempo Real**:
   - Detecta rostros en videos o mediante la cámara web.

## Resultados y Validación
- El sistema funciona bien con expresiones claras (sonrisa, cara neutra, sorpresa).
- Puede tener dificultades con expresiones sutiles o con mala iluminación.

## Demostración en Video
Puedes ver una demostración del sistema en funcionamiento en el siguiente enlace:  
🔗 [https://youtu.be/5nQ1ln3Lcag](https://youtu.be/5nQ1ln3Lcag)

## Archivos Importantes
- `cargador_conjuntodatos.py`: Maneja la carga y preprocesamiento de los datos.
- `pipeline_entrenamiento.py`: Controla el proceso de entrenamiento del modelo.

## Conclusión
Este proyecto representa un primer paso exitoso hacia un sistema más robusto de reconocimiento de emociones. Aunque tiene limitaciones, demuestra el potencial de la inteligencia artificial en el análisis del comportamiento humano. Con más ajustes y datos, podría convertirse en una herramienta valiosa para diversas aplicaciones.