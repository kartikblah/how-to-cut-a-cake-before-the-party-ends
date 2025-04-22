# demo_random.py
from gen_valuations import generate_random_valuations
from plot_valuations import plot_valuations, plot_allocations
from valuations import PiecewiseLinearValuation
from algorithm import EFCakeCutter


# Generate 6 agents with 4-piece valuations
n = 3
k = 4
agents = generate_random_valuations(n, k)

# Visualize
plot_valuations(agents)


# Run EF algorithm
cutter = EFCakeCutter(agents)
allocation = cutter.ef_allocate(0.0, 1.0)


# plot_allocations(agents, allocation)

# Print results
# print("EF Allocation:")
# for agent, pieces in allocation.items():
#     print(f"Agent {agent + 1}: {pieces}")
print(f"Total queries: {cutter.query_count}")

# Verify EF
for i in range(n):
    my_pieces = allocation.get(i, [])
    # print(my_pieces)
    # my_value = sum(agent[i].eval(s, e)  for (s, e) in my_pieces)
    my_value = 0 
    for (s, e) in my_pieces:
        my_value += agents[i].eval(s, e)
    for j in range(n):
        their_pieces = allocation.get(j, [])
        their_value = 0
        for (s, e) in their_pieces:
            their_value += agents[i].eval(s, e)
        # their_value = sum(agents[j].eval(s, e)  for (s, e) in their_pieces)
        if (my_value + (10*cutter.epsilon)) < their_value:
            print(f"Agent {i + 1} value for its pieces: {my_value}")
            print(f"Agent {i + 1} value for {j + 1} pieces: {their_value}")
            print(f"Agent {i + 1} envies Agent {j + 1}!")
            break
    else:
        print(f"Agent {i + 1} does not envy others.")


# print value of each agent :
for i in range(n):
    my_pieces = allocation.get(i, [])
    my_value = 0
    for (s, e) in my_pieces:
        my_value += agents[i].eval(s, e)
    # my_value = sum(agent[i].eval(s, e)  for (s, e) in my_pieces)
    print(f"Agent {i + 1} value: {my_value}")



# plot the allocation too 
plot_allocations(agents, allocation)
