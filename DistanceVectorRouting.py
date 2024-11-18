class NetworkNode:
    def __init__(self, name, neighbors):
        """
        name: Nome del nodo
        neighbors: Dizionario dei vicini {vicino: costo}
        """
        self.name = name
        self.neighbors = neighbors
        self.distance_vector = {name: 0}  # Inizializza il DV con la distanza a sé stesso
        for neighbor, cost in neighbors.items():
            self.distance_vector[neighbor] = cost  # Distanze iniziali verso i vicini diretti

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


class DistanceVectorNetwork:
    def __init__(self, topology):
        """
        topology: Dizionario che rappresenta la rete {nodo: {vicino: costo}}
        """
        self.nodes = {name: NetworkNode(name, neighbors) for name, neighbors in topology.items()}

    def simulate_routing(self):
        iteration = 0
        print(f"Iterazione {iteration}: Stato iniziale")
        self.print_distance_vectors()

        # Continuare fino a che i DV non smettono di aggiornarsi
        while True:
            updated = False
            iteration += 1
            for node in self.nodes.values():
                if node.update_distance_vector(self.nodes):
                    updated = True

            print(f"\nIterazione {iteration}: Aggiornamento")
            self.print_distance_vectors()

            if not updated:  # Se nessun DV è stato aggiornato, la convergenza è stata raggiunta
                print("\nConvergenza raggiunta!")
                break

    def print_distance_vectors(self):
        for name, node in self.nodes.items():
            print(f"Nodo {name}: {node.distance_vector}")


# Topologia della rete (modificabile)
network_topology = {
    'A': {'B': 1, 'D': 4},
    'B': {'A': 1, 'C': 2},
    'C': {'B': 2, 'D': 1},
    'D': {'A': 4, 'C': 1}
}

# Creare la rete e simulare il protocollo di routing
network = DistanceVectorNetwork(network_topology)
network.simulate_routing()
