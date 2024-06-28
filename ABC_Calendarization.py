import random

if __name__ == "__main__":
    maestros = []
    op = 1
    salones_n = int(input("¿Cuantos salones hay?"))
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
        maestro["materias"] = materias
        horario_profe_inicio = input("¿A qué hora ENTRA a trabajar este profesor? (hrs): ")
        horario_profe_fin = input("¿A qué hora SALE de trabajar este profesor? (hrs): ")
        maestro["horario"] = {
            "inicio": horario_profe_inicio,
            "fin": horario_profe_fin
        }
        # Agregar el diccionario del maestro a la lista de maestros
        maestros.append(maestro)
        op = int(input("1- Agregar maestro\n2- Continuar\nOpción: "))
    
    #INICIAMOS ALGORITMO ABC
    abejas_observadoras_n = 20 #Primer parametro
    abejas_exploradoras_n = 5 #Segundo parametro
    abejas_empleadas_n = 0
    zonas_n = 0

    abejas_exploradoras = []
    
    for _ in range(abejas_exploradoras_n):
        abeja = []
        for maestro in maestros:
            horarios_materias = []
            for materia in maestro["materias"]:
                horario = random.randint(7, 21)  # Generar un horario aleatorio entre 7 y 21
                salon = random.randint(1, salones_n)  # Asignar un salón aleatorio entre 1 y salones_n
                horarios_materias.append({"materia": materia, "horario": horario, "salon": salon})
            abeja.append({"maestro": maestro["nombre"], "horarios_materias": horarios_materias})
        abejas_exploradoras.append(abeja)

    

    # # Imprimir la información de las abejas exploradoras
    # for i, abeja in enumerate(abejas_exploradoras):
    #     print(f"\nAbeja exploradora {i + 1}:")
    #     for maestro in abeja:
    #         print(f"Maestro: {maestro['maestro']}")
    #         for materia in maestro["horarios_materias"]:
    #             print(f"  Materia: {materia['materia']}, Horario: {materia['horario']}, Salón: {materia['salon']}")

    # # Imprimir la información de todos los maestros almacenados
    # for maestro in maestros:
    #     print(f"\nNombre del maestro: {maestro['nombre']}")
    #     print("Materias que cursa:")
    #     for materia in maestro["materias"]:
    #         print(f"- {materia}")
    #     print(f"Horario de trabajo: {maestro['horario']['inicio']} - {maestro['horario']['fin']}")