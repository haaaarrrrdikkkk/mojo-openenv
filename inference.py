# inference.py

import os
from openai import OpenAI

from env import MojoEnv, Action
from tasks import TASKS
from grader import grade


# ---------------- ENV VARIABLES ---------------- #
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")


# ---------------- SAFE CLIENT ---------------- #
client = None

if API_BASE_URL and HF_TOKEN:
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=HF_TOKEN
        )
    except Exception:
        client = None


# ---------------- ACTION SPACE ---------------- #
ACTIONS = [
    "learn_skill",
    "workout",
    "socialize",
    "rest",
    "sleep",
    "scroll_social_media"
]


# ---------------- AGENT ---------------- #
def get_action(observation):

    # -------- TRY API -------- #
    if client is not None:
        try:
            prompt = f"""
Choose best action from:
learn_skill, workout, socialize, rest, sleep, scroll_social_media

Energy: {observation.energy}
Stress: {observation.stress}
Tasks: {[(t.type, t.urgency) for t in observation.tasks]}
"""

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            action = response.choices[0].message.content.strip()

            if action in ACTIONS:
                return action

        except Exception:
            pass

    # -------- FALLBACK -------- #
    energy = observation.energy
    stress = observation.stress
    task = max(observation.tasks, key=lambda t: t.urgency)

    if energy < 25:
        return "sleep"

    if stress > 70:
        return "rest"

    return {
        "learning": "learn_skill",
        "health": "workout",
        "social": "socialize"
    }.get(task.type, "rest")


# ---------------- RUN ---------------- #
def run_all_tasks():
    results = {}

    for name, task_fn in TASKS.items():

        print("[START]")
        print(f"task={name}")

        env = task_fn()
        obs = env._get_observation()

        done = False
        step_count = 0

        while not done:
            action_str = get_action(obs)
            action = Action(action=action_str)

            obs, reward, done, _ = env.step(action)

            step_count += 1

            print(f"[STEP] step={step_count} action={action_str} reward={reward.value}")

        score = grade(env)
        results[name] = score

        print("[END]")
        print(f"score={score}")

    return results


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    final_scores = run_all_tasks()

    print("[END]")
    print(f"final_scores={final_scores}")