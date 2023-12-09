import gymnasium as gym
import numpy as np

env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=False, render_mode="human")

def argmax_random(vector):
    vmax = np.max(vector)
    vidx = np.where(vector == vmax)[0]
    return np.random.choice(vidx)

Q = np.zeros([env.observation_space.n, env.action_space.n])
for _ in range(2000):
    state, info = env.reset()
    terminated = False

    while not terminated:
        # policy에 따라 action 선택
        action = argmax_random(Q[state, :])

        # action을 수행하여 다음 상태 및 reward 확인.
        new_state, reward, terminated, truncated, info = env.step(action)
        print(f"{state}\t{reward}\t{terminated}\t{truncated}")

        # # hole에 빠진 상황 인식
        if terminated and reward == 0:
            reward = -1
        
        # update Q-Table
        Q[state, action] = reward + np.max(Q[new_state, :])
        state = new_state
