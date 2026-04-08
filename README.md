# 🧠 Mojo Life Optimization Environment

## 📌 Overview

Mojo is a real-world simulation environment where an AI agent learns to manage a student's daily life effectively.

The agent must balance:
- 📚 Skill development
- 💪 Health & fitness
- 🤝 Social interactions

while optimizing:
- ⚡ Energy levels
- 🧠 Stress management
- ⏳ Time constraints

---

## 🎯 Objective

The goal is to design an environment where an agent can make sequential decisions to maximize productivity and well-being.

This environment emphasizes:
- Long-term planning
- Trade-offs between actions
- Realistic human constraints

---

## 🧱 Environment Design

### 🔹 State (Observation Space)

Each state includes:

- `time` → current time step  
- `energy` → agent stamina (0–100)  
- `stress` → mental load (0–100)  
- `mood` → qualitative state  
- `tasks` → list of tasks with:
  - name  
  - type (`learning`, `health`, `social`)  
  - urgency  
  - progress  
  - deadline  

---

### 🔹 Actions (Action Space)

The agent can choose:

- `learn_skill`
- `workout`
- `socialize`
- `rest`
- `sleep`
- `scroll_social_media`

---

### 🔹 Reward Function

The reward is designed to reflect realistic human outcomes:

✅ Positive signals:
- Task progress
- Balanced lifestyle
- Efficient time use

❌ Negative signals:
- Missed deadlines
- High stress
- Low energy
- Irrelevant actions

---

## 🧪 Tasks & Difficulty Levels

### 🟢 Easy
- Single-task optimization  
- Focus on skill development  

---

### 🟡 Medium
- Multi-task balancing  
- Requires managing energy and stress  

---

### 🔴 Hard
- High urgency + limited resources  
- Requires strategic decision-making  

---

## 📊 Evaluation

Each task is scored between:

0.0 - 1.0

Based on: 
- Task Completion
- Energy Management
- Stress Levels
- Balanced Performance

---

## Agent Design

A deterministic decision-making agent is ised to ensure:

- Reproducibility
- Stability
- Consistent Evaluation

The agent:
- Prioritizes hih-urgency tasks
- Adapts to energy and stress levels
- Balances learning, health, and social actions 

---

## How to Run

### Local Executuion

'''bash
python inference.py

Docker Execution:

docker build -t mojo-env .
docker run mojo-env

*KEY FEATURES*

1. Real world simulation(non-toy environment)
2. Multi-objective decision-making
3. Deterministic and reproducible evaluation
4. Dynamic task progression
5. Balanced reward system

*CONCLUSION*

Mojo demonstrates how AI agents can be evaluated in realistic environments involving human-like constraints.

The project highlights:

1. Decision-making under resouce limitations
2. Trade-offs between productivity and well-being
3. Scalable environment design for RL-style evaluation

*FUTURE IMPROVEMENTS*

1. Multi-agent interactions
2. Personalized user profiles
3. Adaptive difficulty scaling
4. Integration with real-world data

-------

