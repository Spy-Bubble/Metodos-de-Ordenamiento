import os
import tempfile
import heapq


def balanced_multiway_merging(archivo_entrada, num_vias=4, tamanio_bloque=1000):
    """
    Balanced Multiway Merging - Mezcla Balanceada Multivía.
    Complejidad: O(n log k) donde k es el número de vías.
    Uso: Reduce pasadas sobre disco usando fusión k-vías.
    """
    # Fase 1: Dividir y ordenar bloques
    archivos_temp = []
    
    with open(archivo_entrada, 'r') as f:
        while True:
            lineas = []
            for _ in range(tamanio_bloque):
                linea = f.readline()
                if not linea:
                    break
                lineas.append(int(linea.strip()))
            
            if not lineas:
                break
            
            lineas.sort()
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            for numero in lineas:
                temp_file.write(f"{numero}\n")
            temp_file.close()
            archivos_temp.append(temp_file.name)
    
    # Fase 2: Fusión multivía
    while len(archivos_temp) > 1:
        nuevos_archivos = []
        
        # Fusionar en grupos de num_vias archivos
        for i in range(0, len(archivos_temp), num_vias):
            grupo = archivos_temp[i:i + num_vias]
            archivo_fusionado = fusionar_multiples_archivos(grupo)
            nuevos_archivos.append(archivo_fusionado)
            
            # Eliminar archivos temporales
            for archivo in grupo:
                os.remove(archivo)
        
        archivos_temp = nuevos_archivos
    
    archivo_salida = archivo_entrada.replace('.txt', '_ordenado_multiway.txt')
    os.rename(archivos_temp[0], archivo_salida)
    
    return archivo_salida


def fusionar_multiples_archivos(archivos):
    """Fusiona múltiples archivos usando un heap."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    # Abrir todos los archivos
    files = [open(archivo, 'r') for archivo in archivos]
    
    # Heap: (valor, índice_archivo)
    heap = []
    
    # Inicializar heap con primer elemento de cada archivo
    for i, f in enumerate(files):
        linea = f.readline()
        if linea:
            heapq.heappush(heap, (int(linea.strip()), i))
    
    # Extraer mínimo y agregar siguiente elemento del mismo archivo
    while heap:
        valor, indice = heapq.heappop(heap)
        temp_file.write(f"{valor}\n")
        
        # Leer siguiente línea del archivo correspondiente
        linea = files[indice].readline()
        if linea:
            heapq.heappush(heap, (int(linea.strip()), indice))
    
    # Cerrar todos los archivos
    for f in files:
        f.close()
    
    temp_file.close()
    return temp_file.name


# Ejemplo de uso
if __name__ == "__main__":
    # Crear archivo grande
    with open('datos_multiway.txt', 'w') as f:
        import random
        for _ in range(8000):
            f.write(f"{random.randint(1, 10000)}\n")
    
    print("Ordenando con Balanced Multiway Merging...")
    resultado = balanced_multiway_merging('datos_multiway.txt', num_vias=4)
    print(f"Archivo ordenado: {resultado}")