def insertion_sort(arr):
    """
    Ordenamiento por Inserción.
    Complejidad: O(n^2) en el peor caso, O(n) si está casi ordenado.
    Estable: Si
    In-place: Si
    """
    n = len(arr)
    
    # Comenzar desde el segundo elemento
    for i in range(1, n):
        clave = arr[i]
        j = i - 1
        
        # Mover elementos mayores que clave una posición adelante
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insertar clave en su posición correcta
        arr[j + 1] = clave
    
    return arr


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = insertion_sort(lista.copy())
    print("Lista ordenada (Insertion Sort):", resultado)