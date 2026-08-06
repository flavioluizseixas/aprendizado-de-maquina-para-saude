import numpy as np

from src.reinforcement_env import DengueInventoryEnv, evaluate_policy, train_q_learning


def test_environment_transition_and_cost_components():
    env = DengueInventoryEnv(
        [10, 20, 30, 20],
        stock_levels=[10, 20, 30],
        shortage_cost=5,
        excess_cost=1,
        operational_cost=0,
    )
    state = env.reset()
    next_state, reward, done, info = env.step(0)
    assert 0 <= state < 9 and 0 <= next_state < 9
    assert reward == -100
    assert info["falta"] == 20
    assert done is False


def test_q_learning_shapes_and_policy_evaluation():
    demand = np.tile([10, 20, 30, 20], 3)
    env = DengueInventoryEnv(demand, stock_levels=[10, 20, 30])
    table, history = train_q_learning(env, episodes=5)
    assert table.shape == (9, 3)
    assert list(history.columns) == ["episódio", "recompensa", "epsilon"]
    totals = evaluate_policy(env, np.argmax(table, axis=1))
    assert totals["recompensa"] <= 0
