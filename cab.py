# the cab object
class Cab():
	def __init__(self, city_map, cur_loc = None):
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

	def update(self, cur_time):
		# If the cab is in state 0 or state 1, do nothing
		if self.state == 0 or self.state == 1:
			return
		# If the state is 2, and the cab has finished the distance from the last edge
		elif self.state == 2 and self.speed * (cur_time - index_timestamp) >= self.path[self.index][1]:
			# Update the current location, current index, and the timestamp
			self.cur_loc = self.path[self.index][0]
			self.index = self.index + 1
			self.index_timestamp = cur_time
			# If has arrived at pickup location, then update the state to 3
			if (self.index - 1) == self.pick_up_index:
				self.state = 3
				return self.request
		# If the state is 2, and the cab has finished the distance from the last edge
		elif self.state == 3 and self.speed * (cur_time - index_timestamp) >= self.path[self.index][1]:
			if self.index == len(self.path) - 1:
				# Arrive at location, clear the states
				self.state = 0
				self.index_timestamp = -1
				self.index = -1
				self.pick_up_index = -1
				self.path = None
			else:
				# Move one step forward
				self.cur_loc = self.path[self.index][0]
				self.index = self.index + 1
				self.index_timestamp = cur_time
		return None

	def handle_request(self, request, cur_time):
		if self.state == 0 or self.state == 1:
			cust_loc = request[3]
			dest_loc = request[4]
			first_leg = self.city_map.shortest_path(self.cur_loc, cust_loc)
			second_leg = self.city_map.shortest_path(cust_loc, dest_loc)
			self.index_timestamp = cur_time
			self.pick_up_index = len(first_leg) - 1
			self.path = first_leg + second_leg
			self.index = 0