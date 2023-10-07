import pickle
import random
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio

import community  # python-louvain library
import networkx as nx


def detect_clusters(graph):
    # Using the Louvain method for community detection
    partition = community.best_partition(graph)

    # Convert the partition dictionary to a list of clusters
    clusters = {}
    for node, cluster_id in partition.items():
        if cluster_id in clusters:
            clusters[cluster_id].append(node)
        else:
            clusters[cluster_id] = [node]

    return clusters


def make_plot(G, clusters):
    # Calculate node positions using a layout algorithm (e.g., Spring layout)
    pos = nx.spring_layout(G, seed=42)

    # Node degrees
    node_degrees = dict(G.degree())
    # Create a Plotly figure
    fig = go.Figure()

    # Define a layout for the graph
    layout = go.Layout(
        hovermode="closest",
        title="Author Network",
        showlegend=False,
        width=1000,
        height=1000,
    )

    # Create edges
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Add edges to the graph
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace["x"] += tuple([x0, x1, None])
        edge_trace["y"] += tuple([y0, y1, None])

    fig.add_trace(edge_trace)

    # Create nodes
    color_palette = np.random.randn(len(clusters))

    # Create a dictionary to map authors to their cluster's color
    author_to_color = {}
    for cluster_id, authors in clusters.items():
        color = color_palette[cluster_id]
        for author in authors:
            author_to_color[author] = color
    colors = [author_to_color[author] for author in G.nodes()]

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers",
        hoverinfo="text",
        marker=dict(
            size=[node_degrees[node] for node in G.nodes()],
            color=colors,
            # colorbar=dict(
            #     thickness=15,
            #     title="Node Connections",
            #     xanchor="left",
            #     titleside="right",
            #     ),
            # showscale=True,
            colorscale='YlGnBu'
            )
    )

    # Add nodes to the graph
    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += tuple([x])
        node_trace["y"] += tuple([y])

    # Set the text for node hover information
    for node in G.nodes():
        node_trace["text"] += tuple([node])

    fig.add_trace(node_trace)

    # Update the layout
    fig.update_layout(layout)

    # Show the interactive graph
    fig.show()
    pio.write_html(fig, 'author_network.html')
    pio.write_image(fig, 'author_network.svg', format='svg')


if __name__ == '__main__':
    with open('authors_graph', 'rb') as handler:
        g = pickle.load(handler)

    # # Call the function to detect clusters in your graph G
    # sample_percentage = 0.1
    #
    # # Get a random subset of nodes
    # sampled_nodes = random.sample(g.nodes(), int(len(g.nodes()) * sample_percentage))
    #
    # # Create a subgraph containing only the sampled nodes and their associated edges
    # sampled_graph = g.subgraph(sampled_nodes)
    #
    # # clstrs = detect_clusters(sampled_graph)
    # #
    # # make_plot(sampled_graph, clstrs)

    clstrs = detect_clusters(g)

    make_plot(g, clstrs)
