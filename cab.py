# the cab object

# stopwatch to model travel over time
class StopWatch():
	def __init__(self, travel_time):
		self.reset(travel_time)

	def update(self):
		 if self.done:
		 	pass
		 else:
			self.curr_time += 1
			if self.curr_time >= self.travel_time:
				self.done = True

	def reset(self, travel_time):
		self.travel_time = travel_time
		self.curr_time = 0
		self.done = False
		if self.travel_time == 0:
			self.done = True

class Cab():
	def __init__(self, citymap, node = None):
		# the universe of the cab
		self.map = citymap
		# the position on the map
		self.node = node
		# is this cab available to pick up?
		self.available = True
		# is this cab currently travelling?
		self.travelling = False
		# the path this cab has been told to follow
		self.path = []
		# stopwatch to model travel time
		self.watch = StopWatch(0)

	# timestep the cab
	def update(self):
		self.watch.update()
		if self.watch.done:
			self.path.pop()
			if len(self.path) == 0:
				self.travelling = False
			else:
				self.watch.set(self.path[-1][1])

	def set_destination(self, dest):
		self.path = self.map.get_path(self.source, self.dest)
		# reverse so we can pop off
		self.path.reverse()
		self.travelling = True
		self.watch.reset(0)


