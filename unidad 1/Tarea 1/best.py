# Clase para representar un nodo del árbol
class Nodo:
    def __init__(self, valor):
        """
        Inicializa un nodo con un valor dado.
        """
        self.valor = valor  # Valor del nodo
        self.izquierda = None  # Referencia al nodo izquierdo
        self.derecha = None  # Referencia al nodo derecho

# Clase para representar el árbol binario de búsqueda (BST)
class BST:
    def __init__(self):
        """
        Inicializa un árbol vacío.
        """
        self.raiz = None  # La raíz del árbol comienza como None

    # Método para agregar un nodo al árbol
    def agregar_nodo(self, valor):
        """
        Agrega un nuevo nodo con el valor dado al árbol.
        """
        if self.raiz is None:  # Si el árbol está vacío, el nuevo nodo es la raíz
            self.raiz = Nodo(valor)
        else:
            self._agregar_nodo_recursivo(self.raiz, valor)  # Llama a la función recursiva

    # Función recursiva para agregar un nodo
    def _agregar_nodo_recursivo(self, nodo_actual, valor):
        """
        Función auxiliar para agregar un nodo de manera recursiva.
        """
        if valor < nodo_actual.valor:  # Si el valor es menor, va a la izquierda
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self._agregar_nodo_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:  # Si el valor es mayor, va a la derecha
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self._agregar_nodo_recursivo(nodo_actual.derecha, valor)
        # Si el valor es igual, no se hace nada (no se permiten duplicados)

    # Método para buscar un valor en el árbol
    def buscar(self, valor):
        """
        Busca un valor en el árbol y devuelve True si existe, False en caso contrario.
        """
        return self._buscar_recursivo(self.raiz, valor)

    # Función recursiva para buscar un valor
    def _buscar_recursivo(self, nodo_actual, valor):
        """
        Función auxiliar para buscar un valor de manera recursiva.
        """
        if nodo_actual is None:  # Si el nodo actual es None, el valor no existe
            return False
        if valor == nodo_actual.valor:  # Si el valor coincide, se encontró
            return True
        elif valor < nodo_actual.valor:  # Si el valor es menor, busca en el subárbol izquierdo
            return self._buscar_recursivo(nodo_actual.izquierda, valor)
        else:  # Si el valor es mayor, busca en el subárbol derecho
            return self._buscar_recursivo(nodo_actual.derecha, valor)

    # Método para imprimir los nodos del árbol (recorrido inorden)
    def imprimir_nodos(self):
        """
        Imprime los valores de los nodos en orden inorden (izquierda-raíz-derecha).
        """
        print("Nodos del árbol (Inorden):")
        self._inorden(self.raiz)
        print()  # Salto de línea al final

    # Función recursiva para recorrido inorden
    def _inorden(self, nodo):
        """
        Función auxiliar para recorrer el árbol en orden inorden.
        """
        if nodo:
            self._inorden(nodo.izquierda)  # Recorre el subárbol izquierdo
            print(nodo.valor, end=" ")  # Imprime el valor del nodo actual
            self._inorden(nodo.derecha)  # Recorre el subárbol derecho

# Función principal para interactuar con el usuario
def main():
    arbol = BST()  # Inicializa un árbol vacío

    while True:
        # Solicitar un valor al usuario
        valor = input("Ingresa un valor para agregar al árbol (o escribe 'salir' para terminar): ")

        # Salir del bucle si el usuario escribe 'salir'
        if valor.lower() == "salir":
            break

        # Intentar convertir el valor a entero
        try:
            valor = int(valor)
            arbol.agregar_nodo(valor)  # Agregar el valor al árbol
            print(f"Valor {valor} agregado al árbol.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")

    # Imprimir los nodos del árbol
    arbol.imprimir_nodos()

    # Buscar un valor en el árbol
    while True:
        buscar_valor = input("Ingresa un valor para buscar en el árbol (o escribe 'salir' para terminar): ")

        # Salir del bucle si el usuario escribe 'salir'
        if buscar_valor.lower() == "salir":
            break

        # Intentar convertir el valor a entero
        try:
            buscar_valor = int(buscar_valor)
            if arbol.buscar(buscar_valor):
                print(f"El valor {buscar_valor} está en el árbol.")
            else:
                print(f"El valor {buscar_valor} no está en el árbol.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()