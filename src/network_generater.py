import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt
import japanize_matplotlib

class NetworkGenerater:

    def to_min(self,value, min = 0.1):
        if value > min:
            return value
        return min

    def network(
        self,
        values:list, 
        size = 100,
        node_v = 0.1,
        edge_v = 0.002,
    ):

        plt.figure(figsize=(15, 15))

        #新規グラフを作成
        #G = nx.MultiDiGraph()
        G = nx.DiGraph()

        G.add_weighted_edges_from(values)
        node_size = []    
        color_map = []
        for node in G:
            if str(node).startswith("to_ad_"):
                color_map.append('red')
            elif str(node).startswith("to_article_"):
                color_map.append('yellow')
            elif str(node).startswith("to_"):
                color_map.append('red')            
            else: 
                color_map.append('green')


            node_size.append(size)

        pos = nx.spring_layout(G, k=100)
        #pos = nx.spiral_layout(G)    
        #top = nx.bipartite.sets(G)[0]
        #pos = nx.bipartite_layout(G, top)    

        #pos = nx.shell_layout(G)
        bbox = dict(color='white', alpha=0.5, edgecolor=None)
        edge_labels = {(i, j): w['weight'] for i, j, w in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, alpha=0.5, bbox=bbox, edge_labels=edge_labels)

        nx.draw(
            G, 
            pos, 
            node_color=color_map, 
            with_labels=True, 
            alpha=0.7,
            width=[self.to_min(w['weight'] * edge_v) for i, j, w in G.edges(data=True)],
            node_size=node_size, 
            font_family='IPAexGothic'
        )

        # 表示
        plt.axis("off")
        plt.show()