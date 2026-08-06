import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Assuming preprocessed OhioT1DM dataset is loaded
#data = pd.read_csv('ohioT1DM.csv')

# Exemplo de uso do ambiente
data = pd.DataFrame({
    'glucose': [180, 150, 110, 80, 140, 90],
    'carbs':   [45, 30, 25, 20, 50, 10],
    'time':    [2, 1.5, 1.0, 0.5, 2.5, 0.8]
})

# Define environment variables
states = data[['glucose', 'carbs', 'time']]  # Multi-dimensional state space
actions = np.linspace(0, 10, 21)  # Continuous insulin doses

# Build DQN model
def build_dqn_model():
    model = Sequential([
        Dense(24, input_dim=states.shape[1], activation='relu'),
        Dense(24, activation='relu'),
        Dense(len(actions), activation='linear')  # Output for each action
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# Hyperparameters
gamma = 0.95  # Discount factor
epsilon = 0.1  # Exploration rate
batch_size = 32
epochs = 1000

# Initialize the model
model = build_dqn_model()

# Experience replay buffer (to store past experiences)
experience_buffer = []

# Reward function
def reward(glucose):
    if 80 <= glucose <= 120:  # Target glucose range
        return 1
    else:
        return -1


def simulate_glucose_level(current_state, insulin_dose):
    # Unpack the current state variables
    glucose = current_state['glucose']  # Current glucose level in mg/dL
    carbs = current_state['carbs']  # Carbohydrate intake in grams
    time = current_state['time']  # Time since last insulin dose in hours
    
    # Parameters (you can adjust these based on your understanding of the system)
    carb_to_glucose_factor = 3  # How much glucose 1g of carbs increases glucose level (example)
    insulin_sensitivity = 15  # How much 1 unit of insulin decreases glucose (example)
    insulin_decay = np.exp(-0.1 * time)  # Exponential decay of insulin effect over time
    carb_metabolism_rate = np.exp(-0.05 * time)  # Decay rate of glucose increase over time
    
    # Calculate the effect of carbs on glucose level
    glucose_increase_from_carbs = carbs * carb_to_glucose_factor * carb_metabolism_rate
    
    # Calculate the effect of insulin on glucose level
    glucose_decrease_from_insulin = insulin_dose * insulin_sensitivity * insulin_decay
    
    # Update glucose level
    new_glucose = glucose + glucose_increase_from_carbs - glucose_decrease_from_insulin
    
    # Ensure glucose level is non-negative (physiologically realistic)
    new_glucose = abs(new_glucose.values[0])
    
    return new_glucose


# Training loop
for episode in range(epochs):
    current_state = states.sample() # Initial state

    for step in range(100):  # Steps per episode
        if np.random.rand() < epsilon:
            action = np.random.choice(actions)  # Random action
        else:
            q_values = model.predict(current_state.values.reshape(1,-1))  # Predict Q-values
            action = actions[np.argmax(q_values)]  # Best action

        # Simulate next state and reward
        glucose = simulate_glucose_level(current_state, action)
        reward_value = reward(glucose)

        new_state = {
            'glucose': glucose,
            'carbs': data['carbs'].sample().values[0],
            'time':  data['time'].sample().values[0]
        }
        new_state = pd.DataFrame([new_state], columns=current_state.columns)

        # Store experience
        experience_buffer.append((current_state, action, reward_value, new_state))

        # Update state
        current_state = new_state

        # Train DQN using a mini-batch from the experience buffer
        if len(experience_buffer) > batch_size:
            mini_batch = experience_buffer
            for state, action, reward_value, next_state in mini_batch:
                target = reward_value + gamma * np.max(model.predict(next_state.values.reshape(1, -1)))
                q_values = model.predict(state.values.reshape(1, -1))
                q_values[0, actions == action] = target
                model.fit(state.values.reshape(1, -1), q_values, epochs=1, verbose=0)
  


# Função de teste do desempenho do modelo
def test_model(model, episodes=10):
    total_rewards = []
    
    for episode in range(episodes):
        current_state = states.sample()  # Estado inicial aleatório
        episode_reward = 0
        
        for step in range(100):  # Passos por episódio
            q_values = model.predict(current_state.values.reshape(1, -1))  # Previsão dos valores Q
            action = actions[np.argmax(q_values)]  # Melhor ação
            
            # Simular o próximo estado e recompensa
            glucose = simulate_glucose_level(current_state, action)
            reward_value = reward(glucose)
            episode_reward += reward_value  # Acumular recompensa do episódio
            
            # Gerar o próximo estado
            new_state = {
                'glucose': glucose,
                'carbs': data['carbs'].sample().values[0],
                'time': data['time'].sample().values[0]
            }
            new_state = pd.DataFrame([new_state], columns=current_state.columns)

            # Atualizar o estado atual
            current_state = new_state
        
        # Armazenar a recompensa total do episódio
        total_rewards.append(episode_reward)
    
    # Calcular a média de recompensas ao final dos episódios de teste
    average_reward = np.mean(total_rewards)
    print(f"Média de recompensas por episódio nos testes: {average_reward}")
    return total_rewards

# Testar o modelo após o treinamento
test_model(model, episodes=10)