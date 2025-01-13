import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from pathlib import Path

from scripts.graphics import create_results_table, plot_quality_comparison, plot_nodes_comparison, plot_time_comparison, \
    plot_quality_nodes_comparison
from scripts.paths import *
from scripts.results import *
from scripts.results import parse_results


def execute_problem(p_id: ProblemId):
    command = [
        "./downward/fast-downward.py", "--overall-time-limit", "1800", f"--sas-file", f"{p_id.output_path()}.sas",  p_id.domain_path(), p_id.problem_path(), "--search", p_id.search,
    ]

    if os.path.exists(p_id.output_path()):
        print(f"Output file {p_id.output_path()} already exists. Skipping problem...")
        return

    print(f"Executing ({p_id.search}): {' '.join(command)}")
    with open(p_id.output_path(), "w") as outfile:
        subprocess.run(command, stdout=outfile, stderr=subprocess.STDOUT)

def build():
    command = [
       "./downward/build.py"
    ]
    subprocess.run(command)

def create_directories():
    for algo in SEARCH_ALGORITHM:
        for k in K_BEST:
            for w in W_VALUE:
                os.makedirs(f"./output/{algo}([add()], w={w}, k_best={k})/{DOMAINS[0]}", exist_ok=True)
                os.makedirs(f"./output/{algo}([add()], w={w}, k_best={k})/{DOMAINS[1]}", exist_ok=True)
                # os.makedirs(f"./output/{algo}([add()], w={w}, k_best={k})/{DOMAINS[2]}", exist_ok=True)

def build_and_collect_problems():
    # build()  # Suponiendo que `build` está definido previamente
    problem_ids = []
    for i in range(8, 9):  # Bucle externo sobre los problemas (p1 a p10)
        for algo in SEARCH_ALGORITHM:
            for k in K_BEST:
                for w in W_VALUE:
                    problem_ids.append(ProblemId(algo, w, k, DOMAINS[0], f"p{i:02}"))
                    problem_ids.append(ProblemId(algo, w, k, DOMAINS[1], f"p{i:02}"))
                    # problem_ids.append(ProblemId(algo, w, k, DOMAINS[2], f"p{i:02}"))
    return problem_ids

def execute_problem_threaded(problem_id):
    execute_problem(problem_id)  # Suponiendo que `execute_problem` está definido previamente

if __name__ == "__main__":
    create_directories()
    problem_ids = build_and_collect_problems()

    # Ejecutar en múltiples hilos
    with ThreadPoolExecutor(max_workers=2) as executor:  # Puedes ajustar `max_workers` según tus necesidades
        futures = [executor.submit(execute_problem_threaded, problem_id) for problem_id in problem_ids]

        # Opcional: mostrar el progreso
        for future in as_completed(futures):
            try:
                future.result()  # Verifica si hay excepciones
            except Exception as e:
                print(f"Error ejecutando un problema: {e}")

    results = {
        w: [parse_results(problem) for problem in problem_ids if problem.domain == "transport" and w == problem.w and problem.name == "p08"]
        for w in W_VALUE
    }

    create_results_table(results)
    plot_quality_comparison(results)
    plot_nodes_comparison(results)
    plot_time_comparison(results)
    plot_quality_nodes_comparison(results)
