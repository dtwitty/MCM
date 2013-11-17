# the cab object
class Cab():
	def __init__(self, city_map, cur_loc):
		# Miles per minute
		self.speed = 35.0 / 60

		# The map of Ithaca
		self.city_map = city_map

		# the position on the map
		self.cur_loc = cur_loc

		# The states:
		# 0: standing
		# 1: roaming
		# 2: on the way to handle a request
		# 3: on the way handling a request
		self.state = 0
		self.request = None # request being handled
		self.index_timestamp = -1 # the time the cab arrived at the last index on the path
		self.index = -1 # the next index in the path
		self.pick_up_index = -1 # the index where the customer is
		self.path = None # the path the cab is going in
		self.paid_distance = -1

	def update(self, cur_time):
		# If the cab is in state 0 or state 1, do nothing
		if self.state == 0 or self.state == 1:
			return None
		# If the state is 2, and the cab has finished the distance from the last edge
		elif self.state == 2 or self.state == 3:
			has_picked_up = False
			distance = self.speed * (cur_time - self.index_timestamp)
			if self.state == 2:
				while distance >= self.path[self.index][1]:
					if self.index == len(self.path) - 1:
						break
					distance = distance - self.path[self.index][1]
					# Update the current location, current index, and the timestamp
					self.cur_loc = self.path[self.index][0]
					self.index = self.index + 1
					self.index_timestamp = cur_time
					# If has arrived at pickup location or destination location, then update the state to 3
					if (self.index - 1) == self.pick_up_index or self.index == (len(self.path) - 1):
						self.state = 3
						has_picked_up = True
						break
			if self.state == 3:
				while distance >= self.path[self.index][1]:
					distance = distance - self.path[self.index][1]
					self.cur_loc = self.path[self.index][0]
					if self.index == len(self.path) - 1:
						# Arrive at location, clear the states
						self.state = 0
						self.index_timestamp = -1
						self.index = -1
						self.pick_up_index = -1
						self.path = None
						break
					else:
						# Move one step forward
						self.index = self.index + 1
						self.index_timestamp = cur_time
			if has_picked_up:
				return self.request
			else:
				return None

	def handle_request(self, request, cur_time):
		if self.state == 0 or self.state == 1:
			cust_loc = request[3]
			dest_loc = request[4]
			first_leg = self.city_map.get_shortest_path(self.cur_loc['id'], cust_loc['id'])
			second_leg = self.city_map.get_shortest_path(cust_loc['id'], dest_loc['id'])
			self.paid_distance = sum(map(lambda x: x[1], second_leg))
			request[5] = self.paid_distance
			self.state = 2
			self.index_timestamp = cur_time
			self.pick_up_index = len(first_leg) - 1
			self.path = first_leg + second_leg
			self.index = 0
			self.request = request