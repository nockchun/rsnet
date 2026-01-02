import gymnasium as gym
import numpy as np

env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=False, render_mode="human")

def argmax_random(vector):
    vmax = np.max(vector)
    vidx = np.where(vector == vmax)[0]
    return np.random.choice(vidx)

Q = np.zeros([env.observation_space.n, env.action_space.n])
for episode_idx in range(2000):
    print(f"episode {episode_idx}")
    state, info = env.reset()
    terminated = False
    e = 1. / ((episode_idx/100)+1) # 100 episode 이후에 0.5% 이하로 탐험.

    while True:
        # policy에 따라 action 선택 + decaying E-Greedy (exploit vs exploration)
        if np.random.rand(1)[0] < e:
            action = env.action_space.sample()
            # while Q[state, action] == -1: # 인식된 hole에는 다시 빠지지 않음.
            #     action = env.action_space.sample()
        else:
            action = argmax_random(Q[state, :])

        # action을 수행하여 다음 상태 및 reward 확인.
        new_state, reward, terminated, truncated, info = env.step(action)
        # print(f"{state}\t{reward}\t{terminated}\t{truncated}")

        # # hole에 빠진 상황 인식
        if terminated and reward == 0:
            reward = -1
        
        # update Q-Table
        Q[state, action] = reward + np.max(Q[new_state, :])
        state = new_state

        # End episode
        if terminated or truncated:
            break
