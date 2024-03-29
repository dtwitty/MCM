# map with with support for running plug-in simulations

import networkx as nx
from mapbuilder import build_ithaca
from random import choice, randint

def build_sim_map():
	G = build_ithaca('ithaca.osm')
	m = Map(G)
	return m

class Map():
	def __init__(self, graph):
		self.graph = graph
	# get a list of nodes that satisfy the inlier function
	def get_nodes(self, inlier_function):
		out = []
		for node in self.graph.nodes_iter():
			if inlier_function(node):
				out.append(node)
		return out

	def get_shortest_path(self, a, b):
		path_from_graph = nx.shortest_path(self.graph, source=a, target=b, weight='distance')
		out_path = []
		for i in range(1, len(path_from_graph)):
			u = path_from_graph[i - 1]
			v = path_from_graph[i]
			distance = self.graph.edge[u][v]['distance']
			out_path.append((self.graph.node[v], distance))
		return out_path

	def get_bad_dest(self, b):
		# pick a random node near b
		count = 0
		ret = None
		for edge in nx.dfs_edges(self.graph, b):
			if count == 1000:
				break
			node = edge[1]
			count += 1
			if count == 1:
				ret = node
			i = randint(0, count - 1)
			if i == count - 1:
				ret = node
		return node



	def get_distance(self, a, b):
		return nx.shortest_path_length(self.graph, source=a, target=b, weight='distance')
