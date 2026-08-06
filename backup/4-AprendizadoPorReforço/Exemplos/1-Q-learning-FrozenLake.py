import numpy as np
import gymnasium as gym

def eps_greedy(Q, s, eps=0.1):
    '''
    Epsilon greedy policy
    '''
    if np.random.uniform(0, 1) < eps:
        # Escolhe uma ação aleatória
        return np.random.randint(Q.shape[1])
    else:
        # Escolhe a ação da política greedy
        return greedy(Q, s)


def greedy(Q, s):
    '''
    Greedy policy
    Retorna o índice correspondente ao maior valor de ação-estado
    '''
    return np.argmax(Q[s])


def run_episodes(env, Q, num_episodes=100, to_print=False):
    '''
    Roda alguns episódios para testar a política
    '''
    tot_rew = []
    state, _ = env.reset()

    for _ in range(num_episodes):
        done = False
        game_rew = 0

        while not done:
            # Seleciona uma ação greedy
            next_state, rew, done, _, _ = env.step(greedy(Q, state))

            state = next_state
            game_rew += rew
            if done:
                state, _ = env.reset()
                tot_rew.append(game_rew)

    if to_print:
        print(f'Mean score: {np.mean(tot_rew):.3f} of {num_episodes} games!')

    return np.mean(tot_rew)


def Q_learning(env, lr=0.01, num_episodes=10000, eps=0.2, gamma=0.95, eps_decay=0.00005):
    nA = env.action_space.n
    nS = env.observation_space.n

    # Inicializa a matriz Q
    Q = np.zeros((nS, nA))
    games_reward = []
    test_rewards = []

    for ep in range(num_episodes):
        state, _ = env.reset()
        done = False
        tot_rew = 0
        
        # Decai o valor de epsilon até atingir o limiar de 0.01
        if eps > 0.01:
            eps -= eps_decay

        # Loop principal até o ambiente parar
        while not done:
            # Seleciona uma ação usando a política eps-greedy
            action = eps_greedy(Q, state, eps)
            next_state, rew, done, _, _ = env.step(action)  # Executa um passo no ambiente

            # Atualização do Q-learning
            Q[state][action] = Q[state][action] + lr * (rew + gamma * np.max(Q[next_state]) - Q[state][action])

            state = next_state
            tot_rew += rew
            if done:
                games_reward.append(tot_rew)

        # Testa a política a cada 300 episódios e imprime os resultados
        if (ep % 300) == 0:
            test_rew = run_episodes(env, Q, 1000)
            print(f"Episode:{ep:5d}  Eps:{eps:.4f}  Rew:{test_rew:.4f}")
            test_rewards.append(test_rew)

    return Q


if __name__ == '__main__':
    #env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=True, render_mode='human')
    env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=True)
    
    # Definir uma semente para a geração de números aleatórios
    np.random.seed(42)
    Q_qlearning = Q_learning(env, lr=.1, num_episodes=5000, eps=0.4, gamma=0.95, eps_decay=0.0001)
    print(Q_qlearning)