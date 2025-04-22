# main.py
from valuations import PiecewiseLinearValuation
from algorithm import EFCakeCutter
from plot_valuations import plot_valuations ,plot_allocations



# Define 2 agents with piecewise linear valuations
agent1 = PiecewiseLinearValuation([
    (0.0, 0.5, 0, 1.0), (0.5, 1.0, 4, -2)  # Constant 2.0 on [0, 0.5]
       # Zero on [0.5, 1.0]
])

# start, end, slope, intercept

agent2 = PiecewiseLinearValuation([
    (0.0, 1.0, 0, 1.0)  # Constant 2.0 on [0.5, 1.0]
])


agent3 = PiecewiseLinearValuation([
    (0.0, 0.5, 2, 0.5), (0.5, 1.0, -2, 2.5)  # Constant 2.0 on [0.5, 1.0]
])

agent4 = PiecewiseLinearValuation([
    (0.0, 1.0, 2.0, 0.0)  # Constant 2.0 on [0.5, 1.0]
])

agent5 = PiecewiseLinearValuation([
    (0.0, 1.0, -2.0, 2)  # Constant 2.0 on [0.5, 1.0]
])

agents = [agent1, agent2, agent3, agent4, agent5]
n = len(agents)
plot_valuations(agents)


# Run EF algorithm
cutter = EFCakeCutter(agents)
allocation = cutter.ef_allocate(0.0, 1.0)


# Print results
# print("EF Allocation:")
# for agent, pieces in allocation.items():
#     print(f"Agent {agent + 1}: {pieces}")
print(f"Total queries: {cutter.query_count}")

# Verify EF
for i in range(n):
    my_pieces = allocation.get(i, [])
    # my_value = sum(agent1.eval(s, e) if i == 0 else agent2.eval(s, e) for (s, e) in my_pieces)
    # my_value = sum(agents[i].eval(s, e) for (s, e) in my_pieces)
    my_value = 0 
    for (s, e) in my_pieces:
        my_value += agents[i].eval(s, e)
    for j in range(n):
        their_pieces = allocation.get(j, [])
        # their_value = sum(agent1.eval(s, e) if i == 0 else agent2.eval(s, e) for (s, e) in their_pieces)
        # their_value = sum(agents[j].eval(s, e) for (s, e) in their_pieces)
        their_value = 0
        for (s, e) in their_pieces:
            their_value += agents[i].eval(s, e)
        if (my_value + (10*cutter.epsilon)) < their_value:
        # if my_value< their_value : 
            print(f"Agent {i + 1} value for its pieces: {my_value}")
            print(f"Agent {i+1} value for {j+1} peices: {their_value}")
            print(f"Agent {i + 1} envies Agent {j + 1}!")
            break
    else:
        print(f"Agent {i + 1} does not envy others.")


# print value of each agent : 
for i in range(n):
    my_pieces = allocation.get(i, [])
    # my_value = sum(agent1.eval(s, e) if i == 0 else agent2.eval(s, e) for (s, e) in my_pieces)
    my_value = sum(agents[i].eval(s, e) for (s, e) in my_pieces)
    print(f"Agent {i + 1} value: {my_value}")


plot_allocations(agents, allocation)