import random
import math
import networkx as nx
import matplotlib.pyplot as plt

cities = 10
ants = 20
iterations = 1000
alpha = 6
beta = 4
rate = 0.8

dist_matrix = [[0 for i in range(cities)] for j in range(cities)]

for i in range(cities):
    for j in range(cities):
        if i != j:
            dist_matrix[i][j] = random.randint(1,100)
print("Distance matrix is:")
print(dist_matrix)

ph_matrix = [[1 for i in range(cities)] for j in range(cities)]
prob_matrix = [[-1 for i in range(cities)] for j in range(cities)]
visited = [[0 for i in range(ants)] for j in range(cities)]
path_taken = [[] for i in range(ants)]
L = [0 for i in range(ants)]
#print(dist_matrix)
#print(ph_matrix)
#print(prob_matrix)
iterations = 1000
lk = 0
iteration_no = 0

while 1:
    iteration_no = iteration_no + 1
    visited = [[0 for i in range(ants)] for j in range(cities)]
    path_taken = [[] for i in range(ants)]
    prob_matrix = [[-1 for i in range(cities)] for j in range(cities)]
    curr = 0
    G = nx.Graph()
    for nd in range(cities):
        G.add_node(nd)

    for i in range(cities):
        den = 0
        for j in range(1,cities):
            if i != j:
                t1 = pow(ph_matrix[i][j],alpha)
                t2 = 1 / dist_matrix[i][j]
                t2 = pow(t2, beta)
                prod = t1 * t2
                #print(f"Product is {prod}")
                den = den + prod
        for j in range(cities):
            if i != j:
                t1 = pow(ph_matrix[i][j], alpha)
                t2 = 1 / dist_matrix[i][j]
                t2 = pow(t2, beta)
                prod = t1 * t2
                #print(f"Numerator is {prod}")
                """if den == 0:
                    prob_matrix[i][j] = 0
                else:"""
                prob = prod / den
                prob_matrix[i][j] = prob
    # print(prob_matrix)

    for k in range(ants):
        curr = 0
        for move_no in range(cities - 1):
            if iteration_no == 1:
                choices = []
                for w in range(1, cities):
                    if w != curr and visited[w][k] != 1:
                        choices.append(w)
                len_choices = len(choices)
                idx = random.randint(0, len_choices - 1)
                idx_max_prob = choices[idx]
                # print(idx_max_prob)
            else:
                temp_prob = []
                temp_city = []
                for q in range(1, cities):
                    if q != curr and visited[q][k] == 0:
                        temp_prob.append(prob_matrix[curr][q])
                        temp_city.append(q)


                cum_prob = []
                prob_rand = random.uniform(0, 1)
                for v in range(len(temp_prob)):
                    sum = 0
                    for w in range(v,len(temp_prob)):
                        sum = sum + temp_prob[w]
                    cum_prob.append(sum)

                flag2 = 0
                for it_prob in range(len(cum_prob) - 1):
                    if prob_rand <= cum_prob[it_prob] and prob_rand > cum_prob[it_prob+1]:
                        chosen = it_prob
                        flag2 = 1
                        break
                if flag2 == 0:
                    chosen = len(cum_prob) - 1

                #idx = temp_prob.index(chosen_prob)
                idx_max_prob = temp_city[chosen]

            visited[idx_max_prob][k] = 1
            #print(f"idx max prob is {idx_max_prob}")
            edge = (curr, idx_max_prob)
            path_taken[k].append(edge)
            ed_list = [edge]
            G.add_edges_from(ed_list)
            L[k] = L[k] + dist_matrix[curr][idx_max_prob]
            curr = idx_max_prob
        L[k] = L[k] + dist_matrix[curr][0]
        edge = (curr, 0)
        path_taken[k].append(edge)
        ed_list = [edge]
        G.add_edges_from(ed_list)

    for f in range(cities):
        for g in range(cities):
            check = (f, g)
            delta_ph = 0
            for h in range(ants):
                if check in path_taken[h]:
                    delta_ph = delta_ph + (1 / L[h])

            new_ph = (1 - rate) * ph_matrix[f][g] + delta_ph
            ph_matrix[f][g] = new_ph
    count_ed = G.number_of_edges()
    print("$$$$$$$$$")
    print(f"Edges in graph = {count_ed}")

    if count_ed == cities or iteration_no == iterations:
        if count_ed == cities:
            print(f"Best path is {path_taken[0]}")
            print(f"Best path length is {L[0]}")
        else:
            print("Not converged")
        break
    # print("$$$$$$$$")
    # print(L)
    #plt.subplot(211)
    #print("The original Graph:")
    #nx.draw_networkx(G)
    #plt.show()

print("PH matrix is:")
print(ph_matrix)

print("L values are:")
print(L)

print("Paths taken are:")
print(path_taken)

print(f"Found in iteration  = {iteration_no}")

plt.subplot(211)
print("The original Graph:")

nx.draw_networkx(G)
plt.show()