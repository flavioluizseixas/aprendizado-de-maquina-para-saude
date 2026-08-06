import numpy as np
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# Definição da rede neural
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Replay buffer para armazenar as transições
class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size

    def add(self, experience):
        self.memory.append(experience)

    def sample(self):
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.tensor(np.vstack([e[0] for e in experiences]), dtype=torch.float32)
        actions = torch.tensor(np.vstack([e[1] for e in experiences]), dtype=torch.long)
        rewards = torch.tensor(np.vstack([e[2] for e in experiences]), dtype=torch.float32)
        next_states = torch.tensor(np.vstack([e[3] for e in experiences]), dtype=torch.float32)
        dones = torch.tensor(np.vstack([e[4] for e in experiences]).astype(np.uint8), dtype=torch.float32)

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        return len(self.memory)

# Função epsilon-greedy para seleção de ações
def eps_greedy_action(network, state, eps, action_size):
    if np.random.rand() < eps:
        return random.choice(np.arange(action_size))
    else:
        with torch.no_grad():
            state = torch.tensor(state, dtype=torch.float32)
            action_values = network(state)
            return np.argmax(action_values.numpy())

# Função de treinamento DQN
def dqn(env, state_size, action_size, lr=0.001, num_episodes=1000, gamma=0.99, eps=1.0, eps_min=0.01, eps_decay=0.995, buffer_size=10000, batch_size=64, tau=0.1):
    # Inicializa a rede Q e a rede target
    qnetwork_local = QNetwork(state_size, action_size)
    qnetwork_target = QNetwork(state_size, action_size)
    optimizer = optim.Adam(qnetwork_local.parameters(), lr=lr)
    
    # Replay buffer
    memory = ReplayBuffer(buffer_size, batch_size)

    scores = []
    epsilons = []
    for ep in range(num_episodes):
        state, _ = env.reset()
        state = np.identity(state_size)[state:state+1]  # Codificação one-hot do estado discreto
        done = False
        total_reward = 0

        while not done:
            # Seleciona uma ação
            action = eps_greedy_action(qnetwork_local, state, eps, action_size)
            
            # Realiza a ação no ambiente
            next_state, reward, done, _, _ = env.step(action)
            next_state = np.identity(state_size)[next_state:next_state+1]  # Codificação one-hot do próximo estado

            # Armazena a transição no replay buffer
            memory.add((state, action, reward, next_state, done))

            state = next_state
            total_reward += reward

            # Atualiza a rede neural com amostras do replay buffer
            if len(memory) > batch_size:
                experiences = memory.sample()
                states, actions, rewards, next_states, dones = experiences

                Q_targets_next = qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
                Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

                Q_expected = qnetwork_local(states).gather(1, actions)

                loss = nn.MSELoss()(Q_expected, Q_targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # Atualiza a rede target com uma média ponderada (soft update)
                for target_param, local_param in zip(qnetwork_target.parameters(), qnetwork_local.parameters()):
                    target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)

        # Decaimento do epsilon
        if eps > eps_min:
            eps *= eps_decay

        scores.append(total_reward)
        epsilons.append(eps)

        # Exibe os resultados a cada 100 episódios
        if ep % 100 == 0:
            print(f'Episode {ep}, Mean Reward: {np.mean(scores[-100:]):.2f}, Epsilon: {eps:.4f}')

    return qnetwork_local


def display_q_values(qnetwork_local, state_size, action_size):
    # Gera uma "tabela de Q" baseada nos estados do ambiente
    print("\nQ-Values for each state-action pair:")
    for state in range(state_size):
        state_input = np.identity(state_size)[state:state+1]  # Codificação one-hot do estado
        state_tensor = torch.FloatTensor(state_input)  # Converte o estado para tensor do PyTorch
        q_values = qnetwork_local(state_tensor)  # Calcula os Q-valores para esse estado
        print(f"State {state}: {q_values.detach().numpy()}")


if __name__ == '__main__':
    env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=True)

    # Tamanho dos estados e ações
    state_size = env.observation_space.n  # Estado é discreto, logo tem n possíveis estados
    action_size = env.action_space.n      # Número de ações possíveis
    
    # Rodando o treinamento do DQN
    Q_qlearning = dqn(env, state_size, action_size)

    # Exibe os valores de Q para todos os estados possíveis
    display_q_values(Q_qlearning, state_size, action_size)