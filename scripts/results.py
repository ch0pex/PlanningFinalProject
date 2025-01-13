import re


class ProblemId:
    def __init__(self, algorithm, w_value, k_value, domain, name):
        self.search = f"{algorithm}([add()], w={w_value}, k_best={k_value})"
        self.domain = domain
        self.name = name
        self.k = k_value
        self.w = w_value
        self.algorithm = algorithm

    def output_path(self):
        return f"./output/{self.search}/{self.domain}/{self.name}.txt"

    def domain_path(self):
        return f"./{self.domain}/domain.pddl"

    def problem_path(self):
        return f"./{self.domain}/{self.name}.pddl"

    def __repr__(self):
        return (f"({self.search}, {self.domain}, {self.name})")


class Results:
    def __init__(self, problem_id: ProblemId, time, length, quality, nodes):
        self.id = problem_id
        self.time = time
        self.length = length
        self.quality = quality
        self.nodes_count = nodes

    def __repr__(self):
        return (f"Results for {self.id}: \nTime: {self.time},\n"
                f"Length: {self.length}\nQuality: {self.quality}\nNodes: {self.nodes_count})\n")


def parse_results(problem_id: ProblemId):
    with open(problem_id.output_path()) as f:
        file_content = f.read()

        match_time = re.findall(r'Total time: ([\d\.]+)', file_content)
        match_length = re.findall(r'Plan length: (\d+)', file_content)
        match_cost = re.findall(r'Plan cost: (\d+)', file_content)
        match_generated = re.findall(r'Generated ([\d]+) state', file_content)

        result = Results(
            problem_id=problem_id,  # El ID del problema podría extraerse de otra parte si es necesario
            time=float(match_time[-1]) if len(match_time) else 1800,
            length=int(match_length[-1]) if len(match_length) else 0,
            quality=int(match_cost[-1]) if len(match_cost) else 0,
            nodes=int(match_generated[-1]) if len(match_generated) else 0
        )

    return result
