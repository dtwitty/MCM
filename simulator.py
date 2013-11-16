import mapbuilder

#fp = mapbuilder.download_osm(-76.534, 42.407316, -76.4304, 42.50056)

zone_recs = [
	(-76.4947, 42.4394, -76.4748, 42.45588),      #Cornell 0
	(-76.4997, 42.4196, -76.4903, 42.4258),            #IC 1
	(-76.5106, 42.4401, -76.4947, 42.4424), #Upperdowntown 2
	(-76.5106, 42.4367, -76.4947, 42.4401), #Lowerdowntown 3
	(-76.5261, 42.4270, -76.5106, 42.4401),       #Walmart 4
	(-76.5106, 42.4424, -76.4947, 42.45588),    #Uppertown 5
	(-76.5106, 42.4307, -76.4947, 42.4367),     #Lowertown 6
	(-76.4947, 42.4307, -76.4748, 42.4394),  #Lowercornell 7
	(-76.5261, 42.4401, -76.5106, 42.45588),         #Lake 8
	(-76.464116, 42.4869, -76.4613, 42.4905),     #Airport 9
	(-76.49315, 42.48106, -76.48766, 42.48635),      #Mall 10
]

# Only takes into account the traffic to and from Ithaca Mall
# Weekdays, number of requests to zones per hour
day_freqs = {
	0: [0, 0, 0, 0, 3, 0, 0, 0, 0, 8, 3],
	1: [0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 1],
	2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	4: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	8: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	9: [8, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	10:[3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

night_freqs = {
	0: [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3],
	1: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	4: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	8: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	9: [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	10:[0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

class Simulator():
	def __init__(self, num_cabs, initfunction):
		self.map = mapbuilder.read_osm('ithaca.osm')
		self.zones = {}
		for i in range(len(zone_recs)):
			nodes = self.filter_nodes_by_zone(*(zone_recs[i]))
			self.zones[i] = nodes

	def filter_nodes_by_zone(self, left, bottom, right, top):
		nodes = []
		for key, value in self.map.node.iteritems():
			data = value['data']
			if data.lat > bottom and data.lat < top and data.lon > left and data.lon < right:
				nodes.append(data)
		return nodes


