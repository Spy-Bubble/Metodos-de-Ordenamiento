def merge_sort(arr):
    """
    Ordenamiento por Mezcla (Merge Sort).
    Complejidad: O(n log n) en todos los casos.
    Estable: Si
    In-place: No
    """
    if len(arr) <= 1:
        return arr
    
    # Dividir el arreglo en dos mitades
    medio = len(arr) // 2
    izquierda = merge_sort(arr[:medio])
    derecha = merge_sort(arr[medio:])
    
    # Fusionar las mitades ordenadas
    return merge(izquierda, derecha)


def merge(izquierda, derecha):
    """Fusiona dos listas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0
    
    # Comparar elementos de ambas listas
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    
    # Agregar elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    
    return resultado


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = merge_sort(lista.copy())
    print("Lista ordenada (Merge Sort):", resultado)