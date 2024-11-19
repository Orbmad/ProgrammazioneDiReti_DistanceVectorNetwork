import sys
import json
import random
import os

class NetworkNode:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.distance_vector = {name: 0}  # Initialize the DistanceVector with self distance.
        self.next_hop = {name: None}  # Initialize the next hop table with None.
        for neighbor, cost in neighbors.items():
            self.distance_vector[neighbor] = cost  # Initialize starting distances with neighbors.
            self.next_hop[neighbor] = neighbor  # Neighbor is the next hop for directly connected nodes.

    def update_distance_vector(self, network_nodes):
        updated = False
        for neighbor in self.neighbors:
            if neighbor not in network_nodes:
                continue
            neighbor_vector = network_nodes[neighbor].distance_vector
            for dest, cost in neighbor_vector.items():
                if dest == self.name:
                    continue
                new_cost = self.neighbors[neighbor] + cost
                if dest not in self.distance_vector or new_cost < self.distance_vector[dest]:
                    self.distance_vector[dest] = new_cost
                    self.next_hop[dest] = neighbor  # Update next hop for this destination.
                    updated = True
        return updated


class Network:
    def __init__(self, topology):
        self.nodes = {name: NetworkNode(name, neighbors) for name, neighbors in topology.items()}

    def simulate_routing(self):
        iteration = 0
        print(f"Iterazione {iteration}: Stato iniziale")
        self.print_distance_vectors()

        # Continue until Distance Vectors stop updating.
        while True:
            updated = False
            iteration += 1
            for node in self.nodes.values():
                if node.update_distance_vector(self.nodes):
                    updated = True

            print(f"\nIterazione {iteration}: Aggiornamento")
            self.print_distance_vectors()

            if not updated:  # If no Distance Vector is updated, convergence is reached.
                print("\nConvergenza raggiunta!")
                break

        # Final routes output.
        print("\nTabelle di routing finali dopo la convergenza:")
        self.print_distance_vectors()

    def print_distance_vectors(self):
        for name, node in self.nodes.items():
            print(f"Nodo {name}:")
            print(f"  Distance Vector: {node.distance_vector}")
            print(f"  Next Hop: {node.next_hop}")

# Generates a random cost between 1 and 5.
def rand():
    return random.randint(1, 5)

# Returns default topology
def default_topology(hop_count):
    if hop_count:
        costs = [1 for _ in range(10)]
    else:
        costs = [rand() for _ in range(10)]
        
    return {
                'A': {'B': costs[0], 'D': costs[1]},
                'B': {'A': costs[0], 'C': costs[3], 'F': costs[4]},
                'C': {'B': costs[3], 'D': costs[5], 'F': costs[6], 'G': costs[7]},
                'D': {'A': costs[1], 'C': costs[5], 'E': costs[8], 'G': costs[9]},
                'E': {'D': costs[8], 'H': costs[2]},
                'F': {'B': costs[4], 'C': costs[6]},
                'G': {'C': costs[7], 'D': costs[9]},
                'H': {'E': costs[2]}
            }

def load_topology(input_data, hop_count):
    # Checks if the file exists
    if os.path.isfile(input_data):
        try:
            with open(input_data, 'r') as file:
                print("Caricamento topologia da file JSON:")
                return json.load(file)
        except FileNotFoundError:
            print(f"Errore: File '{input_data}' non trovato.")
            return default_topology(hop_count)
        except json.JSONDecodeError:
            print(f"Errore: Il file '{input_data}' non contiene un JSON valido.")
            return default_topology(hop_count)
    else:
        # Tries to load the input as JSON string
        try:
            load = json.loads(input_data)
            print("Caricamento della topologia da stringa di input:")
            return load
        except json.JSONDecodeError:
            print("Errore: Argomento non è un JSON valido né un file esistente.")
            return default_topology(hop_count)
            
def main():
    hop_count=True
    # Check if there are command line parameters.
    if len(sys.argv) > 1:
        if sys.argv[1] == '0':
            hop_count=False
            # Use default topology.
            topology = default_topology(hop_count)
            print("Utilizzo della topologia di default con costi randomizzati:")
        else:
            input_file = sys.argv[1]
            topology = load_topology(input_file, hop_count)
    else:
        # Use default topology.
        topology = default_topology(hop_count)
        print("Nessuna topologia specificata. Utilizzo della topologia di default:")

    # Print topology.
    try:
        for node, neighbors in topology.items():
            print(f"{node}: {neighbors}")
        print("\n")
    except (AttributeError, UnboundLocalError):
        print("Errore: La topologia caricata non è valida. Terminazione forzata")
        sys.exit(1)

    # Creates the network and simulates routing protocol.
    network = Network(topology)
    network.simulate_routing()

if __name__ == "__main__":
    main()
