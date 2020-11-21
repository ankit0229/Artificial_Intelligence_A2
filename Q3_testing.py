import pickle

Picklefile1 = open('Qtable2', 'rb')
q_table2 = pickle.load(Picklefile1)
print(q_table2)
print(type(q_table2))
import random
import numpy as np

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

print(dict_action)
print(dict_inv_action)
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

episodes = 5

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
for ep_no in range(episodes):
    print(f"EPISODE NO = {ep_no}")
    grid = [[] for i in range(3)]
    no = 1
    for i in range(3):
        for j in range(3):
            grid[i].append(no)
            no = no + 1
    while 1:
        prev_obs2 = encode_state()
        idx_prev_obs2 = dict_global2.get(prev_obs2)
        if idx_prev_obs2 is None:
            dict_global2[prev_obs2] = global_state_idx2
            global_state_idx2 = global_state_idx2 + 1
        idx_prev_obs2 = dict_global2.get(prev_obs2)

        q_table = q_table2.copy()
        opt_action = max_action(idx_prev_obs2)
        grid[opt_action[0]][opt_action[1]] = 'O'
        action2 = dict_action[opt_action]
        do_printing()

        next_obs2 = encode_state()
        idx_next_obs2 = dict_global2.get(next_obs2)
        if idx_next_obs2 is None:
            dict_global2[next_obs2] = global_state_idx2
            global_state_idx2 = global_state_idx2 + 1
        empty_places = checkEmpty()
        reward1 = checkEnd('O')

        if len(empty_places) == 0 or reward1 == 1:
            if reward1 == 1:
                print("Episode over and O wins the game")
                win_ag2.append(reward1)
            else:
                print("Game is a draw")
            break

        #Now playing the human
        print("Enter the row and column co-orddinates:")
        x_no = input()
        x_no = int(x_no)
        y_no = input()
        y_no = int(y_no)
        grid[x_no][y_no] = 'X'
        reward2 = checkEnd('X')
        do_printing()
        if len(empty_places) == 0 or reward2 == 1:
            if reward2 == 1:
                print("Episode over and X wins the game")
                win_ag1.append(reward2)
            else:
                print("Game is a draw")
            break

wa1 = 0
wa2 = 0
for m in win_ag1:
    if m == 1:
        wa1 = wa1 + 1
for n in win_ag2:
    if n == 1:
        wa2 = wa2 + 1

print("The reward list of agent 1")
print(win_ag1)
print(f"No. of wins of agent 1 = {wa1}")
print("The reward list of agent 2")
print(win_ag2)
print(f"No. of wins of agent 2 = {wa2}")
