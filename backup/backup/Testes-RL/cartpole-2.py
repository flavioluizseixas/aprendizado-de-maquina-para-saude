import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

# Criar o ambiente CartPole
#env = gym.make('CartPole-v1')
env = gym.make("CartPole-v1", render_mode="rgb_array")

# Criar o modelo DQN
model = DQN('MlpPolicy', env, verbose=1)

# Treinar o modelo
model.learn(total_timesteps=20000)

# Avaliar o modelo
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Recompensa média: {mean_reward} +/- {std_reward}")

# Testar o modelo treinado
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render("human")

#    if done:
#        obs = env.reset()

env.close()