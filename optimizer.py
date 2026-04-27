from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def optimize_tasks(tasks, available_time, energy_limit, w1, w2, w3):

    model = LpProblem(name="decision-autopilot", sense=LpMaximize)

    x = [LpVariable(f"x_{i}", cat="Binary") for i in range(len(tasks))]

    # Objective
    model += lpSum(
        (w1 * tasks[i]["priority"] +
         w2 * tasks[i]["regret"] -
         w3 * tasks[i]["energy"]) * x[i]
        for i in range(len(tasks))
    )

    # Constraints
    model += lpSum(tasks[i]["time"] * x[i] for i in range(len(tasks))) <= available_time
    model += lpSum(tasks[i]["energy"] * x[i] for i in range(len(tasks))) <= energy_limit

    model.solve()

    selected, rejected = [], []

    for i in range(len(tasks)):

        score = (w1 * tasks[i]["priority"] +
                 w2 * tasks[i]["regret"] -
                 w3 * tasks[i]["energy"])

        task_data = tasks[i].copy()
        task_data["score"] = round(score, 2)

        if x[i].value() == 1:
            selected.append(task_data)
        else:
            rejected.append(task_data)

    return selected, rejected
