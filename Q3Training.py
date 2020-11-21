import random
import numpy as np
import pickle
import matplotlib.pyplot as plt

val = 0
dict_action = {}
dict_inv_action = {}
win_ag1 = []
win_ag2 = []
global_state_idx1 = 0
dict_global1 = {}
global_state_idx2 = 0
dict_global2 = {}

for i in range(3):
    for j in range(3):
        pair = (i, j)
        dict_action[pair] = val
        dict_inv_action[val] = pair
        val = val + 1


grid = [[] for i in range(3)]
no = 1
q_table1 = np.zeros((400000, 9))
q_table2 = np.zeros((400000, 9))
q_table = np.zeros((400000, 9))
for i in range(3):
    for j in range(3):
        grid[i].append(no)
        no = no + 1
print(grid)
print(grid[2][2])

episodes = 40000
alpha1 = 0.2
gamma1 = 0.99
epsilon1 = 1
max_epsilon1 = 1
min_epsilon1 = 0.01
epsilon_decay1 = 0.0001

alpha2 = 0.1
gamma2 = 0.9
epsilon2 = 1
max_epsilon2 = 1
min_epsilon2 = 0.01
epsilon_decay2 = 0.0001

def checkEmpty():
    empty_places = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] != 'X' and grid[i][j] != 'O':
                pair = (i, j)
                empty_places.append(pair)
    return empty_places

def encode_state():
    temp_state = ''
    for i in range(3):
        for j in range(3):
            temp_state = temp_state + str(grid[i][j])
    return temp_state

def checkEnd(symbol):
    empty_places = checkEmpty()
    reward = 0
    # Now checking if any one row is same
    princ_diag = []
    other_diag = []
    for i in range(3):
        triple = []
        for j in range(3):
            triple.append(grid[i][j])
            if i == j:
                princ_diag.append(grid[i][j])
            if i-j == 2 or j-i == 2 or (i == 1 and j == 1):
                other_diag.append(grid[i][j])
        if triple[0] == symbol and triple[1] == symbol and triple[2] == symbol:
            reward = 1
            return reward
    if princ_diag[0] == symbol and princ_diag[1] == symbol and princ_diag[2] == symbol:
        reward = 1
        return reward
    if other_diag[0] == symbol and other_diag[1] == symbol and other_diag[2] == symbol:
        reward = 1
        return reward

    #Now checking if any one column is same
    for j in range(3):
        triple = []
        for i in range(3):
            triple.append(grid[i][j])
        if triple[0] == symbol and triple[1] == symbol and triple[2] == symbol:
            reward = 1
            return reward
    return reward

def max_action(idx_prev_obs2):
    list_idx = []
    list_values = []
    for j in range(9):
        list_idx.append(j)
        list_values.append(q_table[idx_prev_obs2, j])
    idx_temp_max = list_values.index(max(list_values))
    idx_temp_max = list_idx[idx_temp_max]
    temp_coord = dict_inv_action[idx_temp_max]
    #print(temp_coord)
    rest_idx = []
    while grid[temp_coord[0]][temp_coord[1]] == 'X' or grid[temp_coord[0]][temp_coord[1]] == 'O':
        rest_idx.append(idx_temp_max)
        list_idx = []
        list_values = []
        for j in range(9):
            if j not in rest_idx:
                list_idx.append(j)
                list_values.append(q_table[idx_prev_obs2, j])
        #print(list_values)
        #print(list_idx)
        idx_temp_max = list_values.index(max(list_values))
        idx_temp_max = list_idx[idx_temp_max]
        temp_coord = dict_inv_action[idx_temp_max]
        #print(temp_coord)
    return  temp_coord

def rand_coord():
    empty_places = checkEmpty()
    len_empty_places = len(empty_places)
    len_empty_places = len_empty_places - 1
    rand_idx = random.randint(0, len_empty_places)
    rand_pos = empty_places[rand_idx]
    return rand_pos

def do_printing():
    for row in grid:
        print(row)
        print()
    print("\n\n")


pend_a1 = []
pend_a2 = []
pend_act1 = []
pend_act2 = []
y_cord = []
gl_ctr = 0
for ep_no in range(episodes):
    gl_ctr = gl_ctr + 1
    print(ep_no)
    grid = [[] for i in range(3)]
    no = 1
    for i in range(3):
        for j in range(3):
            grid[i].append(no)
            no = no + 1
    while 1:
        rand_greedy2 = random.uniform(0, 1)
        prev_obs2 = encode_state()
        idx_prev_obs2 = dict_global2.get(prev_obs2)
        if idx_prev_obs2 is None:
            dict_global2[prev_obs2] = global_state_idx2
            global_state_idx2 = global_state_idx2 + 1
        idx_prev_obs2 = dict_global2.get(prev_obs2)
        pend_a2.append(prev_obs2)
        if rand_greedy2 < epsilon2:
            rand_pos2 = rand_coord()
            #print(rand_pos2)
            grid[rand_pos2[0]][rand_pos2[1]] = 'O'
            action2 = dict_action[rand_pos2]
        else:
            q_table = q_table2.copy()
            opt_action = max_action(idx_prev_obs2)
            grid[opt_action[0]][opt_action[1]] = 'O'
            action2 = dict_action[opt_action]

        #do_printing()

        next_obs2 = encode_state()
        idx_next_obs2 = dict_global2.get(next_obs2)
        if idx_next_obs2 is None:
            dict_global2[next_obs2] = global_state_idx2
            global_state_idx2 = global_state_idx2 + 1
        pend_a2.append(next_obs2)
        pend_act2.append(action2)
        empty_places = checkEmpty()
        reward1 = checkEnd('O')

        t_reward1 = reward1
        if reward1 == 1:
            t_reward1 = -1

        if len(pend_a1) == 2:
            tprev1 = pend_a1[0]
            idx_tprev1 = dict_global1.get(tprev1)
            tnext1 = pend_a1[1]
            idx_tnext1 = dict_global1.get(tnext1)
            pend_a1 = []
            tact1 = pend_act1[0]
            pend_act1 = []
            q_table1[idx_tprev1, tact1] = (1 - alpha1) * q_table1[idx_tprev1, tact1] + alpha1 * (t_reward1 + gamma1 * (np.max(q_table1[idx_tnext1, :])))
        if len(empty_places) == 0 or reward1 == 1:
            q_table2[idx_prev_obs2, action2] = (1 - alpha2) * q_table2[idx_prev_obs2, action2] + alpha2 * (reward1 + gamma2 * (np.max(q_table2[idx_next_obs2, :])))
            if reward1 == 1:
                #print("Episode over and O wins the game")
                if gl_ctr >= 1000:
                    gl_ctr = 0
                    y_cord.append(len(win_ag2))
                    win_ag2 = []
                win_ag2.append(reward1)
            """else:
                print("Game is a draw")"""
            break

        rand_greedy1 = random.uniform(0, 1)
        prev_obs1 = encode_state()

        idx_prev_obs1 = dict_global1.get(prev_obs1)
        if idx_prev_obs1 is None:
            dict_global1[prev_obs1] = global_state_idx1
            global_state_idx1 = global_state_idx1 + 1
        idx_prev_obs1 = dict_global1.get(prev_obs1)

        pend_a1.append(prev_obs1)
        if rand_greedy1 < epsilon1:
            rand_pos1 = rand_coord()
            # print(rand_pos2)

            grid[rand_pos1[0]][rand_pos1[1]] = 'X'
            action1 = dict_action[rand_pos1]
        else:
            q_table = q_table1.copy()
            opt_action = max_action(idx_prev_obs1)
            grid[opt_action[0]][opt_action[1]] = 'X'
            action1 = dict_action[opt_action]

        #do_printing()

        next_obs1 = encode_state()
        idx_next_obs1 = dict_global1.get(next_obs1)
        if idx_next_obs1 is None:
            dict_global1[next_obs1] = global_state_idx1
            global_state_idx1 = global_state_idx1 + 1
        pend_a1.append(next_obs1)
        pend_act1.append(action1)
        empty_places = checkEmpty()
        reward2 = checkEnd('X')
        t_reward2 = reward2
        if reward2 == 1:
            t_reward2 = -1

        if len(pend_a2) == 2:
            tprev2 = pend_a2[0]
            idx_tprev2 = dict_global2.get(tprev2)
            tnext2 = pend_a2[1]
            idx_tnext2 = dict_global2.get(tnext2)
            pend_a2 = []
            tact2 = pend_act2[0]
            pend_act2 = []
            q_table2[idx_tprev2, tact2] = (1 - alpha2) * q_table2[idx_tprev2, tact2] + alpha2 * (t_reward2 + gamma2 * (np.max(q_table2[idx_tnext2, :])))
        if len(empty_places) == 0 or reward2 == 1:
            q_table1[idx_prev_obs1, action1] = (1 - alpha1) * q_table1[idx_prev_obs1, action1] + alpha1 * (reward2 + gamma1 * (np.max(q_table2[idx_next_obs1, :])))
            if reward2 == 1:
                #print("Episode over and X wins the game")
                win_ag1.append(reward2)
            """else:
                print("Game is a draw")"""
            break
    if epsilon1 > min_epsilon1:
        epsilon1 = epsilon1 - epsilon_decay1
    if epsilon2 > min_epsilon2:
        epsilon2 = epsilon2 - epsilon_decay2

wa1 = 0
wa2 = 0
for m in win_ag1:
    if m == 1:
        wa1 = wa1 + 1
for n in win_ag2:
    if n == 1:
        wa2 = wa2 + 1
len_dict1 = len(dict_global1)
len_dict2 = len(dict_global2)
cnt_nz1 = 0
cnt_nz2 = 0
for i in range(len_dict1):
    for j in range(9):
        if q_table1[i][j] != 0:
            cnt_nz1 = cnt_nz1 + 1
for i in range(len_dict2):
    for j in range(9):
        if q_table2[i][j] != 0:
            cnt_nz2 = cnt_nz2 + 1

Picklefile1 = open('Qtable2', 'wb')
pickle.dump(q_table2, Picklefile1)
Picklefile1.close()

print(f"No. of non zero for agent 1 = {cnt_nz1}")
print(f"No. of non zero for agent 2 = {cnt_nz2}")
print("The reward list of agent 1")
print(win_ag1)
print(f"No. of wins of agent 1 = {wa1}")
print("The reward list of agent 2")
print(win_ag2)
print(f"No. of wins of agent 2 = {wa2}")
print("Q table 1")
print(q_table1)
print("Q table 2")
print(q_table2)
print(dict_global1)
print(dict_global2)
x_cord = []
st = 1000
for i in range(40):
    x_cord.append(st)
    st = st + 1000

y_cord.append(len(win_ag2))
plt.plot(x_cord, y_cord)
plt.xlabel('Episode range')
plt.ylabel('Win counts')
plt.show()
