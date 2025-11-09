def bubble_sort(arr):
    """
    Ordenamiento por Intercambio (Bubble Sort).
    Complejidad: O(n^2) en el peor caso, O(n) si está ordenado.
    Estable: Si
    In-place: Si
    """
    n = len(arr)
    
    # Recorrer todos los elementos
    for i in range(n):
        intercambio = False
        
        # Los últimos i elementos ya están ordenados
        for j in range(0, n - i - 1):
            # Intercambiar si el elemento actual es mayor que el siguiente
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        
        # Si no hubo intercambios, la lista ya está ordenada
        if not intercambio:
            break
    
    return arr


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = bubble_sort(lista.copy())
    print("Lista ordenada (Bubble Sort):", resultado)