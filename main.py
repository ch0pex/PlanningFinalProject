import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from scripts.graphics import compare_field, compare_field_single, coverage
from scripts.paths import *
from scripts.results import *


def execute_problem(p_id: ProblemId):
    command = [
        "./downward/fast-downward.py", "--overall-time-limit", "1800", "--alias", p_id.planner,
        p_id.domain_path(), p_id.problem_path()
    ]

    if os.path.exists(p_id.output_path()):
        print(f"Output file {p_id.output_path()} already exists. Skipping problem...")
        return

    print(f"Executing ({p_id.planner}): {' '.join(command)}")
    with open(p_id.output_path(), "w") as outfile:
        subprocess.run(command, stdout=outfile, stderr=subprocess.STDOUT)

def build():
    command = [
       "./downward/build.py"
    ]
    subprocess.run(command)

if __name__ == "__main__":
    # Create directories
    os.makedirs(LAMA_FIRST_E, exist_ok=True)
    os.makedirs(LAMA_FIRST_T, exist_ok=True)
    os.makedirs(SEQ_SAT_LAMA_E, exist_ok=True)
    os.makedirs(SEQ_SAT_LAMA_T, exist_ok=True)
    os.makedirs(SEQ_OPT_FDSS_E, exist_ok=True)
    os.makedirs(SEQ_OPT_FDSS_T, exist_ok=True)

    build()
    # Problem names
    problem_ids = []
    for planner in PLANNERS:
        problem_ids.extend([ProblemId(planner, DOMAINS[0], f"p{i:02}") for i in range(1, 11)])
        problem_ids.extend([ProblemId(planner, DOMAINS[1], f"p{i:02}") for i in range(1, 11)])

    for problem_id in problem_ids:
        execute_problem(problem_id)

    # results = [parse_results(problem) for problem in problem_ids]
    results = {
        domain: {
            planner: [parse_results(problem) for problem in problem_ids if
                      problem.domain == domain and problem.planner == planner]
            for planner in PLANNERS
        }
        for domain in DOMAINS
    }

    for domain, planners in results.items():
        compare_field(domain, "Time(s)",
                      [result.time for result in planners[PLANNERS[0]]],
                      [result.time for result in planners[PLANNERS[1]]],
                      [result.time for result in planners[PLANNERS[2]]], True)
        compare_field(domain, "Length",
                      [result.length for result in planners[PLANNERS[0]]],
                      [result.length for result in planners[PLANNERS[1]]],
                      [result.length for result in planners[PLANNERS[2]]])
        compare_field(domain, "Quality",
                      [result.quality for result in planners[PLANNERS[0]]],
                      [result.quality for result in planners[PLANNERS[1]]],
                      [result.quality for result in planners[PLANNERS[2]]])
        compare_field(domain, "Nodes",
                      [result.nodes_count for result in planners[PLANNERS[0]]],
                      [result.nodes_count for result in planners[PLANNERS[1]]],
                      [result.nodes_count for result in planners[PLANNERS[2]]], True)
        
        # Graficar resultados para lama_first
        res_lama_first = [result.time for result in planners[PLANNERS[0]]]
        compare_field_single(domain, field="Time(s)", method_name="lama-first", results=res_lama_first)

        # Graficar resultados para seq_lama
        res_seq_lama = [result.time for result in planners[PLANNERS[1]]]
        compare_field_single(domain, field="Time(s)", method_name="seq-sat-lama-2011", results=res_seq_lama)

        # Graficar resultados para seq_opt
        res_opt = [result.time for result in planners[PLANNERS[2]]]
        compare_field_single(domain, field="Time(s)", method_name="seq-opt-fdss-1", results=res_opt)

    #Coverage graphic
    coverage()
    print("Finish")
