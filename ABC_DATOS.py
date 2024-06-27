import json

# Función para leer datos desde un archivo JSON
def leer_datos_json(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Función para mostrar los datos leídos
def mostrar_datos(datos):
    aulas = datos['aulas']
    profesores = datos['profesores']
    clases = datos['clases']

    print("Aulas:")
    for aula in aulas:
        print(f"  {aula['nombre']}: {', '.join(aula['disponibilidad'])}")

    print("\nProfesores:")
    for profesor in profesores:
        print(f"  {profesor['nombre']}: {', '.join(profesor['disponibilidad'])} | Clases: {', '.join(profesor['clases'])}")

    print("\nClases:")
    for clase in clases:
        print(f"  {clase['nombre']}: {clase['duracion']} | Profesor: {clase['profesor']}")

# Función principal
def main():
    # Nombre del archivo JSON
    nombre_archivo = 'Bioinspirados/proyecto/abeja/datos.json'

    # Leer los datos desde el archivo JSON
    datos = leer_datos_json(nombre_archivo)

    # Mostrar los datos leídos
    mostrar_datos(datos)

    # Aquí puedes continuar con la implementación de tu algoritmo genético
    # utilizando los datos leídos desde el archivo JSON

# Llamada a la función principal
if __name__ == "__main__":
    main()
