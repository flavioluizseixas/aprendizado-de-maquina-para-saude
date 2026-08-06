"""Ambiente didático de estoque e treinamento Q-learning tabular."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np
import pandas as pd


class DengueInventoryEnv:
    """Ambiente discreto de estoque baseado em demanda epidemiológica real.

    Os dados de demanda são reais; ações, estoque, custos e recompensas são uma
    simulação operacional simplificada, sem decisão clínica.
    """

    n_states = 9
    n_actions = 3

    def __init__(
        self,
        demand_series: Sequence[float],
        stock_levels: Sequence[float] | None = None,
        shortage_cost: float = 5.0,
        excess_cost: float = 1.0,
        operational_cost: float = 0.05,
        random_state: int = 42,
        demand_thresholds: Sequence[float] | None = None,
        trend_tolerance: float | None = None,
    ) -> None:
        demand = np.asarray(demand_series, dtype=float)
        if len(demand) < 3 or not np.isfinite(demand).all():
            raise ValueError("demand_series requer ao menos três valores finitos.")
        self.demand = demand
        thresholds = (
            np.quantile(demand, [1 / 3, 2 / 3])
            if demand_thresholds is None
            else np.asarray(demand_thresholds, dtype=float)
        )
        if len(thresholds) != 2:
            raise ValueError("demand_thresholds deve conter dois limites.")
        self.demand_thresholds = np.asarray(thresholds, dtype=float)
        self.trend_tolerance = (
            max(float(np.std(demand) * 0.05), 1e-9)
            if trend_tolerance is None
            else float(trend_tolerance)
        )
        if stock_levels is None:
            stock_levels = np.quantile(demand, [0.25, 0.5, 0.75])
        self.stock_levels = np.asarray(stock_levels, dtype=float)
        if len(self.stock_levels) != self.n_actions:
            raise ValueError("stock_levels deve conter três níveis.")
        self.shortage_cost = float(shortage_cost)
        self.excess_cost = float(excess_cost)
        self.operational_cost = float(operational_cost)
        self.rng = np.random.default_rng(random_state)
        self.index = 2

    def _state_at(self, index: int) -> int:
        """Codifica apenas demanda já observada antes da decisão de ``index``."""

        observed = max(1, min(index - 1, len(self.demand) - 1))
        demand_bin = int(np.digitize(self.demand[observed], self.demand_thresholds))
        delta = self.demand[observed] - self.demand[observed - 1]
        trend_bin = int(np.digitize(delta, [-self.trend_tolerance, self.trend_tolerance]))
        return demand_bin * 3 + trend_bin

    def reset(self) -> int:
        """Reinicia no segundo ponto, necessário para calcular a tendência."""

        self.index = 2
        return self._state_at(self.index)

    def step(self, action: int) -> tuple[int, float, bool, dict[str, float]]:
        """Aplica um nível de estoque e avança uma semana."""

        if action not in range(self.n_actions):
            raise ValueError("action deve ser 0, 1 ou 2.")
        stock = float(self.stock_levels[action])
        demand = float(self.demand[self.index])
        shortage = max(demand - stock, 0.0)
        excess = max(stock - demand, 0.0)
        operational = self.operational_cost * stock
        reward = -(
            self.shortage_cost * shortage + self.excess_cost * excess + operational
        )
        self.index += 1
        done = self.index >= len(self.demand)
        state_index = min(self.index, len(self.demand))
        info = {
            "demanda": demand,
            "estoque": stock,
            "falta": shortage,
            "excesso": excess,
            "custo_operacional": operational,
        }
        return self._state_at(state_index), float(reward), done, info


def train_q_learning(
    env: DengueInventoryEnv,
    episodes: int = 1_000,
    alpha: float = 0.1,
    gamma: float = 0.95,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    random_state: int = 42,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Treina Q-learning tabular com decaimento linear de epsilon."""

    if episodes <= 0:
        raise ValueError("episodes deve ser positivo.")
    rng = np.random.default_rng(random_state)
    q_table = np.zeros((env.n_states, env.n_actions), dtype=float)
    history = []
    for episode in range(episodes):
        fraction = episode / max(episodes - 1, 1)
        epsilon = epsilon_start + fraction * (epsilon_end - epsilon_start)
        state = env.reset()
        total_reward = 0.0
        done = False
        while not done:
            if rng.random() < epsilon:
                action = int(rng.integers(env.n_actions))
            else:
                action = int(np.argmax(q_table[state]))
            next_state, reward, done, _ = env.step(action)
            future = 0.0 if done else float(np.max(q_table[next_state]))
            q_table[state, action] += alpha * (
                reward + gamma * future - q_table[state, action]
            )
            state = next_state
            total_reward += reward
        history.append(
            {"episódio": episode + 1, "recompensa": total_reward, "epsilon": epsilon}
        )
    return q_table, pd.DataFrame(history)


def evaluate_policy(
    env: DengueInventoryEnv,
    policy: Callable[[int, DengueInventoryEnv], int] | Sequence[int],
) -> dict[str, float | int]:
    """Avalia uma política fixa em uma série sem aprender com o teste."""

    state = env.reset()
    totals = {"recompensa": 0.0, "falta": 0.0, "excesso": 0.0, "semanas_com_falta": 0}
    done = False
    while not done:
        action = int(policy(state, env) if callable(policy) else policy[state])
        state, reward, done, info = env.step(action)
        totals["recompensa"] += reward
        totals["falta"] += info["falta"]
        totals["excesso"] += info["excesso"]
        totals["semanas_com_falta"] += int(info["falta"] > 0)
    return totals
