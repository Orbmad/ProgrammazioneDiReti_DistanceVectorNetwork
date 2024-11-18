import sys
import json
import random

class NetworkNode:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.distance_vector = {name: 0}  # Initialize the DistanceVector with self distance.
        for neighbor, cost in neighbors.items():
            self.distance_vector[neighbor] = cost  # Initialize starting distances with neighbors.

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

            if not updated:  # If no Distance Vector is uptated convergence is reached.
                print("\nConvergenza raggiunta!")
                break

    def print_distance_vectors(self):
        for name, node in self.nodes.items():
            print(f"Nodo {name}: {node.distance_vector}")
            
# Generates a random cost between 1 and 5.
def rand():
    return random.randint(1, 6)

# Returns default topology
def default_topology():
    return {
                'A': {'B': rand(), 'D': rand(), 'F': rand()},
                'B': {'A': rand(), 'C': rand(), 'F': rand()},
                'C': {'A': rand(), 'B': rand(), 'D': rand(), 'F': rand(), 'G': rand()},
                'D': {'C': rand(), 'E': rand(), 'G': rand()},
                'E': {'D': rand(), 'F': rand(), 'H': rand()},
                'F': {'A': rand(), 'B': rand(), 'C': rand(), 'E': rand()},
                'G': {'C': rand(), 'D': rand()},
                'H': {'E': rand()}
            }

def main():
    # Check if there are command line parameters.
    if len(sys.argv) > 1:
        try:
            # Convert JSON string in a dictionary.
            topology = json.loads(sys.argv[1])
            print("Topologia personalizzata caricata:")
        except json.JSONDecodeError:
            print("Errore: Impossibile analizzare la topologia: assicurati che sia in formato JSON valido.\n"
                  "Caricamento topologia di default.")
            topology = default_topology()
    else:
        # Use default topology.
        topology = default_topology()
        print("Nessuna topologia specificata. Utilizzo della topologia di default:")

    # Print topology.
    for node, neighbors in topology.items():
        print(f"{node}: {neighbors}")
    print("\n")

    # Creates the network and simulates routing protocol.
    network = Network(topology)
    network.simulate_routing()


if __name__ == "__main__":
    main()
