import gym
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque

# Definir o ambiente simulado
class DiabetesEnv(gym.Env):
    def __init__(self):
        super(DiabetesEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(3)  # 3 ações: "Aumentar Insulina", "Diminuir Insulina", "Não Fazer Nada"
        self.observation_space = gym.spaces.Box(low=70, high=200, shape=(1,), dtype=np.float32)  # Glicose
        self.state = np.array([100], dtype=np.float32)  # Estado inicial (glicose normal)
        self.target_range = [80, 130]  # Faixa saudável de glicose

    def step(self, action):
        # Simula o efeito da ação sobre os níveis de glicose
        if action == 0:  # Aumentar insulina
            self.state[0] -= random.uniform(10, 20)  # Reduz a glicose
        elif action == 1:  # Diminuir insulina
            self.state[0] += random.uniform(5, 15)  # Aumenta a glicose
        elif action == 2:  # Não fazer nada
            self.state[0] += random.uniform(-5, 5)  # Flutuação aleatória

        done = bool(self.state[0] < 70 or self.state[0] > 200)  # Termina se sair dos limites
        reward = -1 if not (self.target_range[0] <= self.state[0] <= self.target_range[1]) else 1  # Recompensa
        return self.state, reward, done, {}

    def reset(self):
        self.state = np.array([100], dtype=np.float32)  # Reset para o estado inicial
        return self.state

    def render(self, mode='human'):
        pass

# Rede Neural para o DDQN
def build_model(input_shape, action_space):
    model = tf.keras.Sequential()
    model.add(layers.Input(shape=input_shape))  # Adiciona a camada de entrada corretamente
    model.add(layers.Dense(24, activation='relu'))
    model.add(layers.Dense(24, activation='relu'))
    model.add(layers.Dense(action_space, activation='linear'))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')  # Corrige o parâmetro para 'learning_rate'
    return model

class DDQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # fator de desconto
        self.epsilon = 1.0  # Taxa de exploração
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = build_model((state_size,), action_size)  # Rede Neural principal
        self.target_model = build_model((state_size,), action_size)  # Rede Neural alvo
        self.update_target_model()

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                # Double DQN
                a = np.argmax(self.model.predict(next_state)[0])
                target[0][action] = reward + self.gamma * self.target_model.predict(next_state)[0][a]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Parâmetros
env = DiabetesEnv()
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DDQNAgent(state_size, action_size)
episodes = 1000
batch_size = 32

# Loop de treino
for e in range(episodes):
    state = env.reset()
    state = np.reshape(state, [1, state_size])

    for time in range(500):
        action = agent.act(state)  # Escolher ação
        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        if done:
            agent.update_target_model()  # Atualiza a rede alvo
            print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
            break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)