import os # Manejo de rutas y directorios
import sys # Para salida del programa

# FUNCIONES
# Muestra mensaje de error y continúa el programa
def mostrar_error(mensaje_error):
    print(mensaje_error) # Mostrar mensaje de error proporcionado

# Lee archivo txt línea por línea y extrae números telefónicos
def leer_numeros_desde_archivo(ruta_archivo):
    numeros_lista = [] # Lista para almacenar números extraídos
    
    try:
        # Abrir archivo en modo lectura
        with open(ruta_archivo, 'r', encoding = 'utf-8') as archivo_txt:
            # Leer cada línea del archivo
            for linea in archivo_txt:
                # Limpiar espacios y saltos de línea
                numero_limpio = linea.strip()
                
                # Verificar que la línea no esté vacía
                if numero_limpio:
                    # Agregar número a la lista
                    numeros_lista.append(numero_limpio)
    
    except FileNotFoundError:
        mostrar_error("File not found")
        
        return []
    
    except PermissionError:
        mostrar_error("Permission denied")
        
        return []
    
    except Exception as error_general:
        mostrar_error(f"Error reading file: {error_general}")
        
        return []
    
    return numeros_lista

# Genera contenido VCF a partir de lista de números telefónicos
def generar_contenido_vcf(lista_numeros):
    contenido_vcf = [] # Lista para almacenar líneas VCF
    
    # Generar entrada VCF para cada número
    for indice, numero_telefono in enumerate(lista_numeros, 1):
        contenido_vcf.append("BEGIN:VCARD")
        contenido_vcf.append("VERSION:2.1")
        contenido_vcf.append(f"N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{indice};;")
        contenido_vcf.append(f"FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{indice}")
        contenido_vcf.append(f"TEL;CELL:{numero_telefono}")
        contenido_vcf.append("END:VCARD")
        contenido_vcf.append("") # Línea en blanco entre contactos
    
    # Unir líneas con saltos de línea
    return "\n".join(contenido_vcf)

# Guarda contenido VCF en archivo con nombre específico
def guardar_archivo_vcf(contenido_vcf, directorio_salida):
    # Definir ruta completa del archivo de salida
    ruta_salida = os.path.join(directorio_salida, "Generated VCF.vcf")
    
    try:
        # Escribir contenido en archivo
        with open(ruta_salida, 'w', encoding = 'utf-8') as archivo_vcf:
            archivo_vcf.write(contenido_vcf)
        
        return ruta_salida # Retornar ruta del archivo generado
    
    except PermissionError:
        mostrar_error("Permission denied for writing file")
        
        return None
    
    except Exception as error_general:
        mostrar_error(f"Error writing file: {error_general}")
        
        return None

# BUCLE PRINCIPAL DEL PROGRAMA
try:
    # Obtener directorio del script actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Bucle principal para procesar múltiples archivos
    while True:
        # Solicitar ruta del archivo txt al usuario
        ruta_txt_input = input("Enter TXT file path: ").strip()
        
        # Salir del programa si se ingresa texto vacío (sólo Enter)
        if ruta_txt_input == "":
            break
        
        # Expandir rutas con caracteres especiales como ~
        ruta_txt_expandida = os.path.expanduser(ruta_txt_input)
        
        # Verificar que el archivo existe
        if not os.path.isfile(ruta_txt_expandida):
            print("File does not exist\n")
            
            continue
        
        # Leer números del archivo txt
        lista_numeros = leer_numeros_desde_archivo(ruta_txt_expandida)
        
        # Verificar que se encontraron números
        if not lista_numeros:
            print("No phone numbers found in file\n")
            
            continue
        
        # Generar contenido VCF
        contenido_vcf = generar_contenido_vcf(lista_numeros)
        
        # Guardar archivo VCF en directorio del script
        ruta_guardado = guardar_archivo_vcf(contenido_vcf, directorio_actual)
        
        # Mostrar resultado si se guardó correctamente
        if ruta_guardado:
            print(f"{len(lista_numeros)} contacts generated\n")

except KeyboardInterrupt:
    print("\nOperation cancelled by user")

except Exception as error_inesperado:
    print(f"Unexpected error: {error_inesperado}")
