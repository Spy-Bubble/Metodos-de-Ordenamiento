def selection_sort(arr):
    """
    Ordenamiento por Selección.
    Complejidad: O(n^2) en todos los casos.
    Estable: No
    In-place: Si
    """
    n = len(arr)
    
    # Recorrer toda la lista
    for i in range(n):
        # Encontrar el índice del elemento mínimo
        indice_minimo = i
        
        for j in range(i + 1, n):
            if arr[j] < arr[indice_minimo]:
                indice_minimo = j
        
        # Intercambiar el elemento mínimo con el primero no ordenado
        arr[i], arr[indice_minimo] = arr[indice_minimo], arr[i]
    
    return arr


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = selection_sort(lista.copy())
    print("Lista ordenada (Selection Sort):", resultado)