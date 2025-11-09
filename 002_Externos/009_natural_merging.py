"""
Natural Merging (Mezcla Natural)
Algoritmo de ordenamiento externo que aprovecha secuencias ordenadas naturales.
"""

import os
import tempfile


def natural_merging(archivo_entrada):
    """
    Natural Merging - Mezcla Natural.
    Complejidad: O(n log m) donde m es el número de runs naturales.
    Uso: Archivos parcialmente ordenados.
    """
    # Fase 1: Identificar y distribuir runs naturales
    archivos_temp = distribuir_runs_naturales(archivo_entrada)
    
    # Fase 2: Fusionar archivos hasta quedar uno solo
    while len(archivos_temp) > 1:
        nuevos_archivos = []
        
        for i in range(0, len(archivos_temp), 2):
            if i + 1 < len(archivos_temp):
                archivo_fusionado = fusionar_dos_archivos(
                    archivos_temp[i],
                    archivos_temp[i + 1]
                )
                nuevos_archivos.append(archivo_fusionado)
                os.remove(archivos_temp[i])
                os.remove(archivos_temp[i + 1])
            else:
                nuevos_archivos.append(archivos_temp[i])
        
        archivos_temp = nuevos_archivos
    
    archivo_salida = archivo_entrada.replace('.txt', '_ordenado_natural.txt')
    os.rename(archivos_temp[0], archivo_salida)
    
    return archivo_salida


def distribuir_runs_naturales(archivo):
    """Identifica y distribuye secuencias ordenadas naturales."""
    archivos_temp = []
    
    with open(archivo, 'r') as f:
        run_actual = []
        valor_anterior = None
        
        for linea in f:
            valor = int(linea.strip())
            
            # Si el valor mantiene orden ascendente, agregarlo al run
            if valor_anterior is None or valor >= valor_anterior:
                run_actual.append(valor)
            else:
                # Fin del run, guardar en archivo temporal
                if run_actual:
                    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
                    for num in run_actual:
                        temp_file.write(f"{num}\n")
                    temp_file.close()
                    archivos_temp.append(temp_file.name)
                
                # Iniciar nuevo run
                run_actual = [valor]
            
            valor_anterior = valor
        
        # Guardar último run
        if run_actual:
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            for num in run_actual:
                temp_file.write(f"{num}\n")
            temp_file.close()
            archivos_temp.append(temp_file.name)
    
    return archivos_temp


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
    
    with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
        linea1 = f1.readline()
        linea2 = f2.readline()
        
        # Comparar y escribir el menor elemento
        while linea1 and linea2:
            num1 = int(linea1.strip())
            num2 = int(linea2.strip())
            
            if num1 <= num2:
                temp_file.write(f"{num1}\n")
                linea1 = f1.readline()
            else:
                temp_file.write(f"{num2}\n")
                linea2 = f2.readline()
        
        # Escribir elementos restantes del archivo 1
        while linea1:
            temp_file.write(linea1)
            linea1 = f1.readline()
        
        # Escribir elementos restantes del archivo 2
        while linea2:
            temp_file.write(linea2)
            linea2 = f2.readline()
    
    temp_file.close()
    return temp_file.name


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("NATURAL MERGING - Mezcla Natural")
    print("=" * 70)
    
    # Crear archivo con algunos runs naturales
    archivo_test = 'datos_parcialmente_ordenados.txt'
    print(f"\nCreando archivo de prueba: {archivo_test}")
    
    with open(archivo_test, 'w') as f:
        import random
        
        # Crear 5 runs ordenados de tamaño variable
        for _ in range(5):
            # Crear run ordenado de 200 elementos
            run = sorted([random.randint(1, 1000) for _ in range(200)])
            for num in run:
                f.write(f"{num}\n")
    
    print(f"Archivo creado con runs naturales ordenados")
    
    # Aplicar Natural Merging
    print("\nOrdenando con Natural Merging...")
    resultado = natural_merging(archivo_test)
    
    print(f"Archivo ordenado guardado como: {resultado}")
    
    # Verificar que está ordenado
    print("\nVerificando orden...")
    anterior = None
    ordenado = True
    contador = 0
    
    with open(resultado, 'r') as f:
        for linea in f:
            valor = int(linea.strip())
            contador += 1
            
            if anterior is not None and valor < anterior:
                ordenado = False
                print(f"ERROR: Desorden encontrado en línea {contador}")
                print(f"  Valor anterior: {anterior}, Valor actual: {valor}")
                break
            
            anterior = valor
    
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
    print("\nLimpiando archivos temporales...")
    if os.path.exists(archivo_test):
        os.remove(archivo_test)
        print(f"  Eliminado: {archivo_test}")
    
    if os.path.exists(resultado):
        os.remove(resultado)
        print(f"  Eliminado: {resultado}")
    
    print("\n[OK] Demostración completada")