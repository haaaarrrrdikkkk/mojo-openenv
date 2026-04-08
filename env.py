# env.py

from typing import List, Tuple, Dict
from pydantic import BaseModel, Field
import copy


# ---------------- MODELS ---------------- #

class Task(BaseModel):
    name: str
    type: str  # learning / health / social
    urgency: int = Field(ge=1, le=10)
    progress: int = Field(ge=0, le=100)
    deadline: int = Field(ge=0)


class Observation(BaseModel):
    time: int
    energy: int
    stress: int
    mood: str
    tasks: List[Task]


class Action(BaseModel):
    action: str


class Reward(BaseModel):
    value: float


# ---------------- ENVIRONMENT ---------------- #

class MojoEnv:
    def __init__(self):
        self.initial_state = {}
        self.current_state = {}
        self.done = False
        self.total_reward = 0.0
        self.history = []

    # ---------------- RESET ---------------- #
    def reset(self) -> Observation:
        self.initial_state = {
            "time": 8,
            "energy": 60,
            "stress": 30,
            "mood": "neutral",
            "tasks": [
                Task(name="Learn Skills", type="learning", urgency=7, progress=20, deadline=5),
                Task(name="Gym Workout", type="health", urgency=6, progress=10, deadline=4),
                Task(name="Networking", type="social", urgency=5, progress=30, deadline=6),
            ]
        }

        self.current_state = copy.deepcopy(self.initial_state)
        self.done = False
        self.total_reward = 0.0
        self.history = []

        return self._get_observation()

    # ---------------- STATE ---------------- #
    def state(self) -> Dict:
        return copy.deepcopy(self.current_state)

    # ---------------- STEP ---------------- #
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
        if self.done:
            return self._get_observation(), Reward(value=0.0), True, {}

        act = action.action.strip().lower()
        reward_value = 0.0

        # anti-repeat penalty
        if self.history and self.history[-1] == act:
            reward_value -= 0.2

        self.history.append(act)

        reward_value += self._apply_action(act)

        # time progression
        self.current_state["time"] += 1

        # deadlines
        reward_value += self._update_deadlines()

        # normalize
        self._normalize_state()

        # end condition
        if self.current_state["time"] >= 34:
            self.done = True

        self.total_reward += reward_value

        return self._get_observation(), Reward(value=reward_value), self.done, {}

    # ---------------- ACTION LOGIC ---------------- #
    def _apply_action(self, act: str) -> float:
        s = self.current_state
        reward = 0.0

        if act == "learn_skill":
            task = next((t for t in s["tasks"] if t.type == "learning"), None)
            if task:
                gain = 30 if s["energy"] > 20 else 15
                task.progress = min(100, task.progress + gain)
                s["energy"] -= 15
                s["stress"] += 5
                reward += 0.5
            else:
                reward -= 1.0

        elif act == "workout":
            task = next((t for t in s["tasks"] if t.type == "health"), None)
            if task:
                task.progress = min(100, task.progress + 25)
                s["energy"] -= 15
                s["stress"] -= 10
                reward += 0.4
            else:
                reward -= 1.0

        elif act == "socialize":
            task = next((t for t in s["tasks"] if t.type == "social"), None)
            if task:
                task.progress = min(100, task.progress + 20)
                s["energy"] -= 10
                s["stress"] -= 8
                reward += 0.3
            else:
                reward -= 1.0

        elif act == "rest":
            s["energy"] += 15
            s["stress"] -= 10
            reward += 0.2

        elif act == "sleep":
            s["energy"] += 40
            s["stress"] -= 15
            self.current_state["time"] += 5
            reward += 0.4

        elif act == "scroll_social_media":
            s["energy"] -= 5
            s["stress"] -= 2
            reward -= 0.3

        else:
            reward -= 1.0

        return reward

    # ---------------- DEADLINES ---------------- #
    def _update_deadlines(self) -> float:
        penalty = 0.0
        for task in self.current_state["tasks"]:
            task.deadline -= 1
            if task.deadline < 0 and task.progress < 100:
                penalty -= 0.5
        return penalty

    # ---------------- NORMALIZATION ---------------- #
    def _normalize_state(self):
        s = self.current_state

        s["energy"] = max(0, min(100, s["energy"]))
        s["stress"] = max(0, min(100, s["stress"]))

        if s["energy"] == 0:
            s["mood"] = "exhausted"
        elif s["stress"] > 70:
            s["mood"] = "overwhelmed"
        else:
            s["mood"] = "normal"

    # ---------------- OBSERVATION ---------------- #
    def _get_observation(self) -> Observation:
        s = self.current_state

        return Observation(
            time=s["time"],
            energy=s["energy"],
            stress=s["stress"],
            mood=s["mood"],
            tasks=s["tasks"]
        )