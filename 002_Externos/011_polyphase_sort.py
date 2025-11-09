"""
Polyphase Sort (Ordenamiento Polifásico)
Algoritmo de ordenamiento externo optimizado.
"""

import os
import tempfile


def polyphase_sort(archivo_entrada, num_archivos=3, tamanio_bloque=500):
    """
    Polyphase Sort - Ordenamiento Polifásico.
    Complejidad: O(n log n) con menos operaciones de fusión.
    Uso: Optimización cuando el número de archivos temporales es limitado.
    """
    # Fase 1: Crear runs ordenados
    runs = crear_runs_ordenados(archivo_entrada, tamanio_bloque)
    
    if not runs:
        print("ERROR: No se pudieron crear runs")
        return None
    
    print(f"  Se crearon {len(runs)} runs iniciales")
    
    # Fase 2: Distribuir runs según secuencia de Fibonacci
    archivos_temp = distribuir_polifasico(runs, num_archivos)
    
    print(f"  Runs distribuidos en {len(archivos_temp)} archivos")
    
    # Fase 3: Fusión polifásica iterativa
    iteracion = 0
    while not todos_runs_fusionados(archivos_temp):
        iteracion += 1
        print(f"  Iteración de fusión {iteracion}...")
        archivos_temp = fase_fusion_polifasica(archivos_temp)
        
        # Prevenir bucle infinito
        if iteracion > 100:
            print("ERROR: Demasiadas iteraciones, posible bucle infinito")
            break
    
    # Encontrar archivo con todos los datos y retornarlo
    return finalizar_ordenamiento(archivos_temp, archivo_entrada)


def crear_runs_ordenados(archivo, tamanio_bloque):
    """Crea runs ordenados del archivo original."""
    runs = []
    
    try:
        with open(archivo, 'r') as f:
            while True:
                bloque = []
                for _ in range(tamanio_bloque):
                    linea = f.readline()
                    if not linea:
                        break
                    bloque.append(int(linea.strip()))
                
                if not bloque:
                    break
                
                runs.append(sorted(bloque))
    except Exception as e:
        print(f"ERROR al crear runs: {e}")
        return []
    
    return runs


def distribuir_polifasico(runs, num_archivos):
    """
    Distribuye runs según patrón polifásico.
    Retorna lista de nombres de archivos temporales.
    """
    archivos = []
    
    # Crear archivos temporales
    for _ in range(num_archivos):
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp_file.close()
        archivos.append(temp_file.name)
    
    # Distribución simple: alternar entre archivos (dejar uno vacío para fusión)
    for i, run in enumerate(runs):
        indice_archivo = i % (num_archivos - 1)
        
        with open(archivos[indice_archivo], 'a') as f:
            for num in run:
                f.write(f"{num}\n")
            f.write("RUN_END\n")
    
    return archivos


def fase_fusion_polifasica(archivos):
    """
    Realiza una fase de fusión polifásica.
    Retorna lista actualizada de archivos.
    """
    # Encontrar archivo de salida (el que tiene menos runs)
    conteo_runs = []
    for archivo in archivos:
        conteo_runs.append(contar_runs(archivo))
    
    indice_salida = conteo_runs.index(min(conteo_runs))
    archivo_salida = archivos[indice_salida]
    archivos_entrada = [f for i, f in enumerate(archivos) if i != indice_salida]
    
    # Fusionar un run de cada archivo de entrada
    fusionar_un_run_cada_archivo(archivos_entrada, archivo_salida)
    
    return archivos


def contar_runs(archivo):
    """Cuenta el número de runs en un archivo."""
    if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
        return 0
    
    conteo = 0
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                if linea.strip() == "RUN_END":
                    conteo += 1
    except:
        return 0
    
    return conteo


def fusionar_un_run_cada_archivo(archivos_entrada, archivo_salida):
    """Fusiona un run de cada archivo de entrada al archivo de salida."""
    try:
        files = [open(archivo, 'r') for archivo in archivos_entrada]
    except:
        return
    
    # Leer primer run de cada archivo
    runs = []
    for f in files:
        run = []
        for linea in f:
            if linea.strip() == "RUN_END":
                break
            try:
                run.append(int(linea.strip()))
            except:
                continue
        if run:
            runs.append(run)
    
    # Cerrar archivos
    for f in files:
        f.close()
    
    # Fusionar runs
    if runs:
        run_fusionado = fusionar_runs(runs)
        
        # Escribir run fusionado
        with open(archivo_salida, 'a') as f:
            for num in run_fusionado:
                f.write(f"{num}\n")
            f.write("RUN_END\n")
    
    # Reescribir archivos de entrada sin el run procesado
    for archivo in archivos_entrada:
        reescribir_sin_primer_run(archivo)


def fusionar_runs(runs):
    """Fusiona múltiples runs ordenados en uno solo."""
    import heapq
    
    resultado = []
    heap = []
    indices = [0] * len(runs)
    
    # Inicializar heap
    for i, run in enumerate(runs):
        if run:
            heapq.heappush(heap, (run[0], i))
    
    # Extraer mínimos
    while heap:
        valor, indice_run = heapq.heappop(heap)
        resultado.append(valor)
        
        indices[indice_run] += 1
        if indices[indice_run] < len(runs[indice_run]):
            heapq.heappush(heap, (runs[indice_run][indices[indice_run]], indice_run))
    
    return resultado


def reescribir_sin_primer_run(archivo):
    """Reescribe el archivo eliminando el primer run."""
    try:
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        
        primer_run_eliminado = False
        with open(archivo, 'r') as f:
            for linea in f:
                if not primer_run_eliminado:
                    if linea.strip() == "RUN_END":
                        primer_run_eliminado = True
                    continue
                temp_file.write(linea)
        
        temp_file.close()
        os.remove(archivo)
        os.rename(temp_file.name, archivo)
    except Exception as e:
        print(f"ERROR al reescribir archivo: {e}")


def todos_runs_fusionados(archivos):
    """Verifica si todos los runs están en un solo archivo."""
    archivos_con_datos = 0
    total_runs = 0
    
    for archivo in archivos:
        if os.path.exists(archivo):
            runs = contar_runs(archivo)
            if runs > 0:
                archivos_con_datos += 1
                total_runs += runs
    
    # Terminamos cuando solo queda 1 run en 1 archivo
    return archivos_con_datos == 1 and total_runs == 1


def finalizar_ordenamiento(archivos_temp, archivo_entrada):
    """
    Encuentra el archivo con los datos ordenados y lo renombra.
    Retorna el nombre del archivo de salida.
    """
    # Encontrar archivo con datos
    archivo_con_datos = None
    for archivo in archivos_temp:
        if os.path.exists(archivo) and os.path.getsize(archivo) > 0:
            archivo_con_datos = archivo
            break
    
    if archivo_con_datos is None:
        print("ERROR: No se encontró archivo con datos ordenados")
        return None
    
    # Crear archivo de salida sin marcadores RUN_END
    archivo_salida = archivo_entrada.replace('.txt', '_ordenado_polyphase.txt')
    
    with open(archivo_con_datos, 'r') as entrada, open(archivo_salida, 'w') as salida:
        for linea in entrada:
            if linea.strip() != "RUN_END":
                salida.write(linea)
    
    # Eliminar archivos temporales
    for archivo in archivos_temp:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
            except:
                pass
    
    return archivo_salida


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("POLYPHASE SORT - Ordenamiento Polifásico")
    print("=" * 70)
    
    # Crear archivo de prueba
    archivo_test = 'datos_polyphase.txt'
    print(f"\nCreando archivo de prueba: {archivo_test}")
    
    import random
    with open(archivo_test, 'w') as f:
        for _ in range(3000):
            f.write(f"{random.randint(1, 5000)}\n")
    
    print(f"Archivo creado con 3000 números aleatorios")
    
    # Aplicar Polyphase Sort
    print("\nOrdenando con Polyphase Sort...")
    resultado = polyphase_sort(archivo_test, num_archivos=3, tamanio_bloque=400)
    
    if resultado:
        print(f"\nArchivo ordenado guardado como: {resultado}")
        
        # Verificar que está ordenado
        print("\nVerificando orden...")
        anterior = None
        ordenado = True
        contador = 0
        
        with open(resultado, 'r') as f:
            for linea in f:
                try:
                    valor = int(linea.strip())
                    contador += 1
                    
                    if anterior is not None and valor < anterior:
                        ordenado = False
                        print(f"ERROR: Desorden encontrado en línea {contador}")
                        print(f"  Valor anterior: {anterior}, Valor actual: {valor}")
                        break
                    
                    anterior = valor
                except:
                    continue
        
        if ordenado:
            print(f"[OK] Archivo correctamente ordenado ({contador} elementos)")
        else:
            print("[ERROR] Archivo NO está ordenado correctamente")
        
        # Mostrar primeros 20 elementos
        print("\nPrimeros 20 elementos ordenados:")
        with open(resultado, 'r') as f:
            for i in range(20):
                linea = f.readline()
                if linea:
                    print(f"  {i+1}. {linea.strip()}")
        
        # Limpiar archivos
        print("\nLimpiando archivos...")
        if os.path.exists(archivo_test):
            os.remove(archivo_test)
            print(f"  Eliminado: {archivo_test}")
        
        if os.path.exists(resultado):
            os.remove(resultado)
            print(f"  Eliminado: {resultado}")
    else:
        print("\n[ERROR] No se pudo completar el ordenamiento")
    
    print("\n[OK] Demostración completada")