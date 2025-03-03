# Resolución del Puzzle 8 con A* usando Árboles y Matrices en Python

Este proyecto implementa una solución al clásico problema del Puzzle 8 utilizando el algoritmo de búsqueda A*, representado con árboles y matrices en Python.

## Descripción

El Puzzle 8 consiste en un tablero de 3x3 con 8 fichas numeradas y un espacio vacío. El objetivo es mover las fichas hasta alcanzar una configuración objetivo específica. Este programa utiliza el algoritmo A* para encontrar la secuencia de movimientos más corta que resuelve el puzzle.

## Funcionamiento del Código

* **Representación del Nodo:**
    * La clase `Nodo` representa cada estado del puzzle, almacenando el estado actual, el nodo padre, el costo del camino y la heurística.
* **Funciones Auxiliares:**
    * `encontrar_vacio(estado)`: Encuentra la posición del espacio vacío en la matriz.
    * `movimientos_posibles(estado)`: Genera los posibles estados resultantes de mover el espacio vacío.
    * `heuristica(estado)`: Calcula la distancia de Manhattan como heurística.
    * `es_objetivo(estado)`: Verifica si el estado actual es el estado objetivo.
    * `imprimir_estado(estado)`: Imprime el estado del puzzle de forma legible.
* **Algoritmo A*:**
    * Utiliza una cola de prioridad (`heapq`) para explorar los nodos más prometedores.
    * Mantiene un conjunto de estados visitados para evitar ciclos.
    * Reconstruye el camino óptimo una vez que se encuentra el estado objetivo.

## Ejemplo de Uso

El código incluye un ejemplo de uso con un estado inicial predefinido. Puedes modificar el estado inicial en la variable `estado_inicial` para probar diferentes configuraciones del puzzle.

## Dependencias

* `heapq`: Módulo de Python para la implementación de colas de prioridad.

## Notas

* La heurística utilizada es la distancia de Manhattan, que proporciona una estimación admisible del costo restante.
* El algoritmo A* garantiza encontrar la solución óptima (la secuencia de movimientos más corta) si existe una solución.

## Autor

* \arcia Noriz Juan Eduardo
* Herrera Quiñones Abraham Gael

