# Preprocesamiento de Imágenes

Este script aplica aumentos de datos a imágenes en escala de grises. Por cada imagen original, genera 9 versiones combinando:

- 3 rotaciones: -10°, 0°, 10°
- 3 ajustes de brillo: 0.8, 1.0, 1.2

Cada imagen se redimensiona a 48x48 píxeles y se guarda en una carpeta de salida con nombres que indican las transformaciones aplicadas.

Pusimos en el input dir la ruta para sacar las imagenes originales
y el output dir para guardar las imagenes procesadas