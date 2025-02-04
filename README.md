# Árbol Binario de Búsqueda (BST) en Python

Este proyecto implementa un Árbol Binario de Búsqueda (BST, por sus siglas en inglés) en Python. Un BST es una estructura de datos que permite almacenar y organizar datos de manera eficiente, facilitando operaciones como la inserción, búsqueda y recorrido de nodos.

## Estructura del Proyecto

El proyecto consta de dos clases principales:

1. **Clase `Nodo`**: Representa un nodo en el árbol binario de búsqueda. Cada nodo tiene un valor, una referencia a su hijo izquierdo y una referencia a su hijo derecho.

2. **Clase `BST`**: Representa el árbol binario de búsqueda en sí. Esta clase contiene métodos para agregar nodos, buscar valores y recorrer el árbol.

## Funcionalidades Implementadas

### 1. Inserción de Nodos
- **Método `agregar_nodo`**: Permite agregar un nuevo nodo al árbol. Si el árbol está vacío, el nuevo nodo se convierte en la raíz. Si no, se inserta en la posición correcta según las reglas del BST (los valores menores van a la izquierda y los mayores a la derecha).

### 2. Búsqueda de Valores
- **Método `buscar`**: Permite buscar un valor en el árbol. Devuelve `True` si el valor existe en el árbol y `False` en caso contrario.

### 3. Imprimir el Árbol
- **Método `imprimir_nodos`**: Realiza un recorrido inorden del árbol, imprimiendo los valores de los nodos en orden ascendente.

### 4. Agregar valores al arbol
- **Función `main`**: Permite al usuario interactuar con el árbol. El usuario puede agregar valores al árbol y luego buscar valores específicos. El programa también imprime los nodos del árbol en orden inorden.

## Ejecución del Programa
 El programa solicitará al usuario que ingrese valores para agregar al árbol. Para salir del modo de inserción, el usuario debe escribir "salir". Luego, el programa permitirá al usuario buscar valores en el árbol.
