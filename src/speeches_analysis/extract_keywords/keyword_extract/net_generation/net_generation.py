import networkx as nx
import itertools
import joblib


class NetGenerator():
    """Uses a tokenized text to generate the necessary network.
    This process will the coocurence network"""
    discursos: list[list[list[str]]]
    graph: nx.Graph

    def __init__(self, discursos: list[list[list[str]]] | None = None):
        if discursos is not None and discursos != []:
            self.discursos = discursos
        self.graph = nx.Graph()

    def gen_coocurence_net(self, n_jobs: int = 4) -> nx.Graph:
        G = nx.Graph()
        if self.discursos is None:
            raise AttributeError("The discursos attribute must be set.")
        # For each conjunct of sppeches of a party
        final_results = []
        for discursos in self.discursos:
            # For each sppech in the corpus
            results = joblib.Parallel(n_jobs=n_jobs)(joblib.delayed(
                self.__gen_coocurenct_net_process)(discurso)
                for discurso in discursos)
            final_results.extend(results)
        G = nx.compose_all(final_results)
        return G

    def __gen_coocurenct_net_process(self,
                                     discurso: list[str],
                                     window_size: int = 7
                                     ) -> nx.Graph:
        G = nx.Graph()
        # Makes all edges combinations for the first window
        init_text = itertools.combinations(discurso[:window_size], 2)
        for pair in init_text:
            if not G.has_edge(*pair):
                G.add_edge(pair[0], pair[1])
        # Creates the connections to the preoccuring window_size-1 words
        # Those are the necessary words once there are connections already done
        for i, token in enumerate(discurso[window_size:]):
            window = discurso[i-window_size+1:i]
            for pair in itertools.product([token], window):
                if not G.has_edge(*pair):
                    G.add_edge(*pair)
        return G

    def gen_similarity_net(self):
        pass

    def unify_nets(self):
        pass

    def extract_keywords(self):
        pass

    def get_edges(self):
        return self.graph.edges

    def get_nodes(self):
        return self.graph.nodes
