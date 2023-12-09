import gymnasium as gym
import numpy as np

env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=True, render_mode="ansi")
episode_results = []

def argmax_random(vector):
    vmax = np.max(vector)
    vidx = np.where(vector == vmax)[0]
    return np.random.choice(vidx)

discount_gamma = 0.99
learning_alpha = 0.85
episode_length = 2000

Q = np.zeros([env.observation_space.n, env.action_space.n])
for episode_idx in range(episode_length):
    state, info = env.reset()

    while True:
        # policy에 따라 action 선택 + noise picking (exploit vs exploration)
        action = np.argmax(Q[state, :] + np.random.randn(1, env.action_space.n) / (episode_idx+1))

        # action을 수행하여 다음 상태 및 reward 확인.
        new_state, reward, terminated, truncated, info = env.step(action)
        # print(f"{state}\t{reward}\t{terminated}\t{truncated}")

        # update Q-Table
        q_learn = reward + discount_gamma * np.max(Q[new_state, :])
        # Q[state, action] = q_learn
        Q[state, action] += learning_alpha * (q_learn - Q[state, action])
        state = new_state

        # End episode
        if terminated or truncated:
            episode_results.append(reward)
            break
    
    rewards = sum(episode_results)
    print(f"episode {episode_idx+1}, success: {rewards:.0f}, rate: {rewards/(episode_idx+1) * 100:.02f}", end="\r")

print(f"episode {episode_idx+1}, success: {rewards:.0f}, rate: {rewards/episode_length * 100:.02f}{' '*20}")