# Sistema Experto para el Diagnóstico de Fallas Electrónicas

Este proyecto es un sistema experto que ayuda a diagnosticar fallas en dispositivos electrónicos con base en los síntomas observados. Fue desarrollado en Python y cuenta con una interfaz gráfica hecha en Tkinter, donde el usuario puede seleccionar los síntomas y obtener un diagnóstico posible según las reglas programadas.

## ¿Cómo funciona?

El programa muestra una lista de síntomas. El usuario selecciona los que ha detectado en el dispositivo y luego el sistema revisa si alguna de las reglas se cumple. Si es así, muestra uno o varios diagnósticos posibles.

Las reglas están basadas en combinaciones de síntomas reales, como por ejemplo: si el dispositivo no enciende y no tiene energía de entrada, se sugiere revisar el cable o la fuente externa.

## Archivos

- `sistema_experto_gui.py`: Código principal del sistema con la interfaz gráfica.
- `Sistema_Experto_Diagnostico_Evidencia.docx`: Documento con la evidencia del proyecto, reglas y tabla de diagnóstico.

## Requisitos

- Python 3.x
- No se necesitan librerías externas. Tkinter ya viene incluido con Python.

## Instrucciones para ejecutar

1. Asegúrate de tener Python instalado.
2. Ejecuta el archivo con el siguiente comando:

```
python sistema_experto_gui.py
```

3. Se abrirá una ventana donde puedes seleccionar los síntomas.
4. Presiona el botón "Diagnosticar" para ver los resultados.

---

### Proyecto realizado por:

- Abraham Gael Herrera Quiñones  
- Eduardo García Noriz

**Carrera:** Ingeniería en Sistemas Computacionales  
**Escuela:** Instituto Tecnológico de Ensenada  
**Materia:** Inteligencia Artificial  
**Profesor:** Zuriel Dathan Mora Félix  
**Horario:** 09:00 – 10:00 hrs
