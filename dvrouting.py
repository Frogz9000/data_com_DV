import csv

#process initialization
with open("Node_Init.csv") as init_file:
    reader = csv.reader(init_file)
    node_and_neighbors = next(reader)
    node_costs = next(reader)

print(node_and_neighbors)
print(node_costs)
#index 0 gives local node id
local_node_id =  node_and_neighbors[0]
node_ids = [local_node_ids]
distance_table = dict();
for i in range(1,len(node_and_neighbors)):
    node_ids.append(node_and_neighbors[i])
    distance_table[(local_node_id,node_and_neighbors[i])] = node_costs[i]
print(distance_table)
for node in node_ids:
    

