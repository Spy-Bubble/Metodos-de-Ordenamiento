class NodoArbol:
    """Nodo de árbol binario de búsqueda."""
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


def insertar_nodo(raiz, valor):
    """Inserta un valor en el árbol binario de búsqueda."""
    if raiz is None:
        return NodoArbol(valor)
    
    if valor < raiz.valor:
        raiz.izquierda = insertar_nodo(raiz.izquierda, valor)
    else:
        raiz.derecha = insertar_nodo(raiz.derecha, valor)
    
    return raiz


def recorrido_inorden(raiz, resultado):
    """Recorrido inorden: izquierda, raíz, derecha."""
    if raiz is not None:
        recorrido_inorden(raiz.izquierda, resultado)
        resultado.append(raiz.valor)
        recorrido_inorden(raiz.derecha, resultado)


def tree_sort(arr):
    """
    Ordenamiento de Árbol (Tree Sort).
    Complejidad: O(n log n) en promedio, O(n^2) en el peor caso.
    Estable: No
    In-place: No
    """
    if not arr:
        return arr
    
    # Construir árbol binario de búsqueda
    raiz = None
    for valor in arr:
        raiz = insertar_nodo(raiz, valor)
    
    # Obtener elementos ordenados mediante recorrido inorden
    resultado = []
    recorrido_inorden(raiz, resultado)
    
    return resultado


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = tree_sort(lista.copy())
    print("Lista ordenada (Tree Sort):", resultado)