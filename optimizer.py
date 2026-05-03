from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def optimize_tasks(tasks, available_time, energy_limit):

    model = LpProblem(name="decision-agent", sense=LpMaximize)

    # Decision variables
    x = [LpVariable(f"x_{i}", cat="Binary") for i in range(len(tasks))]

    # Objective function
    model += lpSum(
        (tasks[i]["priority"] + tasks[i]["regret"] - tasks[i]["energy"]) * x[i]
        for i in range(len(tasks))
    )

    # Constraints
    model += lpSum(tasks[i]["time"] * x[i] for i in range(len(tasks))) <= available_time
    model += lpSum(tasks[i]["energy"] * x[i] for i in range(len(tasks))) <= energy_limit

    # Solve
    model.solve()

    selected, rejected = [], []

    for i in range(len(tasks)):
        score = tasks[i]["priority"] + tasks[i]["regret"] - tasks[i]["energy"]

        task = tasks[i].copy()
        task["score"] = round(score, 2)

        if x[i].value() == 1:
            selected.append(task)
        else:
            rejected.append(task)

    return selected, rejected
