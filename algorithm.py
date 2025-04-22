import matplotlib.pyplot as plt
import numpy as np
# from random import randrange as rand

def plot_allocations(agents, allocations):
    """
    Plot the allocations for each agent.
    """

    plt.figure(figsize=(12, 6))
    x = np.linspace(0, 1, 1000)
    colors = plt.cm.tab10(np.arange(len(agents)))
 
    for agent_id, pieces in allocations.items():
        for (start, end) in pieces:
            plt.fill_between(x, 0, 1, color = colors[agent_id], where=((x >= start) & (x <= end)), alpha=0.3)
    
    plt.title(f"Allocations for {len(agents)} Agents")
    plt.xlabel("Cake Position [0, 1]")
    plt.ylabel("Value Density")
    plt.legend()
    plt.grid(True)
    plt.show()




# algorithm.py
class EFCakeCutter:
    def __init__(self, agents):
        self.agents = agents
        self.n = len(agents)
        self.query_count = 0
        self.epsilon = 1e-6 # Tolerance for floating-point comparisons

    
    def eval_query(self, i, a, b):
        """Agent i's value for [a, b]."""
        self.query_count += 1
        ret = self.agents[i].eval(a, b)
        return ret
    
    def cut_query(self, i, a, w):
        """Leftmost y where agent i's value for [a, y] = w."""
        self.query_count += 1
        ret = self.agents[i].cut(a, w)
        return ret
    
    def cover(self, a, b):
        n = self.n
        total_values = [self.eval_query(i, a, b) for i in range(n)]
        cover = []
        alpha = a
        while True:
            min_beta = b
            champion = -1
            for i in range(n):
                if total_values[i] <= self.epsilon:
                    continue
                required = total_values[i] / n
                beta = self.cut_query(i, alpha, required)
                # Check if beta is valid within tolerance
                if beta is not None  and beta < min_beta:
                    min_beta = beta
                    champion = i
            if champion == -1 :
                break
            cover.append((alpha, min_beta, champion))
            alpha = min_beta
        # Handle remaining [alpha, b]
        max_alpha_star = 0
        champion = -1
        for i in range(n):
            if total_values[i] <= self.epsilon:
                continue
            required = (total_values[i] * (n - 1)) / n
            alpha_star = self.cut_query(i, a, required)
            if alpha_star is not None and alpha_star > max_alpha_star:
                champion = i
                max_alpha_star = alpha_star
        if champion == -1 :
            return cover 
            # champion = rand()%self.n 
        cover.append((max_alpha_star, b, champion))  
        return cover
    
    def sandwich_allocation_ef(self, a, b, sep_interval):
        alpha, beta, champion = sep_interval
        n = self.n
        left_length = alpha - a
        right_length = b - beta
        gamma = left_length / (2 * (n - 1)) 
        delta = right_length / (2 * (n - 1)) 
        pieces = {}
        pieces[champion] = [(alpha, beta)]
        for j in range(n - 1):
            # Assign pairs of intervals to non-champion agents
            agent = (champion + j + 1) % n
            left_pieces = []
            right_pieces = []
            if gamma : 
                left_pieces = [(a+ j * gamma, a + (j + 1) * gamma), (alpha - (j + 1) * gamma, alpha - j * gamma)]
            if delta : 
                right_pieces = [(beta + j * delta, beta + (j + 1) * delta), (b - (j + 1) * delta, b - j * delta)]
            pieces[agent] = left_pieces + right_pieces
            

        # plot_allocations(self.agents, pieces)
        # Verify EF
        is_ef = True
        for i in range(n):
            my_value = sum(self.eval_query(i, s, e) for (s, e) in pieces.get(i, []))
            for j in range(n):
                if i == j:
                    continue
                their_value = sum(self.eval_query(i, s, e) for (s, e) in pieces.get(j, []))
                if (their_value - self.epsilon)>my_value : 
                    is_ef = False
                    break
            if not is_ef:
                break
        return pieces if is_ef else None
    
    def ef_allocate(self, a, b):
        # print(f"Allocating EF for [{a}, {b}]")
        """Recursively compute EF allocation for [a, b]."""
        temp = {}
        delta = (b-a)/self.n
        if abs(b - a) < self.epsilon:
            for i in range(self.n):
                temp[i] = [(a + i*delta, a + (i+1)*delta)]
            return temp
        
        cover = self.cover(a, b)
        # Try sandwich allocations
        # endpoints = sorted({a, b} | {s for (s, e, _) in cover} | {e for (s, e, _) in cover})
        # print(endpoints)
        for interval in cover:
            allocation = self.sandwich_allocation_ef(a, b, interval)
            # print(allocation)
            if allocation:
                return allocation
        # Recurse on subintervals
        endpoints = sorted({a, b} | {s for (s, e, _) in cover} | {e for (s, e, _) in cover})
        # print(endpoints)
        allocations = []
        for i in range(len(endpoints) - 1):
            sub_a, sub_b = endpoints[i], endpoints[i + 1]
            # print(sub_a, sub_b)
            sub_allocation = self.ef_allocate(sub_a, sub_b)
            allocations.append(sub_allocation)
        # Merge allocations
        # print(allocations)
        merged = {}
        for alloc in allocations:
            for agent, pieces in alloc.items():
                if agent not in merged:
                    merged[agent] = []
                merged[agent].extend(pieces)
        return merged