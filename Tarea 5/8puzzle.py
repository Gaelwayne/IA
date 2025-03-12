import tkinter as tk
from tkinter import messagebox

class JuegoPuzzle:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Juego del 8-Puzzle")
        self.piezas = [1, 4, 3, 7, 0, 6, 5, 8, 2]  # Estado inicial (0 representa el espacio vacío)
        self.estado_objetivo = [1, 2, 3, 8, 0, 4, 7, 6, 5]  # Estado objetivo
        self.botones = []
        self.etiqueta_movimientos = None  # Para mostrar los movimientos realizados
        self.contador_movimientos = 0  # Contador de movimientos
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear los botones para representar el puzzle
        for i in range(9):
            fila, columna = divmod(i, 3)
            valor = self.piezas[i]
            boton = tk.Button(
                self.ventana,
                text=str(valor) if valor != 0 else "",
                font=("Arial", 24),
                width=4,
                height=2,
                command=lambda idx=i: self.mover_pieza(idx),
            )
            boton.grid(row=fila, column=columna)
            self.botones.append(boton)

        # Botón para reiniciar el juego
        boton_reiniciar = tk.Button(self.ventana, text="Reiniciar", command=self.reiniciar_juego)
        boton_reiniciar.grid(row=3, column=1, pady=10)

        # Área para mostrar los movimientos realizados
        self.etiqueta_movimientos = tk.Label(self.ventana, text="Movimientos:\n", font=("Arial", 12), justify="left")
        self.etiqueta_movimientos.grid(row=4, column=0, columnspan=3, pady=10)

    def mover_pieza(self, indice):
        # Encontrar la posición del espacio vacío (0)
        indice_vacio = self.piezas.index(0)
        # Verificar si el movimiento es válido
        if self.movimiento_es_valido(indice, indice_vacio):
            # Determinar el tipo de movimiento (R1, R2, R3, R4)
            tipo_movimiento = self.obtener_tipo_movimiento(indice, indice_vacio)
            # Intercambiar la pieza con el espacio vacío
            self.piezas[indice_vacio], self.piezas[indice] = self.piezas[indice], self.piezas[indice_vacio]
            self.actualizar_botones()
            # Mostrar el movimiento realizado
            self.mostrar_movimiento(tipo_movimiento)
            # Verificar si el puzzle está resuelto
            if self.piezas == self.estado_objetivo:
                messagebox.showinfo("¡Felicidades!", "¡Has resuelto el puzzle!")

    def movimiento_es_valido(self, indice, indice_vacio):
        # Verificar si la pieza está adyacente al espacio vacío
        fila, columna = divmod(indice, 3)
        fila_vacia, columna_vacia = divmod(indice_vacio, 3)
        return (abs(fila - fila_vacia) == 1 and columna == columna_vacia) or (
            abs(columna - columna_vacia) == 1 and fila == fila_vacia
        )

    def obtener_tipo_movimiento(self, indice, indice_vacio):
        # Determinar el tipo de movimiento (R1, R2, R3, R4)
        fila, columna = divmod(indice, 3)
        fila_vacia, columna_vacia = divmod(indice_vacio, 3)
        if fila < fila_vacia:
            return "R1"  # Mover hueco arriba
        elif fila > fila_vacia:
            return "R2"  # Mover hueco abajo
        elif columna < columna_vacia:
            return "R4"  # Mover hueco a la izquierda
        elif columna > columna_vacia:
            return "R3"  # Mover hueco a la derecha

    def mostrar_movimiento(self, tipo_movimiento):
        # Mostrar el movimiento realizado en la interfaz
        self.contador_movimientos += 1
        texto_actual = self.etiqueta_movimientos.cget("text")
        if self.contador_movimientos % 10 == 0:  # Saltar de línea cada 10 movimientos
            texto_actual += "\n"
        self.etiqueta_movimientos.config(text=texto_actual + " " + tipo_movimiento)

    def actualizar_botones(self):
        # Actualizar el texto de los botones según el estado actual del puzzle
        for i in range(9):
            valor = self.piezas[i]
            self.botones[i].config(text=str(valor) if valor != 0 else "")

    def reiniciar_juego(self):
        # Reiniciar el juego al estado inicial
        self.piezas = [1, 4, 3, 7, 0, 6, 5, 8, 2]
        self.actualizar_botones()
        self.etiqueta_movimientos.config(text="Movimientos:\n")
        self.contador_movimientos = 0

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry("300x400")  # Tamaño inicial de la ventana
juego = JuegoPuzzle(ventana_principal)
ventana_principal.mainloop()