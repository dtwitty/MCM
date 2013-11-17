import citymap
import random
import numpy as np
from cab import Cab
from Queue import Queue

city_map = citymap.build_sim_map()

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

# Only takes into account the traffic to and from Ithaca Mall, Walmart, and Airport
# Will add touris attraction & downtown later
# Weekdays, number of requests to zones per hour

price_per_mile = 2.39
zone_fees = {
	0: [4.6, 5.1, 5.1, 5.1, 5.6, 5.1, 5.1, 5.1, 5.6, 14, 11],
	1: [5.1, 4.6, 5.1, 5.1, 5.6, 5.1, 5.1, 5.1, 5.6, 14, 11],
	2: [5.1, 5.1, 4.6, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 14, 11],
	3: [5.1, 5.1, 5.1, 4.6, 5.1, 5.1, 5.1, 5.1, 5.1, 14, 11],
	4: [5.6, 5.6, 5.1, 5.1, 4.6, 5.1, 5.1, 5.6, 5.1, 14, 11],
	5: [5.1, 5.1, 5.1, 5.1, 5.1, 4.6, 5.1, 5.1, 5.1, 14, 11],
	6: [5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 4.6, 5.1, 5.1, 14, 11],
	7: [5.1, 5.1, 5.1, 5.1, 5.6, 5.1, 5.1, 4.6, 5.6, 14, 11],
	8: [5.6, 5.6, 5.1, 5.1, 5.1, 5.1, 5.1, 5.6, 4.6, 14, 11],
	9: [14, 14, 14, 14, 14, 14, 14, 14, 14, 4.6, 14],
	10:[11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 4.6],
}

day_freqs = {
	0: [0, 0, 0.5, 0.5, 3, 0, 0, 0, 3, 8, 3],
	1: [0, 0, 0.5, 0.5, 1, 0, 0, 0, 1, 3, 1],
	2: [0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	3: [0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	4: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	8: [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	9: [8, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	10:[3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

for i in range(11):
	for j in range(11):
		day_freqs[i][j] = day_freqs[i][j] + (1.0 / 6)

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

test_freqs = {
	0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
	1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	8: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	9: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	10:[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
freqs = day_freqs

class RequestSimulator():
	def __init__(self):
		self.zones = {}
		self.requests = {}
		for i in range(len(zone_recs)):
			nodes = self.filter_nodes_by_zone(*(zone_recs[i]))
			self.zones[i] = nodes

	def filter_nodes_by_zone(self, left, bottom, right, top):
		nodes = []
		for key, data in city_map.graph.node.iteritems():
			if data['lat'] > bottom and data['lat'] < top and data['long'] > left and data['long'] < right:
				nodes.append(data)
		return nodes

	# Use poisson distribution to simulate the requests in every hour
	def generate_request(self, cur_time):
		# clear the buffer
		self.requests = {}
		for i in range(len(self.zones)):
			for j in range(len(self.zones)):
				freq = np.random.poisson(freqs[i][j])
				if freq > 0:
					request_minutes = random.sample(range(60), freq)
					for request_minute in request_minutes:
						request_time = cur_time + request_minute
						src = random.choice(self.zones[i])
						dest = random.choice(self.zones[j])
						# The request is formatted as: (request_time, src_zone, dest_zone, src_node, dest_node)
						request = [request_time, i, j, src, dest, 0]
						if request_time in self.requests:
							self.requests[request_time].append(request)
						else:
							self.requests[request_time] = [request]

	# Only exposed endpoint: call this every minute to get a list of requests
	def call_this_every_minute(self, cur_time):
		if cur_time % 60 == 0:
			self.generate_request(cur_time)
		if cur_time in self.requests:
			return self.requests[cur_time]
		else:
			return []

class CabSimulator():
	def __init__(self, number_cabs, init_loc):
		self.number_cabs = number_cabs
		self.cabs = []
		for i in range(self.number_cabs):
			cab = Cab(city_map, init_loc)
			self.cabs.append(cab)

	def find_free_cabs(self):
		res = []
		for cab in self.cabs:
			if cab.state == 0 or cab.state == 1 or cab.state == 4:
				res.append(cab)
		return res

	# Heuristic: use the Euclidean distance to substitute Dijstra distance
	def dist(self, loc1, loc2):
		return (loc1['lat'] - loc2['lat']) ** 2 + (loc1['long'] - loc2['long']) ** 2

	def find_closest_free_cab_for_request(self, free_cabs, request):
		shortest_distance = 10**10
		shortest_cab = None
		cust_loc = request[3]
		for cab in free_cabs:
			dist = self.dist(cab.cur_loc, cust_loc)
			if dist < shortest_distance:
				shortest_distance = dist
				shortest_cab = cab
		return cab


	def call_this_every_minute(self, cur_time):
		for cab in self.cabs:
			res = cab.update(cur_time)
			if res:
				global old_revenue, new_revenue, waiting_time, num_err, num_handled
				zone_i = res[1]
				zone_j = res[2]
				distance = res[5]
				num_handled = num_handled + 1
				old_revenue = old_revenue + zone_fees[zone_i][zone_j]
				new_revenue = new_revenue + (2.5 + price_per_mile * distance)
				waiting_time = waiting_time + (cur_time - res[0])
				if (cur_time - res[0]) > 25:
					num_err = num_err + 1

		free_cabs = self.find_free_cabs()
		while pending_requests.qsize() > 0 and len(free_cabs) > 0:
			request = pending_requests.get()
			cab = self.find_closest_free_cab_for_request(free_cabs, request)
			cab.handle_request(request, cur_time)
			free_cabs.remove(cab)

old_revenue = 0
new_revenue = 0
waiting_time = 0
num_err = 0
num_handled = 0
pending_requests = Queue()
request_sim = RequestSimulator()

cornell = request_sim.zones[0][0]
airport = request_sim.zones[9][0]
mall = request_sim.zones[10][0]

cab_sim = CabSimulator(14, airport)

# has_started = False

for i in range(60 * 24):
	if i % 60 == 0 and num_handled > 0:
		print float(waiting_time) / num_handled
		print float(num_err) / num_handled
		print float(old_revenue) / num_handled
		print float(new_revenue) / num_handled		
		print "==========================================="
	requests = request_sim.call_this_every_minute(i)
	# if requests:
	# 	has_started = True
	# if has_started:
	# 	for cab in cab_sim.cabs:
	# 		print "Cab:"
	# 		print cab.state
	# 		print cab.cur_loc
	# 		print cab.request
	# 		if cab.path:
	# 			print cab.index, cab.pick_up_index, cab.drop_off_index, len(cab.path)
	for request in requests:
		pending_requests.put(request)
	cab_sim.call_this_every_minute(i)







