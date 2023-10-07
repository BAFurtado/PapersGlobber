import json_analysis

import collections
import matplotlib.pyplot as plt
import networkx as nx


def improving_readability(G, number_top_authors=50):
    # Calculate author degrees (number of co-authored papers)
    author_degrees = dict(G.degree())

    # Get the top 30 authors based on degrees
    top_authors = dict(sorted(author_degrees.items(), key=lambda x: x[1], reverse=True)[:number_top_authors])

    # Create a subgraph with only top authors and their neighbors
    top_author_nodes = list(top_authors.keys())
    top_author_subgraph = G.subgraph(top_author_nodes)

    # Create a subgraph with non-top authors and their neighbors
    non_top_author_nodes = [author for author in G.nodes() if author not in top_author_nodes]
    non_top_author_subgraph = G.subgraph(non_top_author_nodes)

    plt.figure(figsize=(20, 6))

    # Draw top authors
    pos = nx.fruchterman_reingold_layout(top_author_subgraph)
    nx.draw_networkx_nodes(top_author_subgraph, pos, node_size=8, node_color="skyblue")
    nx.draw_networkx_edges(top_author_subgraph, pos, alpha=.7, edge_color='blue', width=.5)
    labels = {author: author for author in top_author_subgraph.nodes()}
    nx.draw_networkx_labels(top_author_subgraph, pos, labels, font_size=7, font_color="green")

    # Draw non-top authors (without labels)
    pos = nx.fruchterman_reingold_layout(non_top_author_subgraph)
    nx.draw_networkx_nodes(non_top_author_subgraph, pos, node_size=4, node_color="lightblue")
    nx.draw_networkx_edges(non_top_author_subgraph, pos, alpha=.5, edge_color='blue')

    plt.title("Author Network")
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    f = 'results_no_duplicates.json'
    k, j, abst, aut, aut_net, g, t = json_analysis.main(f)
    improving_readability(g)
