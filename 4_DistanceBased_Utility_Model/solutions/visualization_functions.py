import matplotlib.pyplot as plt
import networkx as nx


def plot_network(world, ax=None):
    """Plot the networkx graph for the given World object"""
    if ax is None:
        ax = __provide_missing_ax()
    net = world.net
    pos = nx.drawing.layout.fruchterman_reingold_layout(
        net
    )
    nodelist = [x.unique_id for x in world.agents()]

    colors = [a.utility(a.subgraph()) for a in world.agents()]
    nx.draw_networkx(net, nodelist=nodelist, node_color=colors, pos=pos, ax=ax)

    norm = plt.matplotlib.colors.Normalize(vmin=min(colors), vmax=max(colors))
    scalar_map = plt.cm.ScalarMappable(norm=norm)
    scalar_map._A = []
    ax.figure.colorbar(scalar_map, ax=ax)
    ax.axis("off")


def __provide_missing_ax():
    return plt.subplot(1, 1, 1)