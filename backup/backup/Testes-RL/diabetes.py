import gym
from gym import spaces
import numpy as np
import pandas as pd

class DiabetesEnv(gym.Env):
    def __init__(self, glucose_data):
        super(DiabetesEnv, self).__init__()
        # Espaço de ação: doses de insulina entre 0 e 10 unidades
        self.action_space = spaces.Discrete(11)  # 0 a 10 unidades
        # Espaço de observação: nível de glicose no sangue, carboidratos e dose anterior
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(3,), dtype=np.float32)
        self.state = None
        self.glucose_data = glucose_data
        self.current_step = 0
    
    def reset(self):
        # Resetar o ambiente (inicializar os estados)
        self.current_step = 0
        self.state = self.glucose_data.iloc[self.current_step, :3].values  # glucose, carbs, last insulin dose
        return self.state
    
    def step(self, action):
        # Aplicar ação (dose de insulina)
        dose = action
        
        # Atualizar o estado
        glucose_level = self.state[0] - (dose * 10)  # Exemplo simplificado de redução
        carb_intake = self.state[1]
        
        # Calcular recompensa
        if 70 <= glucose_level <= 140:
            reward = 1  # Glicose dentro da faixa saudável
        elif glucose_level < 70:
            reward = -1  # Hipoglicemia
        else:
            reward = -1  # Hiperglicemia
        
        self.current_step += 1
        done = self.current_step >= len(self.glucose_data)
        
        # Novo estado
        self.state = self.glucose_data.iloc[self.current_step, :3].values if not done else None
        return self.state, reward, done, {}
    
    def render(self):
        pass

# Exemplo de uso do ambiente
glucose_data = pd.DataFrame({
    'Glucose_Level': [180, 150, 110, 80, 140, 90],
    'Carbohydrate_Intake': [45, 30, 25, 20, 50, 10],
    'Insulin_Dose': [2, 1.5, 1.0, 0.5, 2.5, 0.8]
})

env = DiabetesEnv(glucose_data)
state = env.reset()

for _ in range(10):
    action = env.action_space.sample()  # Selecionar uma ação aleatória
    next_state, reward, done, _ = env.step(action)

    if done:
        break
