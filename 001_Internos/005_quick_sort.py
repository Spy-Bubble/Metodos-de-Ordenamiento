def quick_sort(arr):
    """
    Ordenamiento Rápido (Quick Sort).
    Complejidad: O(n log n) en promedio, O(n^2) en el peor caso.
    Estable: No (implementación estándar)
    In-place: Si (con optimizaciones)
    """
    if len(arr) <= 1:
        return arr
    
    # Seleccionar pivote (elemento central)
    pivote = arr[len(arr) // 2]
    
    # Particionar en tres grupos
    menores = [x for x in arr if x < pivote]
    iguales = [x for x in arr if x == pivote]
    mayores = [x for x in arr if x > pivote]
    
    # Aplicar recursión y combinar
    return quick_sort(menores) + iguales + quick_sort(mayores)


# Ejemplo de uso
if __name__ == "__main__":
    lista = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", lista)
    resultado = quick_sort(lista.copy())
    print("Lista ordenada (Quick Sort):", resultado)