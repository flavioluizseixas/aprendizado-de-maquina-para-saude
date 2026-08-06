import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random

# Exemplo de dados do ambiente
data = pd.DataFrame({
    'glucose': [180, 150, 110, 80, 140, 90],
    'carbs':   [45, 30, 25, 20, 50, 10],
    'time':    [2, 1.5, 1.0, 0.5, 2.5, 0.8]
})

# Definindo variáveis do ambiente
states = data[['glucose', 'carbs', 'time']]  # Espaço de estado multidimensional
actions = np.linspace(0, 10, 21)  # Doses de insulina contínuas

# Construção do modelo DQN
def build_dqn_model():
    model = Sequential([
        Dense(24, input_dim=states.shape[1], activation='relu'),
        Dense(24, activation='relu'),
        Dense(len(actions), activation='linear')  # Saída para cada ação
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# Hiperparâmetros
gamma = 0.95  # Fator de desconto
epsilon = 1.0  # Taxa de exploração inicial
epsilon_min = 0.01  # Valor mínimo de epsilon
epsilon_decay = 0.995  # Decaimento de epsilon
batch_size = 32
epochs = 1000
max_buffer_size = 1000  # Limite do buffer de experiências

# Inicializando o modelo
model = build_dqn_model()

# Buffer de experiência
experience_buffer = []

# Função de recompensa
def reward(glucose):
    if 80 <= glucose <= 120:  # Faixa alvo de glicose
        return 1
    else:
        return -1

# Função para simular o nível de glicose
def simulate_glucose_level(current_state, insulin_dose):
    glucose = current_state['glucose'].values[0]  # Nível de glicose atual em mg/dL
    carbs = current_state['carbs'].values[0]  # Consumo de carboidratos em gramas
    time = current_state['time'].values[0]  # Tempo desde a última dose de insulina em horas
    
    # Parâmetros de simulação
    carb_to_glucose_factor = 3  # Quanto 1g de carboidrato aumenta o nível de glicose
    insulin_sensitivity = 15  # Quanto 1 unidade de insulina diminui o nível de glicose
    insulin_decay = np.exp(-0.1 * time)  # Decaimento exponencial da insulina ao longo do tempo
    carb_metabolism_rate = np.exp(-0.05 * time)  # Taxa de decaimento do aumento de glicose ao longo do tempo
    
    # Efeito dos carboidratos no nível de glicose
    glucose_increase_from_carbs = carbs * carb_to_glucose_factor * carb_metabolism_rate
    
    # Efeito da insulina no nível de glicose
    glucose_decrease_from_insulin = insulin_dose * insulin_sensitivity * insulin_decay
    
    # Atualiza o nível de glicose
    new_glucose = glucose + glucose_increase_from_carbs - glucose_decrease_from_insulin
    
    # Garante que o nível de glicose não seja negativo
    new_glucose = max(0, new_glucose)
    
    return new_glucose

# Função para atualizar o epsilon (estratégia de exploração)
def update_epsilon(epsilon):
    return max(epsilon_min, epsilon * epsilon_decay)

# Função para treinar o DQN
def train_dqn(experience_buffer, model, batch_size):
    mini_batch = random.sample(experience_buffer, batch_size)
    
    for state, action, reward_value, next_state in mini_batch:
        target = reward_value
        if len(next_state) > 0:  # Se não for o estado final
            target += gamma * np.max(model.predict(next_state.values.reshape(1, -1), verbose=0))
        
        q_values = model.predict(state.values.reshape(1, -1), verbose=0)
        q_values[0, actions == action] = target
        
        model.fit(state.values.reshape(1, -1), q_values, epochs=1, verbose=0)

# Loop de treinamento
for episode in range(epochs):
    # Imprime o número do episódio
    print(f"Episode {episode + 1}/{epochs}")

    current_state = states.sample()  # Estado inicial

    for step in range(100):  # Passos por episódio
        if np.random.rand() < epsilon:
            action = np.random.choice(actions)  # Ação aleatória (exploração)
        else:
            q_values = model.predict(current_state.values.reshape(1, -1), verbose=0)  # Predição de Q-valores
            action = actions[np.argmax(q_values)]  # Melhor ação (exploração)
        
        # Simula o próximo estado e a recompensa
        glucose = simulate_glucose_level(current_state, action)
        reward_value = reward(glucose)
        
        new_state = {
            'glucose': glucose,
            'carbs': data['carbs'].sample().values[0],
            'time':  data['time'].sample().values[0]
        }
        new_state = pd.DataFrame([new_state], columns=current_state.columns)

        # Armazena a experiência no buffer
        experience_buffer.append((current_state, action, reward_value, new_state))
        
        # Limita o tamanho do buffer de experiência
        if len(experience_buffer) > max_buffer_size:
            experience_buffer.pop(0)

        # Atualiza o estado atual
        current_state = new_state

        # Treina o DQN usando mini-batch do buffer de experiência
        if len(experience_buffer) > batch_size:
            train_dqn(experience_buffer, model, batch_size)
    
    # Atualiza o epsilon
    epsilon = update_epsilon(epsilon)