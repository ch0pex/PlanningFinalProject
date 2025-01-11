import os

import matplotlib.pyplot as plt
import numpy as np
import results


def compare_results_2(res):
    problem_ids = [result.id.name for result in res]
    times = [result.time for result in res]
    lengths = [result.length for result in res]
    qualities = [result.quality for result in res]
    nodes = [result.nodes_count for result in res]

    # Configurar la posición de las barras en el eje x
    x = np.arange(len(problem_ids))  # La posición de cada problema
    width = 0.15  # Ancho de las barras

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(14, 8))

    # Graficar las barras de cada atributo
    ax.bar(x - 2 * width, times, width, label='Time', color='blue')
    ax.bar(x - width, lengths, width, label='Length', color='green')
    ax.bar(x, qualities, width, label='Quality', color='red')
    ax.bar(x + width, nodes, width, label='Nodes', color='orange')

    # Configurar etiquetas y título
    ax.set_xlabel('Problem ID')
    ax.set_ylabel('Values')
    ax.set_title('Comparison of Attributes for 10 Problems')
    ax.set_xticks(x)
    ax.set_xticklabels(problem_ids)
    ax.legend()

    # Guardar la imagen a un archivo
    plt.tight_layout()
    plt.savefig('./results/comparison_chart.png')  # Cambia el nombre de archivo si es necesario


def compare_field(domain, field, res_lama_first, res_seq_lama, res_opt, logaritmic = False):
    # Datos del eje x
    problem_ids = [f"p{i:02}" for i in range(1, 11)]
    x = np.arange(len(problem_ids))  # Posiciones de los grupos
    width = 0.25  # Ancho de las barras (más estrecho para evitar superposiciones)

    # Crear la figura y los ejes con un diseño más limpio
    fig, ax = plt.subplots(figsize=(12, 6))

    # Crear barras con colores y bordes mejorados
    bars1 = ax.bar(x - width, res_lama_first, width, label='lama-first', color='royalblue', edgecolor='black', alpha=0.85)
    bars2 = ax.bar(x, res_seq_lama, width, label='seq-sat-lama-2011', color='forestgreen', edgecolor='black', alpha=0.85)
    bars3 = ax.bar(x + width, res_opt, width, label='seq-opt-fdss-1', color='indianred', edgecolor='black', alpha=0.85)

    # Añadir texto sobre cada barra con diseño ajustado
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Posición x
                height,   # Posición y (ligeramente por encima)
                f'{height:.2f}' if (height < 1 and height != 0) else f'{height:.0f}',  # Texto con 1 decimal o sin decimales
                ha='center', va='bottom', fontsize=7, color='black', fontweight='bold'  # Estilo del texto
            )

    # Mejorar etiquetas y título
    ax.set_title(f'{field} {domain}', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel(field, fontsize=12, fontweight='bold', labelpad=15)
    ax.set_xlabel('Problem ID', fontsize=12, fontweight='bold', labelpad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(problem_ids, fontsize=10)
    ax.legend(fontsize=10, loc='upper left', frameon=True, shadow=True)

    if logaritmic:
        ax.set_yscale('log')

    # Ajustar el diseño del gráfico
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Líneas de cuadrícula en el eje Y
    ax.spines['top'].set_visible(False)  # Ocultar borde superior
    ax.spines['right'].set_visible(False)  # Ocultar borde derecho
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Espacio para evitar que los números o etiquetas se corten
    plt.tight_layout(pad=2.0)

    # Guardar gráfico
    file_name = f'./results/{domain}-{field}.png'
    plt.savefig(file_name, dpi=300)

def compare_field_single(domain, field, method_name, results):
    # Datos del eje x
    problem_ids = [f"p{i:02}" for i in range(1, 11)]
    x = np.arange(len(problem_ids))  # Posiciones de los problemas

    # Crear la figura y el eje con un diseño más limpio
    fig, ax = plt.subplots(figsize=(10, 5))

    # Colores específicos para cada método
    color_map = {
        'lama-first': 'royalblue',
        'seq-sat-lama-2011': 'forestgreen',
        'seq-opt-fdss-1': 'indianred'
    }
    color = color_map.get(method_name, 'gray')  # Color por defecto en caso de nombre desconocido

    # Crear barras con bordes mejorados
    bars = ax.bar(x, results, width=0.5, label=method_name, color=color, edgecolor='black', alpha=0.85)

    # Añadir texto sobre cada barra con diseño ajustado
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # Posición x
            height + min(height * 0.02, 2),  # Posición y (ligeramente por encima)
            f'{height:.2f}' if height % 1 != 0 else f'{height:.0f}',
            ha='center', va='bottom', fontsize=8, color='black', fontweight='bold'  # Estilo del texto
        )

    # Mejorar etiquetas y título
    ax.set_title(f'{field} - {method_name} {domain}', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel(field, fontsize=12, fontweight='bold', labelpad=15)
    ax.set_xlabel('Problem ID', fontsize=12, fontweight='bold', labelpad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(problem_ids, fontsize=10)
    # ax.legend(fontsize=10, loc='upper left', frameon=True, shadow=True)

    # Ajustar el diseño del gráfico
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Líneas de cuadrícula en el eje Y
    ax.spines['top'].set_visible(False)  # Ocultar borde superior
    ax.spines['right'].set_visible(False)  # Ocultar borde derecho
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Espacio para evitar que los números o etiquetas se corten
    plt.tight_layout()

    # Guardar gráfico
    file_name = f'./results/{domain}-{field}-{method_name}.png'
    plt.savefig(file_name, dpi=300)

def coverage():
    planners = ['lama-first', 'seq-sat-lama-2011', 'seq-opt-fdss-1']
    domains = ['Elevators', 'Transport']
    values = {
        'lama-first': [10, 10],  # Valores ficticios para Domain 1 y Domain 2
        'seq-sat-lama-2011': [10, 10],
        'seq-opt-fdss-1': [8, 5],
    }

    x = np.arange(len(planners))  # Posiciones para los planificadores
    width = 0.35  # Ancho de las barras

    fig, ax = plt.subplots(figsize=(8, 6))

    # Dibujar barras para cada dominio
    bars1 = ax.bar(x - width / 2, [values[planner][0] for planner in planners], width, label=domains[0], color='royalblue', edgecolor="black")
    bars2 = ax.bar(x + width / 2, [values[planner][1] for planner in planners], width, label=domains[1], color='indianred', edgecolor="black")

    # Etiquetas y formato
    y_ticks = np.arange(0, 11, 1)
    ax.set_xlabel('Planners')
    ax.set_ylabel('Solutions')
    ax.set_title('Coverage')
    ax.set_xticks(x)
    ax.set_xticklabels(planners)
    ax.set_yticks(y_ticks)
    ax.legend()

    # Añadir los valores encima de las barras
    def add_bar_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2, height , f'{height}', ha='center', va='bottom'
            )

    add_bar_labels(bars1)
    add_bar_labels(bars2)

    # Mostrar gráfica
    plt.tight_layout()

    file_name = f'./results/coverage.png'
    plt.savefig(file_name, dpi=300)
