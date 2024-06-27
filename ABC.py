import numpy as np
import matplotlib.pyplot as plt

# Definición de la función de aptitud: Función de Ackley
def ackley(x):
    a = 20
    b = 0.2
    c = 2 * np.pi
    d = len(x)
    sum1 = np.sum(x ** 2)
    sum2 = np.sum(np.cos(c * x))
    term1 = -a * np.exp(-b * np.sqrt(sum1 / d))
    term2 = -np.exp(sum2 / d)
    return term1 + term2 + a + np.exp(1)

# Inicialización de parámetros
tamaño_población = 50
dim = 10
max_iteraciones = 1000
nep = 10
nsp = 10
sitios_elite = 3
mejores_sitios = 10
criterio_paro = 0.01

# Generar la población inicial de soluciones aleatorias
población = np.random.uniform(-32.768, 32.768, (tamaño_población, dim))

# Evaluación Inicial
aptitud = np.array([ackley(ind) for ind in población])

# Almacenar el mejor valor de aptitud en cada iteración
mejores_valores_aptitud = []

# Bucle Principal
for iteración in range(max_iteraciones):
    # Ordenar la Población
    índices_ordenados = np.argsort(aptitud)
    población = población[índices_ordenados]
    aptitud = aptitud[índices_ordenados]
    
    nueva_población = []

    # Búsqueda Intensiva en Sitios de Élites
    for i in range(sitios_elite):
        individuo_elite = población[i]
        for _ in range(nep):
            k = np.random.choice([j for j in range(tamaño_población) if j != i])
            phi = np.random.uniform(-1, 1, dim)
            nueva_solución = individuo_elite + phi * (individuo_elite - población[k])
            nueva_solución = np.clip(nueva_solución, -32.768, 32.768)
            nueva_aptitud = ackley(nueva_solución)
            if nueva_aptitud < aptitud[i]:
                población[i] = nueva_solución
                aptitud[i] = nueva_aptitud

    # Búsqueda en Mejores Sitios No Élites
    for i in range(sitios_elite, mejores_sitios):
        mejor_individuo = población[i]
        for _ in range(nsp):
            k = np.random.choice([j for j in range(tamaño_población) if j != i])
            phi = np.random.uniform(-1, 1, dim)
            nueva_solución = mejor_individuo + phi * (mejor_individuo - población[k])
            nueva_solución = np.clip(nueva_solución, -32.768, 32.768)
            nueva_aptitud = ackley(nueva_solución)
            if nueva_aptitud < aptitud[i]:
                población[i] = nueva_solución
                aptitud[i] = nueva_aptitud

    # Búsqueda Global
    for i in range(mejores_sitios, tamaño_población):
        nueva_solución = np.random.uniform(-32.768, 32.768, dim)
        población[i] = nueva_solución
        aptitud[i] = ackley(nueva_solución)

    # Reemplazo de la Población y Actualización del Mejor Resultado
    mejor_solución = población[np.argmin(aptitud)]
    mejor_aptitud = np.min(aptitud)

    # Almacenar el mejor valor de aptitud de esta iteración
    mejores_valores_aptitud.append(mejor_aptitud)

    print(f"Iteración {iteración + 1}: Mejor Aptitud = {mejor_aptitud}")

    # Criterio de parada
    if mejor_aptitud <= criterio_paro:
        print(f"Criterio de parada alcanzado en la iteración {iteración + 1}")
        break

# Graficar la convergencia
plt.figure(figsize=(10, 6))
plt.plot(mejores_valores_aptitud, label='Mejor Valor de Aptitud')
plt.xlabel('Iteración')
plt.ylabel('Mejor Aptitud')
plt.title('Curva de Convergencia')
plt.legend()
plt.grid(True)
plt.show()

print("Mejor Solución Encontrada: ", mejor_solución)
print("Mejor Valor de Aptitud: ", mejor_aptitud)
