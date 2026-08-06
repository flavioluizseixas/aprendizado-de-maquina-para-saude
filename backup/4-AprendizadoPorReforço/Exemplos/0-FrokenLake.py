import numpy as np
import gymnasium as gym

environment = gym.make("FrozenLake-v1", is_slippery=False, render_mode='human')

# Mapear teclas para ações
action_dict = {
    'w': 3,  # Para cima
    'a': 0,  # Para a esquerda
    's': 1,  # Para baixo
    'd': 2   # Para a direita
}

# Resetar o ambiente e renderizar o estado inicial
state, _ = environment.reset()
done = False

print("Controles: w (cima), a (esquerda), s (baixo), d (direita)")
print("Digite a ação (w/a/s/d) e pressione Enter:")

while not done:
    # Receber entrada do usuário
    action_key = input("Sua ação: ").lower()
    
    # Verificar se a entrada é válida
    if action_key in action_dict:
        action = action_dict[action_key]
    else:
        print("Ação inválida! Use apenas w/a/s/d.")
        continue

    # Executar a ação
    state, reward, done, truncated, info = environment.step(action)

    print(reward)
    
    # Renderizar o ambiente após a ação
    environment.render()

    # Checar se o episódio terminou
    if done:
        print(f"Fim do jogo! Recompensa: {reward}")
        break


