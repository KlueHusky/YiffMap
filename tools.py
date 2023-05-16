import yaml
from itertools import groupby, combinations
import networkx as nx
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2
import pickle
import numpy as np


KEY_INDIVIDUALS = "individuals"
KEY_RELATIONS = "relations"
KEY_INDIVIDUAL_NAME = "name"
KEY_INDIVIDUALS_COUNTRY_CODE = "country_code"
KEY_RELATIONS_INDIVIDUALS = "individuals"
KEY_RELATIONS_PRIVACY = "privacy"
KEY_INDIVIDUALS_SPECIES = "species"


class ColorPalette:
    #background = (0.02, 0.02, 0.04)
    #edges = (0.35, 0.31, 0.68)
    background = np.array([12, 18, 12]) / 255
    edges = np.array([194, 1, 20]) / 255
    nodes = np.array([109, 114, 117]) / 255
    labels = np.array([199, 214, 213]) / 255

FIGURE_SIZE = (20,20)
DPI = 200

FONT_SIZE = 5

NODE_SIZE = lambda degree : 15 + 10*degree

EDGE_WIDTH = lambda weight : weight

EDGE_ALPHA = 0.6

ITERATIONS = 5000

forceatlas2 = ForceAtlas2(
    # Behavior alternatives
    outboundAttractionDistribution=True,  # Dissuade hubs
    linLogMode=False,  # NOT IMPLEMENTED
    adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    edgeWeightInfluence=1,
#    radius_per_degree=lambda x : 2*x,

    # Performance
    jitterTolerance=1.0,  # Tolerance
    barnesHutOptimize=False,
    barnesHutTheta=1.0,
    multiThreaded=False,  # NOT IMPLEMENTED

    # Tuning
    scalingRatio=1,
    strongGravityMode=False,
    gravity=8,

    # Log
    verbose=True)


def check_arguments(argv):
    if len(argv) < 3:
        raise RuntimeError("Not enough arguments, try running python yiffmap.py <data_file>.yaml <output_file>.[png|pdf]")
    elif len(argv) > 3:
        raise RuntimeError("Too many arguments, try running python yiffmap.py <data_file>.yaml <output_file>.[png|pdf]")


class Map:
    def __init__(self, data_file : str, verbose : bool = False) -> None:
        self._file = data_file
        self._verbose = verbose
        self._names = None

        self._print_verbose(f"Reading data from {data_file}...", end='')
        with open(data_file, 'r', encoding='utf-8') as f: 
            self._data = yaml.full_load(f)
        print("ok")

    def check_file_contents(self):
        print("Checking file contents...")
        print("  checking keys...", end='')
        self._check_keys()
        print("ok")
        print("  checking species...", end='')
        self._check_species()
        print("ok")
        print("  checking names...", end='')
        self._check_names()
        print("ok")
        print("  checking relations...", end='')
        self._check_relations()
        print("ok")

    def _check_keys(self):
        for k in [KEY_INDIVIDUALS, KEY_RELATIONS]:
            assert k in self._data, f"Missing key {k} in {self._file}"

    def _check_species(self):
        # Check species
        individuals = self._data[KEY_INDIVIDUALS]
        for i in individuals:
            if KEY_INDIVIDUALS_SPECIES in i.keys():
                assert isinstance(i[KEY_INDIVIDUALS_SPECIES], list), "Species must be a list, even if there's a single value"

    def _check_names(self):
        # Check for duplicates
        self._names = []
        for ind in self._data[KEY_INDIVIDUALS]:
            name = ind[KEY_INDIVIDUAL_NAME]
            if name in self._names:
                raise RuntimeError(f"Duplicate of name {name}")
            else:
                self._names.append(name)

        

    def _check_relations(self):
        if self._names is None:
            self._check_names()
        # Relations
        relations = self._data[KEY_RELATIONS]
        duplicates_test_list = []
        for r in relations:
            # Check for misformed relations
            sorted_individuals_list = r[KEY_RELATIONS_INDIVIDUALS]
            sorted_individuals_list.sort()

            if(len(sorted_individuals_list) == 1):
                raise RuntimeError(f"Single person relation {sorted_individuals_list}")
            ind_list_str = ''.join(sorted_individuals_list)
            if ind_list_str in duplicates_test_list:
                raise RuntimeError(f"Duplicate of relation {sorted_individuals_list}")
            else:
                duplicates_test_list.append(ind_list_str)

            # Check for unknown name
            for name in r[KEY_RELATIONS_INDIVIDUALS]:
                if name not in self._names:
                    raise RuntimeError(f"Name \"{name}\" is missing from individuals list")
                
    def graph(self, output_file : str):
        #G = nx.DiGraph()
        G = nx.Graph()

        G.add_nodes_from(self._names)

        for r in self._data[KEY_RELATIONS]:
            rSize = len(r[KEY_RELATIONS_INDIVIDUALS])
            for c in combinations(r[KEY_RELATIONS_INDIVIDUALS], 2):
                G.add_edge(*c, weight=2/rSize)
            #G.add_edges_from([r[KEY_RELATIONS_INDIVIDUALS]])

        plt.figure(figsize=FIGURE_SIZE, dpi=DPI)
        #positions = nx.spring_layout(G, k=0.15)
        #positions = nx.kamada_kawai_layout(G)
        #print(type(G.edges.values()))

        #nx.draw_networkx_nodes(G, positions, node_size=20, node_color="blue", alpha=0.4, label="test")
        #nx.draw_networkx_edges(G, positions, edge_color=(1,1,1), alpha=0.05)
        #plt.figure(dpi=50)
        #positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=500)
        #positions = nx.fruchterman_reingold_layout(G)
        #positions = nx.spring_layout(G)
        #nx.draw_networkx_nodes(G, positions, node_size=20, node_color="blue", alpha=0.4, label="test")
        #nx.draw_networkx_edges(G, positions, edge_color=(1,1,1), alpha=0.05)

        positions = forceatlas2.forceatlas2_networkx_layout(G, iterations=ITERATIONS)

        nx.draw_networkx_nodes(
            G,
            positions,
            node_size=[NODE_SIZE(v) for v in dict(G.degree).values()],
            node_color=[ColorPalette.nodes for _ in G.nodes.values()]
            )
        nx.draw_networkx_edges(
            G,
            positions,
            connectionstyle='arc3,rad=0.2',
            arrows=True,
            node_size=[NODE_SIZE(v) for v in dict(G.degree).values()],
            min_source_margin=0,
            min_target_margin=0,
            arrowstyle='<|-|>',
            arrowsize=5,
            width=[EDGE_WIDTH(attr['weight']) for attr in G.edges.values()],
            edge_color=ColorPalette.edges,
            alpha=EDGE_ALPHA,
            )
        nx.draw_networkx_labels(
            G,
            positions,
            font_color=ColorPalette.labels,
            font_size=FONT_SIZE
            )

        fig = plt.gcf()
        fig.patch.set_facecolor(ColorPalette.background)
        plt.axis('off')
        plt.gca().set_facecolor(ColorPalette.edges)
        plt.tight_layout()
        if output_file is not None:
            plt.savefig(output_file, dpi=DPI)
        #plt.show()
        

    def display_stats(self):
        relations_sizes = [len(r[KEY_RELATIONS_INDIVIDUALS]) for r in self._data[KEY_RELATIONS]]
        relations_sizes.sort()
        print("Statistics : ")
        print(f"  {len(self._names)} names")
        print(f"  {len(self._data[KEY_RELATIONS])} relations")
        for k, grp in groupby(relations_sizes):
            N = len(list(grp))
            print(f"  {N:3d}x {k:2d} people")

    def _print_verbose(self, text : str, *args, **kwargs):
        if self._verbose:
            print(text, *args, **kwargs)




    
