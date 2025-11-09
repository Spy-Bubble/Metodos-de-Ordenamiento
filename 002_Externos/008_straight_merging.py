import os
import tempfile


def straight_merging(archivo_entrada, tamanio_bloque=1000):
    """
    Straight Merging - Mezcla Directa.
    Complejidad: O(n log n) con acceso a disco.
    Uso: Archivos grandes que no caben en memoria.
    """
    archivos_temp = []
    
    # Fase 1: Dividir y ordenar bloques
    with open(archivo_entrada, 'r') as f:
        bloque_numero = 0
        while True:
            # Leer bloque de datos
            lineas = []
            for _ in range(tamanio_bloque):
                linea = f.readline()
                if not linea:
                    break
                lineas.append(int(linea.strip()))
            
            if not lineas:
                break
            
            # Ordenar bloque en memoria
            lineas.sort()
            
            # Escribir bloque ordenado a archivo temporal
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            for numero in lineas:
                temp_file.write(f"{numero}\n")
            temp_file.close()
            archivos_temp.append(temp_file.name)
            bloque_numero += 1
    
    # Fase 2: Fusionar archivos temporales
    while len(archivos_temp) > 1:
        nuevos_archivos = []
        
        # Fusionar pares de archivos
        for i in range(0, len(archivos_temp), 2):
            if i + 1 < len(archivos_temp):
                archivo_fusionado = fusionar_dos_archivos(
                    archivos_temp[i], 
                    archivos_temp[i + 1]
                )
                nuevos_archivos.append(archivo_fusionado)
                
                # Eliminar archivos temporales usados
                os.remove(archivos_temp[i])
                os.remove(archivos_temp[i + 1])
            else:
                nuevos_archivos.append(archivos_temp[i])
        
        archivos_temp = nuevos_archivos
    
    # Renombrar archivo final
    archivo_salida = archivo_entrada.replace('.txt', '_ordenado.txt')
    os.rename(archivos_temp[0], archivo_salida)
    
    return archivo_salida


def fusionar_dos_archivos(archivo1, archivo2):
    """Fusiona dos archivos ordenados en uno solo."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
        linea1 = f1.readline()
        linea2 = f2.readline()
        
        while linea1 and linea2:
            num1 = int(linea1.strip())
            num2 = int(linea2.strip())
            
            if num1 <= num2:
                temp_file.write(f"{num1}\n")
                linea1 = f1.readline()
            else:
                temp_file.write(f"{num2}\n")
                linea2 = f2.readline()
        
        # Escribir elementos restantes
        while linea1:
            temp_file.write(linea1)
            linea1 = f1.readline()
        
        while linea2:
            temp_file.write(linea2)
            linea2 = f2.readline()
    
    temp_file.close()
    return temp_file.name


# Ejemplo de uso
if __name__ == "__main__":
    # Crear archivo de prueba
    with open('datos_grandes.txt', 'w') as f:
        import random
        for _ in range(5000):
            f.write(f"{random.randint(1, 10000)}\n")
    
    print("Ordenando archivo con Straight Merging...")
    resultado = straight_merging('datos_grandes.txt', tamanio_bloque=500)
    print(f"Archivo ordenado guardado como: {resultado}")