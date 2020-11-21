import pickle
import numpy as np
import gym

Pickle_frozen = open('frozen_q', 'rb')
q_table = pickle.load(Pickle_frozen)
#print(q_table)

env = gym.make('FrozenLake-v0')
env.reset()
max_steps = 100
episode_rewards  =[]

for ep_no in range(10):
    observation = env.reset()
    done = False
    for step_no in range(max_steps):
        env.render()
        action = np.argmax(q_table[observation,:])

        prev_obs = observation
        observation, reward, done, info = env.step(action)
        if done:
            if reward == 1:
                env.render()
                print(f"Won at episode no = {ep_no +1}")
                exit(1)
            print(f"Episode finished after {step_no}  steps")
            episode_rewards.append(reward)
            break


print(f"\n\nEpisode no. finally is {ep_no}")