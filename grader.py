# grader.py

def grade(env):
    state = env.state()
    tasks = state["tasks"]

    # ---------------- TASK PROGRESS SCORE ---------------- #
    total_progress = sum(task.progress for task in tasks)
    max_progress = 100 * len(tasks)

    progress_score = total_progress / max_progress  # normalized (0–1)

    # ---------------- STRESS PENALTY ---------------- #
    stress_penalty = 0.0
    if state["stress"] > 80:
        stress_penalty = 0.1
    elif state["stress"] > 60:
        stress_penalty = 0.05

    # ---------------- ENERGY PENALTY ---------------- #
    energy_penalty = 0.0
    if state["energy"] == 0:
        energy_penalty = 0.1
    elif state["energy"] < 20:
        energy_penalty = 0.05

    # ---------------- BALANCE BONUS ---------------- #
    completed_tasks = sum(1 for t in tasks if t.progress >= 50)

    balance_bonus = 0.0
    if completed_tasks >= 2:
        balance_bonus = 0.15
    elif completed_tasks == 1:
        balance_bonus = 0.05

    # ---------------- FINAL SCORE ---------------- #
    score = progress_score + balance_bonus - stress_penalty - energy_penalty

    # Clamp between 0 and 1
    score = max(0.0, min(1.0, score))

    return score