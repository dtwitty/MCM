class Sim1():
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

class Sim3():
	def __init__(self, number_cabs, init_loc):
		self.number_cabs = number_cabs
		self.cab_companies = [[], [], []]
		for i in range(self.number_cabs):
			# create a cab
			cab = Cab(city_map, init_loc)
			# assign it to a random company
			prob = randint(0, 2)
			self.cab_companies[prob].append(cab)
			# unlicensed with probability 2/3
			prob = randint(0,2)
			cab.licensed = (prob < 3)

			

	def find_free_cabs(self):
		# choose a cab company at random
		prob = randint(0,2)
		res = []
		for cab in self.cab_companies[prob]:
			if cab.state == 0 or cab.state == 1 or cab.state == 4:
				res.append(cab)
		return res

	def find_closest_free_cab_for_request(self, free_cabs, request):
		shortest_distance = 10**10
		shortest_cab = None
		cust_loc = request[3]
		dist_func = lambda l1,l2: ((l1[0] - l2[0])**2 + (l1[1] - l2[1])**2)**0.5
		for cab in free_cabs:
			(lat1, long1) = cab.cur_loc['lat'], cab.cur_loc['long']
			(lat2, long2) = cust_loc['lat'], cust_loc['long']
			dist = dist_func((lat1,long1),(lat2,long2))
			if dist < shortest_distance:
				shortest_distance = dist
				shortest_cab = cab
		return cab

	def call_this_every_minute(self, cur_time):
		for company in self.cab_companies:
			for cab in company:
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
			# print "New Appointed Hanlde:"
			# print request
			free_cabs.remove(cab)

class Sim4():