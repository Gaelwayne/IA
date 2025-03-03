8-Puzzle Game

Este proyecto es del clásico juego de rompecabezas 8-puzzle

Integrantes

Herrera Quiñones Abraham Gael

García Noriz Juan Eduardo

Materia

Inteligencia Artificial

Horario: 9:00 a 10:00 AM

Escuela

Instituto Tecnológico de Culiacán

Descripción del Proyecto

El 8-puzzle es un juego de rompecabezas deslizante que consiste en una cuadrícula de 3x3 con 8 fichas numeradas y un espacio vacío. El objetivo es reorganizar las fichas desde una configuración inicial hasta una configuración objetivo deslizando las fichas adyacentes al espacio vacío.

Este proyecto incluye:

Interfaz gráfica: Un juego interactivo donde puedes mover los tiles manualmente.

Movimientos R1, R2, R3, ****R4: Los movimientos se muestran en la interfaz gráfica, saltando de línea cada 10 movimientos.

Explicación del Código

Métodos y su Funcionalidad

__init__(self, ventana): Constructor de la clase. Inicializa la ventana del juego, define el estado inicial y el estado objetivo, y crea la interfaz gráfica.

crear_interfaz(self): Crea la interfaz gráfica, generando los botones que representan las piezas del puzzle, el botón de reinicio y la etiqueta de movimientos.

mover_pieza(self, indice): Mueve una pieza si el movimiento es válido. Intercambia la posición de la pieza con el espacio vacío y verifica si se ha completado el juego.

movimiento_es_valido(self, indice, indice_vacio): Verifica si la pieza seleccionada está adyacente al espacio vacío y si el movimiento es posible.

obtener_tipo_movimiento(self, indice, indice_vacio): Determina el tipo de movimiento realizado (arriba, abajo, izquierda o derecha) y lo devuelve en formato R1, R2, R3, R4.

mostrar_movimiento(self, tipo_movimiento): Muestra en pantalla el movimiento realizado y actualiza el contador de movimientos.

actualizar_botones(self): Refresca la interfaz gráfica con la nueva disposición de las piezas después de cada movimiento.

reiniciar_juego(self): Reinicia el juego al estado inicial, restableciendo la posición de las piezas y el contador de movimientos.