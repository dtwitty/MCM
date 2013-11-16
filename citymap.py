# map with with support for running plug-in simulations

from queue import Queue

class Request():
	def __init__(self, dest, simulator):
		self.dest = dest
		self.waiting_time = 0

	def update(self):
		self.waiting_time += 1

	def service(self, cab):
		self.simulator.finish_request(self.waiting_time)
		self.cab.set_destination(self.dest)

# locations on the map
class MapNode():
	def __init__(self):
		# probability that a new request will occur each timestep
		self.request_chance = 0
		# time since an available cab has visited this location
		self.time_since_visit = 0
		# pending requests
		self.pending_requests = Queue()

	def add_request(self, request):
		self.pending_requests.append(request)

	def service_request(self, cab):
		if len(self.pending_requests) == 0:
			raise KeyError("No requests to handle!")
		if cab.node != self:
			raise ValueError("Cab tried to pick up at wrong node!")
		# fifo ordering
		req = self.pending_requests.popleft()
		req.service(cab)

	def update(self):
		for r in self.pending_requests:
			r.update()
		self.time_since_visit += 1

	def visit(self, cab):
		if cab.node != self:
			raise ValueError("Cab visited wrong node!")
		self.time_since_visit = 0

class Map():
	def __init__(self):
		pass

	# get a list of nodes that satisfy the inlier function
	def get_nodes(self, inlier_function)