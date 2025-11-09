def counting_sort_radix(arr, posicion):
    """
    Counting Sort para una posición de dígito específica.
    Usado como subrutina de Radix Sort.
    """
    n = len(arr)
    resultado = [0] * n
    conteo = [0] * 10  # Dígitos 0-9
    
    # Contar ocurrencias de cada dígito
    for i in range(n):
        indice = arr[i] // posicion
        conteo[indice % 10] += 1
    
    # Calcular posiciones acumuladas
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]
    
    # Construir arreglo ordenado
    i = n - 1
    while i >= 0:
        indice = arr[i] // posicion
        resultado[conteo[indice % 10] - 1] = arr[i]
        conteo[indice % 10] -= 1
        i -= 1
    
    # Copiar resultado al arreglo original
    for i in range(n):
        arr[i] = resultado[i]


def radix_sort(arr):
    """
    Ordenamiento Radix (Radix Sort).
    Complejidad: O(d * (n + k)) donde d es el número de dígitos.
    Estable: Si
    In-place: No
    """
    if not arr:
        return arr
    
    # Encontrar el elemento máximo para determinar número de dígitos
    maximo = max(arr)
    
    # Aplicar counting sort para cada posición de dígito
    posicion = 1
    while maximo // posicion > 0:
        counting_sort_radix(arr, posicion)
        posicion *= 10
    
    return arr


# Ejemplo de uso
if __name__ == "__main__":
    lista = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Lista original:", lista)
    resultado = radix_sort(lista.copy())
    print("Lista ordenada (Radix Sort):", resultado)