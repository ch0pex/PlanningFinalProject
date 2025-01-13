import os
from collections import defaultdict
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np

from scripts.paths import K_BEST


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
    bars1 = ax.bar(x - width, res_lama_first, width, label='astar(add())', color='royalblue', edgecolor='black', alpha=0.85)
    bars2 = ax.bar(x, res_seq_lama, width, label='astar(add(), k_best=2)', color='forestgreen', edgecolor='black', alpha=0.85)
    bars3 = ax.bar(x + width, res_opt, width, label='astar(add(), k_best=5)', color='indianred', edgecolor='black', alpha=0.85)

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
        'astar(add())': 'royalblue',
        'astar(add(), k_best=2)': 'forestgreen',
        'astar(add(), k_best=5)': 'indianred'
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


def create_results_table(results):
    """
    Crea e imprime con matplotlib una tabla que:
      - Tiene una fila por cada w.
      - Para cada k, se generan dos columnas: "Q(k)" y "N(k)".

    Además, añade una leyenda que indica que "Q" representa la calidad y "N" representa el número de nodos.

    :param results: diccionario en la forma:
        {
          w: [Results(w, k1), Results(w, k2), ...],
          ...
        }
    """
    # 1) Reorganizamos la información en un diccionario de la forma:
    #
    #     agrupados[w][k] = objeto Results
    #
    agrupados = defaultdict(dict)

    # Para recopilar todos los k que aparezcan
    all_ks = set()

    for w, results_list in results.items():
        for res_obj in results_list:
            # Aquí asumimos que res_obj.id tiene un atributo k
            k_value = res_obj.id.k
            agrupados[w][k_value] = res_obj
            all_ks.add(k_value)

    # Ordenamos la lista de k para que las columnas aparezcan en orden
    all_ks = sorted(all_ks)

    # 2) Construimos los encabezados.
    #    El primero será "W" y luego, para cada k, dos columnas: "Q(k)" y "N(k)".
    headers = ["W"]
    for k in all_ks:
        headers.append(f"Q(k={k})")
        headers.append(f"N(k={k})")

    # 3) Construimos las filas de la tabla:
    #    - una fila por cada w
    #    - en cada fila, para cada k, ponemos quality y nodes
    table_data = []
    for w in sorted(agrupados.keys()):
        row = [w]  # la primera celda de la fila
        for k in all_ks:
            res = agrupados[w].get(k, None)
            if res is not None:
                row.append(res.quality)
                row.append(res.nodes_count)
            else:
                # Si no hay resultado para ese k, dejamos la celda vacía
                row.append("")
                row.append("")
        table_data.append(row)

    # 4) Dibujamos la tabla con matplotlib
    # Ajustamos el tamaño de la figura según el número de columnas y filas
    fig_height = max(6, len(table_data) * 0.3)  # Ajusta la altura según las filas
    fig_width = max(8, len(headers) * 1.2)     # Ajusta el ancho según las columnas
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')  # ocultamos los ejes

    tabla = ax.table(
        cellText=table_data,
        colLabels=headers,
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)

    # 5) Añadimos la leyenda cerca de la tabla
    # Obtenemos la posición de la tabla para colocar la leyenda justo debajo
    # Usamos transformaciones de coordenadas para una posición relativa

    # Obtener los límites de la tabla
    tabla_pos = tabla.get_window_extent(renderer=fig.canvas.get_renderer())
    # Convertir los límites a coordenadas de la figura
    tabla_fig_coord = fig.transFigure.inverted().transform(tabla_pos)
    x_center = 0.5  # Centrado horizontalmente

    # Añadir la leyenda justo debajo de la tabla
    leyenda = "Leyenda: Q(k) = Calidad para k, N(k) = Número de nodos para k"
    # Ajustamos el parámetro y para que esté más cerca (por ejemplo, 0.02)
    plt.figtext(x_center, 0.02, leyenda, wrap=True, horizontalalignment='center', fontsize=12)

    # Ajustamos el layout para dejar espacio para la leyenda
    plt.tight_layout(rect=[0, 0.05, 1, 1])  # Reducimos el espacio inferior

    plt.show()

def plot_quality_comparison(results):
    """
    Crea una gráfica que compara los valores de Q para cada k y w.

    Parámetros:
        results (dict): Diccionario donde la clave es w y el valor es una lista de objetos Result.
                        Cada Result tiene .id.w, .id.k, .quality y .nodes_count.
    """
    # 1) Agrupar resultados por w y k
    agrupados = defaultdict(dict)  # agrupados[w][k] = Q
    all_ws = set()
    all_ks = set()

    for w, list_of_results in results.items():
        for res in list_of_results:
            k_val = res.id.k
            agrupados[w][k_val] = res.quality
            all_ws.add(w)
            all_ks.add(k_val)

    all_ws = sorted(all_ws)
    all_ks = sorted(all_ks)

    # 2) Crear la gráfica
    plt.figure(figsize=(10, 6))

    for w in all_ws:
        qs = [agrupados[w].get(k, None) for k in all_ks]
        plt.plot(all_ks, qs, marker='o', label=f'w={w}')

    plt.xlabel('K-best', fontsize=12)
    plt.ylabel('Plan cost', fontsize=12)
    plt.title('Resultados KWA*', fontsize=14)
    plt.legend(title='Valores de w')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(all_ks)  # Asegura que todos los valores de k se muestren en el eje X
    plt.tight_layout()
    plt.show()

def plot_nodes_comparison(results):
    """
    Crea una gráfica que compara los valores de Q para cada k y w.

    Parámetros:
        results (dict): Diccionario donde la clave es w y el valor es una lista de objetos Result.
                        Cada Result tiene .id.w, .id.k, .quality y .nodes_count.
    """
    # 1) Agrupar resultados por w y k
    agrupados = defaultdict(dict)  # agrupados[w][k] = Q
    all_ws = set()
    all_ks = set()

    for w, list_of_results in results.items():
        for res in list_of_results:
            k_val = res.id.k
            agrupados[w][k_val] = res.nodes_count
            all_ws.add(w)
            all_ks.add(k_val)

    all_ws = sorted(all_ws)
    all_ks = sorted(all_ks)

    # 2) Crear la gráfica
    plt.figure(figsize=(10, 6))

    for w in all_ws:
        qs = [agrupados[w].get(k, None) for k in all_ks]
        plt.plot(all_ks, qs, marker='o', label=f'w={w}')

    plt.xlabel('K-best', fontsize=12)
    plt.ylabel('Nodes generated', fontsize=12)
    plt.title('Resultados KWA*', fontsize=14)
    plt.legend(title='Valores de w')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(all_ks)  # Asegura que todos los valores de k se muestren en el eje X
    plt.tight_layout()
    plt.show()

def plot_time_comparison(results):
    """
    Crea una gráfica que compara los valores de Q para cada k y w.

    Parámetros:
        results (dict): Diccionario donde la clave es w y el valor es una lista de objetos Result.
                        Cada Result tiene .id.w, .id.k, .quality y .nodes_count.
    """
    # 1) Agrupar resultados por w y k
    agrupados = defaultdict(dict)  # agrupados[w][k] = Q
    all_ws = set()
    all_ks = set()

    for w, list_of_results in results.items():
        for res in list_of_results:
            k_val = res.id.k
            agrupados[w][k_val] = res.time
            all_ws.add(w)
            all_ks.add(k_val)

    all_ws = sorted(all_ws)
    all_ks = sorted(all_ks)

    # 2) Crear la gráfica
    plt.figure(figsize=(10, 6))

    for w in all_ws:
        qs = [agrupados[w].get(k, None) for k in all_ks]
        plt.plot(all_ks, qs, marker='o', label=f'w={w}')

    plt.xlabel('K-best', fontsize=12)
    plt.ylabel('Execution time', fontsize=12)
    plt.title('Resultados KWA*', fontsize=14)
    plt.legend(title='Valores de w')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(all_ks)  # Asegura que todos los valores de k se muestren en el eje X
    plt.tight_layout()
    plt.show()

def plot_quality_nodes_comparison(results):
    # Crear una gráfica con líneas por cada K-best, ordenando por calidad (Quality)
    plt.figure(figsize=(12, 8))
    colors = cycle(['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'brown'])

    for k_best in K_BEST:
        data_points = []
        for w, list_of_results in results.items():
            for res in list_of_results:
                if res.id.k == k_best:
                    data_points.append((res.quality, res.nodes_count))

        # Ordenar por calidad
        data_points = sorted(data_points)
        qualities, nodes_expanded = zip(*data_points) if data_points else ([], [])

        # Graficar línea para este K-best si hay datos
        if qualities and nodes_expanded:
            plt.plot(qualities, nodes_expanded, marker='o', label=f'K-best={k_best}', color=next(colors))

    plt.xlabel('Quality of Solution', fontsize=14)
    plt.ylabel('Nodes Expanded', fontsize=14)
    plt.yscale('log')
    plt.title('Quality vs Nodes Expanded', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='K-best Values', loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

