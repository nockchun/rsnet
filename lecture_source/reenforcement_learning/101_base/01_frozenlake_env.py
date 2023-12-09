import gymnasium as gym

env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=False, render_mode="human")
observation = env.reset()

for _ in range(20):
    env.render()
    action = env.action_space.sample()
    state, reward, terminated, truncated, info = env.step(action)
    print(state, reward, terminated, truncated)
    if terminated:
        break
