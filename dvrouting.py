#No AI was used, just w3schools, python docs, and stack overflow
import csv

class node:
    def __init__(self,id,neighbors = None):
        self.id = id
        if neighbors == None:
            self.neighbors = []
        else:
            self.neighbors = neighbors
    def get_neighbors(self):
        return self.neighbors
    def add_neighbor(self,id,distance):
        self.neighbors.append((id,distance))
    def get_distance(self, target_id):
        for i in self.neighbors:
            id, dist = i
            if id == target_id:
                return dist
        return None
#process initialization
with open("Node_Init.csv") as init_file:
    reader = csv.reader(init_file)
    node_and_neighbors = next(reader)
    node_costs = next(reader)
#index 0 gives local node id
start_node = node(node_and_neighbors[0])
for i in range(1,len(node_and_neighbors)):
    start_node.add_neighbor(node_and_neighbors[i],int(node_costs[i]))

#initial distance table
distance_table = {}#dest -> neighbor -> cost
print("DistanceTable:")
print(f"  {start_node.id} |  {start_node.neighbors[0][0]}  |  {start_node.neighbors[1][0]} ")
print("-----------------")
for i in range(1,12):
    distance_table[str(i)] = {}#distance table row I
    row_string = f" {str(i).rjust(2)} |"
    for j in start_node.neighbors:
        #distance table col I
        id, dist = j
        if str(i) == str(id):
            distance_table[str(i)][id] = dist
            row_string += f" {int(dist):.1f} |"
        else:
            distance_table[str(i)][id] = float('inf')
            row_string += " inf |"
    print(row_string)
#initial routing table
routing_table = {}#dest -> next hop -> min dist
print("RoutingTable:")
print(f"Dest | NEXT |  MINIMUM ")
print(f"     | HOP  |  DISTANCE ")
print("-----------------")
for i in range(1,12):
    #routing table rows
    row_string = f" {str(i).rjust(2)}  |"
    dist = start_node.get_distance(str(i))
    if dist != None:
        routing_table[str(i)] = (int(i),int(dist))
        row_string += f" {int(i):.1f}  | {int(dist):.1f} |"
    else:
        routing_table[str(i)] = (float('inf'),float('inf'))
        row_string += " inf  | inf |"
    print(row_string)
#Vectors to send
print("Distance Vector to send:")
for j in start_node.neighbors:
        id, dist = j
        print(f"[{start_node.id}, {id}, {int(dist):.1f}]")  
#round one input
with open("Node_Round1_DV_Rcv.csv") as r1:
    reader = csv.reader(r1)
    for row in reader:
        #process new route data row by row
        source, dest, cost = row
        cost = int(cost)
        if (dest == start_node.id):
            #ignore routes back to local start snode
            continue
        cost_to_neighbor = start_node.get_distance(source)
        total_cost = cost_to_neighbor + cost
        if distance_table[dest][source] > total_cost:
            distance_table[dest][source] = total_cost
                
                
print("DistanceTable:")
print(f"  {start_node.id} |  {start_node.neighbors[0][0]}  |  {start_node.neighbors[1][0]} ")
print("-----------------")
for i in range(1,12):
    row_string = f" {str(i).rjust(2)} |"
    for j in start_node.neighbors:
        id, dist = j
        #distance table col I
        if id in distance_table[str(i)]:
            dist = distance_table[str(i)][id];
            if dist == float('inf'):
                row_string += " inf |"    
            else:
                row_string += f" {int(dist):.1f} |"
    print(row_string)
    
#update routing based on new distance:
distance_vectors = []

for dest in distance_table:
    min_dist = float('inf')#set highest possible distance
    next_hop = None        #set hope to None
    for neighbor in distance_table[dest]:
        #get distance to each neighbor and each destination and iterate through to find minimum dist
        dist = distance_table[dest][neighbor]
        if dist < min_dist:
            min_dist = dist;
            next_hop = neighbor
    if next_hop == None:
        next_hop = float('inf')
    _, current_dist = routing_table[dest]
    if min_dist < current_dist:
        #there has been an update in the routing that needs to be transmitted
        distance_vector = [start_node.id, dest, min_dist]
        distance_vectors.append(distance_vector)
    routing_table[dest] = (next_hop,min_dist)
#print updated routing table:
print("RoutingTable:")
print(f"Dest | NEXT |  MINIMUM ")
print(f"     | HOP  |  DISTANCE ")
print("-----------------")
for i in routing_table:
    #routing table rows
    row_string = f" {str(i).rjust(2)}  |"
    id, dist = routing_table[i]
    if dist != None and dist != float('inf'):
        row_string += f" {int(id):.1f}  | {int(dist):.1f} |"
    else:
        row_string += " inf  | inf |"
    print(row_string)
#vector state to send:
print("Distance Vector to send:")
for i in distance_vectors:
    node_id, dest_id, dist = i
    print(f"[{node_id}, {dest_id}, {int(dist):.1f}]") 
    
    
#generalize the round one functiuonality:
def update_route_from_csv(filename):
    #round one input
    with open(filename) as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            #process new route data row by row
            source, dest, cost = row
            cost = int(cost)
            if (dest == start_node.id):
                #ignore routes back to local start snode
                continue
            cost_to_neighbor = start_node.get_distance(source)
            total_cost = cost_to_neighbor + cost
            if distance_table[dest][source] > total_cost:
                distance_table[dest][source] = total_cost
                    
                    
    print("DistanceTable:")
    print(f"  {start_node.id} |  {start_node.neighbors[0][0]}  |  {start_node.neighbors[1][0]} ")
    print("-----------------")
    for i in range(1,12):
        row_string = f" {str(i).rjust(2)} |"
        for j in start_node.neighbors:
            id, dist = j
            if id in distance_table[str(i)]:
                dist = distance_table[str(i)][id];
                if dist == float('inf'):
                    row_string += " inf |"    
                else:
                    row_string += f" {int(dist):.1f} |"
        print(row_string)
        
    #update routing based on new distance:
    distance_vectors = []

    for dest in distance_table:
        min_dist = float('inf')#set highest possible distance
        next_hop = None        #set hope to None
        for neighbor in distance_table[dest]:
            #get distance to each neighbor and each destination and iterate through to find minimum dist
            dist = distance_table[dest][neighbor]
            if dist < min_dist:
                min_dist = dist;
                next_hop = neighbor
        if next_hop == None:
            next_hop = float('inf')
        _, current_dist = routing_table[dest]
        if min_dist < current_dist:
            #there has been an update in the routing that needs to be transmitted
            distance_vector = [start_node.id, dest, min_dist]
            distance_vectors.append(distance_vector)
        routing_table[dest] = (next_hop,min_dist)
    #print updated routing table:
    print("RoutingTable:")
    print(f"Dest | NEXT |  MINIMUM ")
    print(f"     | HOP  |  DISTANCE ")
    print("-----------------")
    for i in routing_table:
        #routing table rows
        row_string = f" {str(i).rjust(2)}  |"
        id, dist = routing_table[i]
        if dist != None and dist != float('inf'):
            row_string += f" {int(id):.1f}  | {int(dist):.1f} |"
        else:
            row_string += " inf  | inf |"
        print(row_string)
    #vector state to send:
    print("Distance Vector to send:")
    for i in distance_vectors:
        node_id, dest_id, dist = i
        print(f"[{node_id}, {dest_id}, {int(dist):.1f}]") 
        
        
update_route_from_csv("Node_Round2_DV_Rcv.csv")
update_route_from_csv("Node_Round3_DV_Rcv.csv")