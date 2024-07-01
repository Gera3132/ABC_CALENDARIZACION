#Serrano Fernandez Gerardo Adonai
#Rios Rivera Fernanda Anahi
#Sireno Ojeda Cesar Abraham
#Martinez Serrano Alexis Geovanni
#Algoritmos bioinspirados
#Profesora Miriam Pescador Rojas
#Grupo 5BM2
import random
import json
#Esta funcion simplemente nos ayuda a diferenciar cada dia que asigna el algoritmo tomando 1 como Lunes, 2 como Martes
#y asi consecutivamente...
def imprimir_dia_semana(dia):
    if dia == 1:
        return "Lunes"
    elif dia == 2:
        return "Martes"
    elif dia == 3:
        return "Miércoles"
    elif dia == 4:
        return "Jueves"
    elif dia == 5:
        return "Viernes"
    else:
        return "Día no válido"

def cargar_datos_json(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos


def obtener_rango_horarios(profesores):
    horario_min = float('inf')
    horario_max = float('-inf')
    
    for profesor in profesores:
        disponibilidad = profesor.get("disponibilidad", [])
        for horario_str in disponibilidad:
            inicio_str, fin_str = horario_str.split('-')
            horario_inicio = int(inicio_str[:2])  # Convertir la hora de inicio a entero
            horario_fin = int(fin_str[:2])  # Convertir la hora de fin a entero
            horario_min = min(horario_min, horario_inicio)
            horario_max = max(horario_max, horario_fin)
    
    return horario_min, horario_max

def imprimir_tabla_asignacion(abejas_empleadas, aulas, dias_semana):
    tabla_asignacion = []
    for _ in range(len(aulas)):
        fila = ["-" for _ in range(dias_semana)]
        tabla_asignacion.append(fila)

    for abeja in abejas_empleadas:
        for maestro_info in abeja["horarios"]:
            for materia in maestro_info["horarios_materias"]:
                salon = materia["salon"] - 1
                dia = materia["dia"] - 1
                horario_inicio = materia["horario"]
                horario_fin = horario_inicio + 1
                clase = materia["materia"]
                maestro = maestro_info["maestro"]
                asignacion = f"({clase},{maestro})"
                tabla_asignacion[salon][dia] = asignacion

    print("Tabla de Asignación de Horarios:")
    encabezado_horarios = "Salón | " + " | ".join([f"{hora}-{hora+1}" for hora in range(horario_min, horario_max)])
    print(encabezado_horarios)
    print("-" * len(encabezado_horarios))

    for i, fila in enumerate(tabla_asignacion):
        fila_imprimir = f"{i+1:<6} | " + " | ".join([f"{casilla:<12}" for casilla in fila])
        print(fila_imprimir)

if __name__ == "__main__":
    # Cargar datos desde el archivo JSON
    datos = cargar_datos_json('datos.json')

    # Obtener aulas, profesores y clases del archivo JSON
    aulas = datos.get('aulas', [])
    profesores = datos.get('profesores', [])
    clases = datos.get('clases', [])
    horario_min, horario_max = obtener_rango_horarios(profesores)
    # Número de salones disponibles
    salones_n = len(aulas)

    # Crear diccionario de maestros a partir de los datos del JSON
    maestros = {}
    for profesor in profesores:
        nombre_maestro = profesor["nombre"]
        maestro = {
            "nombre": nombre_maestro,
            "horario": {
                "inicio": 9,  # Suponiendo un horario fijo de entrada y salida para ejemplo
                "fin": 12
            },
            "materias": profesor["clases"]
        }
        maestros[nombre_maestro] = maestro


    # INICIAMOS ALGORITMO ABC
    abejas_exploradoras_n = 1  # Número de abejas exploradoras
    abejas_empleadas_n = 0     # Número inicial de abejas empleadas
    dias = 1000                   # Número máximo de iteraciones del algoritmo
    #Consideramos que cada que el algoritmo manda a abejas a explorar, es un día.
    dias_semana = 3            #Indica si queremos que asigne horarios para lunes, Lunes y Martes
                                #Lunes, Martes, Miercoles y Jueves...
    dias_sin_mejora2 = 100      #variable para hacer que el algoritmo pare si no hay mejoras en una cantidad de iteraciones
    mejor_puntuacion = 0
    mejor_puntuacion_local = 0

    #Es importante destacar que se tomará que todas las clases duran una hora y por simplicidad, decidimos
    #no dar la opción de preguntar cuantas veces daría la materia el profesor, pero esto se podría solucionar
    #dando la materia la N cantidad de veces que se quiere que el profesor la de a la semana
    #El horario en que asigna las clases esta limitado al horario del profesor como rango de busqueda.


    abejas_exploradoras = [] #Inicializamos nuestras abejas exploradoras


    # GENERAR LA POBLACIÓN INICIAL
    #El siguiente ciclo crea la cantidad de abejas exploradoras deseadas aleatoriamente con los campos
    #horarios y puntuacion. 
    #Basicamente almacena los horarios que tendrá cada materia que imparte cada profesor dado y un campo llamado 
    #llamado puntuacion que servirá más adelante
    iteracion = 0
    dias_sin_mejora = 0
    while iteracion < dias and dias_sin_mejora < dias_sin_mejora2:
        if abejas_exploradoras_n > 0:
            for _ in range(abejas_exploradoras_n): 
                abeja = {"horarios": [], "puntuacion": 0}
                for nombre_maestro, maestro_info in maestros.items():
                    horarios_materias = []
                    for materia in maestro_info["materias"]:
                        horario = random.randint(maestro_info["horario"]["inicio"], maestro_info["horario"]["fin"] - 1)  # Generar un horario dentro del rango del maestro
                        dia = random.randint(1, dias_semana)  # Asignar un día aleatorio de la semana (1 para Lunes, 2 para Martes, etc.)
                        salon = random.randint(1, salones_n)  # Asignar un salón aleatorio entre 1 y salones_n
                        horarios_materias.append({"materia": materia, "horario": horario, "salon": salon, "dia": dia})
                    abeja["horarios"].append({"maestro": nombre_maestro, "horarios_materias": horarios_materias})
                abejas_exploradoras.append(abeja)


            #Después de generar la población inicial, eválua para obtener a las mejores abejas. El sistema de puntuación es el siguiente:
            #Que el salón no esté ya ocupado en ese horario +70
            #Que los horarios de cada profesor no choquen entre sí +70
            #-1 por cada hora de diferencia entre cada clase que da cada profesor
            #-N * 5 por cada día que el profesor tenga que ir a la escuela. Es decir si tiene que ir 4 dias, restará 12 puntos
            #-100 si choca algún horario entre profesores
            #-10 si el salón ya estaba ocupado


            # EVALUAR DISPONIBILIDAD DE SALONES
            for abeja in abejas_exploradoras:
                horario_salon_ocupado = {}  # Diccionario para verificar la disponibilidad del horario en cada salón
                for maestro in abeja["horarios"]:
                    for materia in maestro["horarios_materias"]:
                        horario = materia["horario"]
                        salon = materia["salon"]
                        dia = materia["dia"]
                        if (salon, dia) not in horario_salon_ocupado:
                            horario_salon_ocupado[(salon, dia)] = set()
                        #Conforme va leyendo los horarios los va agregando como ocupados y aca abjito verifica que no estuviera
                        #ya ocupado.
                        if horario not in horario_salon_ocupado[(salon, dia)]:
                            #70 porque son 14 horas por dia por 5 dias de la semana
                            abeja["puntuacion"] += 70
                            horario_salon_ocupado[(salon, dia)].add(horario)
                        else:
                            abeja["puntuacion"] -= 10
            
            # EVALUAR QUE NO CHOQUEN LOS HORARIOS DE LOS PROFESORES
            #Funciona practicamente igual que el ciclo anterior, solo que ahora checa entre los horarios de los profesores
            for abeja in abejas_exploradoras:
                horario_profesor_ocupado = {}  # Diccionario para verificar la disponibilidad del horario de cada profesor
                for maestro in abeja["horarios"]:
                    profesor = maestro["maestro"] #para que pueda evaluar igual que antes
                    if profesor not in horario_profesor_ocupado:
                        horario_profesor_ocupado[profesor] = {}
                    for materia in maestro["horarios_materias"]:
                        horario = materia["horario"]
                        dia = materia["dia"]
                        if dia not in horario_profesor_ocupado[profesor]:
                            horario_profesor_ocupado[profesor][dia] = set()
                        # Verificar si el horario está disponible para el profesor
                        if horario not in horario_profesor_ocupado[profesor][dia]:
                            #70 porque son 14 horas por dia por 5 dias de la semana
                            abeja["puntuacion"] += 70
                            horario_profesor_ocupado[profesor][dia].add(horario)
                        else:
                            abeja["puntuacion"] -=100


            # RESTAR PUNTOS POR DIFERENCIA DE HORAS ENTRE CLASES QUE TIENE EL MISMO DÍA
            for abeja in abejas_exploradoras:
                for maestro in abeja["horarios"]:
                    profesor = maestro["maestro"]
                    dias_ocupados = set() 
                    for dia, horarios in horario_profesor_ocupado[profesor].items():
                        #Creamos la lista de días que tiene el profesor con sus horarios acomodados
                        dias_ocupados.add(dia) 
                        horarios = sorted(horarios)
                        for i in range(len(horarios) - 1):
                            #Restamos la diferencia de horas que tiene de descanso en total por dia
                            diferencia_horas = horarios[i + 1] - horarios[i]
                            abeja["puntuacion"] -= diferencia_horas
                    # Restar puntos por cada día diferente que el profesor tenga una clase
                    abeja["puntuacion"] -= len(dias_ocupados) * 5


            # ORDENAR ABEJAS POR PUNTUACIÓN
            abejas_exploradoras.sort(key=lambda x: x["puntuacion"], reverse=True)
            # Crear abejas empleadas basadas en la mejor puntuación
            mejor_puntuacion_local = abejas_exploradoras[0]["puntuacion"]

        if(mejor_puntuacion_local > mejor_puntuacion):
            mejor_puntuacion = mejor_puntuacion_local
            abejas_empleadas = []
            #Segun el algoritmo ABC, cuando una abeja encuentra una zona buena de alimentación,
            #se convierte en abeja ampleada según la información que tienen las abejas exploradoras
            #es decir, únicamente las mejores abejas exploradoras se convierten en empleadas, por 
            #eso hacemos el filtro con la puntuación y dejamos al resto de abejas que sigan explorando hasta que sean
            #parte de las mejores.

            for abeja in abejas_exploradoras:
                if abeja["puntuacion"] == mejor_puntuacion:
                    abejas_empleadas.append(abeja.copy())  # Agrega copia de la abeja a abejas_empleadas
                    abejas_empleadas_n += 1
                    abejas_exploradoras_n -= 1    

        mejor_puntuacion_actual = mejor_puntuacion
        iteracion += 1
        # Generar nuevos horarios para las abejas empleadas
        #todo esto funciona de la misma manera que con la población inicial.
        for abeja in abejas_empleadas:
            horario_salon_ocupado2 = {}  # Diccionario para verificar la disponibilidad del horario en cada salón
            horario_profesor_ocupado2 = {}
            for maestro_info in abeja["horarios"]:
                horarios_materias_nuevos = []
                for materia in maestro_info["horarios_materias"]:
                    horario = random.randint(maestros[maestro_info["maestro"]]["horario"]["inicio"],
                                             maestros[maestro_info["maestro"]]["horario"]["fin"] - 1)
                    dia = random.randint(1, dias_semana)
                    salon = random.randint(1, salones_n)
                    horarios_materias_nuevos.append({"materia": materia["materia"], "horario": horario,
                                                     "salon": salon, "dia": dia})
                # Evaluar nuevos horarios
                nueva_puntuacion = 0
                for materia in horarios_materias_nuevos:
                    horario = materia["horario"]
                    salon = materia["salon"]
                    dia = materia["dia"]
                    if (salon, dia) not in horario_salon_ocupado2:
                        horario_salon_ocupado2[(salon, dia)] = set()
                    # Verificar si el horario está disponible
                    if horario not in horario_salon_ocupado2[(salon, dia)]:
                        nueva_puntuacion += 70
                        #horario_salon_ocupado[(salon, dia)].add(horario)
                    else:
                        nueva_puntuacion -= 10
                profesor = maestro_info["maestro"]
                if profesor not in horario_profesor_ocupado2:
                    horario_profesor_ocupado2[profesor] = {}
                for materia in horarios_materias_nuevos:
                    horario = materia["horario"]
                    dia = materia["dia"]
                    if dia not in horario_profesor_ocupado2[profesor]:
                        horario_profesor_ocupado2[profesor][dia] = set()
                    # Verificar si el horario está disponible para el profesor
                    if horario not in horario_profesor_ocupado2[profesor][dia]:
                        nueva_puntuacion += 70
                        #horario_profesor_ocupado[profesor][dia].add(horario)
                    else:
                         nueva_puntuacion -=100
                for dia, horarios in horario_profesor_ocupado2[profesor].items():
                    horarios = sorted(horarios)
                    for i in range(len(horarios) - 1):
                        diferencia_horas = horarios[i + 1] - horarios[i]
                        nueva_puntuacion -= diferencia_horas
                dias_ocupados = set(horario_profesor_ocupado2[profesor].keys())
                nueva_puntuacion -= len(dias_ocupados) * 5
                # Comparar puntuaciones y actualizar si es mejor
                if nueva_puntuacion >= mejor_puntuacion_actual:#if nueva_puntuacion >= abeja["puntuacion"]:
                    abeja["puntuacion"] = nueva_puntuacion
                    abeja["horarios"] = [{"maestro": maestro_info["maestro"], "horarios_materias": horarios_materias_nuevos}]
                    print(f"Mejora encontrada en la Abeja Empleada {abejas_empleadas.index(abeja) + 1} en la Iteración {iteracion}.")
                    # Reiniciar contador de días sin mejora
                    dias_sin_mejora = 0
                else:
                    dias_sin_mejora += 1
    # Mostrar resultados finales
    print(f"\nIteraciones: {iteracion}:")
    print("\nResultados finales de las Abejas Empleadas:")
    for i, abeja in enumerate(abejas_empleadas):
        print(f"\nAbeja Empleada {i + 1}:")
        print(f"Puntuación: {abeja['puntuacion']}")
        for maestro_info in abeja["horarios"]:
            print(f"Maestro: {maestro_info['maestro']}")
            for materia in maestro_info["horarios_materias"]:
                print(f"  Materia: {materia['materia']}, Horario: {materia['horario']}:00 - {materia['horario'] + 1}:00, Salón: {materia['salon']}, Día: {imprimir_dia_semana(materia['dia'])}")
                
    imprimir_tabla_asignacion(abejas_empleadas, aulas, dias_semana=3)