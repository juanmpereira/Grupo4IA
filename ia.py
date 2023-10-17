import random
import matplotlib.pyplot as plt

familias = ["Thalos", "Virens", "Auros"]
sellos = ["plata", "oro", "esmeralda"]

def aptitud(cromosoma):
    solucion_correcta = ["plata", "esmeralda", "oro"]
    aptitud = sum(1 for i, j in zip(cromosoma, solucion_correcta) if i == j) - sum(1 for i, j in zip(cromosoma, solucion_correcta) if i != j)
    return aptitud

def inicializar_poblacion(tamano_poblacion):
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = random.sample(sellos, len(sellos))
        poblacion.append(individuo)
    print("poblacion:")
    print(poblacion)
    return poblacion

def seleccion_torneo(poblacion, num_padres):
    padres = []
    for _ in range(num_padres):
        torneo = random.sample(poblacion, min(len(poblacion), 2))  # Ajuste aquí
        mejor = max(torneo, key=lambda x: aptitud(x))
        padres.append(mejor)
    return padres

def cruce(padres):
    punto_cruce = random.randint(1, len(sellos)-1)
    descendencia = []
    for i in range(0, len(padres), 2):
        hijo1 = padres[i][:punto_cruce] + padres[i+1][punto_cruce:]
        hijo2 = padres[i+1][:punto_cruce] + padres[i][punto_cruce:]
        descendencia.extend([hijo1, hijo2])
    return descendencia

def mutacion(descendencia, prob_mutacion):
    for i in range(len(descendencia)):
        if random.random() < prob_mutacion:
            punto_mutacion = random.randint(0, len(sellos)-1)
            descendencia[i][punto_mutacion] = random.choice(sellos)
    return descendencia


def algoritmo_genetico(tamano_poblacion, num_generaciones, prob_mutacion):
    poblacion = inicializar_poblacion(tamano_poblacion)
    mejores_soluciones = []
    aptitudes_generacion = [] 

    for generacion in range(num_generaciones):
        padres = seleccion_torneo(poblacion, num_padres=2)
        descendencia = cruce(padres)
        descendencia = mutacion(descendencia, prob_mutacion)
        poblacion = descendencia

        # Encontrar y registrar la mejor solución de esta generación
        mejor_individuo = max(poblacion, key=lambda x: aptitud(x))
        mejores_soluciones.append(mejor_individuo[:]) 

        # Registrar aptitud del mejor individuo
        aptitudes_generacion.append(aptitud(mejor_individuo))

        if aptitud(mejor_individuo) == len(sellos):
            return mejor_individuo, mejores_soluciones, aptitudes_generacion

    return None, mejores_soluciones, aptitudes_generacion


resultado, mejores_soluciones, aptitudes_generacion = algoritmo_genetico(tamano_poblacion=50, num_generaciones=1000, prob_mutacion=0.1)

# Imprimir resultado
if resultado is not None:
    print("Solución encontrada:", resultado)
else:
    print("No se encontró una solución en el número de generaciones especificado.")

# Generar gráfico de la evolución de aptitudes
"""
for generacion, solucion in enumerate(mejores_soluciones):
    print(f'Generación {generacion+1}: {solucion}')

    cantidades = [sellos.count(sello) for sello in solucion]

    # Agregar un pequeño valor para asegurarnos de que siempre haya una barra visible
    cantidades = [cant + 0.1 for cant in cantidades]

    colores = {'plata': 'silver', 'oro': 'gold', 'esmeralda': 'green'}

    colores_sellos = [colores[sello] for sello in solucion]

    plt.bar(familias, cantidades, color=colores_sellos)
    plt.xlabel('Familias')
    plt.ylabel('Sellos')
    plt.title(f'Sellos en la Generación {generacion+1}')
    plt.show()
"""
# Generar gráfico de aptitudes
plt.plot(range(1, len(aptitudes_generacion) + 1), aptitudes_generacion)
plt.xlabel('Generación')
plt.ylabel('Aptitud')
plt.title('Comportamiento de la Aptitud')
plt.show()