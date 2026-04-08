# tasks.py

from env import MojoEnv


def easy_task():
    env = MojoEnv()
    env.reset()

    # only one task but ensure all types exist logically
    env.current_state["tasks"] = [
        env.current_state["tasks"][0]  # Python Learning only
    ]

    return env


def medium_task():
    env = MojoEnv()
    obs = env.reset()

    # Balanced tasks
    env.current_state["tasks"] = [
        env.current_state["tasks"][0],  # learning
        env.current_state["tasks"][1],  # fitness
    ]

    return env


def hard_task():
    env = MojoEnv()
    env.reset()

    # Full complexity + stress
    env.current_state["energy"] = 50
    env.current_state["stress"] = 60

    # Increase urgency to make decisions meaningful
    for task in env.current_state["tasks"]:
        task.urgency += 2
        

    return env


TASKS = {
    "easy": easy_task,
    "medium": medium_task,
    "hard": hard_task,
}