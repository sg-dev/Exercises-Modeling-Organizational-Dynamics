import matplotlib.pyplot as plt
import networkx as nx

def plot_graph_with_labels(G, pos=None, load_attr='load', capacity_attr='capacity', state_attr='state',
                           state_color_map=None, node_size=500, offset=(0.1, 0.1)):
    """
    Plots a NetworkX graph with load values displayed inside the nodes, capacity values displayed 
    next to the nodes, and node colors based on a 'state' attribute.
    
    Parameters:
        G (networkx.Graph): Graph with node attributes.
        pos (dict, optional): Dictionary of node positions. If None, spring layout is computed.
        load_attr (str, optional): Node attribute for load (displayed inside nodes).
        capacity_attr (str, optional): Node attribute for capacity (displayed next to nodes).
        state_attr (str, optional): Node attribute representing state.
        state_color_map (dict, optional): Mapping from state names to colors. 
            Defaults to {'healthy': 'green', 'failing': 'orange', 'failed': 'red'}.
        node_size (int, optional): Size of nodes.
        offset (tuple, optional): (x, y) offset for capacity labels.
    """
    # Compute positions if not provided
    if pos is None:
        pos = nx.spring_layout(G)
    
    # Set default color mapping if none provided
    if state_color_map is None:
        state_color_map = {'healthy': 'lightblue', 'failing': 'pink', 'failed': 'red', 'unknown': 'gray'}
    
    # Create a list of node colors based on their state attribute
    node_colors = [
        state_color_map.get(G.nodes[node].get(state_attr, 'unknown'), 'gray') 
        for node in G.nodes()
    ]
    
    # Draw nodes and edges with state-based colors
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_size)
    nx.draw_networkx_edges(G, pos)
    
    # Create and draw load labels (rounded to two decimals)
    load_labels = {node: f"{G.nodes[node][load_attr]:.2f}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=load_labels, font_color='black')
    
    # Create and draw capacity labels with offset
    capacity_labels = {node: G.nodes[node][capacity_attr] for node in G.nodes()}
    pos_capacity = {node: (x + offset[0], y + offset[1]) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, pos_capacity, labels=capacity_labels, font_color='red')
    
    plt.axis('off')
    plt.show()
