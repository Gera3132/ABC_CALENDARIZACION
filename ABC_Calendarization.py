import random

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

if __name__ == "__main__":
    maestros = {}
    op = 1
    salones_n = int(input("¿Cuántos salones hay? "))

    while op == 1:
        # Crear un diccionario para almacenar la información del maestro actual
        maestro = {}
        nombre_maestro = input("Dame el nombre del maestro: ")
        maestro["nombre"] = nombre_maestro
        materias = []
        op_materias = 1
        while op_materias == 1:
            materia = input("Nombre de la materia que cursa: ")
            materias.append(materia)
            op_materias = int(input("1- Agregar más materias\n2- Continuar\nOpción: "))
        horario_profe_inicio = int(input("¿A qué hora ENTRA a trabajar este profesor? (hrs): "))
        horario_profe_fin = int(input("¿A qué hora SALE de trabajar este profesor? (hrs): "))
        maestro["horario"] = {
            "inicio": horario_profe_inicio,
            "fin": horario_profe_fin
        }
        maestro["materias"] = materias
        # Agregar el diccionario del maestro al diccionario de maestros con nombre como clave
        maestros[nombre_maestro] = maestro
        op = int(input("1- Agregar maestro\n2- Continuar\nOpción: "))

    # INICIAMOS ALGORITMO ABC
    abejas_exploradoras_n = 1  # Número de abejas exploradoras
    abejas_empleadas_n = 0     # Número inicial de abejas empleadas
    dias = 1000                   # Número máximo de iteraciones del algoritmo
    dias_semana = 1
    dias_sin_mejora2 = 100

    abejas_exploradoras = []

    # GENERAR LA POBLACIÓN INICIAL
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
                
                # Verificar si el horario está disponible
                if horario not in horario_salon_ocupado[(salon, dia)]:
                    #70 porque son 14 horas por dia por 5 dias de la semana
                    abeja["puntuacion"] += 70
                    horario_salon_ocupado[(salon, dia)].add(horario)
    
    # EVALUAR NO SUPERPOSICIÓN DE HORARIOS ENTRE PROFESORES
    for abeja in abejas_exploradoras:
        horario_profesor_ocupado = {}  # Diccionario para verificar la disponibilidad del horario de cada profesor
        
        for maestro in abeja["horarios"]:
            profesor = maestro["maestro"]
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

    # RESTAR PUNTOS POR DIFERENCIA DE HORAS ENTRE CLASES Y DÍAS DIFERENTES
    for abeja in abejas_exploradoras:
        for maestro in abeja["horarios"]:
            profesor = maestro["maestro"]
            dias_ocupados = set()
            for dia, horarios in horario_profesor_ocupado[profesor].items():
                dias_ocupados.add(dia)
                horarios = sorted(horarios)
                for i in range(len(horarios) - 1):
                    diferencia_horas = horarios[i + 1] - horarios[i]
                    abeja["puntuacion"] -= diferencia_horas
            
            # Restar puntos por cada día diferente que el profesor tenga una clase
            abeja["puntuacion"] -= len(dias_ocupados) * 3

    # ORDENAR ABEJAS POR PUNTUACIÓN
    abejas_exploradoras.sort(key=lambda x: x["puntuacion"], reverse=True)

    # Crear abejas empleadas basadas en la mejor puntuación
    mejor_puntuacion = abejas_exploradoras[0]["puntuacion"]
    abejas_empleadas = []

    for abeja in abejas_exploradoras:
        if abeja["puntuacion"] == mejor_puntuacion:
            abejas_empleadas.append(abeja.copy())  # Agrega copia de la abeja a abejas_empleadas
            abejas_empleadas_n += 1
            abejas_exploradoras_n -= 1

    # Iniciar el ciclo evolutivo
    iteracion = 0
    mejor_puntuacion_actual = mejor_puntuacion
    dias_sin_mejora = 0

    while iteracion < dias and dias_sin_mejora < dias_sin_mejora2:
        iteracion += 1
        print(f"\nIteración {iteracion}:")

        # Generar nuevos horarios para las abejas empleadas
        for abeja in abejas_empleadas:
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

                    if (salon, dia) not in horario_salon_ocupado:
                        horario_salon_ocupado[(salon, dia)] = set()

                    # Verificar si el horario está disponible
                    if horario not in horario_salon_ocupado[(salon, dia)]:
                        nueva_puntuacion += 70
                        #horario_salon_ocupado[(salon, dia)].add(horario)

                profesor = maestro_info["maestro"]
                if profesor not in horario_profesor_ocupado:
                    horario_profesor_ocupado[profesor] = {}
                for materia in horarios_materias_nuevos:
                    horario = materia["horario"]
                    dia = materia["dia"]

                    if dia not in horario_profesor_ocupado[profesor]:
                        horario_profesor_ocupado[profesor][dia] = set()

                    # Verificar si el horario está disponible para el profesor
                    if horario not in horario_profesor_ocupado[profesor][dia]:
                        nueva_puntuacion += 70
                        #horario_profesor_ocupado[profesor][dia].add(horario)

                for dia, horarios in horario_profesor_ocupado[profesor].items():
                    horarios = sorted(horarios)
                    for i in range(len(horarios) - 1):
                        diferencia_horas = horarios[i + 1] - horarios[i]
                        nueva_puntuacion -= diferencia_horas

                dias_ocupados = set(horario_profesor_ocupado[profesor].keys())
                nueva_puntuacion -= len(dias_ocupados) * 3

                # Comparar puntuaciones y actualizar si es mejor
                print(nueva_puntuacion)
                print(abeja["puntuacion"])
                if nueva_puntuacion >= abeja["puntuacion"]:
                    abeja["puntuacion"] = nueva_puntuacion
                    abeja["horarios"] = [{"maestro": maestro_info["maestro"], "horarios_materias": horarios_materias_nuevos}]

                    print(f"Mejora encontrada en la Abeja Empleada {abejas_empleadas.index(abeja) + 1} en la Iteración {iteracion}.")

                    # Reiniciar contador de días sin mejora
                    dias_sin_mejora = 0
                else:
                    print("no hay mejora")
                    dias_sin_mejora += 1

        # Mostrar horarios actuales de todas las abejas empleadas
        # print("\nHorarios actuales de todas las Abejas Empleadas:")
        # for i, abeja in enumerate(abejas_empleadas):
        #     print(f"\nAbeja Empleada {i + 1}:")
        #     for maestro_info in abeja["horarios"]:
        #         print(f"Maestro: {maestro_info['maestro']}")
        #         for materia in maestro_info["horarios_materias"]:
        #             print(f"  Materia: {materia['materia']}, Horario: {materia['horario']}, Salón: {materia['salon']}, Día: {materia['dia']}")

    # Mostrar resultados finales
    print("\nResultados finales de las Abejas Empleadas:")
    for i, abeja in enumerate(abejas_empleadas):
        print(f"\nAbeja Empleada {i + 1}:")
        print(f"Puntuación: {abeja['puntuacion']}")
        for maestro_info in abeja["horarios"]:
            print(f"Maestro: {maestro_info['maestro']}")
            for materia in maestro_info["horarios_materias"]:
                print(f"  Materia: {materia['materia']}, Horario: {materia['horario']}:00 - {materia['horario'] + 1}:00, Salón: {materia['salon']}, Día: {imprimir_dia_semana(materia['dia'])}")

    # # Mostrar resultados finales
    # print("\nResultados finales de las Abejas Empleadas:")
    # for i, abeja in enumerate(abejas_empleadas):
    #     print(f"\nAbeja Empleada {i + 1}:")
    #     print(f"Puntuación: {abeja['puntuacion']}")
    #     print("Horarios:")
    #     print("Hora\tLunes\tMartes\tMiércoles\tJueves\tViernes")
    #     for hora in range(7, 18):
    #         print(f"{hora}:00", end='\t')
    #         for dia in range(1, 6):
    #             encontrado = False
    #             for maestro_info in abeja["horarios"]:
    #                 for materia in maestro_info["horarios_materias"]:
    #                     if materia["horario"] == hora and materia["dia"] == dia:
    #                         print(f"{maestro_info['maestro']} ({materia['materia']})", end='\t')
    #                         encontrado = True
    #                         break
    #                 if encontrado:
    #                     break
    #             if not encontrado:
    #                 print("-", end='\t')
    #         print()