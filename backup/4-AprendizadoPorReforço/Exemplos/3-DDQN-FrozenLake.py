import numpy as np
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# Configurações
GAMMA = 0.99         # Fator de desconto
LR = 0.001           # Taxa de aprendizado
BATCH_SIZE = 64      # Tamanho do batch
MEMORY_SIZE = 10000  # Capacidade do replay buffer
TARGET_UPDATE = 10   # A cada quantos episódios a rede alvo será atualizada
EPS_START = 1.0      # Epsilon inicial (exploração)
EPS_END = 0.01       # Epsilon mínimo
EPS_DECAY = 0.995    # Decaimento do epsilon

# Definição da Rede Neural
class DQNetwork(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQNetwork, self).__init__()
        self.fc1 = nn.Linear(n_observations, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Função para converter estado em one-hot encoding
def one_hot_encode(state, n_states):
    one_hot = np.zeros(n_states)
    one_hot[state] = 1
    return one_hot

# Função para selecionar uma ação (epsilon-greedy)
def select_action(state, policy_net, epsilon, n_actions):
    if random.random() > epsilon:
        with torch.no_grad():
            return policy_net(state).argmax(dim=1).item()
    else:
        return random.randrange(n_actions)

# Replay buffer
class ReplayBuffer:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        transitions = random.sample(self.memory, batch_size)
        return zip(*transitions)

    def __len__(self):
        return len(self.memory)

# Função para treinar a rede principal
def optimize_model(memory, policy_net, target_net, optimizer):
    if len(memory) < BATCH_SIZE:
        return

    # Amostra batch do replay buffer
    transitions = memory.sample(BATCH_SIZE)
    states, actions, rewards, next_states, dones = transitions

    # Converte tudo em tensores
    states = torch.FloatTensor(np.vstack(states))  # Corrige para lidar com batches de estados
    actions = torch.LongTensor(actions).unsqueeze(1)
    rewards = torch.FloatTensor(rewards)
    next_states = torch.FloatTensor(np.vstack(next_states))  # Corrige para lidar com batches de estados
    dones = torch.FloatTensor(dones)

    # Previsões das ações atuais
    state_action_values = policy_net(states).gather(1, actions)

    # Calcula o valor Q esperado usando a rede alvo (Double DQN)
    next_state_actions = policy_net(next_states).argmax(dim=1, keepdim=True)
    next_state_values = target_net(next_states).gather(1, next_state_actions).squeeze(1)
    expected_state_action_values = rewards + (GAMMA * next_state_values * (1 - dones))

    # Calcula a perda
    loss = nn.functional.mse_loss(state_action_values.squeeze(1), expected_state_action_values)

    # Otimiza a rede
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Função principal de treinamento
def train_double_dqn(env, num_episodes=500):
    n_actions = env.action_space.n
    n_states = env.observation_space.n  # Total de estados (16 no caso do FrozenLake)

    # Redes e otimizador
    policy_net = DQNetwork(n_states, n_actions)
    target_net = DQNetwork(n_states, n_actions)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    memory = ReplayBuffer(MEMORY_SIZE)

    epsilon = EPS_START
    for episode in range(num_episodes):
        state, _ = env.reset()
        state = one_hot_encode(state, n_states)  # Converte o estado em one-hot encoding

        done = False
        total_reward = 0

        while not done:
            state_tensor = torch.FloatTensor([state])  # Converte para tensor para passar pela rede
            action = select_action(state_tensor, policy_net, epsilon, n_actions)
            next_state, reward, done, _, _ = env.step(action)
            next_state = one_hot_encode(next_state, n_states)  # Converte o próximo estado em one-hot encoding

            # Salva transição no buffer
            memory.push(state, action, reward, next_state, done)

            # Move para o próximo estado
            state = next_state
            total_reward += reward

            # Treina a rede
            optimize_model(memory, policy_net, target_net, optimizer)

        # Atualiza epsilon (para menos exploração ao longo do tempo)
        epsilon = max(EPS_END, EPS_DECAY * epsilon)

        # Atualiza a rede alvo periodicamente
        if episode % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())

        # Imprime progresso
        if episode % 10 == 0:
            print(f'Episódio {episode}, Recompensa Total: {total_reward}, Epsilon: {epsilon:.4f}')

    print("Treinamento Concluído!")

    # Exibe a Q-table após o treinamento
    display_q_table(policy_net, n_states, n_actions)


# Função para exibir a "Q-table"
def display_q_table(policy_net, n_states, n_actions):
    q_table = np.zeros((n_states, n_actions))  # Cria uma tabela de Q com zeros
    for state in range(n_states):
        state_tensor = torch.FloatTensor([one_hot_encode(state, n_states)])  # Codifica o estado em one-hot
        with torch.no_grad():
            q_values = policy_net(state_tensor)  # Obtém os valores de Q para o estado atual
        q_table[state] = q_values.numpy()  # Armazena os valores de Q na tabela
    print("\nQ-Table (valores de Q estimados):")
    print(q_table)


if __name__ == '__main__':
    env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=True)
    train_double_dqn(env)

