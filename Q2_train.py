import numpy as np
import gym
import random
import pickle
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0')
env.reset()

action_size = env.action_space.n
state_size = env.observation_space.n

q_table = np.zeros((state_size, action_size))

episodes = 6000
max_steps = 100
alpha = 0.1
gamma = 0.99
epsilon = 0.65
max_epsilon = 1
min_epsilon = 0.01
epsilon_decay = 0.001
episode_rewards = []

for ep_no in range(episodes):
    observation = env.reset()
    #print(observation)
    #done = False
    for step_no in range(max_steps):
        #env.render()
        rand_greedy = random.uniform(0,1)
        if rand_greedy < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[observation,:])
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
            #print(action)
            #action = env.action_space[ac_no]

        prev_obs = observation
        observation, reward, done, info = env.step(action)
        #print(observation)
        first_term = (1 - alpha) * q_table[prev_obs, action]
        fut_max = np.max(q_table[observation, :])
        second_term = reward + gamma * fut_max
        second_term = alpha * second_term
        q_table[prev_obs, action] = first_term + second_term
        if done:
            #print(f"Episode finished after {step_no}  steps")
            episode_rewards.append(reward)
            break
    if epsilon > min_epsilon:
        epsilon = epsilon - epsilon_decay

print(f"\n\nEpisode no. finally is {ep_no}")
print("Finally the Q-table is \n\n\n\n")

print(q_table)
print("\n\n\n")
print(episode_rewards)
print("$$$$$$$$$$$$$$$$$$")
print(len(episode_rewards))
reward_count = []
sum = 0
count = 0
x_cord = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
for i in range(len(episode_rewards)):
    sum = sum + episode_rewards[i]
    count = count + 1
    if count == 500:
        sum = int(sum)
        reward_count.append(sum)
        sum = 0
        count = 0
print("The rewards counts are:")
print(reward_count)
print(x_cord)
env.close()
Pickle_frozen = open('frozen_q', 'wb')
pickle.dump(q_table, Pickle_frozen)
Pickle_frozen.close()
print("Pickle created successfully")
plt.plot(x_cord, reward_count)
plt.xlabel('Episode range')
plt.ylabel('Win counts')
plt.show()

