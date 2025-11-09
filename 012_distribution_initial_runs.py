"""
Distribution of Initial Runs (Distribución de Runs Iniciales)
Algoritmo que optimiza la creación de runs iniciales usando selección por reemplazo.
"""

import os
import tempfile
import heapq


def distribution_initial_runs(archivo_entrada, tamanio_memoria=1000):
    """
    Distribution of Initial Runs - Distribución de Runs Iniciales.
    Complejidad: O(n log m) donde m es tamaño de memoria.
    Uso: Genera runs iniciales más largos mediante selección por reemplazo.
    """
    # Fase 1: Generar runs optimizados con selección por reemplazo
    archivos_runs = generar_runs_optimizados(archivo_entrada, tamanio_memoria)
    
    if not archivos_runs:
        print("ERROR: No se pudieron crear runs")
        return None
    
    print(f"  Se crearon {len(archivos_runs)} runs optimizados")
    
    # Fase 2: Fusionar runs usando merge externo
    iteracion = 0
    while len(archivos_runs) > 1:
        iteracion += 1
        print(f"  Fase de fusión {iteracion}: {len(archivos_runs)} archivos...")
        nuevos_archivos = []
        
        for i in range(0, len(archivos_runs), 2):
            if i + 1 < len(archivos_runs):
                archivo_fusionado = fusionar_dos_archivos(
                    archivos_runs[i],
                    archivos_runs[i + 1]
                )
                nuevos_archivos.append(archivo_fusionado)
                os.remove(archivos_runs[i])
                os.remove(archivos_runs[i + 1])
            else:
                nuevos_archivos.append(archivos_runs[i])
        
        archivos_runs = nuevos_archivos
    
    archivo_salida = archivo_entrada.replace('.txt', '_ordenado_distribution.txt')
    os.rename(archivos_runs[0], archivo_salida)
    
    return archivo_salida


def generar_runs_optimizados(archivo, tamanio_memoria):
    """
    Genera runs usando selección por reemplazo.
    Permite crear runs más largos que la memoria disponible.
    """
    archivos_runs = []
    
    try:
        with open(archivo, 'r') as f:
            buffer = []
            
            # Llenar buffer inicial
            for _ in range(tamanio_memoria):
                linea = f.readline()
                if not linea:
                    break
                buffer.append(int(linea.strip()))
            
            if not buffer:
                return archivos_runs
            
            # Convertir buffer en heap
            heapq.heapify(buffer)
            
            # Variables para control de runs
            run_actual = []
            ultimo_valor_escrito = float('-inf')
            elementos_congelados = []
            
            while buffer or elementos_congelados:
                # Si el heap está vacío, comenzar nuevo run
                if not buffer:
                    # Escribir run actual
                    if run_actual:
                        archivo_run = escribir_run_a_archivo(run_actual)
                        archivos_runs.append(archivo_run)
                        run_actual = []
                    
                    # Descongelar elementos para nuevo run
                    buffer = elementos_congelados
                    heapq.heapify(buffer)
                    elementos_congelados = []
                    ultimo_valor_escrito = float('-inf')
                    continue
                
                # Extraer mínimo del heap
                valor = heapq.heappop(buffer)
                
                # Si el valor puede agregarse al run actual
                if valor >= ultimo_valor_escrito:
                    run_actual.append(valor)
                    ultimo_valor_escrito = valor
                    
                    # Leer siguiente elemento del archivo
                    linea = f.readline()
                    if linea:
                        try:
                            nuevo_valor = int(linea.strip())
                            
                            # Si puede agregarse al run actual, al heap
                            # Si no, congelarlo para el siguiente run
                            if nuevo_valor >= ultimo_valor_escrito:
                                heapq.heappush(buffer, nuevo_valor)
                            else:
                                elementos_congelados.append(nuevo_valor)
                        except:
                            continue
                else:
                    # Congelar este valor para el siguiente run
                    elementos_congelados.append(valor)
            
            # Escribir último run si existe
            if run_actual:
                archivo_run = escribir_run_a_archivo(run_actual)
                archivos_runs.append(archivo_run)
    
    except Exception as e:
        print(f"ERROR al generar runs: {e}")
        return []
    
    return archivos_runs


def escribir_run_a_archivo(run):
    """Escribe un run a un archivo temporal."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    for valor in run:
        temp_file.write(f"{valor}\n")
    temp_file.close()
    return temp_file.name


def fusionar_dos_archivos(archivo1, archivo2):
    """
    Fusiona dos archivos ordenados en uno solo.
    
    Args:
        archivo1: Ruta del primer archivo ordenado
        archivo2: Ruta del segundo archivo ordenado
    
    Returns:
        Ruta del archivo fusionado
    """
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    try:
        with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
            linea1 = f1.readline()
            linea2 = f2.readline()
            
            # Comparar y escribir el menor elemento
            while linea1 and linea2:
                try:
                    num1 = int(linea1.strip())
                    num2 = int(linea2.strip())
                    
                    if num1 <= num2:
                        temp_file.write(f"{num1}\n")
                        linea1 = f1.readline()
                    else:
                        temp_file.write(f"{num2}\n")
                        linea2 = f2.readline()
                except:
                    if linea1:
                        linea1 = f1.readline()
                    if linea2:
                        linea2 = f2.readline()
            
            # Escribir elementos restantes del archivo 1
            while linea1:
                temp_file.write(linea1)
                linea1 = f1.readline()
            
            # Escribir elementos restantes del archivo 2
            while linea2:
                temp_file.write(linea2)
                linea2 = f2.readline()
    
    except Exception as e:
        print(f"ERROR al fusionar archivos: {e}")
    
    temp_file.close()
    return temp_file.name


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("DISTRIBUTION OF INITIAL RUNS - Distribución de Runs Iniciales")
    print("=" * 70)
    
    # Crear archivo de prueba
    archivo_test = 'datos_distribution.txt'
    print(f"\nCreando archivo de prueba: {archivo_test}")
    
    import random
    with open(archivo_test, 'w') as f:
        for _ in range(5000):
            f.write(f"{random.randint(1, 10000)}\n")
    
    print(f"Archivo creado con 5000 números aleatorios")
    
    # Aplicar Distribution of Initial Runs
    print("\nOrdenando con Distribution of Initial Runs...")
    resultado = distribution_initial_runs(archivo_test, tamanio_memoria=500)
    
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
        
        # Mostrar estadísticas
        print("\nEstadísticas:")
        print(f"  Total de elementos: {contador}")
        
        # Mostrar primeros y últimos 10 elementos
        print("\nPrimeros 10 elementos:")
        with open(resultado, 'r') as f:
            for i in range(10):
                linea = f.readline()
                if linea:
                    print(f"  {i+1}. {linea.strip()}")
        
        print("\nÚltimos 10 elementos:")
        with open(resultado, 'r') as f:
            todas_lineas = f.readlines()
            for i, linea in enumerate(todas_lineas[-10:], start=len(todas_lineas)-9):
                print(f"  {i}. {linea.strip()}")
        
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