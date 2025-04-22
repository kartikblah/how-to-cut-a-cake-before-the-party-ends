# plot_valuations.py
import matplotlib.pyplot as plt
import numpy as np

def plot_valuations(agents):
    """
    Plot all agents' piecewise linear value density functions.
    """
    plt.figure(figsize=(12, 6))
    x = np.linspace(0, 1, 1000)
    
    for agent_id, agent in enumerate(agents):
        y = []
        for xi in x:
            # Find the segment containing xi
            for (start, end, slope, intercept) in agent.segments:
                if start <= xi <= end:
                    y.append(slope * xi + intercept)
                    break
            else:
                y.append(0)  # Outside all segments (shouldn't happen)
        
        plt.plot(x, y, label=f"Agent {agent_id + 1}", alpha=0.7)
    
    plt.title(f"Piecewise Linear Value Densities for {len(agents)} Agents")
    plt.xlabel("Cake Position [0, 1]")
    plt.ylabel("Value Density")
    plt.legend()
    plt.grid(True)
    plt.show()



# the allocations of same agent should have same color

def plot_allocations(agents, allocations):
    """
    Plot the allocations for each agent.
    """

    plt.figure(figsize=(12, 6))
    x = np.linspace(0, 1, 1000)
    colors = plt.cm.tab10(np.arange(len(agents)))
    # for agent_id, agent in enumerate(agents):
    #     y = []
    #     for xi in x:
    #         # Find the segment containing xi
    #         for (start, end, slope, intercept) in agent.segments:
    #             if start <= xi <= end:
    #                 y.append(slope * xi + intercept)
    #                 break
    #         else:
    #             y.append(0)  # Outside all segments (shouldn't happen)
        
    #     plt.plot(x, y, label=f"Agent {agent_id + 1}", alpha=0.7)
    
    # Plot allocations
    for agent_id, pieces in allocations.items():
        for (start, end) in pieces:
            plt.fill_between(x, 0, 1, color = colors[agent_id], where=((x >= start) & (x <= end)), alpha=0.3)
    
    plt.title(f"Allocations for {len(agents)} Agents")
    plt.xlabel("Cake Position [0, 1]")
    plt.ylabel("Value Density")
    plt.legend()
    plt.grid(True)
    plt.show()


# def plot_allocations(agents, allocation):
#     """
#     Plot the allocations for each agent, ensuring the same agent's allocations have the same color.
#     """
#     plt.figure(figsize=(12, 6))
#     colors = plt.cm.tab10(np.arange(len(agents)))  # Generate distinct colors for each agent

#     for agent_id, pieces in allocation.items():
#         for (start, end) in pieces:
#             plt.fill_betweenx([0, 1], start, end, color=colors[agent_id], alpha=0.5, label=f"Agent {agent_id + 1}" if start == allocation[agent_id][0][0] else "")
    
#     plt.title(f"Allocations for {len(agents)} Agents")
#     plt.xlabel("Cake Position [0, 1]")
#     plt.ylabel("Allocation")
#     plt.legend()
#     plt.grid(True)
#     plt.show()